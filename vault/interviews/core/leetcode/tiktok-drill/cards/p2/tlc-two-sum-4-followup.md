---
id: tlc-two-sum-4-followup
node: p2.two-sum
type: qa
step: 4
---
## Q
**LC 1 两数之和**｜追问

面试官接着问：（1）数组**已经有序**，要求额外空间 `O(1)`？（2）要返回所有不重复的数值对，而不是下标？（3）改成设计题：反复 `add(number)`，再反复 `find(value)` 问「有没有两个数之和为 `value`」？

## A
1. **有序数组 + `O(1)` 空间**：双指针（two pointers）。和太小就左指针右移，太大就右指针左移，每步排除一个元素，`O(n)` 时间。依据是有序带来的单调性。
```python
def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        if (s := nums[lo] + nums[hi]) == target:
            return [lo, hi]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return []
```
2. **所有不重复的数值对**：不要下标，只要值，用 `Counter` 去重。`x` 和 `target - x` 不同时，各出现一次即可；相同时（`2x == target`）需要出现至少两次。`[1,1,2,3,4,5,5]`、`target = 6` 得到 `(1,5)`、`(2,4)`。
3. **设计题**：`add` 只做 `count[number] += 1`，是 `O(1)`；`find` 遍历 `count` 的键，查 `value - x` 是否存在，`x` 与 `value - x` 相同时要求计数大于 1，是 `O(n)`。读多写少时反过来：`add` 时更新「所有可能的和」集合，`find` 变成 `O(1)`，代价是 `add` 变成 `O(n)`、内存变大。

**Python 提醒**：不要先用 `{x: i for i, x in enumerate(nums)}` 建完整个表再查——重复值会让后面的下标覆盖前面的，`[3,3]` 的两个 3 就会被当成同一个；一旦这样写，必须额外判断 `j != i`。
