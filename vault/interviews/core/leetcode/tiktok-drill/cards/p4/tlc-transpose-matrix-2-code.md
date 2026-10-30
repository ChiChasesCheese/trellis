---
id: tlc-transpose-matrix-2-code
node: p4.transpose-matrix
type: qa
step: 2
---
## Q
**LC 867 转置矩阵**｜写出 Python 实现

给 `m x n` 的二维整数数组 `matrix`（`1 <= m, n <= 1000`，`1 <= m * n <= 10^5`），返回转置矩阵（`n x m`，`res[j][i] = matrix[i][j]`）。再写一个只适用于方阵的原地版本。

## A
**思路。** 非方阵用 `zip(*matrix)` 把行按位置配对得到所有列，每列转成列表；方阵原地版本只交换上三角的对称元素。

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)]     # zip(*rows) 把第 j 列收成一个元组


def transpose_square_in_place(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):                  # 只交换上三角，避免换回去
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`，`[[1,2,3],[4,5,6]]` → `[[1, 4], [2, 5], [3, 6]]`，`[[7]]` → `[[7]]`，`[[1],[2]]` → `[[1, 2]]`；`100 x 1000` 的矩阵得到 `1000 x 100`；原地版本把 `[[1,2,3],[4,5,6],[7,8,9]]` 变成 `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`。

**复杂度。** `transpose` 时间 `O(m·n)`、空间 `O(m·n)`；原地版本时间 `O(n^2)`、空间 `O(1)`。

**写法要点。**
- `zip(*matrix)`：`*` 把 `m` 个行展开成 `m` 个参数，`zip` 把它们按位置配对，产出 `n` 个长度为 `m` 的元组；比双重循环短，也不会写错下标。
- `list(col)`：`zip` 产出元组，要的是列表，所以包一层 `list`。
- 元组交换 `a, b = b, a` 完成原地对换，不用临时变量；`range(i + 1, n)` 保证每一对只换一次。
- `zip` 遇到长度不同的行会静默截断到最短；题目保证每行等长，所以这里没问题，处理不规则输入时要先检查。
