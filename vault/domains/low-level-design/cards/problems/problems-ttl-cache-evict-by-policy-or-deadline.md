---
id: problems-ttl-cache-evict-by-policy-or-deadline
node: problems.components.ttl-cache
type: qa
step: 6
tags: [grown]
---
## Q
带 TTL 的缓存容量满了：该按淘汰策略（如 LRU）赶人，还是先赶走马上就要过期的那条？这个分歧该怎么落到代码里？

## A
两个答案都合理，所以它不该被写死，而该是**同一条接缝的两种实现**——接缝就是「容量满时淘汰谁」这个策略接口，只不过要给它多传一个参数：

```python
class EvictionPolicy(Protocol[K]):
    def record_insert(self, key: K, expires_at: float | None) -> None: ...
    def record_access(self, key: K) -> None: ...
    def remove(self, key: K) -> None: ...
    def evict(self) -> K: ...
```

`record_insert` 收下 `expires_at` 不是 TTL 概念的泄漏：**「什么时候会死」本就是「该让谁先走」的合法输入**，LRU 选择无视它，那是 LRU 的决定。

「最近截止时刻优先」的理由是：反正它马上要死，淘汰它损失的未来命中最少。它的实现可以直接复用那个到期小顶堆（取最早到期的一个）；没有设置 TTL 的 key 不在堆里，它们之间退回 LRU——给一条永不过期的数据硬编一个截止时刻，只会让策略无法解释。
