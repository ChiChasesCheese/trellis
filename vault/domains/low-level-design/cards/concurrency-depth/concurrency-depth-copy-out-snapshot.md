---
id: concurrency-depth-copy-out-snapshot
node: concurrency-depth.confinement
type: qa
step: 5
---
## Q
`Inbox.items()` 在锁里把内部列表直接 `return self._items`，调用方拿到后在锁外遍历，会出什么问题？锁已经加了，为什么还不够？

## A
**引用一旦出了锁，锁就管不到它了：返回快照**

- **泄漏（leak）**：调用方拿着内部列表的引用，别的线程之后 `add` 的内容会出现在他手里，遍历时长度还在变；锁只在方法执行期间有效，之后引用本身就是共享状态；
- **返回副本**：`tuple(self._items)`，在锁里拷贝，之后随调用方怎么用都和内部无关；
- **元素也要独立**：元素是冻结值（`frozen=True` 的数据类、元组）时，浅拷贝就够；元素是可变对象，调用方改了元素还是改到内部，要么深拷贝，要么元素本身不可变；
- **视图不是快照**：`MappingProxyType`、`dict.items()` 都是活的视图，内部变了它跟着变，别当快照返回；
- **代价**：每次读拷贝 O(n)。读多写少、数据大时，改成“发布后不再修改的不可变对象，更新时换引用”更省，读线程不用拷贝。

```python
import threading
class Inbox:
    def __init__(self):
        self._items, self._lock = [], threading.Lock()
    def add(self, x):
        with self._lock: self._items.append(x)
    def leaky(self):
        with self._lock: return self._items          # 引用出了锁
    def items(self):
        with self._lock: return tuple(self._items)   # 快照
box = Inbox(); box.add(1)
view, snap = box.leaky(), box.items()
box.add(2)
print(view, snap)                                    # [1, 2] (1,)
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）
