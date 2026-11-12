---
slug: set-matrix-zeroes
---
## Q
**LC 73 矩阵置零**｜Medium

`m × n` 矩阵中某元素为 `0`，就把它所在的整行整列设为 `0`，要求原地。

## A
**一句话。** 用首行首列当标记，另用两个布尔值记首行首列自己原本有没有 `0`。

```python
def set_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = 0 in matrix[0]                  # 首行原本有 0
    col0 = any(r[0] == 0 for r in matrix)  # 首列原本有 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:          # 记在首行首列
                matrix[i][0] = matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        matrix[0][:] = [0] * n
    if col0:
        for r in matrix:
            r[0] = 0
```

**复杂度。** 时间 `O(mn)`，额外空间 `O(1)`。

**易错点。**
- 边扫边清零：新产生的 `0` 被当成原有的继续扩散，`[[0,1,1],[1,1,1],[1,1,1]]` 会变全 `0`。
- 没先记首行首列是否原有 `0`：标记会覆盖它们，`[[1,0],[1,1]]` 得 `[[0,0],[0,0]]`，应为 `[[0,0],[1,0]]`。
- 先清首行首列：标记被抹掉，内部格子没依据，它们必须最后处理。

**追问。**
- 不要求 `O(1)` 空间怎么做？：用两个集合记要清零的行和列，空间 `O(m + n)`，再统一清零。

**同模式。** LC 289 生命游戏、LC 48 旋转图像、LC 54 螺旋矩阵、LC 1706 球会落何处
