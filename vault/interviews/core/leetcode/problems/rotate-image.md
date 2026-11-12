---
slug: rotate-image
---
## Q
**LC 48 旋转图像**｜Medium

把 `n × n` 矩阵原地顺时针旋转 90 度。

## A
**一句话。** 顺时针 90 度 = 先沿主对角线转置，再把每一行左右翻转。

```python
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):     # 只换上三角
            a = matrix
            a[i][j], a[j][i] = a[j][i], a[i][j]
    for row in matrix:
        row.reverse()
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`。

**易错点。**
- 转置内层从 `0` 开始：每对被换两次，等于没转置。内层要从 `i + 1` 起。
- `matrix = [list(r) for r in zip(*matrix[::-1])]`：只改了局部变量，调用方矩阵不变，要写 `matrix[:] = ...`。
- 两步顺序反了：先翻行再转置得到逆时针。

**追问。**
- 逆时针 90 度？：先转置，再 `matrix.reverse()` 倒转行序。
- 非方阵 `m × n`？：形状变了不能原地，返回 `[list(r) for r in zip(*matrix[::-1])]`。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 867 转置矩阵、LC 73 矩阵置零
