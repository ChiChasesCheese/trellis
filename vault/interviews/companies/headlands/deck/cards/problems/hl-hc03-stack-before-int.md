---
id: hl-hc03-stack-before-int
node: problems.hc03-recursive-sum
type: qa
step: 5
---
## Q
朴素递归求和的 `int` 版有哪几个问题？为什么说「栈比 int 先出问题」？

## A
`static int sum(int n) { if (n == 0) return 0; return n + sum(n - 1); }` 时间 O(n)、栈空间 O(n)，问题有三：
1. `sum(65536)` 应为 2 147 516 416，`int` 装不下，**静默**变成 −2 147 450 880；
2. 改成 `long`，`sum(1_000_000)` 在默认栈上也 `StackOverflowError`；
3. `long` 溢出的 n = 4 294 967 296 需 43 亿次递归，栈撑不到，递归版**根本测不出 long 溢出**。

**栈比 int 先出问题**：默认 1 MiB 栈上 `sumToRecursive(65536)` 先抛 `StackOverflowError`（n = 40000 还行）。所以 INT 溢出的测试必须放进大栈线程（512 MiB 栈）里跑；这也是 Part 2 的伏笔。

验证用的测试做法：`Width.INT` 让溢出在 n = 65535 → `Ok(2147450880)`、n = 65536 → `Overflow(2147516416)` 就出现，不必递归几十亿层。

加法在递归**返回之后**（`w.add(n, 子结果)`），所以这个写法**不是**尾递归。
