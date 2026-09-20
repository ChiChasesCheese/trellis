---
id: problems-ttl-cache-expired-is-invisible
node: problems.components.ttl-cache
type: qa
step: 5
tags: [grown]
---
## Q
带过期时间的缓存（TTL Cache）里，一条已经过期但还没被物理删除的数据，`len()`、遍历、以及「容量满了吗」的判断应该怎么看待它？

## A
**对外必须当它不存在**：`__len__`、`keys()`、`__contains__` 都先做一次到期清理再回答。

两个理由，第二个才是致命的：

1. 把尸体算进去，`len(cache)` 就是一个会骗人的数字，调用方据此做的任何决定都是错的。
2. **「容量满了」会因为一堆尸体而提前触发**，于是缓存去淘汰一条还活着、还会被命中的数据，而那些早该消失的条目还占着位置。命中率就是这样被悄悄拉垮的。

配套的一条：`keys()` 要返回**快照**（`tuple`），不能返回内部视图或内部字典本身。交出去的活视图会在调用方遍历时被别的线程改动，等着他的是 `RuntimeError: dictionary changed size during iteration`；而且调用方还能反过来改你的内部状态。
