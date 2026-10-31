---
id: tlc-two-sum-ii-input-array-is-sorted-0-whole
node: c.two-sum-ii-input-array-is-sorted
type: qa
---
## Q
**LC 167 两数之和 II - 输入有序数组**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 6 次 · 最近 2024-12-05（国内 CodeTop）

给你一个下标从 `1` 开始的整数数组 `numbers`，已按非递减顺序排列。找出满足相加之和等于目标数 `target` 的两个数，设它们是 `numbers[index1]` 和 `numbers[index2]`，其中 `1 <= index1 < index2 <= numbers.length`，以长度为 2 的数组 `[index1, index2]` 返回。每个输入只对应唯一的答案，不能重复使用同一个元素。解决方案必须只使用常数级的额外空间。`2 <= numbers.length <= 3 * 10^4`，`-1000 <= numbers[i] <= 1000`，`-1000 <= target <= 1000`。例：`numbers = [2,7,11,15], target = 9` → `[1,2]`；`numbers = [2,3,4], target = 6` → `[1,3]`；`numbers = [-1,0], target = -1` → `[1,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 有序数组，左右各放一个指针：和太小就左指针右移，和太大就右指针左移，恰好相等就是答案；`O(n)` 时间、`O(1)` 空间。

**识别。** 「有序数组 + 找两个数的和」是对撞双指针的标准信号，而题目明说常数空间，等于禁用了哈希表的 Two Sum。

**推导。** 暴力：枚举所有数对 `O(n²)`；哈希表 `O(n)` 但用了 `O(n)` 空间。利用有序：令 `lo`、`hi` 指向两端，和 `s = numbers[lo] + numbers[hi]`。若 `s < target`，那么 `numbers[lo]` 与 `hi` 以内的**任何**数相加都不超过 `s`，也都小于 `target`，所以 `lo` 不可能是答案的一部分，直接淘汰；`s > target` 时对称地淘汰 `hi`。每一步淘汰一个下标，`n - 1` 步结束。

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    lo, hi = 0, len(numbers) - 1
    while lo < hi:                               # 两个下标必须不同
        s = numbers[lo] + numbers[hi]
        if s == target:
            return [lo + 1, hi + 1]              # 题目要求 1 开始的下标
        if s < target:
            lo += 1                              # numbers[lo] 配 hi 以内最大的数都不够：淘汰 lo
        else:
            hi -= 1                              # numbers[hi] 配 lo 以外最小的数都超了：淘汰 hi
    return []
```

运行：`([2,7,11,15], 9)` → `[1,2]`，`([2,3,4], 6)` → `[1,3]`，`([-1,0], -1)` → `[1,2]`；`([3,3], 6)` → `[1,2]`，`([1,2,3,4,4,9,56,90], 8)` → `[4,5]`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 每个元素二分找补数，`O(n log n)`、`O(1)` 空间；对撞指针更快，但二分在「`k` 个数之和」里可以复用。

```python
from bisect import bisect_left


def two_sum_bisect(numbers: list[int], target: int) -> list[int]:
    for i, x in enumerate(numbers):
        j = bisect_left(numbers, target - x, i + 1)   # 只在 i 右边找，避免重复使用同一元素
        if j < len(numbers) and numbers[j] == target - x:
            return [i + 1, j + 1]
    return []
```

**易错点。**
- 返回 0 开始的下标：`([2,7,11,15], 9)` 得到 `[0,1]`，题目要的是 `[1,2]`。
- 循环条件写成 `lo <= hi`：允许同一个元素用两次。
- 以为 `s < target` 时要移动右指针：方向反了，会漏掉答案。

**追问。**
- 允许多个答案、要求去重输出所有解：移动指针时跳过相同值（见三数之和）。
- 输入无序：先排序（记录原下标）再用对撞指针，或直接用哈希表。

**同模式。** LC 1 两数之和、LC 15 三数之和、LC 16 最接近的三数之和、LC 11 盛最多水的容器、LC 653 两数之和 IV - 输入二叉搜索树。
