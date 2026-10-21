---
id: amz-configurable-cache-followup-add-fifo-policy
node: amazon.amz-configurable-cache
type: qa
step: 6
tags: [grown]
---
## Q
在可配置缓存里，面试官追问「再加一种 FIFO 淘汰策略」，要改哪里、哪些代码不能动？

## A
只新增一个类并在注册表登记一行，`Cache`、`LruPolicy`、`LfuPolicy` 和所有后端一行不改：
```python
class FifoPolicy:
    def __init__(self): self._order = OrderedDict()
    def __len__(self): return len(self._order)
    def __contains__(self, key): return key in self._order
    def on_insert(self, key): self._order[key] = None
    def on_access(self, key): pass
    def on_remove(self, key): self._order.pop(key, None)
    def victim(self): return next(iter(self._order))

POLICIES["fifo"] = FifoPolicy
```
访问不改变顺序：容量 2 时 put a、b，get a，put c，被淘汰的仍是 a。
