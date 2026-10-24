---
id: tlc-spiral-matrix-4-followup
node: a.spiral-matrix
type: qa
step: 4
---
## Q
**LC 54 螺旋矩阵**｜追问

面试官接着问：（1）反过来，生成 `n x n` 的螺旋矩阵（LC 59）？（2）能不能用 `zip` 写得更短？代价是什么？（3）矩阵很大、不能一次性放进内存时呢？

## A
1. **生成螺旋矩阵**：用方向向量，按 `1..n^2` 依次填入；撞墙或遇到已填的格子就顺时针转向，方向 `(dr, dc)` 顺时针转一次是 `(dc, -dr)`。

```python
def generate_matrix(n: int) -> list[list[int]]:
    grid = [[0] * n for _ in range(n)]
    r = c = 0
    dr, dc = 0, 1
    for v in range(1, n * n + 1):
        grid[r][c] = v
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n) or grid[nr][nc]:
            dr, dc = dc, -dr                       # 顺时针转向：(0,1)->(1,0)->(0,-1)->(-1,0)
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return grid
```

`generate_matrix(3)` → `[[1,2,3],[8,9,4],[7,6,5]]`，`generate_matrix(1)` → `[[1]]`。
2. **`zip` 的短写法**：每次取走第一行，剩下的矩阵先 `zip(*...)` 转置再整体反转，相当于逆时针转 90 度，新的第一行就是原来的最右列。

```python
def spiral_zip(matrix: list[list[int]]) -> list[int]:
    result: list[int] = []
    while matrix:
        result += matrix[0]                        # 取走第一行
        matrix = [*zip(*matrix[1:])][::-1]         # 剩下的部分逆时针转 90 度，新的第一行就是原来的右边一列
    return result
```

对示例同样得到 `[1,2,3,6,9,8,7,4,5]`。代价是每圈都重建矩阵，时间 `O(mn * min(m, n))`，只适合小矩阵；而且 `zip(*...)` 产生的是元组，`result += 元组` 在列表上仍可用，但中间矩阵的行是元组，不是列表。
3. **大矩阵**：边界法本来就只需要按行、列顺序访问，写成生成器 `yield` 一个个产出元素，不需要一次性构造结果列表；如果矩阵按行存放在磁盘上，右边和左边需要按列访问，会带来大量随机读取，此时可以先按层号分块读。

**Python 提醒**：`[[0] * n] * n` 创建的 `n` 行是同一个列表对象，填一格等于改一整列；二维数组一定写成 `[[0] * n for _ in range(n)]`。
