---
id: tlc-jump-game-2-code
node: p2.jump-game
type: qa
step: 2
---
## Q
**LC 55 跳跃游戏**｜写出 Python 实现

非负整数数组 `nums`（长度 `1` 到 `10^4`，元素 `0` 到 `10^5`）。你从下标 `0` 出发，位置 `i` 处最多可以向前跳 `nums[i]` 步。判断能否到达最后一个下标。要求 `O(n)` 时间、`O(1)` 空间。

## A
**思路。** 维护最远可达下标 `reach`。遍历每个下标 `i`：若 `i > reach` 说明到不了 `i`，返回 `False`；否则用 `i + nums[i]` 更新 `reach`。遍历结束返回 `True`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0                               # 目前能到达的最远下标
    for i, step in enumerate(nums):
        if i > reach:
            return False                    # 连 i 都够不着，后面更不可能
        reach = max(reach, i + step)
    return True
```

运行：`[2,3,1,1,4]` → `True`，`[3,2,1,0,4]` → `False`，`[0]` → `True`，`[0,1]` → `False`，`[1,0,1]` → `False`。

**复杂度。** 时间 `O(n)`：一趟扫描；空间 `O(1)`。

**写法要点。**
- `enumerate(nums)` 同时给出下标与跳跃长度；变量名 `step` 比 `nums[i]` 更能读出含义。
- 把「不可达就返回」放在更新 `reach` 之前：先确认当前位置可达，才能用它扩展。
- 不需要在循环里判断 `reach >= len(nums) - 1` 提前返回，加上只是常数优化；去掉后，末尾下标自然会在扫描中被确认可达。
- 反向贪心是等价写法：从后往前维护 `last`（最左的“能到终点”的下标），`i + nums[i] >= last` 就把 `last` 左移到 `i`，最后检查 `last == 0`。
