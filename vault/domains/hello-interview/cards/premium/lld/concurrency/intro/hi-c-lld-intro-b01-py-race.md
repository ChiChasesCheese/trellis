---
id: hi-c-lld-intro-b01-py-race
node: lld.concurrency.intro.beyond
type: qa
step: 1
---
## Q
**并发入门 · Python：GIL 不能代替锁**｜拓展 · 加分

Python 的 GIL 底层保护了什么？为什么读改写在 GIL 下仍可能丢更新？

## A
**模式。** 互斥临界区（critical section）：把"读、改、写"罩进同一把锁。

```python
import threading
import time


class Counter:
    def __init__(self) -> None:
        self.n = 0
        self._lock = threading.Lock()

    def inc_unsafe(self) -> None:
        v = self.n            # 读
        time.sleep(0)         # 让出 CPU，模拟调度器恰好在这里切换
        self.n = v + 1        # 写：可能覆盖别人刚写的值

    def inc_safe(self) -> None:
        with self._lock:      # 读到写之间，其他线程进不来
            v = self.n
            time.sleep(0)
            self.n = v + 1


def run(method: str, threads: int = 8, loops: int = 500) -> int:
    c = Counter()
    work = lambda: [getattr(c, method)() for _ in range(loops)]
    ts = [threading.Thread(target=work) for _ in range(threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return c.n


assert run("inc_safe") == 4000
assert run("inc_unsafe") < 4000      # 丢更新
```
- **GIL 做了什么：** 保证解释器内部结构不被破坏，并按字节码边界切换线程；一条 Python 语句常对应多条字节码，线程可在中间被切走
- **自然写法不一定出错：** 新版本的解释器切换点更少，`x += 1` 可能多次运行都对，这是偶然而非保证
- **何时不用锁：** 状态只由一个线程访问（线程封闭），或使用队列传递所有权
