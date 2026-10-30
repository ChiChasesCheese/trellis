---
id: tlc-trapping-rain-water-3-why
node: p2.trapping-rain-water
type: qa
step: 3
---
## Q
**LC 42 接雨水**｜正确性

双指针解法里，为什么 `height[left] < height[right]` 时就可以立刻结算 `left` 这一格，而不用知道它右边的真实最大值？把比较方向写反会错在哪里，给一个具体输入。

## A
**不变量。** `left_max` 是 `height[0..left]` 的最大值，`right_max` 是 `height[right..n-1]` 的最大值。第 `i` 格的真实水量是 `min(L, R) - height[i]`，`L` 是 `height[0..i]` 的最大值，`R` 是 `height[i..n-1]` 的最大值。

**为什么可以结算较矮的一侧。** 设此刻 `height[left] < height[right]`。左指针之前跳过的每一个柱子 `j`，当时都比当时的右指针所指的柱子矮，而那个右指针位置不在 `left` 的左边，所以 `height[j] <= R`；`height[left] < height[right] <= R` 同样成立。因此 `L = left_max <= R`，`min(L, R)` 就是 `left_max`，不需要知道 `R` 的精确值。右侧对称。

**反例：把比较写反。** 输入 `[0,0,1]`，没有凹槽，正确答案 `0`。若写成「`height[left] > height[right]` 时处理左侧，否则处理右侧」：第一步 `0 > 1` 为假，处理右侧，累加 `1 - 1 = 0`，`right` 左移到 `1`；第二步 `0 > 0` 为假，仍处理右侧，`right_max` 还是 `1`，累加 `1 - 0 = 1`，最终答案错成 `1`。被结算的是较高的一侧，而它左边没有任何不低于 `1` 的柱子托住水，水会流走。

**另一个错误：** 用整体最大值减每个高度。`[4,2,0,3,2,5]` 得 `14`，正确是 `9`，因为水位还受两侧各自最大值的限制。
