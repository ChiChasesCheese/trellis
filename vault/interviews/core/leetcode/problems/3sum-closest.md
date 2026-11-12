---
slug: 3sum-closest
---
## Q
**LC 16 最接近的三数之和**｜Medium

从 `nums` 中选三个不同下标的数，使和最接近 `target`，返回这个和（保证唯一解）。

## A
**一句话。** 排序后固定一个数，剩下两个用左右双指针逼近：和偏小右移左指针，偏大左移右指针。

```python
def three_sum_closest(nums, target):
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if abs(s - target) < abs(best - target):
                best = s
            if s == target:
                return s
            if s < target:
                lo += 1
            else:
                hi -= 1
    return best
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n)`。

**易错点。**
- 比较漏了绝对值：`[-1,2,1,-4], target=1` 会得 `-4`，应为 `2`。
- `best` 初值取 `0`：`0` 未必是任何三数之和，`[1,1,1,0], target=-100` 返回 `0`，应为 `2`。
- 指针方向写反：和偏小应右移 `lo`，写反会漏掉答案。

**追问。**
- 要返回具体的三个数？：更新 `best` 时同时记下三个值，或下标。
- 推广到 `k` 个数（LC 18）？：外层再套 `k-2` 层循环，最内层双指针，`O(n^(k-1))`。

**同模式。** LC 15 三数之和、LC 18 四数之和、LC 259 较小的三数之和、LC 611 有效三角形的个数
