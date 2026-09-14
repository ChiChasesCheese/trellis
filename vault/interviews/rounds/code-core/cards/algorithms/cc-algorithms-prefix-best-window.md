---
id: cc-algorithms-prefix-best-window
node: algorithms.prefix
type: qa
---
## Q
Maximum-sum contiguous window, and you must also report its start and end with a stated tie-break. Prefix-sum form?

## A
**The best window ending at `close` starts at the earliest index attaining the minimum prefix before it.**

```python
pre, min_pre, min_at = 0, 0, 0
best = (0, 0, 0)                                   # (score, open, close)
for close, x in enumerate(scores, start=1):
    pre += x
    score = pre - min_pre
    if score > best[0] or (score == best[0] and (min_at, close) < (best[1], best[2])):
        best = (score, min_at, close)
    if pre < min_pre:                              # strict <: earliest minimum
        min_pre, min_at = pre, close
```

- Update the running minimum **after** using it, or the candidate window collapses to empty.
- The strict `<` on the minimum is what resolves ties to the earliest start; the explicit tuple comparison handles the rest of the tie rule ([[cc-algorithms-prefix-argmin-tiebreak]]).
- This is Kadane with the indices made explicit — take this form whenever the *positions* are part of the answer, and the plain running-max form when they are not.
- An empty window scoring 0 must be a legal candidate if the spec allows one; seed `best` with it rather than special-casing later.

## Q zh
求和最大的连续窗口，并且要按规定的 tie-break 报告它的起止位置。前缀和写法？

## A zh
**以 `close` 结尾的最优窗口，起点是它之前取到最小前缀和的最早下标。**

```python
pre, min_pre, min_at = 0, 0, 0
best = (0, 0, 0)                                   # (score, open, close)
for close, x in enumerate(scores, start=1):
    pre += x
    score = pre - min_pre
    if score > best[0] or (score == best[0] and (min_at, close) < (best[1], best[2])):
        best = (score, min_at, close)
    if pre < min_pre:                              # 严格 <：取最早的最小值
        min_pre, min_at = pre, close
```

- 在**用过之后**再更新滚动最小值，否则候选窗口会塌成空。
- 最小值上的严格 `<` 正是让并列落到最早起点的原因；其余的并列规则由那个显式 tuple 比较处理（[[cc-algorithms-prefix-argmin-tiebreak]]）。
- 这就是把下标显式化的 Kadane —— 当*位置*是答案的一部分时用这个形态，不需要位置时用简单的滚动最大值形态。
- 如果 spec 允许空窗口得 0 分，它必须是合法候选；用它初始化 `best`，而不是事后特判。
