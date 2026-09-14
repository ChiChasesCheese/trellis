---
id: distributed-partition-hash-properties
node: distributed.partitioning.schemes
type: qa
---
## Q
What properties must the hash function used for hash partitioning have, which common property does it NOT need — and why is a language's built-in `hash()` a routing bug waiting to happen?

## A
Needs:
- **Deterministic across processes, machines, languages, and versions** — every producer/router/client must map the same key to the same partition, forever.
- **Uniform spread** over the output range, so partitions get even key counts.
- **Fast** — it runs on every request.

Does NOT need: **cryptographic strength**. There's no adversary to resist (an attacker who knows your keys can hit a partition regardless), so systems use cheap non-crypto hashes — MurmurHash (Kafka's partitioner), FNV, xxHash — and keep them frozen for compatibility.

The trap: built-in hashes are not stable. Python's `hash()` is **randomized per process** (`PYTHONHASHSEED`), Java's `hashCode()` for objects is identity-based, and libraries occasionally change algorithms. Any of these silently sends the same key to different partitions from different processes — breaking per-key ordering, cache affinity, and joins.

## Q zh
用于 hash 分区的哈希函数必须具备哪些性质？它不需要哪个常见性质？为什么语言内置的 `hash()` 是一个潜伏的路由 bug？

## A zh
必须具备：
- **跨进程、跨机器、跨语言、跨版本确定性**——每个生产者/路由器/客户端必须把同一个 key 永远映射到同一个分区。
- 在输出空间上**分布均匀**，让各分区的 key 数量均衡。
- **快**——它在每个请求上都要执行。

不需要：**密码学强度**。这里没有需要抵御的对手（知道你 key 的攻击者本来就能打爆某个分区），所以系统用廉价的非加密哈希——MurmurHash（Kafka 的 partitioner）、FNV、xxHash——并为了兼容性把算法冻结不再改。

陷阱在于：内置哈希并不稳定。Python 的 `hash()` **每个进程随机化**（`PYTHONHASHSEED`），Java 对象的 `hashCode()` 基于对象标识，库偶尔还会更换算法。以上任何一种都会让不同进程把同一个 key 悄悄发到不同分区——破坏 per-key 顺序、缓存亲和性和 join。
