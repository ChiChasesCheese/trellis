---
id: tlc-maximum-gap-2-code
node: b.maximum-gap
type: qa
step: 2
---
## Q
**LC 164 最大间距**｜写出 Python 实现

整数数组 `nums`（长度 `1..10^5`，元素 `0..10^9`），返回排序后相邻元素的最大差值，少于两个元素返回 `0`。要求 `O(n)` 时间和额外空间，不能直接排序。

## A
**思路。** 求 `lo`、`hi`；桶宽 `size = max(1, (hi - lo) // (n - 1))`，桶编号 `(x - lo) // size`；每个桶记最小值和最大值；按桶顺序扫描，跳过空桶，用「本桶最小值 - 上一个非空桶最大值」更新答案，再把上一个最大值换成本桶最大值。

```python
def maximum_gap(nums: list[int]) -> int:
    n = len(nums)
    if n < 2:
        return 0
    lo, hi = min(nums), max(nums)
    if lo == hi:                                # 全相等：排序后相邻差全是 0
        return 0
    size = max(1, (hi - lo) // (n - 1))         # 桶宽 <= 平均间距的下界，保证桶内差一定小于答案
    count = (hi - lo) // size + 1
    bucket_min = [hi + 1] * count               # 每个桶只记最小值和最大值
    bucket_max = [-1] * count
    for x in nums:
        i = (x - lo) // size
        bucket_min[i] = min(bucket_min[i], x)
        bucket_max[i] = max(bucket_max[i], x)
    best, prev_max = 0, lo
    for mn, mx in zip(bucket_min, bucket_max):
        if mx < 0:                              # 空桶：跳过，prev_max 保持不变
            continue
        best = max(best, mn - prev_max)         # 只比较"本桶最小 - 上一个非空桶最大"
        prev_max = mx
    return best
```

**运行。** `[3,6,9,1]` → `3`；`[10]` → `0`；`[1,1,1]` → `0`；`[1,10000000]` → `9999999`；`[0,1000000000]` → `1000000000`；`[1,2,100,101]` → `98`。

**复杂度。** 时间 `O(n)`：`min`、`max`、分桶、扫描各一遍；空间 `O(n)`：桶数 `(hi - lo) // size + 1`，不超过 `2n`（整除把桶宽至多缩小一半）。

**写法要点。** 用两个并行列表存桶的最小 / 最大值，空桶用哨兵（最小值取 `hi + 1`，最大值取 `-1`）表示，扫描时 `zip(bucket_min, bucket_max)` 同步遍历，`mx < 0` 即空桶；`prev_max` 初值取 `lo`，这样第一个非空桶（必含 `lo`）的差为 `0`，不用特判；整数除法 `//` 对非负数就是向下取整，所以桶编号不会出现浮点误差。
