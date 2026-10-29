---
id: tlc-find-two-non-overlapping-sub-arrays-each-with-target-sum-3-why
node: b.find-two-non-overlapping-sub-arrays-each-with-target-sum
type: qa
step: 3
---
## Q
**LC 1477 找两个和为目标值且不重叠的子数组**｜正确性

为什么把当前子数组与 `best[left]` 配对就保证了「不重叠」，并且不会漏掉最优解？如果改成直接取全局最短的两个目标子数组，会在什么输入上出错？

## A
**不变量。** 处理完下标 `right` 后，`best[right + 1]` 是 `arr[:right + 1]` 里和为 `target` 的最短子数组长度；窗口 `arr[left..right]` 是以 `right` 结尾、和 `<= target` 的最长窗口。

**为什么不重叠。** 当窗口和恰好为 `target` 时，当前子数组是 `[left, right]`。`best[left]` 只统计 `arr[:left]`，即下标 `0..left-1`，一定完全在当前子数组左边，所以两段不重叠。

**为什么不漏。** 对任意一组最优解（左段 `A`、右段 `B`，`A` 在 `B` 左边），元素为正使得以 `B` 的右端点结尾的目标子数组唯一，所以扫描到 `B.right` 时窗口恰好就是 `B`；此时 `best[B.left] <= len(A)`（`A` 完全在 `B.left` 之前），因此候选值不大于最优值。

**反例（忽略重叠）。** `arr = [1,2,1]`，`target = 3`。和为 `3` 的子数组有 `[1,2]`（下标 `0..1`）和 `[2,1]`（下标 `1..2`），都是长度 `2`。取两个最短的得 `4`，但它们共用下标 `1`，重叠；正确答案 `-1`。用 `best[left]`：扫到 `right=1` 时窗口 `[0,1]`，`best[0] = INF`，不更新；扫到 `right=2` 时窗口 `[1,2]`，`best[1] = INF`（`arr[:1] = [1]` 没有目标子数组），不更新，输出 `-1`。
