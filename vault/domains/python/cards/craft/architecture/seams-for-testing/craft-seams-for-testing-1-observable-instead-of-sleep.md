---
id: craft-seams-for-testing-1-observable-instead-of-sleep
node: craft.architecture.seams-for-testing
type: qa
step: 1
---
## Q
**测试接缝 · 并发测试怎样知道「一个线程真的已经卡住了」**｜架构

有界阻塞队列满了以后，`put` 应该阻塞。测试要验证这一点：启动一个线程去 `put`，然后断言它没有返回。常见写法是 `time.sleep(0.1)` 后断言线程还活着，但线程可能还没来得及开始运行。怎样既不靠猜、也不拖慢测试？

## A
**要点。** 给被测对象开一个只读的可观测量（observable），例如 `waiting_putters`：当前卡在「不满」条件上的线程数。测试轮询它直到等于 1，才说明那个线程真的进了等待，再往下断言。这是一个测试接缝（seam，不改被测逻辑就能在这里观察或替换行为的缝）。

```python
class BoundedQueue:
    def __init__(self, capacity: int) -> None:
        self._items: list[int] = []
        self._cap = capacity
        self._cv = threading.Condition()
        self._waiting_putters = 0                    # 为测试（也为监控）暴露

    def put(self, x: int) -> None:
        with self._cv:
            while len(self._items) >= self._cap:
                self._waiting_putters += 1               # 为测试（也为监控）暴露
                try:
                    self._cv.wait()
                finally:
                    self._waiting_putters -= 1
            self._items.append(x)

    @property
    def waiting_putters(self) -> int:
        with self._cv:
            return self._waiting_putters

    def take(self) -> int:
        with self._cv:
            x = self._items.pop(0)
            self._cv.notify_all()
            return x

def wait_until(pred, timeout=2.0) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if pred():
            return True
        time.sleep(0.001)
    return False

def slow_start_put(q: BoundedQueue) -> None:
    time.sleep(0.05)                                 # 模拟线程调度慢
    q.put(3)

# 靠猜：睡 10 毫秒，就断言「它一定已经阻塞了」
q = BoundedQueue(2); q.put(1); q.put(2)
t = threading.Thread(target=slow_start_put, args=(q,)); t.start()
time.sleep(0.01)                                     # 靠猜
print("猜 sleep：此刻有线程阻塞吗?", q.waiting_putters == 1)
t.join(0.2); q.take(); t.join()

# 靠可观测量：轮询到它真的阻塞为止
q = BoundedQueue(2); q.put(1); q.put(2)
t = threading.Thread(target=slow_start_put, args=(q,)); t.start()
print("轮询计数：确认阻塞", wait_until(lambda: q.waiting_putters == 1))
q.take(); t.join()
```

两种测法各跑一次（`wait_until` 轮询，超时 2 秒），实际输出：

```
猜 sleep：此刻有线程阻塞吗? False
轮询计数：确认阻塞 True
```

**为什么。** 睡的时间短了，测试偶尔失败（调度慢的 CI 机器上）；睡长了，每个并发测试都白等。轮询可观测量既快又稳，条件满足立刻往下走。

**代价。** 这个属性要在锁内读，否则读到的是撕裂的值；它在生产里也有用（卡住的线程多了，说明该扩容），所以暴露的不是纯粹的测试后门。
