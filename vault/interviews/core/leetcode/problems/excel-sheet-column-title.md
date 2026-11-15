---
slug: excel-sheet-column-title
---
## Q
**LC 168 Excel 表列名称**｜Easy

给正整数 `columnNumber`，返回它在 Excel 表中对应的列名：`1→A`，`26→Z`，`27→AA`，`28→AB`……

## A
**一句话。** 26 进制但没有「零」（数字是 1~26），所以每次先减一再取余，把 1~26 平移成 0~25。

```python
def convert_to_title(columnNumber):
    s = ''
    while columnNumber:
        columnNumber -= 1                  # 1~26 变成 0~25
        columnNumber, r = divmod(columnNumber, 26)
        s = chr(65 + r) + s                # 低位先出，所以前插
    return s
```

**复杂度。** 时间 `O(log₂₆ n)`，空间 `O(log₂₆ n)`。

**易错点。**
- 直接 `n % 26`：余数 `0` 没有对应的字母，要先减一再取余。
- 余数为 0 当 `Z` 却不把商减一：`52` 会得到 `BZ`，应为 `AZ`。
- 把低位拼到后面：求出的是从低位到高位，要前插或最后反转。

**追问。**
- 反过来（列名转数字）呢？：`ans = ans * 26 + (c - 'A' + 1)`，这一边不需要平移。
- 为什么减一？：这是「双射 26 进制」，没有零位，平移后就是普通 26 进制。

**同模式。** LC 171 Excel 表列序号、LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 8 字符串转换整数 (atoi)
