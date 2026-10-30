---
id: tlc-find-minimum-in-rotated-sorted-array-0-intuition-left
node: a.find-minimum-in-rotated-sorted-array
type: qa
---
## Q
**LC 153 寻找旋转排序数组中的最小值**｜直觉：和左端比为什么会错，怎么补

如果改成拿 `nums[mid]` 和左端 `nums[lo]` 比（`nums[mid] >= nums[lo]` 就 `lo = mid + 1`），哪里会出错？要怎么补才能用？

## A
**左端说明不了断崖在哪。** `nums[mid] > nums[lo]` 只说明 mid 和 lo 在同一个递增段里，没说这一段后面有没有断崖：

- `[4,5,6,7,0,1,2]`：mid = 7 > lo = 4，后面有断崖，最小值在右边，往右走对
- `[1,2,3,4,5]`：mid = 3 > lo = 1，后面没有断崖，最小值就是 lo 本身，往右走错，返回 `5`

同样的比较结果，两种情况答案相反，无法区分。

**更隐蔽的坑。** `lo = mid + 1` 之后，lo 可能正好跳到最小值上：`[3,4,5,1,2]` 第一步 lo 跳到 `1`，这时 `[lo, hi]` 已经是有序的 `[1,2]`，又落入上面的失效情形，最后返回 `2`。

**补丁。** 先排除「区间已有序」，剩下的区间必然包含断崖，再和左端比就没有歧义：

```python
def find_min_left(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        if nums[lo] < nums[hi]:      # 区间已有序，lo 就是最小值
            return nums[lo]
        mid = (lo + hi) // 2
        if nums[mid] >= nums[lo]:    # mid 在左段（含 mid == lo），往右走
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
```

这里要用 `>=`：`lo == mid` 时 `nums[mid] == nums[lo]`，mid 在左段，应该往右走。

**结论。** 和右端比不需要补丁，也没有等号边界的问题，所以找最小值就和右端比。
