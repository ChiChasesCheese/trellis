---
id: data-invariants-atomic-update
node: data.invariants
type: qa
step: 6
---
## Q
整份替换配置时，第 3 个条目校验失败，旧配置应当原封不动。先 `self._items.clear()` 再逐个添加，为什么不行？

## A
**先在旁边建好新的，再一步换上**

- **先清再填**：校验失败时旧数据已经没了，对象停在“半空”的非法状态；并发的读线程还会看到它；
- **顺序**：读成快照 → 校验全部 → 规范化 → 构造新结构 → 一次赋值；
- **失败路径什么都没写**：不变量始终成立，异常只会在“构造新值”阶段抛出；
- **构造函数与替换走同一条校验路径**：避免两处规则漂移；
- **批量登记同理**：解析、合并全成功后才赋值一次，不是边解析边写入。

```python
import threading

class Filter:
    def __init__(self, words):
        self._lock = threading.Lock()
        self._words: tuple[str, ...] = ()
        self.replace(words)                       # 与替换同一条路径
    def replace(self, words):
        items = list(words)                       # 快照
        if any(not isinstance(w, str) or not w.strip() for w in items):
            raise ValueError("bad word")          # 旧配置原封不动
        new = tuple(w.lower() for w in items)     # 旁边建好
        with self._lock:
            self._words = new                     # 一步换引用
```

**知识点：**不变量与封装（Invariants）
