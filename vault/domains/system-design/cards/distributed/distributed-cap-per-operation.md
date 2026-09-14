---
id: distributed-cap-per-operation
node: distributed.cap
type: qa
---
## Q
Why is "is this system CP or AP?" the wrong granularity — and what is the right one? Give two real examples.

## A
The C/A trade is made **per operation**, not per system — the same store can serve some requests linearizably and others stale.

- **Cassandra/DynamoDB**: consistency level is chosen per read/write (`QUORUM` vs `ONE`; DynamoDB's `ConsistentRead` flag) — one table serves both CP-ish and AP-ish traffic.
- **ZooKeeper**: writes go through consensus, but reads are served **locally by any replica** (possibly stale) unless the client issues `sync` first — so even a "CP" system defaults to non-linearizable reads for speed.

Interview move: instead of labeling the system, state which *operations* need linearizability and pay for only those.

## Q zh
为什么 "这个系统是 CP 还是 AP？" 这个问题的粒度是错的——正确的粒度是什么？给两个真实的例子。

## A zh
C/A 的取舍是**按每个操作**做出的，而不是按整个系统——同一个存储可以对一些请求提供线性一致，对另一些提供陈旧数据。

- **Cassandra/DynamoDB**：一致性级别是按每次读/写选择的（`QUORUM` 对 `ONE`；DynamoDB 的 `ConsistentRead` 标志）——同一张表既能服务偏 CP 的流量，也能服务偏 AP 的流量。
- **ZooKeeper**：写入要经过共识，但读取默认由**任意一个副本本地提供服务**（可能是陈旧的），除非客户端先发出 `sync`——所以即便是"CP"系统，为了速度默认也提供非线性一致的读。

面试要点：与其给系统贴标签，不如说清楚哪些*操作*需要线性一致，并且只为那些操作付出代价。
