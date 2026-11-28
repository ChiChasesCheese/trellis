---
id: hi-c-lld-correctness-b01-py-striping
node: lld.concurrency.correctness.beyond
type: qa
step: 1
---
## Q
**并发正确性 · Python：锁条带取代锁映射**｜拓展 · 加分

按键一把锁需要一个会增长的锁映射。固定数量的锁条带怎么做，多键操作怎么避免死锁？

## A
**模式。** 分段锁（lock striping）：键哈希到固定个数的锁。

```python
import threading
from contextlib import ExitStack


class Booking:
    STRIPES = 16

    def __init__(self) -> None:
        self._locks = [threading.Lock() for _ in range(self.STRIPES)]   # 数量固定，不随座位增长
        self._owner: dict[str, str] = {}

    def _stripe(self, seat: str) -> int:
        return hash(seat) % self.STRIPES

    def book(self, seat: str, who: str) -> bool:
        with self._locks[self._stripe(seat)]:
            if seat in self._owner:
                return False
            self._owner[seat] = who
            return True

    def swap(self, a: str, b: str) -> None:
        # 多个键：条带编号去重并排序，所有线程同序加锁
        idx = sorted({self._stripe(a), self._stripe(b)})
        with ExitStack() as stack:
            for i in idx:
                stack.enter_context(self._locks[i])
            if a in self._owner and b in self._owner:       # 两个座位都已有主人才交换
                self._owner[a], self._owner[b] = self._owner[b], self._owner[a]
```
- **好处：** 没有管理锁、没有无界映射，内存固定
- **代价：** 不同的键可能落在同一条带，出现假竞争；条带数是调参项
- **多键必须去重排序：** 两个键落在同一条带时，`Lock` 不可重入，重复获取会死锁
- **何时不用：** 并发低或键很少时，一把锁更简单
