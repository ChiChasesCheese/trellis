---
id: concurrency-bounded-queue-invariants
node: concurrency.patterns
type: qa
step: 2
---
## Q
如果 `queue.Queue` 的接口不够用，需要自己用 `Condition` 从零实现一个有界阻塞队列，核心不变量和临界区是什么？

## A
不变量：`0 <= len(items) <= capacity`；队列空时消费者必须阻塞，队列满时生产者必须阻塞。用一把锁配两个条件变量表达这两种等待：

```python
class BoundedQueue:
    def __init__(self, capacity):
        self._items, self._cap = [], capacity
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

    def put(self, item):
        with self._not_full:
            while len(self._items) == self._cap:
                self._not_full.wait()
            self._items.append(item)
            self._not_empty.notify()
```

`get()` 是镜像结构：在 `_not_empty` 上等待非空，取出元素后 `notify()` 对应的 `_not_full`。所有对 `_items` 的读写都必须在持有同一把锁的情况下进行，这就是这个结构里唯一的临界区。
