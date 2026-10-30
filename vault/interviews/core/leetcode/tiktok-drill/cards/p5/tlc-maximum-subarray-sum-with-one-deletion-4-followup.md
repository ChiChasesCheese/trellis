---
id: tlc-maximum-subarray-sum-with-one-deletion-4-followup
node: p5.maximum-subarray-sum-with-one-deletion
type: qa
step: 4
---
## Q
**LC 1186 删除一次得到子数组最大和**｜追问

面试官接着问：（1）最多删 `k` 个？（2）能不能用前后缀数组写，思路更直观？（3）要求恰好删一个？

## A
1. **最多删 `k` 个**：`dp[j]` 表示以当前位置结尾、已删 `j` 个的最大和，`j = 0..k`。转移：`dp[0] = max(dp[0], 0) + x`；`dp[j] = max(dp[j] + x, dp[j-1], x)`，更新时 `j` 从大到小，或者用旧数组的拷贝。时间 `O(n·k)`。
2. **前后缀**：`left[i]` = 以 `i` 结尾的最大和，`right[i]` = 以 `i` 开头的最大和。删掉 `arr[i]` 后拼接得 `left[i-1] + right[i+1]`（`1 ≤ i ≤ n-2`）；答案是它与 `max(left)`（不删）的较大者。两遍扫描，`O(n)` 空间；面试里先讲这个更容易讲清，再优化到 `O(1)`。
3. **恰好删一个**：不能取「没删」的状态。`n = 1` 时无解；`n ≥ 2` 时 `skip` 要排除没删过的来源，初值设成不可达（负无穷），转移只用 `skip + x` 和 `keep`。

**对比** 前后缀版易写、易验证；单遍 DP 版更省空间，也更容易推广到 `k` 次。

**Python 提醒**：`arr[1:]` 会拷贝整个切片；`for x in itertools.islice(arr, 1, None)` 不拷贝。表示「负无穷」用 `float('-inf')` 会让变量类型变成 `int | float`，也可以在 `n >= 2` 时直接用 `arr[0]` 初始化来避免。
