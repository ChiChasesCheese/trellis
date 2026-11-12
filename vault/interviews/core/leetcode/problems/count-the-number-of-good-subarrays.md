---
slug: count-the-number-of-good-subarrays
---
## Q
**LC 2537 统计好子数组的数目**｜Medium

子数组中至少有 `k` 对下标 `i < j` 满足 `arr[i] == arr[j]` 就是好子数组，求 `nums` 中好子数组的数目。

## A
**一句话。** 滑动窗口：右端固定，把左端移到再移就不好的位置，左边所有起点都合法，累加 `left`。

```python
def count_good(nums, k):
    cnt = defaultdict(int)
    pairs = left = ans = 0
    for x in nums:
        pairs += cnt[x]          # 与窗口里每个同值元素成一对
        cnt[x] += 1
        while pairs >= k:        # 仍然好：继续缩小
            cnt[nums[left]] -= 1
            pairs -= cnt[nums[left]]
            left += 1
        ans += left              # 起点 0..left-1 都合法
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 套「至多」型模板 `ans += right - left + 1`：这是「至少」型，要数的是能向左延伸的起点数 `left`。
- 移出元素时先减计数再减对数：`pairs -= cnt[x]` 要在 `cnt[x] -= 1` 之后，否则多减一对。

**追问。**
- 只求最短的好子数组长度？：窗口仍好时记录 `right - left + 1` 的最小值。
- `k` 很大怎么办？：超过 `n(n-1)/2` 时直接返回 `0`。

**同模式。** LC 713 乘积小于 K 的子数组、LC 930 和相同的二元子数组、LC 992 K 个不同整数的子数组、LC 1248 统计优美子数组
