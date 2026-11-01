---
slug: find-target-indices-after-sorting-array
---
## Q
**LC 2089 找出数组排序后的目标下标**｜Easy

给你一个下标从 0 开始的整数数组 `nums` 和一个目标元素 `target`。目标下标是满足 `nums[i] == target` 的下标 `i`。将 `nums` 按非递减顺序排序后，返回由 `nums` 中目标下标组成的列表（指排序后数组中的下标）；若不存在目标下标，返回空列表。返回的列表必须按递增顺序排列。`1 <= nums.length <= 100`，`1 <= nums[i], target <= 100`。

例：`nums = [1,2,5,2,3]`，`target = 2` → `[1,2]`（排序后是 `[1,2,2,3,5]`）；`target = 3` → `[3]`；`target = 4` → `[]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 计数代替排序：排序后一个值的位置区间由「比它小的个数」决定。

**核心题。**

- LC 75 颜色分类（Hot 100）：同一个计数排序：先数每个值的个数再按前缀和定位置

**一句话。** 排序后 `target` 占据一段连续下标，起点是数组里**小于** `target` 的元素个数 `less`，长度是 `target` 出现的次数 `equal`，答案就是 `range(less, less + equal)`。

**识别。** 「排序后」「下标」「按递增返回」：答案由排序后的**位置**决定，不需要真的排序；输出本身是一段连续区间，说明只要知道起点和长度。

**推导。** 直接做：排序，再遍历一遍收集等于 `target` 的下标，`O(n log n)`。浪费在于排序把整个数组的顺序都排出来了，而问题只关心 `target` 前面有几个更小的数：排序后，所有更小的数排在它前面且恰好占满下标 `0..less-1`，接着是 `equal` 个 `target`。所以一遍计数就够了，`O(n)`。

**简单解法。** 先 `sorted(nums)`，再 `[i for i, x in enumerate(sorted(nums)) if x == target]`。`n <= 100`，这样写同样是可以直接交上去的答案；计数写法省掉排序，并且把「连续区间」这个结构暴露出来。

```python
def target_indices(nums: list[int], target: int) -> list[int]:
    less = sum(x < target for x in nums)    # 比 target 小的个数 = 排序后 target 的起始下标
    equal = nums.count(target)              # target 的个数 = 区间长度
    return list(range(less, less + equal))  # 不存在时 equal = 0，自然得到 []
```

运行：`nums = [1,2,5,2,3]`，`target = 2` → `[1, 2]`；`target = 3` → `[3]`；`target = 5` → `[4]`；`target = 4` → `[]`；`nums = [1,1,1]`，`target = 1` → `[0, 1, 2]`；`nums = [5]`，`target = 5` → `[0]`。

**复杂度。** 时间 `O(n)`（两趟扫描），额外空间除结果外 `O(1)`。

**易错点。**
- 起点用 `x <= target` 计数：把等于 `target` 的也算进去，`[1,2,5,2,3]`、`target = 2` 得到 `[3, 4]`，正确是 `[1, 2]`。
- 返回原数组里的下标：同一个例子得到 `[1, 3]`，题目要的是**排序后**的下标。
- 对不存在的 `target` 单独分支：`equal = 0` 时 `range` 本来就是空，多写分支只会引入错误。

**同模式。** LC 1365 有多少小于当前数字的数字、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 35 搜索插入位置、LC 912 排序数组。
