---
id: problems-stock-exchange-journal-before-match-replay-recovery
node: problems.commerce.stock-exchange
type: qa
step: 4
tags: [grown]
---
## Q
In a single-threaded, in-memory matching engine, why must an input event (a new order or cancel) be durably written to a replicated journal BEFORE the matching engine processes it, rather than after?

## A
If the engine processed the event first and only journaled it afterward, a crash between those two steps would lose an event that had already changed the in-memory order book but was never recorded — so a passive replica replaying the journal to reconstruct state would produce a different, inconsistent result from what the crashed primary actually had. Journaling first guarantees that every event the matching engine ever acts on is also part of the durable, ordered log that any replica can replay to deterministically reconstruct the exact same sequence of state changes, which is what lets a replica take over after a failure without running a separate consensus protocol on the engine's internal state.

## Q zh
在一个单线程、纯内存运行的撮合引擎里，为什么一条输入事件（新订单或撤单）必须先持久化写入一份复制的日志（journal），然后才能被撮合引擎处理，而不能反过来？

## A zh
如果引擎先处理事件、之后才写日志，那么处理和写日志之间的崩溃会丢失一条已经改变了内存中订单簿状态、却从未被记录下来的事件——这样被动副本靠重放日志重建状态时，得到的结果会和崩溃前的主节点实际状态不一致。先写日志能保证撮合引擎处理过的每一条事件都必然也是那份持久化、有序日志的一部分，任何副本都能重放出完全相同的一串状态变化，这正是副本能在故障后直接接管、而不需要对引擎内部状态另外跑一套共识协议的原因。
