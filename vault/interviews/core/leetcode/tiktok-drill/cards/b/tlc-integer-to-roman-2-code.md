---
id: tlc-integer-to-roman-2-code
node: b.integer-to-roman
type: qa
step: 2
---
## Q
**LC 12 整数转罗马数字**｜写出 Python 实现

给整数 `num`（`1 <= num <= 3999`），按罗马数字规则（`I V X L C D M` 七个符号，4 和 9 用 `IV IX XL XC CD CM` 减法形式，`I X C M` 至多连续 3 次）转成字符串。

## A
**思路。** 把六个减法形式并入符号表，按面值降序遍历；每项用 `divmod` 取出个数，拼接 `symbol * count`。表的顺序保证每一步都取到当前能减去的最大符号。

```python
ROMAN: list[tuple[int, str]] = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]                                          # 必须按面值从大到小排列


def int_to_roman(num: int) -> str:
    parts: list[str] = []
    for value, symbol in ROMAN:
        count, num = divmod(num, value)    # 这个面值能放几个，以及剩余多少
        parts.append(symbol * count)       # count 为 0 时是空串，不需要 if
    return "".join(parts)
```

运行：`3749` → `"MMMDCCXLIX"`，`58` → `"LVIII"`，`1994` → `"MCMXCIV"`，`1` → `"I"`，`4` → `"IV"`，`3888` → `"MMMDCCCLXXXVIII"`，`3999` → `"MMMCMXCIX"`。

**复杂度。** 时间 `O(1)`：13 项各一次 `divmod`，输出至多 15 个字符；空间 `O(1)`。

**写法要点。** 符号表用 `list[tuple[int, str]]` 常量，顺序即算法，比 `dict` 更直接；`divmod` 一次拿商和余数；`symbol * count` 让「放 0 个」自然变成空串；`"".join(parts)` 比循环 `+=` 拼接字符串更惯用。
