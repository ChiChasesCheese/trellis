---
id: concurrency-depth-visibility-happens-before
node: concurrency-depth.memory-model
type: qa
step: 2
---
## Q
一个线程写 `stop = True`，另一个线程在 `while not stop` 里循环读。Java 里这需要特殊的可见性修饰符，Python 里会读不到新值吗？那什么时候还需要同步？

## A
**读不到旧值的问题在 Python 里不存在，要同步的是“等待”和“组合”**

- **可见性**：每次循环都重新读属性，GIL 的交接让写入对其他线程可见。实测 50 次（写入前先让循环跑 10 ms），3.11 和 3.14t 都是 0/50 次循环没退出；Python 的值也不会读到一半（没有撕裂读）；
- **所以 Python 的并发错误是竞态条件（race condition），不是未定义行为**：结果可能错，但每个值都是某次真实写入的值；
- **先行发生（happens-before）靠同步点建立**：`Lock.release()` 先于之后的 `acquire()`；`Thread.start()` 之前的写，新线程能看到；`join()` 返回后能看到那个线程的写；`Event.set()` 先于 `wait()` 返回；`Queue.put` 先于对应的 `get`。拿这些点推理，不要拿“应该能看到”推理；
- **busy-wait 不好**：`while not stop: pass` 空转吃满一个核；示例用 `Event.wait(timeout)`，信号一到立刻醒，没信号就睡；
- **多个字段一起变**：线程 B 读到 `ready=True`，不代表同时更新的别的字段已经是新值，除非写入方在锁里一起改、读取方在锁里一起读。

```python
import threading
stop = threading.Event()
def worker():
    n = 0
    while not stop.wait(0.001):      # 等信号，带超时，不空转
        n += 1
    return n
t = threading.Thread(target=worker); t.start()
stop.set()                           # set 先于 worker 的 wait 返回 True
t.join(timeout=2)
print(t.is_alive())                  # False
```

**知识点：**内存模型与可见性（Memory Model）
