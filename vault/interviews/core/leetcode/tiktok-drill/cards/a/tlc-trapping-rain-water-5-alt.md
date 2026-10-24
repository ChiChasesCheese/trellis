---
id: tlc-trapping-rain-water-5-alt
node: a.trapping-rain-water
type: qa
step: 5
---
## Q
**LC 42 接雨水**｜另一种解法

不用双指针，用前缀最大值和后缀最大值怎么解接雨水？什么时候选它，什么时候选双指针？

## A
**思路。** 第 `i` 格的水量是 `min(prefix[i], suffix[i]) - height[i]`，`prefix[i]` 是 `height[:i+1]` 的最大值，`suffix[i]` 是 `height[i:]` 的最大值。两个数组各用 `itertools.accumulate(..., max)` 一次扫出来，再 `zip` 求和。

```python
from itertools import accumulate


def trap(height: list[int]) -> int:
    prefix = accumulate(height, max)                       # prefix[i] = max(height[:i+1])
    suffix = list(accumulate(reversed(height), max))[::-1]  # suffix[i] = max(height[i:])
    return sum(min(lm, rm) - h for lm, rm, h in zip(prefix, suffix, height))
```

运行：`[0,1,0,2,1,0,1,3,2,1,2,1]` → `6`，`[4,2,0,3,2,5]` → `9`，`[5]` → `0`，`[5,0,5]` → `5`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（后缀数组）。

**怎么选。** 前缀 / 后缀版本三行写完，公式就是题意本身，最不容易写错，也方便改成输出每格水量或在此基础上加约束；面试官问「能不能 `O(1)` 空间」时再换成双指针。单调栈版是第三条路，按层累加，适合同时在做「柱状图中最大的矩形」这类栈题时顺手使用。`accumulate(height, max)` 返回迭代器，`prefix` 在 `zip` 里直接消费，不必转成列表；`suffix` 需要先反向累加再反转，必须转成列表。
