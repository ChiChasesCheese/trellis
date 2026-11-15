---
slug: divide-array-in-sets-of-k-consecutive-numbers
---
## Q
**LC 1296 划分数组为连续数字的集合**｜Medium

整数数组 `nums` 和正整数 `k`，判断能否把数组划分成若干组，每组恰有 `k` 个**连续**整数。

## A
**一句话。** 贪心：从最小的数开始，它必须是某一组的起点，把 `x..x+k-1` 各扣掉它出现的次数。

```python
def is_possible_divide(nums, k):
    if len(nums) % k:
        return False
    cnt = Counter(nums)
    for x in sorted(cnt):            # 从小到大，最小的必为组首
        c = cnt[x]
        if c:
            for y in range(x, x + k):    # 以 x 起头的 c 组
                if cnt[y] < c:
                    return False
                cnt[y] -= c
    return True
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 不检查 `len % k`：数量不是 `k` 的倍数，必不可能。
- 每次只扣一组：重复值多时慢，一次扣掉 `c` 组更快。
- 访问不存在的键：`Counter` 对缺失键返回 0，天然当作不够，不会报错。

**追问。**
- 和「一手顺子」（LC 846）有何关系？：完全一样，`groupSize` 对应 `k`。
- 为什么最小的数一定是组首？：它没有更小的数可作前驱，只能当起点。

**同模式。** LC 846 一手顺子、LC 659 分割数组为连续子序列、LC 128 最长连续序列
