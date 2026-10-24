---
id: tlc-patterns-greedy-2-jump
node: patterns.greedy
type: qa
step: 2
---
## Q
**贪心（Greedy）｜模板：跳跃游戏（LC 55）与跳跃游戏 II（LC 45）**

怎样只用一个"最远可达位置"判断能否到达终点？最少跳跃次数为什么可以按"这一跳的边界"分层？

## A
**LC 55**：从左到右扫描，维护 `far` = 当前能到达的最远下标。如果扫描到的 `i > far`，说明走不到 `i`，失败。

```python
def can_jump(nums: list[int]) -> bool:
    far = 0                                # 目前能到达的最远下标
    for i, x in enumerate(nums):
        if i > far:
            return False                   # 走不到这里
        far = max(far, i + x)
    return True

def jump(nums: list[int]) -> int:
    jumps = cur_end = far = 0
    for i in range(len(nums) - 1):         # 最后一个位置不需要再跳
        far = max(far, i + nums[i])
        if i == cur_end:                   # 走到了这一跳能到的边界：必须再跳一次
            jumps += 1
            cur_end = far                  # 下一跳能覆盖的最远位置
    return jumps
```

运行：`can_jump([2,3,1,1,4])` → `True`；`[3,2,1,0,4]` → `False`；`[0]` → `True`；`[0,1]` → `False`。`jump([2,3,1,1,4])` → `2`；`[2,3,0,1,4]` → `2`；`[0]` → `0`；`[1,1,1,1]` → `3`。

- **LC 45 的思路**：把"跳 `k` 次能到的位置"看成一个区间 `[.., cur_end]`；扫描这个区间时记录下一跳能到的最远 `far`；扫完区间（`i == cur_end`）就必须再跳一次，下一个区间的终点是 `far`。这是 BFS 按层展开的一维版本。
- 时间 `O(n)`，空间 `O(1)`；DP 写法是 `O(n^2)`，`n = 10^4` 时约 `10^8`，Python 会超时，所以这里贪心是必须的。
- 为什么贪心成立：到达某个位置的**更远的可达范围**总是不比更近的差（交换论证）。
- 循环到 `len(nums) - 1` 为止：到了最后一格不用再跳。
