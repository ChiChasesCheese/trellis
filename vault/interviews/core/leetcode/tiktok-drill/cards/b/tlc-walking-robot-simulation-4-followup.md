---
id: tlc-walking-robot-simulation-4-followup
node: b.walking-robot-simulation
type: qa
step: 4
---
## Q
**LC 874 模拟行走机器人**｜追问

面试官接着问：（1）每条前进命令的步数变得很大（比如 `10^9`）怎么办？（2）障碍坐标范围很大时如何省内存？（3）要输出整条路径？

## A
1. **步数很大。** 逐格走不再可行。把障碍按列（同一个 `x` 的所有 `y`）和按行（同一个 `y` 的所有 `x`）分组并排序，沿前进方向用二分（`bisect`）找到最近的障碍，直接把目标坐标截到障碍前一格：

```python
from bisect import bisect_left, bisect_right
from collections import defaultdict


def robot_sim_far(commands: list[int], obstacles: list[list[int]]) -> int:
    by_x: defaultdict[int, list[int]] = defaultdict(list)   # x -> 该列所有障碍的 y（有序）
    by_y: defaultdict[int, list[int]] = defaultdict(list)   # y -> 该行所有障碍的 x（有序）
    for ox, oy in obstacles:
        by_x[ox].append(oy)
        by_y[oy].append(ox)
    for line in (*by_x.values(), *by_y.values()):
        line.sort()
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    x = y = d = best = 0
    for cmd in commands:
        if cmd == -1:
            d = (d + 1) % 4
        elif cmd == -2:
            d = (d - 1) % 4
        else:
            dx, dy = dirs[d]
            vertical = dx == 0
            line = by_x.get(x, []) if vertical else by_y.get(y, [])
            pos, step = (y, dy) if vertical else (x, dx)
            target = pos + step * cmd
            if step > 0:
                i = bisect_right(line, pos)                 # 前方第一个障碍
                if i < len(line):
                    target = min(target, line[i] - 1)
            else:
                i = bisect_left(line, pos)                  # line[i - 1] 是后方最近的障碍
                if i:
                    target = max(target, line[i - 1] + 1)
            if vertical:
                y = target
            else:
                x = target
            best = max(best, x * x + y * y)
    return best
```

时间 `O(m log m + C log m)`。
2. **省内存。** 把 `(x, y)` 编码成一个整数，例如 `(x + 30000) * 60001 + (y + 30000)`，集合里存整数比存元组省内存也更快，但可读性变差；坐标范围无界时就用上面的分组二分。
3. **输出路径。** 每走一格把 `(x, y)` 追加到列表；步数很大时只记录每条命令的终点。

**Python 提醒**：`dict.get(key, [])` 查询不存在的列不会创建键，而 `defaultdict` 的下标读取会插入空列表；这里读取用 `.get`，只在建表时用 `defaultdict`。
