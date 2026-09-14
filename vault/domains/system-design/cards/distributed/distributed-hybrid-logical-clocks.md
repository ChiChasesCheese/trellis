---
id: distributed-hybrid-logical-clocks
node: distributed.time.clocks
type: qa
---
## Q
Lamport timestamps respect causality but bear no relation to wall time; wall clocks read like real time but can order a cause after its effect. What do hybrid logical clocks (HLC) do to get both, and where are they used?

## A
An HLC timestamp is a pair: **(physical component, logical counter)**.

- On every event, take the max of the local wall clock and the largest physical component seen so far; on receiving a message, also take the max with the sender's HLC. If the physical component didn't advance (clock skew, same-millisecond events), **bump the logical counter** to break the tie.
- Result: HLC order **never contradicts causality** (a message's receive time always exceeds its send time, even if the receiver's wall clock lags), while the physical part stays **within the clock-skew bound of true wall time** — so timestamps remain human-meaningful and usable for "as of 3pm" reads.
- Cost is tiny — constant size, unlike O(nodes) vector clocks — but like Lamport clocks, HLCs **cannot detect concurrency**, only order it.

Used by CockroachDB and MongoDB for MVCC/transaction timestamps: causally-safe ordering without TrueTime's special hardware (though CockroachDB still needs a max-skew bound and cannot promise Spanner-grade external consistency).

## Q zh
Lamport 时间戳尊重因果但和真实时间毫无对应；墙上时钟读起来像真实时间，却可能把因排到果之后。混合逻辑时钟（hybrid logical clock, HLC）如何兼得两者？用在哪里？

## A zh
HLC 时间戳是一个二元组：**（物理分量，逻辑计数器）**。

- 每个事件发生时，取本地墙钟与迄今见过的最大物理分量的最大值；收到消息时，再与发送方的 HLC 取最大值。如果物理分量没有前进（时钟偏差、同一毫秒内的事件），就**递增逻辑计数器**来打破平局。
- 结果：HLC 的顺序**永不违背因果**（一条消息的接收时间戳总是大于发送时间戳，即使接收方的墙钟落后），同时物理分量**保持在与真实墙钟的偏差上界之内**——时间戳依然对人有意义，可用于"截至下午 3 点"这类读。
- 代价极小——大小恒定，不像 vector clock 是 O(节点数)——但和 Lamport 时钟一样，HLC **无法检测并发**，只能给并发事件排一个序。

CockroachDB 和 MongoDB 用它做 MVCC/事务时间戳：不需要 TrueTime 的专用硬件就能得到因果安全的定序（不过 CockroachDB 仍需一个最大偏差上界，也无法承诺 Spanner 级别的外部一致性）。
