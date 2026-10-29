---
id: tlc-set-matrix-zeroes-2-code
node: a.set-matrix-zeroes
type: qa
step: 2
---
## Q
**LC 73 矩阵置零**｜写出 Python 实现

`m x n` 的整数矩阵（`1 <= m, n <= 200`，元素在 32 位有符号整数范围内）。若某个元素为 `0`，把它所在行和列的所有元素都设为 `0`。原地修改，函数返回 `None`，只用常量额外空间。

## A
**思路。** 先用两个布尔值记下第 `0` 行、第 `0` 列原本是否含 `0`。扫描内部格子（下标从 `1` 起），遇到 `0` 就把它所在行首、列首写成 `0` 作标记。再按标记把内部清零。最后根据开头的布尔值清第 `0` 行和第 `0` 列。

```python
def set_zeroes(matrix: list[list[int]]) -> None:
    m, n = len(matrix), len(matrix[0])
    first_row_zero = 0 in matrix[0]                   # 第 0 行/列本身要当标记用，先单独记下它们原来有没有 0
    first_col_zero = any(row[0] == 0 for row in matrix)
    for i in range(1, m):                             # 用第 0 行/列记录“这一列/行要清零”
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = matrix[0][j] = 0
    for i in range(1, m):                             # 按标记清零内部；标记只看第 0 行/列，不会被这一步污染
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for row in matrix:
            row[0] = 0
```

运行：`[[1,1,1],[1,0,1],[1,1,1]]` → `[[1, 0, 1], [0, 0, 0], [1, 0, 1]]`；`[[0,1,2,0],[3,4,5,2],[1,3,1,5]]` → `[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]`；`[[1]]` → `[[1]]`；`[[0]]` → `[[0]]`；`[[1,0]]` → `[[0, 0]]`；`[[1],[0]]` → `[[0], [0]]`。

**复杂度。** 时间 `O(mn)`；额外空间 `O(1)`（两个布尔值和循环变量）。

**写法要点。** `0 in matrix[0]` 在 C 层线性扫描，比手写循环快；`any(row[0] == 0 for row in matrix)` 用生成器，找到第一个就停；`matrix[i][0] = matrix[0][j] = 0` 链式赋值一次写两个标记；三个阶段的顺序不能换：写标记、按标记清内部、最后清第 `0` 行 / 列；清第 `0` 行写成显式循环，不用 `matrix[0] = [0] * n`（那会替换行对象，而不是修改原行，调用方持有的其他引用不会看到变化）；函数没有返回值，符合「原地」的要求。
