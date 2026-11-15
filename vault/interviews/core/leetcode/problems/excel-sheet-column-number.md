---
slug: excel-sheet-column-number
---
## Q
**LC 171 Excel 表列序号**｜Easy

Excel 表的列名依次是 `A, B, …, Z, AA, AB, …`。给列名 `column_title`，返回它对应的列序号（`A = 1`，`Z = 26`，`AA = 27`）。

## A
**一句话。** 把列名看成「26 进制」数，字母 `A..Z` 对应数字 `1..26`，逐位乘 26 累加。

```python
def title_to_number(column_title):
    n = 0
    for ch in column_title:
        n = n * 26 + ord(ch) - ord("A") + 1   # A 是 1，不是 0
    return n
```

**复杂度。** 时间 `O(L)`，空间 `O(1)`。

**易错点。**
- 字母映射成 `0..25`：这里没有 0，`A` 必须是 1，否则 `AA` 会错。
- 累加顺序写反：应是 `n * 26 + 当前位`，高位先乘。

**追问。**
- 反过来（LC 168）怎么做？：每次先 `n -= 1` 再取 `n % 26` 作为字母，因为没有 0，要先平移。
- 为什么叫「没有 0 的进制」？：这是双射 26 进制，每个正整数唯一对应一个字符串。

**同模式。** LC 168 Excel 表列名称、LC 13 罗马数字转整数、LC 8 字符串转换整数 (atoi)
