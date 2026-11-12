---
slug: walking-robot-simulation
---
## Q
**LC 874 模拟行走机器人**｜Easy

机器人从 `(0, 0)` 面向北出发，命令 `-2` 左转、`-1` 右转、`1..9` 前进若干格，遇到障碍就停在前一格并继续下一条命令。返回行走过程中离原点最大欧氏距离的平方。例：`commands = [4,-1,3]`，无障碍 → `25`。

## A
**一句话。** 直接模拟：用方向表加下标表示朝向，障碍放集合，前进时一格一格走，下一格是障碍就停，每条前进命令后更新最大距离平方。

```python
def robot_sim(commands, obstacles):
    blocked = set(map(tuple, obstacles))    # 列表不可哈希
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))   # 北东南西
    x = y = d = best = 0
    for cmd in commands:
        if cmd == -1:
            d = (d + 1) % 4     # 右转
        elif cmd == -2:
            d = (d - 1) % 4     # 左转
        else:
            dx, dy = dirs[d]
            for _ in range(cmd):    # 一格一格走
                if (x + dx, y + dy) in blocked:
                    break
                x, y = x + dx, y + dy
            best = max(best, x * x + y * y)
    return best
```

**复杂度。** 时间 `O(9C + m)`，空间 `O(m)`。

**易错点。**
- 只在最后算距离：`[6,-1,-1,6]` 回到原点得 `0`，应为 `36`，最大值要在过程中取。
- 一次跳 `x` 格只查终点：越过中间的障碍，`[4,-1,4,-2,4]` 加障碍 `[2,4]` 得 `80`，应为 `65`。
- 障碍列表直接放进 `set`：抛 `TypeError: unhashable type`，要先 `map(tuple, …)`。

**追问。**
- 步数很大（如 `10^9`）？：障碍按行、列分组排序，二分找前进方向上最近的障碍，一次跳到它前一格。
- 障碍坐标范围很大？：把 `(x, y)` 编码成一个整数，省集合的内存。

**同模式。** LC 657 机器人能否返回原点、LC 489 扫地机器人、LC 2069 模拟行走机器人 II、LC 54 螺旋矩阵
