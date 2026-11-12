---
slug: roman-to-integer
---
## Q
**LC 13 罗马数字转整数**｜Easy

把罗马数字字符串转成整数，小数在大数左边表示减法（`IV=4`、`IX=9`、`XL`、`XC`、`CD`、`CM`）。

## A
**一句话。** 从右往左扫，当前值比右邻小就减，否则加。

```python
def roman_to_int(s):
    val = {"I": 1, "V": 5, "X": 10, "L": 50,
           "C": 100, "D": 500, "M": 1000}
    total = prev = 0         # prev：右邻的值，最右边当 0
    for ch in reversed(s):
        v = val[ch]
        total += v if v >= prev else -v
        prev = v
    return total
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 比较写成 `v > prev`：`"II"` 变成 `1 - 1 = 0`，应为 `2`。
- 从左往右扫：要看右邻，最后一个字符容易越界或漏加。

**追问。**
- 怎么校验是否合法？：正则 `^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$`。

**同模式。** LC 12 整数转罗马数字、LC 8 字符串转换整数、LC 168 Excel 表列名称、LC 171 Excel 表列序号
