---
id: concurrency-augmented-assignment-not-atomic
node: concurrency.model
type: qa
step: 2
---
## Q
`counter += 1` 在多个线程里并发执行，为什么结果会比预期的小，即使 CPython 有 GIL？

## A
`counter += 1` 不是一条字节码，而是"读取 `counter` → 加 1 →写回 `counter`"这样的一串字节码；GIL 只保证其中每一条单独执行时不被打断，但线程可以在读和写之间被切换出去。于是两个线程可能都读到同一个旧值、各自加 1、再各自写回，其中一次写会被覆盖，最终计数比"应该有的次数"少。

```python
import threading

counter = 0
def incr():
    global counter
    for _ in range(100_000):
        counter += 1  # 读-改-写，不是原子操作

threads = [threading.Thread(target=incr) for _ in range(4)]
```

修法和其他复合操作一样：用 `threading.Lock` 把"读-改-写"整体包起来，或者用 `itertools.count()`/`multiprocessing.Value` 这类专门设计过的原子计数器。
