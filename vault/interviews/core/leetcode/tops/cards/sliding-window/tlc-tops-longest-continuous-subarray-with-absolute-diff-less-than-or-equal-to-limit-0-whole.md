---
id: tlc-tops-longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit-0-whole
node: sliding-window.longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit
type: qa
---
## Q
**LC 1438 绝对差不超过限制的最长连续子数组**｜Medium · 全公司热度第 166 名

给你一个整数数组 `nums` 和一个整数 `limit`，返回最长非空子数组的长度，要求该子数组中任意两个元素之间的差的绝对值都小于或等于 `limit`（元素对不必相邻）。`1 <= nums.length <= 10^5`，`1 <= nums[i] <= 10^9`，`0 <= limit <= 10^9`。例：`nums = [8,2,4,7], limit = 4` → `2`；`nums = [10,1,2,4,7,2], limit = 5` → `4`（`[2,4,7,2]`）；`nums = [4,2,2,2,4,4,2,2], limit = 0` → `3`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 滑动窗口（sliding window）+ 单调队列（monotonic deque）维护窗口最大值和最小值。

**一句话。** 「任意两个元素差都不超过 `limit`」等价于「窗口最大值 - 最小值 `<= limit`」；右端点扩张，违反时左端点收缩，两个单调队列分别在 `O(1)` 摊还内给出窗口的最大和最小。

**识别。** 「最长连续子数组 + 窗口内某个聚合量不超限」：缩小窗口只会让最大值变小、最小值变大，所以条件对左端点单调，可以用滑动窗口。聚合量是最大 / 最小就需要单调队列；`n = 10^5` 排除 `O(n^2)`。

**推导。** 暴力枚举每个子数组并求最大最小，`O(n^3)`，用前缀维护可降到 `O(n^2)`。滑动窗口把枚举降到 `O(n)` 个窗口，剩下的问题是窗口变动时如何快速得到最大值和最小值。用「递减队列」存可能成为最大值的元素：新元素进来时，前面比它小的元素永远不可能再是最大值，直接弹出；队首就是当前最大值，左端点越过它时才从队首移除。最小值对称。

```python
def longest_subarray(nums: list[int], limit: int) -> int:
    mx: deque[int] = deque()      # 单调递减：队首是窗口最大值
    mn: deque[int] = deque()      # 单调递增：队首是窗口最小值
    left = best = 0
    for right, x in enumerate(nums):
        while mx and mx[-1] < x:  # 严格小于才弹：相等的元素要留下，左端点离开时才能一个个对应移除
            mx.pop()
        mx.append(x)
        while mn and mn[-1] > x:
            mn.pop()
        mn.append(x)
        while mx[0] - mn[0] > limit:       # 违反条件：收缩左端点，直到合法
            if mx[0] == nums[left]:        # 离开窗口的正好是当前最大 / 最小，从队首移除
                mx.popleft()
            if mn[0] == nums[left]:
                mn.popleft()
            left += 1
        best = max(best, right - left + 1)
    return best
```

运行：`([8,2,4,7], 4)` → `2`，`([10,1,2,4,7,2], 5)` → `4`，`([4,2,2,2,4,4,2,2], 0)` → `3`，`([1], 0)` → `1`。

**复杂度。** 时间 `O(n)`（每个元素最多进出每个队列一次），空间 `O(n)`。

**拓展优化。**
- 只要最大长度、不要每一步的窗口：窗口只增不缩，把内层 `while` 改成 `if`，右端点每走一步左端点最多走一步，最后直接返回 `len(nums) - left`，省掉 `best`。
- 用有序容器代替两个队列：`SortedList` 存窗口内元素，`s[-1] - s[0]` 取极差，每步 `O(log n)`，总共 `O(n log n)`，写法短但不是线性。

**易错点。**
- 单调队列用 `<=` / `>=` 弹出相等元素：左端点离开时按值移除会把还在窗口里的相等元素误删，队列变空后 `mx[0]` 抛 `IndexError`（`[3,3,1,3]`、`limit = 0` 复现）。
- 只比较相邻元素：`[8,2,4,7]`、`limit = 4` 会得到 `3`（`[2,4,7]`，相邻差都 `<= 4`），但 `7 - 2 = 5 > 4`，正确答案是 `2`。

**同模式。** LC 239 滑动窗口最大值、LC 3 无重复字符的最长子串、LC 862 和至少为 K 的最短子数组、LC 1425 带限制的子序列和。
