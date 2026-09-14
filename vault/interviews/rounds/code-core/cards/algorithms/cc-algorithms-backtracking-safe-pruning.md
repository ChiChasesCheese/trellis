---
id: cc-algorithms-backtracking-safe-pruning
node: algorithms.backtracking
type: qa
---
## Q
Name three prunings for a minimum-count search and the argument that each preserves optimality.

## A
- **Branch and bound**: if `len(path) + 1 >= len(best)`, no completion can beat `best`, because the count only grows. Cut.
- **Skip duplicate values at a level**: two candidates with the same remaining balance are interchangeable, so the second explores an isomorphic subtree. Keep a `tried` set per level.
- **Stop after an exact cancel**: a partner that zeroes the current item exactly is never worse than any other choice at this level — settling one item with one transfer cannot be improved on. `break` out of the sibling loop.

Each is an **argument**, not a heuristic — say the argument. A pruning you cannot justify (e.g. "only try the largest surplus") silently turns an exact search into a greedy and loses the optimum ([[cc-algorithms-greedy-counterexample]]).

Together they take an 11!-shaped search to milliseconds, which is the difference between a technique that fits in the round and one that does not.

## Q zh
说出最小次数搜索的三种剪枝，以及每一种保持最优性的论证。

## A zh
- **分支限界**：若 `len(path) + 1 >= len(best)`，任何补全都不可能胜过 `best`，因为计数只增不减。剪掉。
- **同层跳过重复值**：剩余余额相同的两个候选可以互换，所以第二个探索的是同构子树。每层维护一个 `tried` 集合。
- **恰好抵消后停止**：能把当前元素精确清零的伙伴，在这一层永远不劣于任何其他选择 —— 用一笔转账结清一个元素已经无法更好。从兄弟循环中 `break`。

每一条都是**论证**而不是启发式 —— 要把论证讲出来。你论证不了的剪枝（比如「只试最大的盈余」）会悄悄把精确搜索变成贪心并丢掉最优解（[[cc-algorithms-greedy-counterexample]]）。

三者合起来能把 11! 量级的搜索压到毫秒，这正是「这项技术能塞进这一轮」与「塞不进」的差别。
