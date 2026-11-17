---
id: parsing-io-regex-grammar-before-float
node: parsing-io.regex
type: qa
step: 3
---
## Q
汇率字段只允许 `1`、`1.`、`.5`、`+2.5e-1` 这类写法。直接 `float(s)` 为什么不够？该用什么顺序解析？

## A
**先用正则卡语法，再 `float()`**

- **`float()` 比语法宽**：`"1_0"` 得 10.0，`" 1 "` 得 1.0，`"nan"`、`"inf"` 是合法浮点，全角数字也能转；
- **后果**：`nan` 与任何数比较都是 False，范围检查 `0 < r < 1000` 会拿到「不在范围」之外的奇怪结果；`inf` 乘出整串无穷大；
- **顺序**：整串 `fullmatch` 语法，通过才转 `float`，转完再查范围；每一步的错误都归到同一个「格式错」；
- **语法写法**：整数部分、可选小数点与小数部分，或者只有小数点开头的小数，再加可选指数；
- **例子**：`1`、`1.`、`.5`、`+2.5e-1` 合法；`.`、`1e`、`1_0`、`nan`、` 1` 非法。

```python
import re

RATE = re.compile(r"[+-]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")

def parse_rate(s: str) -> float:
    if not RATE.fullmatch(s): raise ValueError("bad_rate")
    return float(s)

print(parse_rate("+2.5e-1"), [bool(RATE.fullmatch(x)) for x in ("1_0", "nan", ".", " 1")])
```

<details class="pt"><summary>延伸</summary>

范围还要拒绝 `1e999`：它符合语法，`float` 得到 `inf`。转换之后用 `math.isfinite` 再查一次。

</details>

**知识点：**正则表达式（Regular Expressions）
