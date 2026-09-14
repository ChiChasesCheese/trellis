---
id: cc-model-ev-current-vs-ever
node: model.event-stream
type: qa
---
## Q
The output is "the accounts that are fraudulent". After a reversal an account drops back below its threshold. Does it appear?

## A
**It depends on which of two different questions the statement asks — and they are one word apart.**

- *Currently* fraudulent: the state after the last event. A reversal can un-flag; the answer is recomputed from the counters.
- *Ever* fraudulent (sticky, "once flagged, stays flagged"): a separate stored bit set on the first crossing and never cleared.

The same event stream produces different output sets, and a grader tests both readings in different problem variants. Because the sticky bit cannot be derived from the current counters, decide before writing the flag logic and keep the alternative one flag away. See [[cc-round-ambiguity-one-flag-away]].

## Q zh
输出是"欺诈账户"。撤销之后某账户回落到阈值以下。它还出现吗？

## A zh
**取决于题面问的是两个不同问题中的哪一个 —— 它们只差一个词。**

- **当前**欺诈：最后一个事件之后的状态。撤销可以取消标记；答案由计数器现算。
- **曾经**欺诈（sticky，「一旦标记，永久标记」）：一个在首次越线时置位、永不清除的独立存储位。

同一条事件流会产出不同的输出集合，而评测机在不同的题面变体里两种读法都测。由于 sticky 位无法从当前计数器推导，必须在写标记逻辑之前决定，并把另一种读法保持在一个 flag 之外。见 [[cc-round-ambiguity-one-flag-away]]。
