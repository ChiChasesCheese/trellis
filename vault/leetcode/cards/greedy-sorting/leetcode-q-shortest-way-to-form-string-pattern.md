---
id: leetcode-q-shortest-way-to-form-string-pattern
node: greedy-sorting.greedy
type: qa
anki: 1787175409584
tags: [lc::1055, leetcode, pattern, recall]
---
## Q
给定 source 和 target，要求用若干个 source 副本拼接后，从中挑选出一个子序列恰好等于 target，求最少需要多少个 source 副本（LC 1055 Shortest Way to Form String）？

## A
贪心 + 子序列自动机思路：先检查 target 中每个字符是否都在 source 的字符集合里，若有字符不存在则直接返回 -1。然后用双指针贪心匹配：外层指针 i 指向 target，每次用一整趟 source（内层指针 j 从 0 到 m）尽量往前推进 i；只要 source 中的字符等于 target[i] 就让 i 前移。每跑完一趟 source 计数器 cnt+1，直到 i 走完整个 target。因为一次 source 遍历中每个字符最多用一次，所以要保证 target 是若干个 source 拼接后的子序列，每'轮'source 最多消耗掉 target 中的一段递增子序列，这就是子序列自动机模式（也用于 392 Is Subsequence、792 Number of Matching Subsequences）。

**Evidence**

source: leetcode-notes/1055; 代码：`char_set = set(source)` 提前判断不可达字符返回 -1；双指针 `while j < m and i < n` 在一趟 source 内贪心匹配 target 字符，外层 `while i < n` 每完成一趟 cnt += 1，直到 i 到达 n。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1055%20-%20Shortest%20Way%20to%20Form%20String)
