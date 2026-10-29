---
id: tlc-number-of-longest-increasing-subsequence-3-why
node: b.number-of-longest-increasing-subsequence
type: qa
step: 3
---
## Q
**LC 673 最长递增子序列的个数**｜正确性

LIS 个数的转移为什么是「更长就覆盖、一样长才累加」？最后为什么要对所有达到最长长度的位置求和？

## A
**不变量。** 处理完 `i` 后，`length[i]` 是以 `nums[i]` 结尾的最长递增子序列长度，`count[i]` 是这个长度的子序列个数。

**为什么这样转移。** 以 `i` 结尾、长度为 `length[i]` 的子序列，去掉末尾后是以某个 `j` 结尾、长度为 `length[i] - 1` 的子序列；它一定是 `j` 结尾的**最长**者（否则 `length[i]` 还能更大）。所以 `count[i]` 恰好是满足 `length[j] + 1 == length[i]` 的各个 `count[j]` 之和。发现更长的来源时，之前累加的计数对应较短的长度，必须丢弃，也就是覆盖。

**反例。** 把覆盖写成累加（`count[i] += count[j]`）：`[1,3,5,4,7]` 得到 `12`，正确是 `2`。

**求和。** 最长序列可以在任何位置结尾，`[2,2,2,2,2]` 每个位置都是长度 1，个数为 `5`；只取 `count[-1]` 或第一个最长位置只会得到 `1`。
