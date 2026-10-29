---
id: tlc-count-complete-subarrays-in-an-array-3-why
node: a.count-complete-subarrays-in-an-array
type: qa
step: 3
---
## Q
**LC 2799 统计完全子数组的数目**｜正确性

为什么 `left` 右移以后 `right` 不需要回退？为什么凑齐的那一刻就能一次性加上 `n - right + 1`？

## A
**不变量。** 外层循环开始处，窗口 `nums[left:right]` 是「以 `left` 开头、且种类数不足时尚未凑齐」的状态，`right` 之前的元素都已计入 `cnt`。内层 `while` 结束后，`right` 是使 `nums[left:right]` 凑齐 `total` 种的**最小**右端。

**为什么不回退。** 设 `r(left)` 为以 `left` 开头、凑齐 `total` 种的最小开区间右端。若 `[left+1, r)` 已经完全，则 `[left, r)` 多了一个元素，种类数不会减少，也完全，所以 `r(left) <= r(left+1)`：`right` 单调不减。

**为什么一次加一批。** 从 `r(left)` 起再向右扩，种类数只会不变（不会超过 `total`，因为 `total` 是整个数组的种类数），所以右端点取 `r(left) - 1, …, n - 1` 的子数组全部完全，共 `n - r(left) + 1` 个。

**反例。** 错误写法一：每个 `left` 只加 `1`。`[1,3,1,2,2]` 返回 `2`，正确是 `4`，因为 `left = 0` 和 `left = 1` 各有两个合法右端。错误写法二：出窗口时不删零计数的键，`len(cnt)` 虚高，同一输入返回 `10`。
