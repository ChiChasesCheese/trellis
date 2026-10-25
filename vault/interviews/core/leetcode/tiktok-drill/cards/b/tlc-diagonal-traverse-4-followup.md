---
id: tlc-diagonal-traverse-4-followup
node: b.diagonal-traverse
type: qa
step: 4
---
## Q
**LC 498 对角线遍历**｜追问

面试官接着问：（1）能不能不额外存分组，只用 `O(1)` 额外空间（不计输出）？（2）如果矩阵非常大，不想一次生成整个结果？（3）模拟行走的写法大致怎么写，难点在哪？

## A
1. **`O(1)` 额外空间**：第 `d` 条对角线上合法的行号区间是 `[max(0, d - n + 1), min(d, m - 1)]`，列号 `j = d - i`。奇数条按行号递增读，偶数条按递减读。

```python
def find_diagonal_order_range(mat: list[list[int]]) -> list[int]:
    m, n = len(mat), len(mat[0])
    result: list[int] = []
    for d in range(m + n - 1):
        lo, hi = max(0, d - n + 1), min(d, m - 1)  # 这条对角线上合法的行号区间
        rows = range(lo, hi + 1) if d % 2 else range(hi, lo - 1, -1)
        result.extend(mat[i][d - i] for i in rows)
    return result
```

`[[1,2,3],[4,5,6],[7,8,9]]` → `[1,2,4,7,5,3,6,8,9]`，`[[1,2],[3,4]]` → `[1,2,3,4]`。
2. **惰性产出**：把 `result.extend(...)` 换成 `yield from`，函数变成生成器，一次只产出一条对角线，调用方可以边消费边处理，额外内存 `O(1)`。
3. **模拟行走**：用 `(i, j)` 和方向 `up`。向右上走时：若 `j == n - 1`，下移一格并改向；否则若 `i == 0`，右移一格并改向；否则 `(i - 1, j + 1)`。向左下走时：若 `i == m - 1`，右移一格并改向；否则若 `j == 0`，下移一格并改向；否则 `(i + 1, j - 1)`。难点是**先判断右 / 下边界、再判断上 / 左边界**的顺序——右上角既在上边界又在右边界，应当先处理右边界（下移），顺序写反就会越界。

**Python 提醒**：`range(hi, lo - 1, -1)` 的终点是 `lo - 1`（开区间），写成 `range(hi, lo, -1)` 会漏掉最后一个元素 `lo`；生成器表达式 `(mat[i][d - i] for i in rows)` 配合 `extend` 不会先建临时列表。
