---
slug: count-complete-subarrays-in-an-array
---
## Q
**LC 2799 统计完全子数组的数目**｜Medium

子数组的不同元素个数等于整个数组的不同元素个数，就叫完全子数组。求完全子数组的数目。

## A
**一句话。** 双指针：对每个左端找最小右端凑齐全部种类，其后所有右端都合法，一次加 `n - right + 1`。

```python
def count_complete_subarrays(nums):
    n, total = len(nums), len(set(nums))
    cnt = Counter()               # 窗口 nums[left:right]
    ans = right = 0
    for left in range(n):
        while right < n and len(cnt) < total:
            cnt[nums[right]] += 1     # 扩右直到凑齐
            right += 1
        if len(cnt) < total:      # 凑不齐，后面更不行
            break
        ans += n - right + 1
        cnt[nums[left]] -= 1      # left 出窗口
        if cnt[nums[left]] == 0:
            del cnt[nums[left]]   # 归零要删键
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 归零不删键：`len(cnt)` 虚高，`[1,3,1,2,2]` 算出 `10`，应为 `4`。
- 写成 `n - right`：`right` 是开区间端点，少算一个，`[1,3,1,2,2]` 得 `2`。
- 凑不齐时不 `break`：每个剩余的 `left` 都白加一次。

**追问。**
- 恰好 `k` 种的子数组数？：`atMost(k) - atMost(k-1)`，见 LC 992。
- 求最短的完全子数组？：同一窗口，凑齐时用 `right - left` 取最小。

**同模式。** LC 992 K 个不同整数的子数组、LC 930 和相同的二元子数组、LC 1248 统计优美子数组、LC 713 乘积小于 K 的子数组
