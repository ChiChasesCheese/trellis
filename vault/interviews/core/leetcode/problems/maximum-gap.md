---
slug: maximum-gap
---
## Q
**LC 164 最大间距**｜Hard

无序整数数组 `nums`，返回排序后相邻元素的最大差值，不足 2 个元素返回 `0`。要求线性时间和空间。

## A
**一句话。** 桶排序加鸽巢原理：桶宽取平均间距，最大间距必出现在相邻非空桶之间，每桶只记最小最大值。

```python
def maximum_gap(nums):
    n = len(nums)
    lo, hi = min(nums), max(nums)
    if n < 2 or lo == hi:
        return 0
    size = max(1, (hi - lo) // (n - 1))   # 桶宽 <= 平均间距
    cnt = (hi - lo) // size + 1
    bmin, bmax = [hi + 1] * cnt, [-1] * cnt
    for x in nums:
        i = (x - lo) // size
        bmin[i] = min(bmin[i], x)
        bmax[i] = max(bmax[i], x)
    best, prev = 0, lo
    for mn, mx in zip(bmin, bmax):
        if mx < 0:                # 空桶跳过
            continue
        best = max(best, mn - prev)
        prev = mx
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 桶宽整除得 `0`：`[1,1,1,2]` 除零，要 `max(1, ...)`。
- 只比较相邻编号的桶：`[1,2,100,101]` 遇空桶断开得 `0`，应为 `98`，要用上一个非空桶的最大值。
- 全部相等没有桶可分，先返回 `0`。

**追问。**
- 为什么桶内不用看？：桶宽不超过平均间距的下界，同桶两数差小于最大间距。
- 值域很小怎么办？：直接开计数数组扫一遍，`O(n+V)`。

**同模式。** LC 220 存在重复元素 III、LC 347 前 K 个高频元素、LC 539 最小时间差
