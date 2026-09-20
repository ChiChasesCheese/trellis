---
id: problems-ttl-cache-heap-tuple-needs-a-counter
node: problems.components.ttl-cache
type: qa
step: 4
tags: [grown]
---
## Q
把 `(截止时刻, key)` 推进小顶堆来管理缓存过期，为什么会在生产里突然抛 `TypeError`？怎么修？

## A
因为两条**截止时刻完全相同**的记录，比较会落到第二项 `key` 上。而缓存对 key 的要求只有「可哈希」（hashable），从不要求「可比较」——放两个自定义对象、两个 `dict` 或两个不同类型的 key 进去，比较就抛 `TypeError: '<' not supported between instances of ...`。

这类 bug 极难在开发期撞上：只有当两个 key 的浮点截止时刻**一模一样**时才触发，测试里用注入时钟反而更容易命中，线上则表现为偶发崩溃。

修法是在中间塞一个全局自增序号：

```python
entry = [deadline, next(self._counter), key]
heapq.heappush(self._heap, entry)
```

序号唯一，比较永远停在第二项，第三项再也不参与；顺带还给同一时刻到期的条目一个稳定的先后顺序，让测试可复现。
