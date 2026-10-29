---
id: tlc-robot-bounded-in-circle-2-code
node: a.robot-bounded-in-circle
type: qa
step: 2
---
## Q
**LC 1041 困于环中的机器人**｜写出 Python 实现

字符串 `instructions`（长度 `1..100`，只含 `G` / `L` / `R`），机器人从原点朝北出发、无限循环执行它。判断机器人的轨迹是否被限制在某个有界区域内（存在环）。要求 `O(n)`。

## A
**思路。** 位置 `(x, y)` 和方向向量 `(dx, dy)`，初始朝北 `(0, 1)`。遍历一轮指令：`G` 按方向走一步，`L` / `R` 旋转方向向量。一轮结束后，回到原点或者朝向不是北，就说明重复若干轮后机器人被困住。

```python
def is_robot_bounded(instructions: str) -> bool:
    x = y = 0
    dx, dy = 0, 1                      # 方向向量，初始朝北
    for ch in instructions:
        if ch == "G":
            x, y = x + dx, y + dy
        elif ch == "L":
            dx, dy = -dy, dx           # 逆时针转 90 度
        else:
            dx, dy = dy, -dx           # 顺时针转 90 度
    # 只模拟一轮：回到原点，或者不再朝北（转 4 轮后必回原点）
    return (x, y) == (0, 0) or (dx, dy) != (0, 1)
```

运行：`"GGLLGG"` → `True`，`"GG"` → `False`，`"GL"` → `True`，`"GLGLGLGL"` → `True`，`"LRG"` → `False`。

**复杂度。** 时间 `O(n)`：只模拟一轮指令；空间 `O(1)`：位置和方向共四个整数。

**写法要点。** 方向用向量 `(dx, dy)` 表示，旋转是一次元组赋值 `dx, dy = -dy, dx`（左）/ `dy, -dx`（右），不需要方向表和取模；`x, y = x + dx, y + dy` 同时更新两个坐标；最后一行用元组比较 `(x, y) == (0, 0)` 与 `(dx, dy) != (0, 1)`，比分别比较两个坐标更清晰。另一种常见写法是 `dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]` 加 `d = (d + 1) % 4`，在需要「朝向编号」时（如打印方位）更方便。
