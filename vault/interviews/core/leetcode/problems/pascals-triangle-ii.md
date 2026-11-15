---
slug: pascals-triangle-ii
---
## Q
**LC 119 杨辉三角 II**｜Easy

给非负整数 `row_index`，返回杨辉三角的第 `row_index` 行（从第 0 行开始）。

## A
**一句话。** 只用一行数组原地滚动：每个数等于上一行它自己加它左边那个，从右往左更新才不会覆盖还没用的值。

```python
def get_row(row_index):
    row = [1] * (row_index + 1)
    for i in range(2, row_index + 1):    # 逐行向下推
        for j in range(i - 1, 0, -1):    # 从右往左，防覆盖
            row[j] += row[j - 1]
    return row
```

**复杂度。** 时间 `O(k^2)`，空间 `O(k)`（`k = row_index`）。

**易错点。**
- 从左往右更新：`row[j - 1]` 已经是新一行的值，会重复累加。
- 更新到 `j = 0` 或 `j = i`：两端永远是 1，不用改。

**追问。**
- 能 `O(k)` 时间吗？：用组合数递推 `C(k, j) = C(k, j - 1) · (k - j + 1) / j`，一遍就出一行。
- 为什么不开二维表？：每行只依赖上一行，滚动数组即可。

**同模式。** LC 118 杨辉三角、LC 120 三角形最小路径和、LC 62 不同路径、LC 70 爬楼梯
