---
slug: count-frequency-staircase-subarrays-i
---
## Q
**LC 4094 统计频次阶梯子数组的数目 I**｜Medium

子数组的不同值按首次出现的顺序，第 `k` 个恰好出现 `k` 次，则是「频次阶梯」。统计 `nums` 中频次阶梯子数组的个数。

## A
**一句话。** 固定左端点向右扩展，按首次出现给值编名次，维护「计数恰好等于 名次+1」的个数 `good`，`good` 等于不同值个数就计一个。

```python
def count_staircase_subarrays(nums):
    ans = 0
    for left in range(len(nums)):
        rank = {}        # 值 -> 首次出现的名次（从 0 起）
        cnt = []         # cnt[k]：名次 k 的出现次数
        good = 0         # 满足 cnt[k] == k + 1 的个数
        for x in nums[left:]:
            if x not in rank:
                rank[x] = len(cnt)
                cnt.append(0)
            k = rank[x]
            if cnt[k] == k + 1:
                good -= 1            # 撤销旧状态
            cnt[k] += 1
            if cnt[k] == k + 1:
                good += 1
            if good == len(cnt):
                ans += 1
    return ans
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 不满足就 `break`：后续元素能把不满足补成满足，`[5,8,8,2,2,2]` 得 `6`，应为 `9`。
- 只比频次多重集合、不看顺序：`[6,6,9]` 频次 `{2,1}` 被错数，先出现的 `6` 必须只出现 `1` 次。

**追问。**
- 能优于 `O(n^2)` 吗？：本题 `n <= 1500`，枚举左端点够用。

**同模式。** LC 992 K 个不同整数的子数组、LC 1248 统计优美子数组、LC 2537 统计好子数组的数目、LC 2262 字符串的总引力
