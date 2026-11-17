---
id: parsing-io-regex-marker-scan
node: parsing-io.regex
type: qa
step: 5
---
## Q
付款备注里要找标记 `paying for:` 或 `paying off:` 后面的发票号：不分大小写，`İ` 和 `ı` 也当作 `i`，发票号取到下一个逗号。为什么不能先 `memo.lower()` 再找，也不能用 `.*` 取号？

## A
**在原串上用 `re.IGNORECASE`，取号用 `[^,]*`**

- **`lower()` 会改长度**：`"İ".lower()` 是两个字符（`i` 加一个组合附点），小写后的串里找不到 `paying`，找到了位置也对不上原串；
- **`re.IGNORECASE`**：按 Unicode 规则匹配，`i`、`I`、`İ`、`ı` 等价，位置直接来自原串；
- **`.*` 是贪婪的**：它会越过逗号，把后面的话一起吃掉，两个标记在同一行时只能找到第一个；
- **`[^,]*`**：「直到下一个逗号」的明确写法，不依赖回溯；
- **多个标记**：`finditer` 从左到右逐个取，每个匹配的结束位置之后继续找。

```python
import re

PAID = re.compile(r"paying (?:for|off):\s*([^,]*)", re.IGNORECASE)
memo = "PAYİNG FOR: INV-7, ok; paying off:INV-9, late"

print([m.group(1).strip() for m in PAID.finditer(memo)])                  # ['INV-7', 'INV-9']
print(re.findall(r"paying (?:for|off):\s*(.*)", memo, re.I))              # 贪婪 .* 只得到一整块
print(len("İ".lower()), "PAYİNG".lower() == "paying")                     # 2 False
```

**知识点：**正则表达式（Regular Expressions）
