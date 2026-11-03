---
id: hi-pt-kv-store-eviction-2-fetch-flow
node: qb.lld.kv-store-eviction.points
type: qa
step: 2
---
## Q
**可配置淘汰策略的内存键值存储 · 命令统一流程 _fetch**｜必会 · 出自：可配置淘汰策略的内存键值存储 › 整体设计

所有命令共用的取值流程是什么？容量满时怎么腾空间？

## A
**流程。** 加锁 → 惰性过期（过期就删并当作不存在）→ 类型检查（类型不对抛 `WrongType`）→ 不存在且要创建则先 `_make_room()` 再插入并 `on_insert` → 已存在则 `on_access` → 执行具体结构的操作。
**腾空间。** 反复问策略 `victim()` 并删除，直到腾出空间。
```python
while len(self._data) >= self._cap:
    self._remove(self._policy.victim())
```
