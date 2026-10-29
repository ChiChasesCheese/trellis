---
id: tlc-rotate-image-2-code
node: b.rotate-image
type: qa
step: 2
---
## Q
**LC 48 旋转图像**｜写出 Python 实现

`n × n` 整数矩阵 `matrix`（`1 <= n <= 20`，元素 `-1000` 到 `1000`），把它顺时针旋转 `90` 度，直接修改传入的矩阵，不返回，也不使用额外的 `n × n` 空间。

## A
**思路。** 顺时针 `90` 度等于「转置 + 每行翻转」。转置只交换上三角和下三角的对称元素，每行翻转用列表的原地 `reverse()`。

```python
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):           # 只交换上三角，沿主对角线转置
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()                       # 再把每一行左右翻转 = 顺时针 90 度
```

运行：`[[1,2,3],[4,5,6],[7,8,9]]` → `[[7, 4, 1], [8, 5, 2], [9, 6, 3]]`；`[[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]` → `[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]`；`[[1]]` → `[[1]]`。

**复杂度。** 时间 `O(n^2)`：转置约 `n^2 / 2` 次交换，翻转 `n^2 / 2` 次；空间 `O(1)`。

**写法要点。**
- `matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]`：元组赋值交换，不需要临时变量。
- 内层 `range(i + 1, n)` 保证每对元素只交换一次；写成 `range(n)` 会交换两次，等于什么都没做。
- `row.reverse()` 原地反转，返回 `None`；不要写成 `row = row[::-1]`，那只是让循环变量指向新列表，矩阵本身没变。
- 函数没有返回值，标注 `-> None`；要在原矩阵上改，循环 `for row in matrix` 拿到的 `row` 就是矩阵里同一个列表对象。
