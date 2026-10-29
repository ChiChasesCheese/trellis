---
id: tlc-walking-robot-simulation-2-code
node: a.walking-robot-simulation
type: qa
step: 2
---
## Q
**LC 874 模拟行走机器人**｜写出 Python 实现

机器人从 `(0, 0)` 出发面向北；命令 `-2` 左转、`-1` 右转、`1..9` 前进若干格；遇到障碍停在前一格。`commands` 长度 `1..10^4`，`obstacles` 长度 `0..10^4`，坐标范围 `±3 * 10^4`。返回行走过程中距原点的最大欧氏距离的平方。

## A
**思路。** 方向表 `dirs` 按北、东、南、西排列，朝向下标 `d`：右转 `+1`，左转 `-1`，都对 `4` 取模。障碍转成元组放进集合。前进命令一格一格走，下一格在集合里就停；每条前进命令结束后用 `x * x + y * y` 更新答案。

```python
def robot_sim(commands: list[int], obstacles: list[list[int]]) -> int:
    blocked = set(map(tuple, obstacles))        # 列表不可哈希，先转成元组放进集合：O(1) 判断障碍
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))   # 北、东、南、西：右转 = 下标 +1，左转 = 下标 -1
    x = y = d = best = 0
    for cmd in commands:
        if cmd == -1:
            d = (d + 1) % 4
        elif cmd == -2:
            d = (d - 1) % 4
        else:
            dx, dy = dirs[d]
            for _ in range(cmd):                # 一格一格走，下一格是障碍就停
                if (x + dx, y + dy) in blocked:
                    break
                x, y = x + dx, y + dy
            best = max(best, x * x + y * y)     # 每条前进命令结束时更新最远距离
    return best
```

**运行。** `[4,-1,3]`，无障碍 → `25`；`[4,-1,4,-2,4]`，障碍 `[[2,4]]` → `65`；`[6,-1,-1,6]`，无障碍 → `36`；`[-2,-1,5]`，障碍 `[[0,0]]` → `25`；`[1,1,1]`，障碍 `[[0,1]]` → `0`。

**复杂度。** 时间 `O(9C + m)`（`C` 为命令数，`m` 为障碍数）；空间 `O(m)`。

**写法要点。** `set(map(tuple, obstacles))` 把每个 `[x, y]` 转成可哈希的元组；方向表 `dirs` 加取模代替四路 `if`；Python 的 `%` 对负数返回非负余数（`(0 - 1) % 4 == 3`），所以左转不需要 `+ 4`；`for _ in range(cmd)` 只要次数不要变量；`x = y = d = best = 0` 一行初始化四个起始值。
