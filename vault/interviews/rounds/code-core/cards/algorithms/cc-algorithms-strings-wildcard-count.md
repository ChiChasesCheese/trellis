---
id: cc-algorithms-strings-wildcard-count
node: algorithms.strings
type: qa
---
## Q
A masked number has several `*` positions and you must count the completions that pass a mod-10 checksum. Brute force is 10^k per query. Better?

## A
**DP over the checksum residue instead of over the candidates.** Walk the positions left to right carrying `dp[r]` = how many ways reach running residue `r` mod 10; a fixed digit shifts every count by that digit's weighted value, a `*` spreads each count over the ten digits with that position's weight.

- Cost O(len × 10) per query regardless of how many `*` there are — ten wildcards is 10^10 by brute force and instant here.
- Brute force is legitimate and much faster to write when the wildcard count is bounded small (`10^k` with k ≤ 5 is a few hundred thousand operations). **Check the constraint before choosing** ([[cc-algorithms-recognition-constraint-sizes]]).
- Independent of the counting: the mask's **length and prefix** decide the network first, and a mask matching no network produces no output line at all rather than a zero ([[cc-output-sentinels-zero-rows]]).
- Report counts in the spec's order (usually alphabetical by network) and omit the zero entries only if it says so.

## Q zh
一个带掩码的号码有若干 `*` 位，你要统计能通过 mod-10 校验的补全数。暴力是每次查询 10^k。有更好的吗？

## A zh
**在校验残差上做 DP，而不是在候选上。** 从左到右遍历各位，携带 `dp[r]` = 到达运行残差 `r`（mod 10）的方案数；固定数字把每个计数按该位的加权值平移，`*` 则把每个计数按该位的权重摊到十个数字上。

- 每次查询 O(len × 10)，与 `*` 的个数无关 —— 十个通配符暴力是 10^10，这里瞬间完成。
- 当通配符个数有小上界时（k ≤ 5 的 `10^k` 只是几十万次操作），暴力既合法又快得多。**先看约束再做选择**（[[cc-algorithms-recognition-constraint-sizes]]）。
- 与计数无关的一点：掩码的**长度和前缀**先决定卡组织，而不匹配任何卡组织的掩码根本不产生输出行，而不是输出 0（[[cc-output-sentinels-zero-rows]]）。
- 按 spec 的顺序（通常按卡组织字母序）报告计数，只有它这么说时才省略零条目。
