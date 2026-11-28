---
id: hi-c-lld-correctness-b03-py-cas
node: lld.concurrency.correctness.beyond
type: qa
step: 3
---
## Q
**并发正确性 · Python：版本号式乐观并发**｜拓展 · 加分

用锁保护整个"读、算、写"会长时间持锁。乐观并发怎么用版本号把锁缩到"比较并替换"一瞬？

## A
**模式。** 乐观并发（optimistic concurrency）：读取时带版本，写入时校验，不一致就重试。

```python
import threading
from typing import Callable


class VersionedStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()                   # 只保护比较并替换这一瞬
        self._data: dict[str, tuple[int, int]] = {}      # key -> (版本, 值)

    def read(self, key: str) -> tuple[int, int]:
        with self._lock:
            return self._data.get(key, (0, 0))

    def cas(self, key: str, expected: int, value: int) -> bool:
        with self._lock:
            ver, _ = self._data.get(key, (0, 0))
            if ver != expected:
                return False                             # 有人先改了
            self._data[key] = (ver + 1, value)
            return True


def update(store: VersionedStore, key: str, fn: Callable[[int], int]) -> None:
    while True:
        ver, val = store.read(key)
        new = fn(val)                                    # 耗时计算在锁外
        if store.cas(key, ver, new):
            return


s = VersionedStore()
ts = [threading.Thread(target=lambda: [update(s, "n", lambda v: v + 1) for _ in range(500)]) for _ in range(8)]
for t in ts:
    t.start()
for t in ts:
    t.join()
assert s.read("n") == (4000, 4000)
```
- **版本号的作用：** 值相同不代表没被改过（A 改成 B 再改回 A，即 ABA 问题），版本号只增不减能识别
- **同形：** 数据库的乐观锁（版本列）、HTTP 的 `If-Match`
- **何时不用：** 冲突频繁时重试风暴，浪费算力；这时用锁
