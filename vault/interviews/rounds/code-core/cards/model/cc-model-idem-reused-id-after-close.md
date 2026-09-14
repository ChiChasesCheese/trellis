---
id: cc-model-idem-reused-id-after-close
node: model.idempotency
type: qa
---
## Q
A connection id is disconnected, then a later `CONNECT` uses the same id. Duplicate, or new?

## A
**New. "Duplicate" means a duplicate of a *live* id, not of an id ever seen.**

The same distinction appears everywhere reversal and idempotency meet: a charge id reused after that charge was disputed is a fresh charge and counts again; a hostname freed and re-allocated is a new host.

So the de-duplication structure must be the set of currently-live ids, and the entry must be **removed** when the entity closes. A monotonically growing "seen ids" set is the wrong model — it silently rejects legitimate reuse, and the failing test is always late in the stream.

## Q zh
一个连接 id 被断开后，稍后的 `CONNECT` 又用了同一个 id。这是重复还是新的？

## A zh
**新的。「重复」指的是与「活动中」的 id 重复，而不是与曾经见过的 id 重复。**

凡是撤销与幂等相遇的地方都有这个区分：某笔扣款被争议之后，同一 charge id 再次出现是一笔全新的扣款，要重新计数；主机名释放后再分配也是一台新主机。

因此去重结构必须是**当前活动** id 的集合，并在实体关闭时**移除**条目。单调增长的"见过的 id"集合是错误模型 —— 它会静默拒绝合法的复用，而失败的测试总是出现在流的后段。
