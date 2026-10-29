---
id: tlc-rotate-image-4-followup
node: b.rotate-image
type: qa
step: 4
---
## Q
**LC 48 旋转图像**｜追问

面试官接着问：（1）改成逆时针 `90` 度或 `180` 度？（2）不用转置，一圈一圈四个元素轮换怎么写？（3）矩阵不是方阵（`m × n`）呢？

## A
1. **逆时针 / 180 度。** 逆时针：转置，再把行的顺序整体倒过来；`180` 度：整个矩阵行序倒置，同时每行翻转。
```python
def rotate_ccw(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    matrix.reverse()                         # 行的顺序倒过来
```
`[[1,2,3],[4,5,6],[7,8,9]]` → `[[3, 6, 9], [2, 5, 8], [1, 4, 7]]`。
2. **四元素轮换。** 第 `i` 圈的每个位置 `(i, j)`，与另外三个旋转到达的位置 `(j, n-1-i)`、`(n-1-i, n-1-j)`、`(n-1-j, i)` 构成一个 4 循环：
```python
def rotate_ring(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n // 2):
        for j in range(i, n - 1 - i):
            matrix[i][j], matrix[j][n - 1 - i], matrix[n - 1 - i][n - 1 - j], matrix[n - 1 - j][i] = (
                matrix[n - 1 - j][i], matrix[i][j], matrix[j][n - 1 - i], matrix[n - 1 - i][n - 1 - j])
```
一次遍历每个元素只动一次，常数比“转置 + 翻转”小，但下标容易写错，面试里先写转置翻转版。
3. **非方阵。** 形状从 `m × n` 变成 `n × m`，无法在原数组里原地完成，只能返回新矩阵：`[list(r) for r in zip(*matrix[::-1])]`，`[[1,2,3],[4,5,6]]` → `[[4, 1], [5, 2], [6, 3]]`。`zip(*rows)` 把行变成列，`[::-1]` 先倒置行序，合起来是顺时针旋转。

**Python 提醒**：`zip(*matrix)` 得到的是元组，要列表请用 `list(r)`；`matrix[::-1]` 是浅拷贝，里面的行仍是原来的列表对象，后面如果就地修改这些行会影响原矩阵。
