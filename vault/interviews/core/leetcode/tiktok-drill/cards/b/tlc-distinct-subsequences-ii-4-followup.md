---
id: tlc-distinct-subsequences-ii-4-followup
node: b.distinct-subsequences-ii
type: qa
step: 4
---
## Q
**LC 940 不同的子序列 II**｜Hard · 字节高频｜追问

面试官接着问：（1）`n` 到 `10^6`，内存吃紧，怎么办？（2）字符串以流的形式输入，每来一个字符就要给出当前的答案？（3）统计 `s` 里等于给定串 `t` 的子序列个数（LC 115）？

## A
1. **大 `n`**：不保存整个 `dp`，改成「以每个字母结尾的不同子序列数」`end[26]`（见另一种解法），空间 `O(26)`；字符集更大时 `O(字符种类数)`。
2. **流式**：同样用 `end` 数组，再维护一个总和 `total`；来了字符 `ch`，新值 `new = total + 1`，`total += new - end[ch]`，`end[ch] = new`。每步 `O(1)`，当前答案就是 `total`，不依赖未来字符。
3. **LC 115**：状态变成两个下标，用完整的二维表：`dp[i][j]` 表示 `s[:i]` 里 `t[:j]` 作为子序列出现的次数，`dp[i][j] = dp[i - 1][j] + (dp[i - 1][j - 1] if s[i - 1] == t[j - 1] else 0)`，`dp[i][0] = 1`。空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：`sum(end)` 每次要遍历 26 项，常数大；追求速度时像上面那样维护 `total`。`%` 对负数返回非负，其他语言需要手动补 `MOD`。
