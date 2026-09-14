---
id: distributed-conflict-detection-siblings
node: distributed.replication.multi-leader
type: qa
---
## Q
Mechanically, how does a replica decide that two writes to the same key *conflict* rather than one superseding the other — and what does it do with the pair?

## A
Each key carries a **version vector** (one counter per leader/replica). A client reads, gets the value plus its version (an opaque "causal context"), and echoes that version on the next write. On arrival the replica compares:

- Incoming version **dominates** the stored one (≥ in every slot) → the writer saw the stored value; **overwrite**.
- Versions are **incomparable** → genuinely concurrent; keep **both as siblings**.

Siblings are then resolved by application semantics — merge (union a shopping cart, take the max), let the user pick, or apply a type whose merge is defined (CRDT). Riak/Dynamo expose siblings explicitly; the *failure* is a store that silently collapses incomparable versions with a timestamp, because that discards a write the system knew was concurrent.

## Q zh
从机制上讲，副本是如何判定对同一个 key 的两次写入是*冲突*的，而不是一个覆盖另一个的？它又是如何处理这一对写入的？

## A zh
每个 key 都带有一个**版本向量**（每个 leader/副本一个计数器）。客户端读取时得到值和它的版本（一个不透明的"因果上下文"），并在下一次写入时带回这个版本。写入到达时，副本比较：

- 传入的版本**支配**（dominate）已存储的版本（在每个槽位上都 ≥）→ 写入者看到了已存储的值；**覆盖**。
- 两个版本**无法比较** → 确实是并发的；**两者都作为兄弟（siblings）保留**。

兄弟之后由应用语义来解决——合并（购物车取并集，取最大值）、让用户选择，或者应用一个定义了合并规则的类型（CRDT）。Riak/Dynamo 会显式暴露兄弟；*错误*的做法是存储悄悄用时间戳把无法比较的版本折叠成一个，因为这样会丢弃一个系统明明知道是并发的写入。
