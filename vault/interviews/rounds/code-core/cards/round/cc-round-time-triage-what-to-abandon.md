---
id: cc-round-time-triage-what-to-abandon
node: round.time
type: qa
---
## Q
Twelve minutes left. Parts 1–3 pass; Part 4 is half-written and currently makes Part 3 crash. What do you cut?

## A
**Cut the unfinished part, never the passing ones.** First move: make Part 4 a correct no-op — parse its command and ignore it — so the program still runs Parts 1–3 cleanly. A crash costs you tests you had already earned.

Order of sacrifice: the performance optimization for the largest input, then the last part's rarest branch, then the last part entirely. A refactor of passing code is never on this list. Partial credit is per test, so three clean parts beat four broken ones.

## Q zh
还剩十二分钟。Part 1–3 都通过，Part 4 写了一半，而且当前会让 Part 3 崩溃。你砍掉什么？

## A zh
**砍掉没写完的那部分，绝不砍已经通过的。** 第一步：把 Part 4 变成一个正确的 no-op —— 解析它的命令然后忽略 —— 让程序仍能干净地跑 Part 1–3。一次崩溃会让你丢掉早已到手的测试。

牺牲顺序：最大输入的性能优化 → 最后一部分里最罕见的分支 → 整个最后一部分。重构已通过的代码永远不在这张清单上。部分分是按测试计的，三个干净的部分胜过四个破的。
