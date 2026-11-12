---
slug: robot-bounded-in-circle
---
## Q
**LC 1041 困于环中的机器人**｜Medium

机器人从原点面朝北，无限循环执行指令串（`G` 直走一步，`L` 左转，`R` 右转）。判断它是否永远困在某个圆里。

## A
**一句话。** 只模拟一轮：回到原点，或不再朝北（至多四轮转回），就会绕环。

```python
def is_robot_bounded(instructions):
    x = y = 0
    dx, dy = 0, 1                  # 朝北
    for ch in instructions:
        if ch == "G":
            x, y = x + dx, y + dy
        elif ch == "L":
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
    return (x, y) == (0, 0) or (dx, dy) != (0, 1)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只判断回到原点：`"GL"` 一轮后在 `(0,1)` 朝西，会错判 `false`，应为 `true`。
- 只判断朝向变化：`"GLGLGLGL"` 一轮后仍朝北但在原点，应为 `true`。
- 朝北且不在原点：`"GG"` 每轮北移 `2` 格，应为 `false`。

**追问。**
- 有障碍物怎么办？：一轮不再是固定的旋转加平移，只能模拟，用每轮结束的（位置，朝向）判重。
- 为什么至多四轮？：净旋转不是 `0°` 时，四轮合成恒等旋转，位移相互抵消。

**同模式。** LC 874 模拟行走机器人、LC 657 机器人能否返回原点、LC 2069 模拟行走机器人 II
