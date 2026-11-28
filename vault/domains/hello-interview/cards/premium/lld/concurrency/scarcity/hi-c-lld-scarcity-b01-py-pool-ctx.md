---
id: hi-c-lld-scarcity-b01-py-pool-ctx
node: lld.concurrency.scarcity.beyond
type: qa
step: 1
---
## Q
**并发稀缺资源 · Python：用上下文管理器让归还无法被遗忘**｜拓展 · 加分

连接池的借还靠调用方自觉调用 `release` 很脆弱。用上下文管理器封装借用，同时加入校验和多还检测，怎么写？

## A
**模式。** 对象池加借用上下文（object pool with lease）：借用与归还成对出现。

```python
import queue
import threading
from contextlib import contextmanager
from typing import Callable, Generic, Iterator, TypeVar

T = TypeVar("T")


class Pool(Generic[T]):
    def __init__(self, size: int, make: Callable[[], T], ok: Callable[[T], bool]) -> None:
        self._q: queue.Queue[T] = queue.Queue(maxsize=size)     # 有界
        self._make, self._ok = make, ok
        for _ in range(size):
            self._q.put(make())

    @contextmanager
    def lease(self, timeout: float = 0.5) -> Iterator[T]:
        try:
            conn = self._q.get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError("pool exhausted") from None
        if not self._ok(conn):                                  # 取出时校验，失效就换新的
            conn = self._make()
        try:
            yield conn
        finally:                                                # 异常也一定归还
            self._q.put_nowait(conn)                            # 满了抛 queue.Full，暴露重复归还


made: list[dict] = []


def make() -> dict:
    c = {"id": len(made), "alive": True}
    made.append(c)
    return c


pool = Pool(1, make, lambda c: c["alive"])
with pool.lease() as c1:
    c1["alive"] = False                       # 模拟连接被服务端断开
with pool.lease() as c2:
    assert c2["alive"] and c2 is not c1      # 失效的已被换成新连接
try:
    with pool.lease():
        raise RuntimeError("boom")
except RuntimeError:
    pass
with pool.lease():                            # 异常之后仍可借出：没有泄漏
    pass
sem = threading.BoundedSemaphore(1)
sem.acquire()
sem.release()
try:
    sem.release()
except ValueError:
    pass                                      # BoundedSemaphore 揪出多余的 release
```
- **`@contextmanager`：** 生成器在 `yield` 处暂停，`with` 退出时恢复并执行 `finally`，所以异常路径也归还
- **`put_nowait`：** 池有界，多还一次会立刻抛 `queue.Full`，而不是悄悄让两个线程共享一个连接
- **`BoundedSemaphore`：** 普通 `Semaphore` 多 `release` 会让许可数超过初始值，不报错；有界版本抛 `ValueError`
- **何时不用：** 短生命周期的廉价对象，直接创建
