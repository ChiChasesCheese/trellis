---
id: tlc-search-insert-position-4-followup
node: p4.search-insert-position
type: qa
step: 4
---
## Q
**LC 35 搜索插入位置**｜追问

升序数组里用半开区间二分求第一个 `>= target` 的下标，已经写好。面试官接着问：（1）数组里有重复元素，要 `target` 的第一个和最后一个位置？（2）想用标准库，等价写法是什么？（3）答案不在数组里，比如「求最小的 `x` 使 `x * x >= 50`」，怎么套同一个模板？（4）数组被旋转过呢？

## A
1. **重复元素**：`first = bisect_left(a, t)` 是第一个 `>= t` 的位置，`last = bisect_right(a, t) - 1` 是最后一个 `<= t` 的位置；`first < bisect_right(a, t)` 才说明 `t` 存在。`a = [1,2,2,2,3]`、`t = 2` → `[1, 3]`，`t = 4` → 不存在（LC 34）。
2. **标准库**：`bisect_left(nums, target)` 与手写完全等价，`O(log n)`；`bisect_right` 对应「第一个 `> target`」。
3. **答案空间不是数组**：写一个单调的判定函数 `ok(x)`，找第一个为真的 `x`。`bisect_left(range(100), True, key=lambda x: x * x >= 50)` → `8`（3.10+ 的 `key` 参数，判定函数先假后真）。手写时同一个半开区间模板，把 `nums[mid] < target` 换成 `not ok(mid)`。
4. **旋转数组**：每次比较 `nums[mid]` 和 `nums[hi]`（或两端），先判断哪一半是有序的，再判断 `target` 是否落在有序的那一半，决定丢哪半；本质仍然是每轮丢掉一半。

**Python 提醒**：`bisect` 只在列表**已排序**时正确，不会检查；`key=` 只作用于列表元素，不作用于 `x`（`bisect_left(a, x, key=f)` 比较 `f(a[i])` 与 `x`，要自己把 `x` 也变换过）。
