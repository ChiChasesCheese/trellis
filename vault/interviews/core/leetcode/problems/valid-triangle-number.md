---
slug: valid-triangle-number
---
## Q
**LC 611 有效三角形的个数**｜Medium

给非负整数数组 `nums`，数出能取三个数做边长构成三角形的三元组个数（按下标区分）。

## A
**一句话。** 排序后固定最长边 `nums[k]`，用双指针数满足 `nums[i] + nums[j] > nums[k]` 的 `(i, j)` 对。

```python
def triangle_number(nums):
    nums.sort()
    ans = 0
    for k in range(len(nums) - 1, 1, -1):  # nums[k] 做最长边
        i, j = 0, k - 1
        while i < j:
            if nums[i] + nums[j] > nums[k]:
                ans += j - i       # i..j-1 配 j 都行
                j -= 1
            else:
                i += 1
    return ans
```

**复杂度。** 时间 `O(n²)`，空间 `O(1)`（不计排序）。

**易错点。**
- 三条边都验证：排序后只需较短两边之和大于最长边，其余两个不等式必成立。
- `ans += 1`：`nums[i] + nums[j] > nums[k]` 时 `i..j-1` 中任何一个配 `j` 都满足，一次加 `j - i`。
- 含 `0` 的边：`0 + x > x` 不成立，会被自然排除，不用特判。

**追问。**
- 为什么固定最长边？：这样「和大于最长边」是唯一要验证的条件，也让两个指针单调移动。
- 能比 `O(n²)` 更快吗？：一般不能，因为答案本身可达 `O(n³)` 个且需按对统计，`O(n²)` 已是常见上界。

**同模式。** LC 15 三数之和、LC 259 较小的三数之和、LC 16 最接近的三数之和、LC 167 两数之和 II - 输入有序数组
