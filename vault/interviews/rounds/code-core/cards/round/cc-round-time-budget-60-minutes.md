---
id: cc-round-time-budget-60-minutes
node: round.time
type: qa
---
## Q
Sixty minutes, one problem, five parts that unlock in sequence. Give a defensible minute budget and the two signals that you are already over it.

## A
**0–5 read every part and fix the state shape · 5–45 code part by part, ~8 minutes each, locking each with its sample · 45–55 boundary sweep · 55–60 output format and debug removal.**

The sweep is not optional: empty, single, duplicate, out-of-order, zero, exactly-at-threshold, and the reversal case, run against every part.

Two overrun signals:
- still parsing at minute 15 — cut to the simplest split that works;
- a part unfinished at its eight-minute mark — simplify the rule or move on and come back.

## Q zh
六十分钟，一道题，五个依次解锁的部分。给出一个站得住脚的分钟预算，以及两个"已经超支"的信号。

## A zh
**0–5 读完所有部分并定下状态形状 · 5–45 逐部分编码，每部分约 8 分钟，用样例锁死 · 45–55 边界扫查 · 55–60 输出格式与清除调试输出。**

边界扫查不是可选项：空、单元素、重复、乱序、零、恰好等于阈值、以及撤销事件，逐一对每个部分跑一遍。

两个超支信号：
- 第 15 分钟还在写解析 —— 退回最简单能用的 split；
- 某部分到第 8 分钟还没做完 —— 简化规则，或先跳过稍后再回来。
