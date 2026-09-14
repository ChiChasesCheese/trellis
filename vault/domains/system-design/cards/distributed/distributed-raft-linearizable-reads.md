---
id: distributed-raft-linearizable-reads
node: distributed.consensus
type: qa
---
## Q
Why can't a Raft leader serve linearizable reads from its local state without extra work, and what are the two standard fixes?

## A
The leader may be **deposed and not know it** (partitioned away, long GC pause): a new leader is already committing writes elsewhere, so the old one's local read returns stale data as authoritative — a phantom-leader read.

- **Read index**: leader records its current commit index, **confirms leadership with a heartbeat round to a majority**, waits until its state machine has applied up to that index, then serves the read. Linearizable, costs one quorum round-trip per read batch.
- **Lease reads**: after a successful heartbeat, the leader assumes leadership for ~an election timeout and serves reads locally within that window. Nearly free, but safety now depends on **bounded clock drift** across nodes — a fast clock lets a deposed leader serve stale reads.

etcd exposes exactly this choice (linearizable vs serializable reads).

## Q zh
为什么 Raft 的 leader 不能不做额外工作就直接从本地状态提供线性一致的读？两种标准的修复方式是什么？

## A zh
这个 leader 可能**已经被废黜了却自己不知道**（被分区隔离、经历了一次长时间的 GC 暂停）：新的 leader 已经在别处提交写入了，所以旧 leader 的本地读会把陈旧数据当作权威数据返回——一次幽灵 leader 读。

- **Read index**：leader 记录当前的 commit index，**用一轮心跳向多数节点确认自己仍是 leader**，等到自己的状态机应用到那个 index 为止，然后才提供这次读。是线性一致的，代价是每批读付出一次 quorum 往返。
- **Lease reads（租约读）**：在一次成功的心跳之后，leader 假设自己在大约一个选举超时的时间窗口内仍是 leader，并在这个窗口内直接本地提供读服务。几乎零成本，但安全性现在依赖于**节点间有界的时钟漂移**——一个走得快的时钟会让一个已被废黜的 leader 继续提供陈旧的读。

etcd 正好把这个选择暴露给你（线性一致读 vs 可序列化读）。
