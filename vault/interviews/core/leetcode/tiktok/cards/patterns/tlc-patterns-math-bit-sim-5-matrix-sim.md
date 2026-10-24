---
id: tlc-patterns-math-bit-sim-5-matrix-sim
node: patterns.math-bit-sim
type: qa
step: 5
---
## Q
**数学、位运算与模拟｜矩阵与方向模拟：螺旋矩阵、旋转图像、困于环中的机器人**

螺旋遍历怎样避免单行 / 单列时重复？顺时针旋转 90 度怎样原地完成？机器人是否回到环里怎样判断，不必模拟无限次？

## A
```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    res: list[int] = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        res.extend(matrix[top][left:right + 1])                    # 上边：左 -> 右
        res.extend(matrix[r][right] for r in range(top + 1, bottom + 1))   # 右边：上 -> 下
        if top < bottom and left < right:                          # 单行 / 单列时没有下边和左边
            res.extend(matrix[bottom][left:right][::-1])           # 下边：右 -> 左
            res.extend(matrix[r][left] for r in range(bottom - 1, top, -1))   # 左边：下 -> 上
        top, bottom, left, right = top + 1, bottom - 1, left + 1, right - 1
    return res

def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]   # 先转置
    for row in matrix:
        row.reverse()                      # 再把每行反转 = 顺时针 90 度

def is_robot_bounded(instructions: str) -> bool:
    x = y = 0
    dx, dy = 0, 1                          # 面朝北
    for ch in instructions:
        if ch == "G":
            x, y = x + dx, y + dy
        elif ch == "L":
            dx, dy = -dy, dx               # 左转 90 度
        else:
            dx, dy = dy, -dx               # 右转 90 度
    return (x, y) == (0, 0) or (dx, dy) != (0, 1)
```

运行：`spiral_order([[1,2,3],[4,5,6],[7,8,9]])` → `[1,2,3,6,9,8,7,4,5]`，`[[1,2,3,4],[5,6,7,8],[9,10,11,12]]` → `[1,2,3,4,8,12,11,10,9,5,6,7]`；`rotate([[1,2,3],[4,5,6],[7,8,9]])` 后为 `[[7,4,1],[8,5,2],[9,6,3]]`；`is_robot_bounded("GGLLGG")` → `True`，`"GG"` → `False`，`"GL"` → `True`。

- **机器人**：执行一遍指令后，若回到原点则一定有环；若朝向不再是北，重复至多 4 遍就会回到原点；若仍朝北且不在原点，则每遍向外走一段，永远出不去。
- 方向用 `(dx, dy)` 表示，旋转是 `(−dy, dx)`（左）和 `(dy, −dx)`（右），不用 `if` 枚举四个方向。
- 逆时针旋转：先反转每行再转置，或先上下翻转再转置。
