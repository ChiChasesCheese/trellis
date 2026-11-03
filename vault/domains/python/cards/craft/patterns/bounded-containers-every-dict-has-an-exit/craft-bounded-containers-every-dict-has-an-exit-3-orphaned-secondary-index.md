---
id: craft-bounded-containers-every-dict-has-an-exit-3-orphaned-secondary-index
node: craft.patterns.bounded-containers-every-dict-has-an-exit
type: qa
step: 3
---
## Q
**有界容器 · 主表删空了，旁边的索引表谁来清**｜写法

内存键值库里，`fields[key][field]` 存数据，另一张 `key_expiry[key]` 记「整个 key 什么时候过期」。用户先给 key 设了 key 级过期时间，再把它的字段一个个手动删光。主表里这个 key 因为没有字段已经删掉了，`key_expiry` 里呢？应该怎样让这类泄漏在测试里现形？

## A
**要点。** 每当一个容器的项被删掉，所有**以同一个 key 为索引的旁路结构**（过期表、堆、反向索引、计数器）都要在同一个动作里一起清。漏掉任何一张，它就成了孤儿，随着「设了 key 级 TTL 再删光字段」这种用法无限增长。做法：把「删主表的最后一项」作为清旁路的唯一触发点，集中在一个写入函数里，不让每个调用方各自记得。

```python
class Store:
    """key -> {field: value}；另有一张 key 级的过期表 key -> 过期时刻。"""
    def __init__(self, clean_orphans):
        self.fields, self.key_expiry, self.clean = {}, {}, clean_orphans
    def set(self, key, field, value, ttl=None):
        self.fields.setdefault(key, {})[field] = value
        if ttl is not None: self.key_expiry[key] = ttl
    def delete(self, key, field):
        bucket = self.fields.get(key)
        if bucket:
            bucket.pop(field, None)
            if not bucket:
                del self.fields[key]                   # 主表的出口
                if self.clean:
                    self.key_expiry.pop(key, None)     # 副表也要跟着走，否则孤立

for clean in (False, True):
    s = Store(clean)
    for i in range(1000):
        s.set(f"k{i}", "f", "v", ttl=10_000)           # 先设 key 级 TTL
        s.delete(f"k{i}", "f")                         # 再手动把字段删光
    print(f"清理副表={clean}: fields={len(s.fields)}  key_expiry={len(s.key_expiry)}")
```

1000 个 key 各设 TTL 再删光字段：

```
清理副表=False: fields=0  key_expiry=1000
清理副表=True: fields=0  key_expiry=0
```

**为什么。** 主表看起来是空的，所有功能测试都通过（查不到就是查不到），泄漏只存在于一张谁也不读的表里。堆里的墓碑、`inflight` 登记表、订阅游标表也是同类：功能不依赖它们，所以不出错，只是越积越多。

**怎么让它现形。** 给每一个会增长的容器暴露一个只读的计数（`expiring_key_count`、`expiry_heap_size`、`inflight_count`、`tracked_keys`、`cursor_count`），然后在测试里写一条「做完一轮操作、全部清理后，计数必须回到 0 或有界」的断言。这些计数属性本身就是设计的一部分，不是调试代码。

**易错。** `finally` 里清理登记表（比如 `inflight.pop`）：异常路径是最容易漏的出口。
