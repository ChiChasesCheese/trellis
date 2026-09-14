---
id: caching-cache-shard-blast-radius
node: caching.placement
type: qa
---
## Q
Clients shard keys across 10 cache nodes. Why consistent hashing instead of `hash(key) % 10`, and what is the blast radius when one node dies?

## A
With modulo, any membership change remaps nearly **all** keys — adding or losing a node is an effective cluster-wide flush, and the resulting miss storm lands on the DB. Consistent hashing moves only ~1/N of the keyspace per membership change.

Blast radius of one dead node: ~1/N of reads become misses — so node count N is a sizing lever: the DB must absorb 1/N of cache read load (plus warming) without falling over ([[caching-hit-rate-outage-math]]).

## Q zh
客户端在 10 个缓存节点中分片键。为什么一致性哈希而不是 `hash(key) % 10`，以及当一个节点死亡时的冲击半径是什么？

## A zh
使用模运算，任何成员资格更改几乎重新映射 **所有** 键 — 添加或丢失节点是有效的集群范围刷新，结果 miss 风暴登陆 DB。一致哈希每次成员资格更改只移动 ~1/N 的键空间。

一个死节点的冲击半径：~1/N 的读变成 miss — 所以节点计数 N 是调整大小杠杆：DB 必须吸收 1/N 的缓存读负载（加上预热）而不会倒下（[[caching-hit-rate-outage-math]]）。
