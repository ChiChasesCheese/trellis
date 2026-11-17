---
id: parsing-io-regex-fullmatch
node: parsing-io.regex
type: qa
step: 1
---
## Q
校验货币码、SKU 这类「整串必须符合格式」的输入时，`re.match(r"[A-Z]{3}$", s)` 为什么会放过 `"USD\n"`？应该怎么写？

## A
**整串校验用 `re.fullmatch`，不靠 `$`**

- **`match` 只锚定开头**：从字符串头开始匹配，不要求匹配到结尾；想要结尾就得自己加 `$`；
- **`$` 的坑**：它匹配结尾，也匹配**结尾那个换行符之前**；`"USD\n"` 的 `USD` 之后正好是换行前的位置，所以通过；
- **后果**：带换行的值进了数据库、日志、文件名，之后的比较和查找莫名其妙地对不上；
- **`fullmatch`**：整串必须被模式吃完，末尾换行也算多出来的字符，所以被拒绝；
- **`\Z`** 也只匹配真正的结尾，但「整串」这个意图用 `fullmatch` 一眼就看得出来。

```python
import re

CODE = re.compile(r"[A-Z]{3}")

print(re.match(r"[A-Z]{3}$", "USD\n"))     # <re.Match ...>：被放过
print(CODE.fullmatch("USD\n"))              # None
print(CODE.fullmatch("USD") is not None)    # True
```

<details class="pt"><summary>延伸</summary>

输入来自文件的一行、命令行或 HTTP 头时，末尾的换行最常见。先 `strip()` 再校验是另一回事：它改变了数据，应当是调用方明确的选择，而不是校验顺手做了。

</details>

**知识点：**正则表达式（Regular Expressions）
