---
id: cc-round-time-lock-before-next
node: round.time
type: qa
---
## Q
Part 2 is "basically working" and you have 30 minutes left. Nothing has told you it is wrong. Do you move on or verify?

## A
**Verify — lock the part.** Run the worked example verbatim, then two cases of your own: the empty input and the exact boundary.

All parts share one program, so a Part 2 bug does not stay in Part 2 — it resurfaces in Part 4 with twice as much state around it and no clue which layer is lying. Locking costs about two minutes; finding the same bug later costs ten, and it costs them at the point when you have the least time and the most code. "Basically working" is the state that precedes both passing and failing.

## Q zh
Part 2「基本能跑」，还剩 30 分钟，也没有任何信号说它错了。继续往下做还是先验证？

## A zh
**先验证 —— 把这一部分锁死。** 逐字跑一遍题面样例，再加两个自己的用例：空输入和恰好的边界值。

所有部分共用一个程序，所以 Part 2 的 bug 不会留在 Part 2 —— 它会在 Part 4 重新冒出来，那时周围的状态多了一倍，而且分不清是哪一层在骗你。锁死约花两分钟；晚点再找同一个 bug 要花十分钟，而且花在你时间最少、代码最多的时刻。「基本能跑」是通过和失败共同的前一个状态。
