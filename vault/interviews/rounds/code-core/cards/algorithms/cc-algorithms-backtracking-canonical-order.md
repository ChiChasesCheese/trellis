---
id: cc-algorithms-backtracking-canonical-order
node: algorithms.backtracking
type: qa
---
## Q
Your search finds the same settlement many times in different orders and times out. What is the structural fix?

## A
**Fix a canonical order so each solution is generated exactly once**: always extend the *first* unresolved item, and only pair it with items that come after it.

```python
while i < n and bal[i] == 0:
    i += 1                       # the first unsettled party
for j in range(i + 1, n):        # only later partners
    ...
```

- This removes the factorial redundancy of "choose any pair" **without excluding any solution**: whichever transfer eventually settles item `i` can be done first, so no optimum is lost.
- The same principle everywhere: pass a `start` index in subset enumeration; fix the *position* and iterate candidate values in permutation problems.
- It also makes the **first** optimal solution found deterministic — which is usually what "output any minimal answer" really means, since the grader has one expected file ([[cc-output-ordering-total-order]]).
- Canonical order is not a pruning; it is a change of search space, and it composes with pruning ([[cc-algorithms-backtracking-safe-pruning]]).

## Q zh
你的搜索以不同顺序反复找到同一个清账方案，然后超时。结构性的修法是什么？

## A zh
**固定一个规范顺序，让每个解恰好被生成一次**：永远扩展*第一个*尚未解决的元素，并且只与排在它之后的元素配对。

```python
while i < n and bal[i] == 0:
    i += 1                       # 第一个未结清的对象
for j in range(i + 1, n):        # 只与更靠后的伙伴配对
    ...
```

- 这消除了「任选一对」带来的阶乘级冗余，而且**不排除任何解**：最终结清元素 `i` 的那笔转账总可以先做，所以不会丢掉最优解。
- 同一原则处处适用：子集枚举时传一个 `start` 下标；排列问题里固定*位置*、遍历候选值。
- 它还让**第一个**找到的最优解是确定的 —— 而这通常正是「输出任意一个最少方案」的真实含义，因为 grader 只有一份期望文件（[[cc-output-ordering-total-order]]）。
- 规范顺序不是剪枝；它改变的是搜索空间，并且能与剪枝叠加（[[cc-algorithms-backtracking-safe-pruning]]）。
