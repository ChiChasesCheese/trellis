---
slug: spiral-matrix-ii
---
## Q
**LC 59 螺旋矩阵 II**｜Medium

生成一个 `n × n` 矩阵，按顺时针螺旋顺序填入 `1` 到 `n²`。

## A
**一句话。** 按右、下、左、上的方向填数，下一格越界或已填就顺时针转向。

```python
def generate_matrix(n):
    mat = [[0] * n for _ in range(n)]     # 0 = 还没填
    r = c = 0
    dr, dc = 0, 1                         # 先向右
    for v in range(1, n * n + 1):
        mat[r][c] = v
        nr, nc = r + dr, c + dc
        if not (0 <= nr < n and 0 <= nc < n
                and mat[nr][nc] == 0):
            dr, dc = dc, -dr              # 顺时针转 90 度
            nr, nc = r + dr, c + dc
        r, c = nr, nc
    return mat
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`（不计输出）。

**易错点。**
- 转向后不重算下一格：`nr, nc` 仍是旧方向的越界位置，下一轮写越界。
- 转向写成 `(-dc, dr)`：那是逆时针，第一次撞墙就向上走出界。

**追问。**
- 反过来读出螺旋顺序（LC 54）？：同样的方向向量，访问并标记，非方阵也适用。
- 逆时针或从中心向外？：改初始方向和转向规则。

**同模式。** LC 54 螺旋矩阵、LC 885 螺旋矩阵 III、LC 2326 螺旋矩阵 IV、LC 498 对角线遍历
