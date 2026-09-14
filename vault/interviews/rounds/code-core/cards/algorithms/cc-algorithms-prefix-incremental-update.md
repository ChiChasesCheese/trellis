---
id: cc-algorithms-prefix-incremental-update
node: algorithms.prefix
type: qa
---
## Q
You need the penalty of closing at hour *j*, for every *j*. Recomputing from the whole log per *j* is 10^10 at n = 10^5. Fix it.

## A
**Compute the answer at j = 0, then update it as j moves by one.**

```python
cur = sum(w for c, w in zip(log, wt) if c == "Y")   # close at 0: every 'Y' is missed
best, at = cur, 0
for j, (c, w) in enumerate(zip(log, wt), start=1):
    cur += -w if c == "Y" else w                    # hour j-1 is now open
    if cur < best:                                  # strict <: keep the earliest
        best, at = cur, j
```

- One pass, O(n) time, O(1) memory — no prefix array at all when the objective changes by a constant per step.
- The **transition is the whole design**: say out loud what changes when the split point moves one step, and the code writes itself.
- `<` versus `<=` decides earliest versus latest optimum ([[cc-algorithms-prefix-argmin-tiebreak]]).
- Both ends are legal answers: closing at 0 and closing at n must both be candidates, so the loop starts from a value, not from the first element.

## Q zh
你要对每个 *j* 求「在第 *j* 小时打烊」的罚分。对每个 *j* 从整个日志重算，在 n = 10^5 时是 10^10。怎么修？

## A zh
**先算出 j = 0 的答案，然后随着 j 每移动一步增量更新。**

```python
cur = sum(w for c, w in zip(log, wt) if c == "Y")   # 0 点打烊：每个 'Y' 都错过
best, at = cur, 0
for j, (c, w) in enumerate(zip(log, wt), start=1):
    cur += -w if c == "Y" else w                    # 第 j-1 小时现在营业了
    if cur < best:                                  # 严格 <：保留最早的
        best, at = cur, j
```

- 一趟，时间 O(n)、内存 O(1) —— 当目标每步只变化一个常量时，根本不需要前缀数组。
- **转移就是全部设计**：把「分割点移动一步时什么变了」讲出来，代码自然就写出来了。
- `<` 与 `<=` 决定取最早还是最晚的最优解（[[cc-algorithms-prefix-argmin-tiebreak]]）。
- 两端都是合法答案：0 点打烊和 n 点打烊都必须是候选，所以循环从一个初值开始，而不是从第一个元素开始。
