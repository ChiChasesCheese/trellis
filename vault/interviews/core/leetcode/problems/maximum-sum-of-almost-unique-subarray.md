---
slug: maximum-sum-of-almost-unique-subarray
---
## Q
**LC 2841 几乎唯一子数组的最大和**｜Medium

整数数组 `nums` 和正整数 `m`、`k`。"几乎唯一"子数组：长度为 `k` 且至少含 `m` 个不同元素。求所有几乎唯一子数组中元素和的最大值，没有则返回 `0`。

## A
**一句话。** 定长滑动窗口：用计数表维护窗口内的不同元素个数和窗口和，每滑一步更新进、出的元素，不同数 `>= m` 时更新答案。

```python
def max_sum(nums, m, k):
    cnt = Counter()
    s = ans = 0
    for i, x in enumerate(nums):
        cnt[x] += 1
        s += x
        if i >= k:                       # 左端滑出
            y = nums[i - k]
            cnt[y] -= 1
            if cnt[y] == 0:
                del cnt[y]               # 不同数个数 = len(cnt)
            s -= y
        if i >= k - 1 and len(cnt) >= m:
            ans = max(ans, s)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 计数为 `0` 时没删掉键：`len(cnt)` 会多算不同元素。
- 窗口没满就更新答案：要 `i >= k - 1`。

**追问。**
- 为什么不要求恰好 `m` 个？：题目是"至少 `m` 个不同"，用 `>=`。

**同模式。** LC 438 找到字符串中所有字母异位词、LC 643 子数组最大平均数 I、LC 3 无重复字符的最长子串
