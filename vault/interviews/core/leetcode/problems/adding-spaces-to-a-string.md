---
slug: adding-spaces-to-a-string
---
## Q
**LC 2109 向字符串添加空格**｜Medium

给字符串 `s` 和严格递增的下标数组 `spaces`，在每个下标对应的字符之前插入一个空格，返回新字符串。

## A
**一句话。** 双指针：一个扫 `s`，一个指向下一个要插空格的位置，到了就先放空格；结果攒进列表最后一次拼接。

```python
def add_spaces(s, spaces):
    out, j = [], 0
    for i, c in enumerate(s):
        if j < len(spaces) and spaces[j] == i:
            out.append(" ")   # spaces 升序，指针只前进
            j += 1
        out.append(c)
    return "".join(out)
```

**复杂度。** 时间 `O(n + k)`，空间 `O(n + k)`。

**易错点。**
- 用 `s = s[:i] + " " + s[i:]` 反复插入：每次复制整串，`O(n·k)`，而且插入后后面的下标全部偏移。
- 用 `+=` 拼字符串：最坏退化成平方，改用列表加 `join`。

**追问。**
- 也可以按段切片？：`s[prev:p]` 逐段加入列表再用空格 `join`，同样线性。
- 原地修改（C 风格字符数组）？：先算新长度，从后往前写，避免覆盖未处理的字符。

**同模式。** LC 88 合并两个有序数组、LC 1768 交替合并字符串
