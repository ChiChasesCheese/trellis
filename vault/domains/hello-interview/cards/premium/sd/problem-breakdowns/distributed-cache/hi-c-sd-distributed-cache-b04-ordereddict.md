---
id: hi-c-sd-distributed-cache-b04-ordereddict
node: sd.problem-breakdowns.distributed-cache.beyond
type: qa
step: 4
---
## Q
**分布式缓存 · 拓展：Python 里一个 OrderedDict 就是 LRU，底下发生了什么**｜拓展 · 加分

面试时为什么手写 DLL 加哈希表，而不直接用 OrderedDict？它底下是什么，什么时候不该用？

## A
- **做法：** `OrderedDict` 的 `move_to_end(key)` 是 O(1)，`popitem(last=False)` 弹出最旧项，十行就是 LRU。
- **底下：** 用 C 实现，结构本质就是"哈希表 + 双向链表"，与手写的完全同构，所以复杂度相同；`dict` 自 3.7 起保持插入顺序，也能用 `pop` 再插入模拟"移到末尾"，但取最旧项要 `next(iter(d))`，开头积累的已删除空位会让它变慢，所以做 LRU 才选专为此设计的 `OrderedDict`。
- **为什么面试还是手写：** 这题考的就是这个结构，直接调库等于回避问题；手写才能体现你知道 O(1) 来自哪里，并能扩展到过期、统计等功能。
- **不该用的时候：**
  - 要线程安全：单个操作受 GIL 保护，但"get 然后 move_to_end"这种复合操作不是原子的，要自己加锁；
  - 要按 TTL 过期：它不管时间，要另外维护；
  - 要极致内存或亿级键：每项还有链表节点的开销，别用 Python 对象存，用 Redis 这类专用系统。
- **相关：** 标准库 `functools.lru_cache` 也是同样结构（C 实现，带锁），但只缓存函数调用，不支持 TTL 和手动失效。

```python
class OdLRU:
    def __init__(self, cap): self.cap, self.d = cap, OrderedDict()
    def get(self, k):
        if k not in self.d: return None
        self.d.move_to_end(k); return self.d[k]
    def set(self, k, v):
        self.d[k] = v; self.d.move_to_end(k)
        if len(self.d) > self.cap: self.d.popitem(last=False)
```
