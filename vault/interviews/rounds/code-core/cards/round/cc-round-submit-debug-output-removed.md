---
id: cc-round-submit-debug-output-removed
node: round.submission
type: qa
---
## Q
Five minutes left. What is the first thing you check, and why that first?

## A
**That nothing but the answer reaches stdout.** A single leftover trace line fails every test in every part at once — it is the highest-damage, lowest-effort defect in the round.

Sweep for: `print(` without a `file=` argument, a progress counter, a `pprint` of state, an `input()` prompt string, and any library that prints on import. Then run one sample end-to-end and look at the raw output. If you kept debug behind a `DEBUG = False` guard from the start, this check takes ten seconds instead of three minutes.

## Q zh
还剩五分钟。你第一个检查什么，为什么是它？

## A zh
**除了答案，没有别的东西进入 stdout。** 一行残留的 trace 会一次性让所有部分的所有测试失败 —— 这是本轮伤害最高、代价最低的缺陷。

要扫的东西：没有 `file=` 参数的 `print(`、进度计数、状态的 `pprint`、`input()` 的提示串，以及任何在 import 时就打印的库。然后端到端跑一个样例，直接看原始输出。如果你从一开始就把调试放在 `DEBUG = False` 开关后面，这一步只要十秒而不是三分钟。
