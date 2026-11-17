---
id: concurrency-depth-iterate-snapshot
node: concurrency-depth.compound-actions
type: qa
step: 5
---
## Q
一个线程在 `for k in d` 遍历字典，另一个线程同时往里插 key，会发生什么？应该怎么写 `top(n)` 这类要遍历内部状态的方法？

## A
**遍历也是复合操作：锁内拷贝，锁外慢慢算**

- **现象**：`RuntimeError: dictionary changed size during iteration`；列表则是悄悄漏项或重复，没有报错；
- **实测（3.11，读线程遍历 1000 个 key 的字典 20 遍，写线程不停插入，100 轮）**：默认间隔 0/100，1e-6 下 100/100 轮抛错；3.14t 默认间隔 99/100；
- **做法**：持锁时只做一件事，把需要的内容拷成快照（`list(d.items())`）；排序、过滤、格式化都在锁外对快照做，写入不被它挡住；
- **不要把内部容器直接返回**：调用方在锁外遍历同样会撞上，返回快照或不可变视图。

```python
import threading

class Board:
    def __init__(self):
        self._scores, self._lock = {}, threading.Lock()
    def add(self, name, pts):
        with self._lock:
            self._scores[name] = self._scores.get(name, 0) + pts
    def top(self, n):
        with self._lock:
            snap = list(self._scores.items())   # 锁内只拷贝
        snap.sort(key=lambda kv: -kv[1])        # 排序在锁外
        return snap[:n]
```

**知识点：**复合操作（Compound Actions）
