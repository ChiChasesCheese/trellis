---
slug: remove-comments
---
## Q
**LC 722 删除注释**｜Medium

`source` 是 C++ 程序的每一行。删去行注释 `//`（到行尾）和块注释 `/* ... */`（可跨行），返回剩下的非空行。`/*/` 不算一个完整块注释。

## A
**一句话。** 逐行逐字符扫描并维护「是否在块注释内」；块注释跨行时，缓冲区保留到注释结束再拼接。

```python
def remove_comments(source):
    ans, buf, in_block = [], [], False
    for line in source:
        i = 0
        while i < len(line):
            two = line[i:i + 2]
            if in_block:
                if two == "*/":
                    in_block = False
                    i += 1              # 吃掉 */ 的两个字符
            elif two == "/*":
                in_block = True
                i += 1
            elif two == "//":
                break                   # 本行余下全是注释
            else:
                buf.append(line[i])
            i += 1
        if buf and not in_block:        # 块注释未结束则不输出
            ans.append("".join(buf))
            buf = []
    return ans
```

**复杂度。** 时间 `O(L)`，空间 `O(L)`（`L` 为字符总数）。

**易错点。**
- 块注释内遇到 `//` 也当成行注释：块注释里一切都是注释，先判断 `in_block`。
- 起止符只前进 1：`/*` 与 `*/` 各占两格，漏掉 `i += 1` 会让 `/*/` 被当成已关闭。
- 缓冲区每行清空：块注释跨行时，前一行的代码要和注释后的代码拼成同一行。

**追问。**
- 为什么先判断 `in_block`？：块内只关心 `*/`，其他字符（包括 `//`）一律丢弃。
- 输出为空行要保留吗？：不要，缓冲区为空就不输出。

**同模式。** LC 68 文本左右对齐、LC 71 简化路径、LC 394 字符串解码
