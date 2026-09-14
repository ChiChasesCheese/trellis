---
id: leetcode-q-sparse-matrix-multiplication-pattern
node: math-number-theory.linear-algebra
type: qa
anki: 1787175626157
tags: [lc::311, leetcode, pattern, recall]
---
## Q
如何计算两个稀疏矩阵 mat1 (m1×n1) 和 mat2 (m2×n2) 的乘积？（暴力做法）

## A
结果矩阵大小为 m1×n2。对每个结果位置 res[i][j]，取 mat1 的第 i 行与 mat2 的第 j 列做点积：sum(mat1[i][k] * mat2[k][j] for k in range(n1))。三重循环，时间复杂度 O(m1*n1*n2)，未利用稀疏性（真正的稀疏优化应跳过零值，例如用哈希表或列表只存非零元素）。

**Evidence**

```
def calc(i, j):
    l1 = mat1[i]
    l2 = [mat2[x][j] for x in range(m2)]
    return sum(x * y for x, y in zip(l1, l2))
res = [[0]*n2 for _ in range(m1)]
for i in range(m1):
    for j in range(n2):
        res[i][j] = calc(i, j)
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F311%20-%20Sparse%20Matrix%20Multiplication)
