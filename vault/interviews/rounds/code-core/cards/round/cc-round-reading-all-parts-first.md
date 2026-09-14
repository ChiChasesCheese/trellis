---
id: cc-round-reading-all-parts-first
node: round.reading
type: qa
---
## Q
Minute 0 of a five-part problem; every part is visible. Part 2 asks for counters per merchant, Part 4 says a dispute reverses an earlier charge. What does reading Part 4 first save you?

## A
**The state shape.** Counters alone cannot be un-applied: to reverse charge `ch_7` you need `charge_id -> (merchant, was_fraud)`, a ledger Part 2 never asked for.

Designing from the last part costs four minutes of reading and turns Part 4 into five lines; discovering it at minute 40 means re-writing the Part 2 loop with Parts 1–3 already passing. Read every part, write down the *last* part's data needs, then implement Part 1 against that shape. See [[cc-model-rev-subtract-both-counters]].

## Q zh
五部分题目的第 0 分钟，所有部分都可见。Part 2 要求给每个商户维护计数器，Part 4 说争议（dispute）会撤销一笔更早的扣款。先读 Part 4 能省下什么？

## A zh
**状态的形状。** 光有计数器无法撤销：要冲掉 `ch_7`，你需要 `charge_id -> (merchant, was_fraud)` 这本账，而 Part 2 从没要求过它。

从最后一部分倒推设计，代价是四分钟阅读，收益是 Part 4 只要五行；等到第 40 分钟才发现，就得在 Part 1–3 已经通过的情况下重写 Part 2 的循环。读完所有部分，写下**最后**一部分需要的数据，再照那个形状实现 Part 1。见 [[cc-model-rev-subtract-both-counters]]。
