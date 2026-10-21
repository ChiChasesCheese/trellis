---
id: amz-configurable-cache-stage1-put-flow-code
node: amazon.amz-configurable-cache
type: qa
step: 3
tags: [grown]
---
## Q
在可配置缓存里，写入一个新 key 的核心流程是什么？用 Python 写出 `put`（策略 `policy` 只记 key，后端 `store` 存值，`victim()` 返回该淘汰的 key）。

## A
先写后端（会失败的一步放最前），再淘汰，最后让策略登记新 key：
```python
def put(self, key, value):
    exists = key in self._policy
    self._store.put(key, value)
    if exists:
        self._policy.on_access(key)
        return
    if len(self._policy) >= self._capacity:
        victim = self._policy.victim()
        self._store.delete(victim)
        self._policy.on_remove(victim)
    self._policy.on_insert(key)
```
覆盖已有 key 不涨容量，只算一次使用。
