---
slug: 4sum
---
## Q
**LC 18 四数之和**｜Medium

在 `nums` 中找出所有和为 `target` 且不重复的四元组。

## A
**一句话。** 排序后两层循环固定前两个数，后两个数用对撞双指针找，每个位置跳过重复值。

```python
def four_sum(nums, target):
    nums.sort()
    n, res = len(nums), []
    for i in range(n - 3):
        if i and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[j] + nums[lo] + nums[hi]
                if s < target:
                    lo += 1
                elif s > target:
                    hi -= 1
                else:
                    res.append([nums[i], nums[j],
                                nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo<hi and nums[lo] == nums[lo-1]:
                        lo += 1   # 跳过重复的第三个数
    return res
```

**复杂度。** 时间 `O(n^3)`，空间 `O(1)`。

**易错点。**
- 第二层去重写成 `j > 0`：`[2,2,2,2,2]`、`8` 把所有 `j` 都跳过，得 `[]`，应为 `[[2,2,2,2]]`。
- 找到解后只动一个指针：重复输出或死循环。

**追问。**
- 怎么推广到 k 数之和？：递归固定 `k-2` 个数，最后两个用双指针，`O(n^(k-1))`。
- 只数个数、不去重（LC 454）？：四个数组分两半，哈希表存两两之和，`O(n^2)`。
- 怎么剪枝？：最小四数和 `> target` 就 `break`，最大组合 `< target` 只能 `continue`。

**同模式。** LC 1 两数之和、LC 15 三数之和、LC 16 最接近的三数之和、LC 454 四数相加 II
