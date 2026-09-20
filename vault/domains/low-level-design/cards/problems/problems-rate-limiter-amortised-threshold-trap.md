---
id: problems-rate-limiter-amortised-threshold-trap
node: problems.components.rate-limiter
type: qa
step: 6
tags: [grown]
---
## Q
限流器（Rate Limiter）用「攒够一批操作就扫一遍分片、回收闲置 key」来摊还清理成本。把触发条件写成 `if ops >= max(64, len(states))` 有什么致命问题？

## A
在「每次操作都带来一个新 key」的场景下它**永远追不上**：`ops` 每加一，`len(states)` 也加一。

第一次扫描（ops=64、条目 64，此时还没有东西过期，回收 0 个）之后 `ops` 归零，从此两者恒差 64，`ops >= len(states)` 再也不成立，扫描不再触发，内存一路涨到一百万。

正确写法是把门槛**定死在上一次整理完的规模**上，而不是每次和当前规模比较：

```python
shard.ops = 0
shard.purge_at = max(64, len(shard.states))
```

修好之后，一百万个只来过一次的 key，常驻条目稳定在一个窗口内出现的 key 数（约一万），不随总量增长。

这和哈希表「按上次 rehash 之后的大小决定下次扩容点」是同一种摊还论证：**和一个会被自己撑大的量比较，摊还就不成立**。
