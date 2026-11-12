---
slug: 3sum-smaller
---
## Q
**LC 259 较小的三数之和**｜Medium

统计下标 `i < j < k` 且 `nums[i] + nums[j] + nums[k] < target` 的三元组个数。

## A
**一句话。** 排序后固定第一个数，剩下两个数用对撞双指针数对：和小于目标时 `right - left` 个右端点全部满足，一次累加。

```python
def three_sum_smaller(nums, target):
    nums.sort()              # 只数个数，排序不影响答案
    cnt = 0
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            if nums[i] + nums[l] + nums[r] < target:
                cnt += r - l   # l 与 l+1..r 都满足
                l += 1
            else:
                r -= 1
    return cnt
```

**复杂度。** 时间 `O(n^2)`，空间 `O(1)`。

**易错点。**
- 满足条件后只加 `1`：应加 `r - l`，示例一得 `1`，应为 `2`。
- 和太大时移动 `l`：只能缩 `r`，移动 `l` 会让和更大。

**追问。**
- 要返回具体三元组？：满足时枚举 `r` 到 `l+1`，输出规模可能是 `O(n^3)`。
- 四数之和小于目标？：固定两个数再双指针，`O(n^3)`。

**同模式。** LC 15 三数之和、LC 16 最接近的三数之和、LC 611 有效三角形的个数、LC 167 两数之和 II
