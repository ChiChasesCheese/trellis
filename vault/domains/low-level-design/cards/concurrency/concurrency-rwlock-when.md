---
id: concurrency-rwlock-when
node: concurrency.patterns
type: qa
step: 5
---
## Q
Python 标准库没有读写锁（reader-writer lock）。什么场景下值得自己实现一个，怎么用 `Condition` 搭出最简单的版本？

## A
读写锁允许多个读者并发持有，但写者要求独占——只有当读远多于写、且读操作本身持锁时间较长时才划算；如果读写比例接近，或者单次操作很快（微秒级），读写锁自身的计数管理开销可能反而比直接用一把 `Lock` 更慢，这种情况下应该先测量，而不是想当然地引入它。

最简单的实现用一把 `Condition` 加一个读者计数：

```python
class SimpleRWLock:
    def __init__(self):
        self._cond = threading.Condition()
        self._readers = 0
        self._writer = False

    def acquire_read(self):
        with self._cond:
            while self._writer:
                self._cond.wait()
            self._readers += 1
```

`acquire_write` 在 `_readers == 0 and not self._writer` 时才能通过，取得后置 `self._writer = True`；对应的 release 方法递减计数并 `notify_all()`。这个朴素版本没做"写者优先"，长期高频写入下可能出现读者持续插队饿死写者的问题。
