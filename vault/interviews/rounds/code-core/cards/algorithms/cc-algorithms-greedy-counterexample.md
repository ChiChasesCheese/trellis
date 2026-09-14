---
id: cc-algorithms-greedy-counterexample
node: algorithms.greedy
type: qa
---
## Q
To settle debts, greedily match the largest surplus with the largest deficit. Does that minimise the number of transfers?

## A
**No.** It produces a valid settlement and a useful upper bound, but not the minimum count. With balances +5, +5, −10 a pairing that splits the deficit takes 2 transfers; a largest-first pass that first drains one surplus against part of the deficit can take 3.

- Minimising the *number of operations* is combinatorial — it is a partition into zero-sum subsets and needs search ([[cc-algorithms-settlement-min-transfers]]).
- When the objective is *total amount moved*, or merely *feasibility*, the greedy is optimal and is the right answer.
- Keep the greedy anyway: it is the fallback for large n, and its result bounds the exact search for small n ([[cc-algorithms-backtracking-safe-pruning]]).
- The general lesson: a greedy that is optimal for one objective is routinely wrong for a neighbouring one. Re-run the exchange argument whenever a later part changes what is being minimised.

## Q zh
为了清账，贪心地把最大盈余与最大缺口配对。这能让转账次数最少吗？

## A zh
**不能。** 它给出一个合法的清账方案和一个有用的上界，但不是最少次数。余额为 +5、+5、−10 时，把缺口拆开配对只要 2 次转账；而先把一个盈余对着部分缺口清空的「从大到小」做法可能要 3 次。

- 最小化*操作次数*是组合问题 —— 它是划分成零和子集，需要搜索（[[cc-algorithms-settlement-min-transfers]]）。
- 当目标是*资金总流动量*、或仅仅是*可行性*时，贪心是最优的，也正是正确答案。
- 无论如何都保留这个贪心：它是大 n 时的兜底，而它的结果又能为小 n 的精确搜索提供上界（[[cc-algorithms-backtracking-safe-pruning]]）。
- 一般性教训：对某个目标最优的贪心，对相邻的另一个目标经常是错的。后面的 part 一旦改变了要最小化的东西，就重跑一遍交换论证。
