---
id: tlc-find-the-score-of-all-prefixes-of-an-array-3-why
node: b.find-the-score-of-all-prefixes-of-an-array
type: qa
step: 3
---
## Q
**LC 2640 一个数组所有前缀的分数**｜正确性

为什么前缀 `nums[0..i]` 的分数可以直接取整体转换数组前 `i + 1` 项的和，而不用针对每个前缀重新计算转换数组？

## A
**不变量。** `conver[j] = nums[j] + max(nums[0..j])` 只依赖下标 `0..j` 的元素。对任意前缀 `nums[0..i]` 和任意 `j <= i`，它自己的转换数组第 `j` 项与整体转换数组第 `j` 项完全相同，因为两者看到的 `nums[0..j]` 一样。因此 `ans[i] = conver[0] + … + conver[i]`，也就是 `conver` 的前缀和，`ans[i] = ans[i-1] + conver[i]`。

**反例（错误写法一）：用全局最大值。** `nums = [2,3,7,5,10]`，把 `max(arr[0..i])` 错当成 `max(nums)`：`ans[0] = 2 + 10 = 12`，正确答案是 `4`。

**反例（错误写法二）：只加一次最大值。** 写成 `ans[i] = 前缀和(nums)[i] + 前缀最大值[i]`：`ans[2] = 12 + 7 = 19`，正确答案是 `4 + 6 + 14 = 24`。分数里**每个位置**都要加一次它自己的前缀最大值，不是整个前缀只加一次。
