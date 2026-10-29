---
id: tlc-subarray-with-elements-greater-than-varying-threshold-1-signal
node: a.subarray-with-elements-greater-than-varying-threshold
type: qa
step: 1
---
## Q
**LC 2334 元素值大于变化阈值的子数组**｜Hard · LC TikTok 热度 88/100

给整数数组 `nums` 和整数 `threshold`。找一个长度为 `k` 的连续子数组，使其中**每个**元素都大于 `threshold / k`，返回任意一个满足的子数组的长度，没有就返回 `-1`。`1 <= nums.length <= 10^5`，`1 <= nums[i], threshold <= 10^9`。例：`nums = [1,3,4,3,1], threshold = 6` → `3`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「每个元素都大于某个值」=「**最小值**大于某个值」→ 关注窗口的最小值。
- 阈值 `threshold / k` 依赖窗口长度 `k` → 对每个元素，问它做最小值时窗口最宽能到多少 → 单调栈（monotonic stack）求左右第一个更小的位置，与 LC 84 柱状图中最大的矩形同构。
- `n <= 10^5`：`O(n^2)` 枚举子数组不行，目标 `O(n)` 或 `O(n log n)`。

**推导链。**
1. 暴力：枚举所有子数组，维护最小值 `m` 和长度 `k`，检查 `m * k > threshold`，`O(n^2)`。
2. 浪费：最小值相同时，窗口越宽 `m * k` 越大，只有最宽的那个才可能是答案。
3. 洞察：每个元素 `h` 做最小值时，最宽区间被左右第一个更小的元素夹住，单调栈弹栈时一次拿到边界，宽度 `k = i - left - 1`。
4. 条件 `h > threshold / k` 乘 `k` 写成 `h * k > threshold`，整数比较，没有精度问题；任意一个满足就返回 `k`。

**同模式的题**：LC 84 柱状图中最大的矩形、LC 907 子数组的最小值之和、LC 85 最大矩形、LC 739 每日温度。
