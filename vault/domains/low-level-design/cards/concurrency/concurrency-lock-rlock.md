---
id: concurrency-lock-rlock
node: concurrency.primitives
type: qa
step: 1
---
## Q
`threading.Lock` 和 `threading.RLock` 有什么区别？为什么一个已经持锁的函数递归调用自己、又想再拿同一把锁时应该用 `RLock`？

## A
`Lock` 不可重入：同一个线程第二次 `acquire()` 会直接阻塞（等着一个永远不会来的 `release()`），造成自锁死锁。`RLock`（reentrant lock，可重入锁）会记录持有它的线程和递归层数，同一线程可以多次 `acquire()`，只要 `release()` 相同次数就行；但这个"同一线程"很关键——别的线程仍然要等它完全释放。

```python
lock = threading.RLock()

def outer():
    with lock:
        inner()  # 同一线程再次拿锁，RLock 不会卡住

def inner():
    with lock:
        ...
```

误用：把 `RLock` 当成"更安全的默认选择"到处用——它比 `Lock` 略重，而且递归加锁往往是设计上把临界区拆得不够干净的信号，能避免就避免。
