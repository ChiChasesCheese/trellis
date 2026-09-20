---
id: problems-reddit-vote-fuzzing-display-vs-ranking
node: problems.social.reddit
type: qa
step: 6
tags: [grown]
---
## Q
In a Reddit-style voting system, why can the vote count shown to users (the display value) deliberately differ from the vote count used internally to compute the ranking score, and why doesn't this divergence affect the correctness of the ranking?

## A
The displayed count can carry a small pseudo-random perturbation tied to the target, which raises the cost of a script trying to read back the exact vote count in real time (useful for detecting or timing manipulation attempts), while the ranking functions (hot, confidence, controversy) always read the true stored ups/downs from the vote ledger. Because these are two separate read paths — one serving the display field, one serving the ranking computation — perturbing the display value has no effect on which content actually ranks higher.

## Q zh
在 Reddit 式的投票系统里，为什么展示给用户的票数（展示值）可以刻意和内部用来计算排序分数的票数不同，而且这种差异不会影响排序结果的正确性？

## A zh
展示的票数可以携带一个和目标绑定的小幅伪随机扰动，提高了脚本实时读出精确票数的成本（有助于探测或延缓刷票行为），而排序函数（hot、confidence、controversy）永远读投票账本里存的真实 ups/downs。因为这是两条独立的读路径——一条服务展示字段，一条服务排序计算——扰动展示值不会影响哪条内容实际排名更高。
