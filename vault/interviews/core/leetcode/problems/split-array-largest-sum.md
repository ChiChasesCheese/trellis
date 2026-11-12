---
slug: split-array-largest-sum
---
## Q
**LC 410 分割数组的最大值**｜Hard

把非负数组 `nums` 切成 `k` 个非空连续段，使各段和的最大值最小，求这个最小值。

## A
**一句话。** 二分答案（每段和的上限 `cap`），贪心数最少要几段，段数 `<= k` 就够用。

```python
def split_array(nums, k):
    def groups(cap):           # 每段和 <= cap 时最少几段
        cnt, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                cnt += 1
                cur = 0
            cur += x
        return cnt

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if groups(mid) <= k:   # 段数少可继续拆，最大值不变大
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**复杂度。** 时间 `O(n log sum)`，空间 `O(1)`。

**易错点。**
- 下界取 `0` 或 `1`：比 `cap` 大的元素被当成自己一段，`[1,4,4]`, `k=3` 得 `1`，应为 `4`。
- 判定写成 `== k`：`[1,4,4]`, `k=3` 得 `9`，应为 `4`，条件是 `<= k`。
- 区间写成 `lo <= hi` 却返回 `hi`：示例一得 `17`，应为 `18`。

**追问。**
- 有负数呢？：贪心判定和单调性都失效，只能用划分 DP，`O(kn²)`。
- 反过来最大化最小值呢？：同一框架，判定改成「能否凑出 `k` 份且每份至少 `cap`」，方向相反。

**同模式。** LC 1011 在 D 天内送达包裹的能力、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数、LC 774 最小化去加油站的最大距离
