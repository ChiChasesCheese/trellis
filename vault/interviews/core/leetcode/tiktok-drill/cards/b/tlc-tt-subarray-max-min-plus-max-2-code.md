---
id: tlc-tt-subarray-max-min-plus-max-2-code
node: b.tt-subarray-max-min-plus-max
type: qa
step: 2
---
## Q
**长度至少为 2 的子数组，最大化 min + max**｜写出 Python 实现

`n` 个正整数的数组 `nums`（`2 <= n <= 10^5`，`1 <= nums[i] <= 10^9`），找一个长度至少为 `2` 的连续子数组，使该子数组的最小值与最大值之和最大，返回这个和，要求线性时间。

## A
**思路。** 任何长度至少为 `2` 的子数组，其 `min + max` 不超过它里面最大值与一个相邻元素之和；这对相邻元素本身是合法子数组，所以答案等于所有相邻两数之和的最大值。

```python
from itertools import pairwise


def max_min_plus_max(nums: list[int]) -> int:
    return max(a + b for a, b in pairwise(nums))     # 最优子数组可以缩成相邻两个数
```

运行：`[5, 12, 9, 6, 4]` → `21`；`[1, 1]` → `2`；`[3, 1, 3]` → `4`；`[1, 100, 1]` → `101`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**写法要点。** `itertools.pairwise`（Python 3.10 起）按 `(nums[0], nums[1])`、`(nums[1], nums[2])` 的方式产出相邻对，比 `zip(nums, nums[1:])` 少一份切片拷贝；生成器表达式直接喂给 `max`，不建中间列表；这里的一行代码是在证明了「相邻两个数就够」之后才写的，它没有隐藏技巧，只是把结构性质表达出来，面试时要把这个性质讲清楚；`n >= 2` 保证 `pairwise` 至少产出一对，`max` 不会收到空序列。
