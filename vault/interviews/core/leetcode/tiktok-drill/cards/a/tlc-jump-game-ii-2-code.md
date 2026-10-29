---
id: tlc-jump-game-ii-2-code
node: a.jump-game-ii
type: qa
step: 2
---
## Q
**LC 45 跳跃游戏 II**｜写出 Python 实现

`nums` 长度 `n`（`1 <= n <= 10^4`，`0 <= nums[i] <= 1000`），从下标 `0` 出发，在下标 `i` 最多可跳 `nums[i]` 格，保证能到 `n - 1`。返回最少跳跃次数，要求 `O(n)`。

## A
**思路。** 当前跳数能覆盖的范围是 `[.., cur_end]`。扫描这个范围内的每个格子，记下它们能到的最远点 `farthest`。扫到 `cur_end` 时，这一跳的范围用完了，必须再跳一次，新范围的右边界就是 `farthest`。

```python
def jump(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):      # 最后一格不用再跳，所以不扫它
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                # 当前这一跳的范围走完了，必须再跳一次
            jumps += 1
            cur_end = farthest          # 下一层的右边界
    return jumps
```

运行：`[2,3,1,1,4]` → `2`，`[2,3,0,1,4]` → `2`，`[0]` → `0`，`[1]` → `0`，`[1,1,1,1]` → `3`，`[1]*10000` → `9999`。

**复杂度。** 时间 `O(n)`：每个下标只看一次；空间 `O(1)`：只有三个整数。

**写法要点。** `jumps = cur_end = farthest = 0` 链式赋值只用于不可变的整数；`range(len(nums) - 1)` 排除终点，是单元素数组返回 `0` 的关键；不需要 `dp` 数组，也不需要队列，层边界两个变量就够。
