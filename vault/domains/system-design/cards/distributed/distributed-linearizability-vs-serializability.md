---
id: distributed-linearizability-vs-serializability
node: distributed.consistency
type: qa
---
## Q
Linearizability vs serializability — what does each guarantee, over what unit, and what do you call their combination?

## A
- **Linearizability**: a *single-object, real-time* guarantee — every read/write appears to take effect atomically at some instant between its start and end, so a read after a completed write must see it. A recency/ordering contract; no notion of multi-object transactions.
- **Serializability**: a *multi-object transaction isolation* guarantee — the outcome equals **some** serial order of transactions. That order may disagree with real time: a serializable system may legally execute yesterday's-snapshot reads.

Together (transactions serialized in an order consistent with real time) = **strict serializability** — what Spanner provides. Classic trap: "serializable" alone does not imply "you read the latest committed data".

## Q zh
线性一致性和可序列化——各自保证什么？作用的单位是什么？它们俩结合在一起叫什么？

## A zh
- **线性一致性（Linearizability）**：一个*单对象、实时*的保证——每次读/写看起来都在其开始和结束之间的某个时刻原子地生效，所以一次写完成之后的读必须能看到它。这是一个新鲜度/顺序上的承诺；没有多对象事务的概念。
- **可序列化（Serializability）**：一个*多对象事务隔离*的保证——结果等价于事务的**某种**串行顺序。这个顺序可能和实时不一致：一个可序列化的系统合法地可以执行"昨天快照"式的读。

两者结合（事务按一个与实时一致的顺序串行化）= **严格可序列化（strict serializability）**——这正是 Spanner 提供的保证。经典的陷阱："serializable" 本身并不意味着"你读到的是最新提交的数据"。
