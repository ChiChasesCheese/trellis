---
slug: amazon-lru-query-results
---
## Q
**LRU 查询结果缓存**｜Medium

实现容量为 `cap` 的查询缓存 `get(key)`：命中就返回并标为最近使用；未命中调用后端 `fetch(key)`，结果写入缓存，超容量时淘汰最久未使用的项。

## A
**一句话。** 有序字典按使用先后排：命中 `move_to_end`，未命中先查后端再插到末尾，超容量 `popitem(last=False)` 弹出最旧的。

```python
class QueryCache:
    def __init__(self, cap, fetch):
        self.cap, self.fetch = cap, fetch
        self.data = OrderedDict()   # 头最旧，尾最新

    def get(self, key):
        if key in self.data:
            self.data.move_to_end(key)  # 读也刷新
            return self.data[key]
        val = self.fetch(key)       # 后端抛错就不缓存
        self.data[key] = val
        if len(self.data) > self.cap:
            self.data.popitem(last=False)
        return val
```

**复杂度。** 时间 `get` 为 `O(1)` 加一次后端调用，空间 `O(cap)`。

**易错点。**
- 命中不 `move_to_end`：只在写入时刷新，热读的 key 会被当成最旧的淘汰。
- 后端失败也写缓存：错误结果一直留到被淘汰，要么不缓存，要么单独给很短的 TTL。

**追问。**
- 同一个 key 并发 miss？：single-flight：每个 key 一个 future，只有第一个请求打后端，其余等它的结果。
- 结果会过期？：存 `(val, expire_at)`，命中时已过期就当 miss；TTL 管新鲜度，LRU 管容量。
- 多租户？：key 里要带租户和权限上下文，否则不同用户会读到彼此的结果。

**同模式。** LC 146 LRU 缓存、LC 460 LFU 缓存、LC 432 全 O(1) 的数据结构
