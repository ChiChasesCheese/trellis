---
id: tlc-reverse-subarray-to-maximize-array-value-2-code
node: a.reverse-subarray-to-maximize-array-value
type: qa
step: 2
---
## Q
**LC 1330 翻转子数组得到最大的数组值**｜Hard · 字节高频｜写出 Python 实现

整数数组 `nums`（`2 <= nums.length <= 3 * 10^4`，`-10^5 <= nums[i] <= 10^5`），数组值是相邻差的绝对值之和。恰好可以翻转一次任意子数组，返回最大的数组值。要求 `O(n)`。

## A
**思路。** 总和 `total` 加上最大增益 `gain`。增益取三种情形的最大值：不翻转（`0`）、翻转在中间（相邻对线段的 `2 * (max 左端点 - min 右端点)`）、翻转贴着左端或右端（只改一条相邻差）。

```python
from itertools import pairwise


def max_value_after_reverse(nums: list[int]) -> int:
    n = len(nums)
    total = sum(abs(a - b) for a, b in pairwise(nums))
    # 情况一：翻转的区间不含两端。相邻两数 (a, b) 看成数轴上的线段 [min, max]，
    # 两条不相交的线段间隔 g，翻转它们之间的部分能多赚 2g
    lo = max(min(a, b) for a, b in pairwise(nums))       # 所有线段左端点里最大的
    hi = min(max(a, b) for a, b in pairwise(nums))       # 所有线段右端点里最小的
    gain = max(0, 2 * (lo - hi))
    # 情况二：翻转的区间顶着数组的左端或右端，只改动一条相邻差
    for i in range(1, n):
        gain = max(gain,
                   abs(nums[0] - nums[i]) - abs(nums[i - 1] - nums[i]),            # 翻转 [0, i-1]
                   abs(nums[-1] - nums[i - 1]) - abs(nums[i - 1] - nums[i]))       # 翻转 [i, n-1]
    return total + gain
```

运行：`[2,3,1,5,4]` → `10`，`[2,4,9,24,2,1,10]` → `68`，`[1,2]` → `1`，`[5,5]` → `0`，`[1,5,4]` → `7`，`[-100000,100000]` → `200000`；`3 * 10^4` 个随机数瞬间返回。

**复杂度。** 时间 `O(n)`：几趟线性扫描；空间 `O(1)`。

**写法要点。** `itertools.pairwise` 一次产出所有相邻对 `(a, b)`，不用 `zip(nums, nums[1:])` 复制切片；`max(min(a, b) for ...)` 与 `min(max(a, b) for ...)` 用生成器表达式，没有中间列表；`max` 接受多个参数，一行同时比较「当前增益」和左右两种边界情形；`nums[-1]` 取最后一个元素。
