---
id: tlc-sparse-matrix-multiplication-2-code
node: a.sparse-matrix-multiplication
type: qa
step: 2
---
## Q
**LC 311 稀疏矩阵的乘法**｜写出 Python 实现

`mat1`（`m x k`）和 `mat2`（`k x n`）是稀疏矩阵，`1 <= m, n, k <= 100`，元素范围 `-100..100`，返回 `mat1 x mat2`。要求利用稀疏性，跳过零。

## A
**思路。** 把 `mat2` 每一行预处理成只含非零项的 `(列号, 值)` 列表。对 `mat1` 逐个元素，为 0 就跳过，非零就把 `a * b` 累加到 `res[i][j]`，其中 `(j, b)` 取自 `mat2` 的第 `k` 行。

```python
def multiply(mat1: list[list[int]], mat2: list[list[int]]) -> list[list[int]]:
    m, n = len(mat1), len(mat2[0])
    # 把 mat2 每一行压成 [(列号, 值), ...]，只留非零项
    rows2 = [[(j, b) for j, b in enumerate(row) if b] for row in mat2]
    res = [[0] * n for _ in range(m)]                # 每行单独建，不能写 [[0] * n] * m
    for i, row in enumerate(mat1):
        for k, a in enumerate(row):
            if a == 0:
                continue                             # mat1[i][k] 为 0：整条 k 都不用算
            for j, b in rows2[k]:
                res[i][j] += a * b
    return res
```

运行：`[[1,0,0],[-1,0,3]] x [[7,0,0],[0,0,0],[0,0,1]]` → `[[7, 0, 0], [-7, 0, 3]]`，`[[0]] x [[0]]` → `[[0]]`，`[[2]] x [[-3]]` → `[[-6]]`。

**复杂度。** 时间：预处理 `O(k*n)`，主循环 `O(m*k)` 加上「`mat1` 非零个数 x `mat2` 对应行的非零个数」；稠密时最坏 `O(m*k*n)`。空间 `O(m*n)` 结果加 `O(nnz(mat2))` 压缩行。

**写法要点。** 嵌套列表推导里用 `enumerate` 同时拿列号和值，`if b` 过滤零；`[[0] * n for _ in range(m)]` 每行一个独立列表；`for i, row in enumerate(mat1)` 比 `range(m)` 加下标更直接。
