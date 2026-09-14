# pc21 Accumulator Interpreter — report

## Summary
TrueInterview 87 题清单第 34 题（"String-Command Calculator"，2026-02）与第 19 题（"SnowCal"，
2026-05）同族合并。3-part：Part 1 累加器计算器（一手）· Part 2 单变量小语言，函数声明/调用，
检测未定义函数与无限递归（一手要求，检测机制重建）· Part 3 `REPEAT` 海量重复调用 + 取模，
仿射映射记忆化 **(reconstructed)**。

## Sources & confidence
MED（TrueInterview 聚合站预览，题面付费）；Part 1/2 的语言元素为原文，`DIV` 截断方向与递归检测
机制为重建；Part 3 全部为重建。

## Approach by part
1. 累加器从 0 开始顺序执行 `ADD`/`SUB`/`MULT`/`DIV`；`DIV` 用 `abs(a)//abs(b)` 再按符号取负实现
   向零截断；除零、未知命令抛 `ValueError`。
2. 先一遍扫描把所有 `FUN...END` 块抽取进字典（声明时不执行），剩余顶层指令按顺序求值；`INV`
   通过递归 `_exec_snowcal_stmt` 执行函数体，用"当前调用链"`frozenset` 传递，即将调用一个已经在
   链上的函数就抛 `ValueError`（直接与间接递归统一处理）。
3. 给每条指令定义仿射变换 `(a,b)`（`ADD n`→`(1,n)`，`MUL n`→`(n,0)`，调用函数→其记忆化的
   `(a,b)`），顺序复合得到整个函数/程序的净仿射映射；`REPEAT count name` 用等比数列闭式解
   （`a≠1` 时用模逆元，`a==1` 时退化成等差数列）把"重复 count 次"压缩成 `O(log count)`。

## Pitfalls hidden tests target
- `DIV` 负数向零截断 vs 向下取整（符号不同的例子）
- 除以 0、未知命令
- 声明函数但不调用是 no-op
- 未定义函数调用、直接自递归、间接互递归都要报错
- Part 3：`REPEAT 0`、`a mod MOD == 1`（纯 `ADD` 函数，等差分支，避免除零）、极大 `count`
  （`~10^15`）、Part 3 里未定义函数/调用环依然要检测

## Complexity & measured cost
Part 1 O(命令数)。Part 2 O(程序长度 + 调用展开的总指令数)。Part 3 O(程序长度 × log(最大
count))，与 `count` 本身大小无关（`REPEAT 10^15` 与 `REPEAT 10` 耗时几乎相同）。编排者验证：
300 组随机 Part 1 程序与独立的浮点截断参考实现 0 不一致；150 组随机无环 Part 2 程序通过"把
顶层 `INV` 换成 `REPEAT 1`"在 Part 3 引擎里重跑，与 Part 2 精确整数结果取模后一致；150 组随机
小 `count`（≤40）程序与独立的"直接循环 REPEAT"暴力实现 0 不一致；`REPEAT 999999999999999`
端到端 < 2 s。

## Test inventory
23 tests — part1 6 · part2 6 · part3 7 · perf 1 · io/fmt 3；edge 15 · fmt 1 · perf 1 · io 2。

## Skills exercised
S04 小型指令解释器 / 状态机 · S06 调用图环检测（隐式有向图，不需要显式建图） · S08 把 O(count)
暴力循环压成 O(log count) 快速幂（仿射映射的可结合性是关键洞察）。
