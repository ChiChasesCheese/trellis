---
id: async-loss-vs-duplicate-asymmetry
node: async.delivery.guarantees
type: qa
---
## Q
Between at-most-once and at-least-once delivery, production systems overwhelmingly build on at-least-once and engineer away the duplicates. What asymmetry between losing a message and duplicating one justifies that default?

## A
The two failures are not symmetric in **detectability and repairability**:

- **A duplicate arrives** — it's an event you can see, carry an id on, and neutralize downstream (idempotent handler, dedup store, versioned upsert). The fix is local, mechanical, and testable.
- **A loss is the absence of an event** — nothing arrives to trigger any handler, so nothing detects it in-band. Discovering losses requires *out-of-band reconciliation* against a source of truth (periodic count/checksum comparison), and repairing them requires that source to still hold the data.

So at-least-once converts an invisible, possibly unrecoverable failure into a visible, engineerable one. Choose at-most-once only when data is genuinely disposable and freshness dominates — a lost heartbeat or position update is superseded by the next one seconds later, and processing it twice buys nothing.

## Q zh
在 at-most-once 和 at-least-once 投递之间，生产系统压倒性地选择以 at-least-once 为基础、再用工程手段消除重复。丢一条消息和重复一条消息之间的什么不对称性，支撑了这个默认选择？

## A zh
这两种故障在**可检测性和可修复性**上并不对称：

- **重复到达**——它是一个你看得见的事件，可以携带 id，并在下游中和掉（幂等处理器、去重存储、带版本的 upsert）。修复是局部的、机械的、可测试的。
- **丢失是事件的缺席**——什么都没到达，任何处理器都不会被触发，所以带内（in-band）无法检测。发现丢失需要对照事实源做*带外核账*（定期比对计数/校验和），修复丢失则要求那个事实源还留着数据。

所以 at-least-once 把一种不可见、可能无法挽回的故障，换成了一种可见的、可工程化处理的故障。只有当数据真正可丢弃、且新鲜度压倒一切时才选 at-most-once——丢掉的一次心跳或位置上报，几秒后就被下一条取代，而把它处理两遍毫无收益。
