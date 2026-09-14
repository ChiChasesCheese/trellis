---
id: cc-algorithms-backtracking-feasibility-pruning
node: algorithms.backtracking
type: qa
---
## Q
Beyond bounding on the objective, what else is worth thirty seconds to add to a backtracking search?

## A
**A feasibility bound — cut the branch when the remaining items *cannot* complete a valid solution.**

- Sum and parity arguments: if the remaining capacity is smaller than the smallest remaining item, or the remaining total cannot reach the required sum, stop now instead of at the leaf.
- A lower bound on remaining cost added to the current cost, compared against `best` — bounding with a smarter estimate than "one more step" ([[cc-algorithms-backtracking-safe-pruning]]).
- **Candidate ordering**: try the most constraining choice first (largest item, most-constrained slot). A strong `best` found early is what makes every later bound bite; ordering is free and often worth more than another pruning.
- **Memoize on the canonical state** — a `frozenset`, a sorted tuple, a bitmask — when different paths reach the same situation. That is the point where backtracking becomes DP ([[cc-algorithms-dp-bitmask]]).

## Q zh
除了对目标做限界，还有什么值得花三十秒加进回溯搜索？

## A zh
**可行性界 —— 当剩余元素*不可能*凑成合法解时就剪掉该分支。**

- 求和与奇偶论证：如果剩余容量小于最小的剩余元素，或剩余总量根本达不到所需的和，就当场停下，而不是走到叶子。
- 把剩余代价的下界加到当前代价上再与 `best` 比较 —— 用比「再走一步」更聪明的估计来限界（[[cc-algorithms-backtracking-safe-pruning]]）。
- **候选顺序**：先试约束最强的选择（最大的元素、最受限的槽位）。早早找到一个强的 `best`，后面每一个界才咬得动；排序是免费的，常常比再加一条剪枝更值。
- 当不同路径到达同一情形时，**在规范状态上做记忆化** —— `frozenset`、有序 tuple、bitmask。那正是回溯变成 DP 的地方（[[cc-algorithms-dp-bitmask]]）。
