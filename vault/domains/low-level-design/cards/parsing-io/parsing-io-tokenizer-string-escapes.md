---
id: parsing-io-tokenizer-string-escapes
node: parsing-io.tokenizer
type: qa
step: 3
---
## Q
手写字符串 token 的读取：只收可打印 ASCII（32 到 126），转义只有八种，其余一律拒绝。循环该怎么写，哪些地方最容易放宽？

## A
**逐字符读，字符要么收下、要么转义查表、要么报错**

- **终止**：遇到未转义的 `"` 返回，位置指向引号之后；读到末尾还没有引号，就是截断，报错；
- **转义表**：`" \ / b f n r t` 八个，查字典；`\u` 和别的转义不在表里，直接拒绝；
- **范围检查**：未转义的字符必须在 32 到 126 之间；原始制表符、换行和非 ASCII 字符都拒绝；
- **容易放宽的地方**：用 `isprintable()`（它接受非 ASCII）、漏掉反斜杠在末尾的情形；
- **转义出来的控制字符可以出现在结果里**：`\n` 解码成换行是允许的，只有原始字符受限。

```python
ESC = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
def read_string(s: str, i: int):           # s[i] 是开头的引号，返回 (值, 下一个位置)
    out, i = [], i + 1
    while i < len(s):
        c = s[i]
        if c == '"': return "".join(out), i + 1
        if c == "\\":
            i += 1
            if i >= len(s) or s[i] not in ESC: raise ValueError("invalid_json")
            out.append(ESC[s[i]])
        elif 32 <= ord(c) <= 126: out.append(c)
        else: raise ValueError("invalid_json")
        i += 1
    raise ValueError("invalid_json")       # 没有闭合
print(read_string('"a\\nb" x', 0))         # ('a\nb', 6)
```

**知识点：**词法分析（Tokenizer）
