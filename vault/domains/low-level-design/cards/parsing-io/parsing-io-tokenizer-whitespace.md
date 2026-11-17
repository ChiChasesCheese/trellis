---
id: parsing-io-tokenizer-whitespace
node: parsing-io.tokenizer
type: qa
step: 2
---
## Q
格式规定空白只有空格、制表、回车、换行四种。用 `str.isspace()` 跳空白或者 `text.strip()` 去首尾空白，为什么会放宽语法？

## A
**空白集合是语法的一部分，写成显式的集合**

- **`isspace()` 的范围**：包括换页符 `\x0b`、`\x0c`，以及 `\xa0`（不换行空格）、全角空格 `　` 等 Unicode 空白；
- **后果**：规则外的字符被当作空白悄悄跳过，格式比合同宽松，别的实现拒绝的输入这里通过了；
- **`strip()` 同理**：不带参数就按 `isspace` 去；要写 `strip(" \t\r\n")`；
- **字符串内部**：空白只在字符串之外算空白；字符串里的空格是内容，不能被跳过；
- **集合放在一处**：常量 `WS = " \t\r\n"`，跳空白、去首尾都引用它。

```python
WS = " \t\r\n"

def skip_ws(s: str, i: int) -> int:
    while i < len(s) and s[i] in WS: i += 1
    return i

print("\x0b".isspace(), " ".isspace())      # True True：isspace 比合同宽
print(skip_ws(' \t{"a": 1}', 0))                  # 2
print(skip_ws("\x0b{", 0))                        # 0：换页符不是空白，下一步按语法报错
print(repr("  x ".strip(WS)))                # '\xa0x'
```

**知识点：**词法分析（Tokenizer）
