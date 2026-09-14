---
id: distributed-consistent-hashing
node: distributed.partitioning.schemes
type: qa
---
## Q
In consistent hashing, what fraction of keys moves when a node joins an N-node ring, why is that the whole point, and what problem do virtual nodes solve?

## A
Only ~**K/N** of K keys move — the keys between the new node and its predecessor on the ring. With naive `hash(key) mod N`, changing N remaps **almost every key**, which would flush caches or trigger a full data reshuffle; consistent hashing makes membership change cheap.

**Virtual nodes** (each physical node owns many ring positions, e.g. 100–256) fix two issues: with few positions, random placement makes ownership arcs **wildly uneven**, and a leaving node dumps its entire range onto **one successor**. Vnodes even out load and spread a departed node's data across the whole cluster.

## Q zh
在一致哈希中，当一个节点加入一个 N 节点的环时，K 个 key 中有多大比例会移动？为什么这正是它的意义所在？虚拟节点解决了什么问题？

## A zh
K 个 key 中只有大约 **K/N** 会移动——也就是环上新节点和它前驱之间的那些 key。而用朴素的 `hash(key) mod N`，改变 N 会让**几乎每个 key** 都被重新映射，这会冲掉缓存或触发一次全量数据重排；一致哈希让成员变化的代价变得很低。

**虚拟节点**（每个物理节点在环上占据多个位置，例如 100–256 个）解决了两个问题：位置数量少时，随机放置会让每个节点所有权对应的弧长**极不均匀**；而且一个离开的节点会把它的整个范围一次性倾倒给**单一的后继节点**。Vnode 既能让负载均衡，也能把一个离开节点的数据分散到整个集群。
