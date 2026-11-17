---
id: concurrency-depth-read-mostly-swap
node: concurrency-depth.safe-structures
type: qa
step: 5
---
## Q
功能开关表几乎只读、偶尔整体更新。读请求每秒几万次，更新时要保证读到的要么是整份旧表、要么是整份新表。为什么不给每次读都加锁，也不原地改字典？

## A
**读多写少：建新表，在锁里只换一个引用**

- **原地改（`clear()` 再逐个 `d[k]=v`）**：读线程可能读到空表或新旧混合。实测（3.11，读线程不停检查 50 个 key 的值是否同一代，更新 300 次，50 轮）默认间隔 43/50 轮读到混合，1e-6 下 50/50；
- **建新表再换引用**：新表在锁外建好，之后不再修改，锁里只做 `self._table = new`；读线程拿到一个引用就用这份，同样的实测 0/50（两种间隔都是），3.14t 上也是 0/50；
- **读不加锁的前提**：发布出去的表是不可变的（约定不改，或用 `MappingProxyType` 包一层），读一次属性只拿一次引用，别在一个请求里读两次 `self._table`；
- **写线程之间仍要互斥**：两个更新同时做“读旧表、改、换回去”会丢更新，换引用这一步和基于旧表的计算要在同一把锁里；
- **标准库没有读写锁**：读写分离靠这种换引用实现，比自己写读写锁简单也难出错。

```python
import threading
from types import MappingProxyType

class Flags:
    def __init__(self, table):
        self._table, self._lock = MappingProxyType(dict(table)), threading.Lock()
    def get(self, name):
        return self._table.get(name, False)       # 只读一次引用
    def update(self, changes):
        with self._lock:                          # 写与写互斥
            new = {**self._table, **changes}      # 基于当前表复制
            self._table = MappingProxyType(new)   # 换引用，旧表留给在读的人
```

**知识点：**线程安全结构的写法（Thread-Safe Structures）
