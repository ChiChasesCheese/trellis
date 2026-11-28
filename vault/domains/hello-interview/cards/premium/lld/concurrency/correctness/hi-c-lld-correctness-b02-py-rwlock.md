---
id: hi-c-lld-correctness-b02-py-rwlock
node: lld.concurrency.correctness.beyond
type: qa
step: 2
---
## Q
**并发正确性 · Python：不会饿死写者的读写锁**｜拓展 · 加分

常见的"计数器加两把锁"手写读写锁有什么隐患？写者优先的版本怎么写？

## A
**模式。** 写者优先的读写锁（条件变量实现）。

```python
import threading
from contextlib import contextmanager


class RWLock:
    def __init__(self) -> None:
        self._cond = threading.Condition()
        self._readers = 0
        self._writer = False
        self._writers_waiting = 0

    @contextmanager
    def read(self):
        with self._cond:
            while self._writer or self._writers_waiting:   # 有写者在等，新读者让路
                self._cond.wait()
            self._readers += 1
        try:
            yield
        finally:
            with self._cond:
                self._readers -= 1
                if self._readers == 0:
                    self._cond.notify_all()

    @contextmanager
    def write(self):
        with self._cond:
            self._writers_waiting += 1
            while self._writer or self._readers:
                self._cond.wait()
            self._writers_waiting -= 1
            self._writer = True
        try:
            yield
        finally:
            with self._cond:
                self._writer = False
                self._cond.notify_all()
```
- **隐患：** 读者优先的实现里，只要读者源源不断，写者永远等不到读者数归零，被饿死
- **写者优先：** 有写者排队时挡住新读者；反过来可能让读者变慢
- **`@contextmanager`：** 把 `yield` 前当进入、后当退出，`finally` 保证异常也释放
- **何时不用：** 临界区极短或读写比例接近时，普通锁更快
