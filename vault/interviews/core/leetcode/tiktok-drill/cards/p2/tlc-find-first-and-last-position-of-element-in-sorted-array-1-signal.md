---
id: tlc-find-first-and-last-position-of-element-in-sorted-array-1-signal
node: p2.find-first-and-last-position-of-element-in-sorted-array
type: qa
step: 1
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜Medium · LC TikTok 近 3 个月热度 62/100（全时段 53） · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 24 次 · 最近 2026-03-30（国内 CodeTop）

给按非递减顺序排列的整数数组 `nums` 和目标值 `target`，返回 `target` 的开始位置和结束位置，不存在则返回 `[-1, -1]`。必须是 `O(log n)`。`0 <= nums.length <= 10^5`，`-10^9 <= nums[i], target <= 10^9`。例：`nums = [5,7,7,8,8,10]`，`target = 8` → `[3,4]`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「有序数组」+「`O(log n)`」→ **二分查找**。
- 「非递减」允许重复，要「第一个」和「最后一个」→ 找**边界**，不是找任意一个相等的位置：二分的变体 **lower bound**（第一个 `>= x`）。
- 条件 `nums[i] >= target` 沿下标单调（前面全假、后面全真）→ 二分的是“分界点”，这类题统一的看法：把问题改写成「找第一个满足条件的位置」。
- `nums` 可能为空、`target` 可能不存在 → 结果可能是越界下标 `len(nums)`，要检查。

**推导链。**
1. 暴力：线性扫描 `O(n)`，不满足 `O(log n)`。
2. 普通二分找到一个 `target` 后向两边扩张：数组全是 `target` 时退化成 `O(n)`。
3. 抽象：`first(x)` = 第一个 `>= x` 的下标，二分 `O(log n)`。
4. 起点 = `first(target)`；终点 = 第一个 `> target` 的下标 - 1。整数里 `> target` 等于 `>= target + 1`，所以终点 = `first(target + 1) - 1`，同一个函数调用两次。
5. 检查存在：`first(target)` 越界或该位置值不等于 `target`，返回 `[-1, -1]`。总共 `O(log n)`。

**同模式的题**：LC 35 搜索插入位置、LC 704 二分查找、LC 540 有序数组中的单一元素、LC 162 寻找峰值、LC 33 搜索旋转排序数组。
