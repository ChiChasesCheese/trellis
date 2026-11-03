---
id: craft-lazy-deletion-heap-2-validity-test
node: craft.patterns.lazy-deletion-heap
type: qa
step: 2
---
## Q
**惰性删除堆 · 弹出一个条目时，怎么判断它是不是墓碑**｜模式

任务调度器、库存预留、TTL 缓存都用惰性删除堆，但判断「这个堆条目还有效吗」的依据各不相同。三种判据分别是什么？如果延期了一个预留，只比对 id 会出什么错？

## A
**要点。** 判据取决于堆条目与「当前真相」怎么对账：（1）任务表里还有没有它的 id；（2）当前记录的状态和到期时间是否还等于堆条目里带的那一份；（3）条目被显式标成已移除。延期时不删旧条目，只 push 新条目，旧条目带着旧的到期时间，所以必须比对到期时间。

```python
# task-scheduler：任务表里没了 = 墓碑
meta = self._tasks.get(entry.id)
if meta is None:
    continue

# inventory-management：状态和到期时间都得对得上
if entry.status is Status.ACTIVE and entry.expires_at == at:
    self._release(entry)       # 否则是被延期、确认或取消作废的旧条目

# ttl-cache：条目被标成 _REMOVED
self._heap = [e for e in self._heap if e[2] is not _REMOVED]
```

预留在 t=10 到期，t=5 延期到 100，到 t=10 时弹出旧条目：

```
只比对 id/状态   -> 已被过早过期
还比对到期时间  -> 仍然有效（延期生效）
```

**易错。** 只比对 id 或状态，延期的预留在旧时间点被误释放，别人的订单拿到了不该有的库存。

**见于。** task-scheduler、inventory-management、ttl-cache、credit-token-balance、amazon-locker。

**信号。** 需要「取消、延期、改期、覆盖」一个已经在堆（或延迟队列）里的元素，而容器没有按值删除。
