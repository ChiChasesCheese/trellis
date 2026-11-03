---
id: hi-pt-kv-store-eviction-3-lru
node: qb.lld.kv-store-eviction.points
type: qa
step: 3
---
## Q
**可配置淘汰策略的内存键值存储 · O(1) 的 LRU**｜必会 · 出自：可配置淘汰策略的内存键值存储 › 深入 1

LRU 策略怎么做到访问、淘汰都是 O(1)？代码长什么样？

## A
**要点。** `OrderedDict` 就是哈希表加双向链表，队尾是最近使用。
```python
def on_access(self, key): self._order.move_to_end(key)
def victim(self): return next(iter(self._order), None)
```
访问 `move_to_end`，淘汰取第一个，都是 O(1)。
