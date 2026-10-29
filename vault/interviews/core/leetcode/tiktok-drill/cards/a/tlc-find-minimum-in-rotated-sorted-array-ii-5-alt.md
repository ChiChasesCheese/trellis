---
id: tlc-find-minimum-in-rotated-sorted-array-ii-5-alt
node: a.find-minimum-in-rotated-sorted-array-ii
type: qa
step: 5
---
## Q
**LC 154 寻找旋转排序数组中的最小值 II**｜另一种解法

除了「与右端点比较、相等时收缩右端点」的二分，还有哪些可以接受的解法？什么时候用它们？（`1 <= n <= 5000`，`-5000 <= nums[i] <= 5000`，允许重复）

## A
**分治：左右各求最小，取较小者。** 如果一个区间两端满足 `nums[lo] < nums[hi]`，它没有被旋转断开，最左边就是最小值，直接返回；否则从中间分成两半递归，取两半最小值中较小的。

```python
def find_min(nums: list[int]) -> int:
    def solve(lo: int, hi: int) -> int:          # 求 nums[lo..hi] 的最小值
        if lo == hi or nums[lo] < nums[hi]:      # 区间没被旋转断开：最左边就是最小
            return nums[lo]
        mid = (lo + hi) // 2
        return min(solve(lo, mid), solve(mid + 1, hi))

    return solve(0, len(nums) - 1)
```

`[1,3,5]` → `1`，`[2,2,2,0,1]` → `0`，`[3,3,1,3]` → `1`，`[1] * 5000` → `1`（递归深度只有 `log n`）。

**还有一种最直接的写法：** `min(nums)`，`O(n)`，在 `n = 5000` 的约束下完全够用。

**怎么选。**
- 面试默认写主解法（与右端点比较的二分）：平均 `O(log n)`，空间 `O(1)`，最能体现对重复元素的处理。
- 分治版不需要想「相等时能不能丢哪一端」，每个分支的正确性一眼可见；没有重复时，被截断的一侧会很快命中 `nums[lo] < nums[hi]`，接近 `O(log n)`；全部相同时每个区间都要继续分下去，`O(n)`，与主解法的最坏情形一致。
- `min(nums)` 是正确性的基线和最短的实现；题目问「步骤尽可能少」时，它是对照而不是答案。
