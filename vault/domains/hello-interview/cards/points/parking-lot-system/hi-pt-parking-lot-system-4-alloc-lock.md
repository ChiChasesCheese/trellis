---
id: hi-pt-parking-lot-system-4-alloc-lock
node: qb.lld.parking-lot-system.points
type: qa
step: 4
---
## Q
**停车场管理系统 · 分配的原子性**｜必会 · 出自：停车场管理系统 › 深入 2、逐步扩展 2

多个入口同时入场，如何保证同一个车位不会分给两辆车？同一车牌重复入场怎么挡？

## A
**要点。** 分配器「检查并取走」在同一把锁的临界区内完成。
```python
with self._lock:
    for kind in COMPAT[vt]:
        if self._free[kind]:
            return heapq.heappop(self._free[kind])[2]
```
**车牌。** 用集合先占位，分配失败要回滚占位。
**粒度。** 几千车位每秒数次进出，一把锁足够；分类型加锁会引入多锁顺序问题。
