---
slug: sparse-matrix-multiplication
---
## Q
**LC 311 稀疏矩阵的乘法**｜Medium

给定稀疏矩阵 `mat1`（`m × k`）和 `mat2`（`k × n`），返回它们的乘积。

## A
**一句话。** 循环顺序改成 `i → k → j`，跳过 `mat1[i][k] == 0`，再只遍历 `mat2` 第 `k` 行预先压好的非零项。

```python
def multiply(mat1, mat2):
    m, n = len(mat1), len(mat2[0])
    # mat2 每行压成 [(列, 值)]，只留非零
    rows2 = [[(j, b) for j, b in enumerate(r) if b]
             for r in mat2]
    res = [[0] * n for _ in range(m)]
    for i, row in enumerate(mat1):
        for k, a in enumerate(row):
            if a == 0:
                continue
            for j, b in rows2[k]:
                res[i][j] += a * b
    return res
```

**复杂度。** 时间 `O(mk + nnz1 · 平均每行非零数)`，空间 `O(mn)`。

**易错点。**
- 用 `[[0] * n] * m` 建结果：各行是同一个列表，改一行全变。
- 把累加写成赋值 `res[i][j] = a * b`：`[[1,1]] x [[1],[1]]` 得 `[[1]]`，应为 `[[2]]`。

**追问。**
- 输入本身是字典存非零项？：按行号给 `mat2` 分组，只遍历 `mat1` 的非零项，相消成 0 的要删。
- 两个矩阵稀疏程度不同？：把更稀疏的放外层。

**同模式。** LC 1570 两个稀疏向量的点积、LC 566 重塑矩阵、LC 54 螺旋矩阵、LC 48 旋转图像
