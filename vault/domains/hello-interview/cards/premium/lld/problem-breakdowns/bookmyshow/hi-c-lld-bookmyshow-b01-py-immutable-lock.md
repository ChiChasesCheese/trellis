---
id: hi-c-lld-bookmyshow-b01-py-immutable-lock
node: lld.problem-breakdowns.bookmyshow.beyond
type: qa
step: 3
---
## Q
**电影票预订 · Python：不可变订单与私有锁**｜拓展 · 加分

订单怎么做到不用防御性拷贝？场次的锁为什么用一个私有的锁对象，而不是 `synchronized(this)` 那样锁对象自己？

## A
**模式。** 不可变值对象，加私有同步原语。

```python
import threading
from dataclasses import dataclass, FrozenInstanceError


@dataclass(frozen=True)                 # frozen：字段赋值会抛 FrozenInstanceError
class Res:
    id: str
    seats: tuple[str, ...]              # 元组不可变：没有 append，也不能原地修改


r = Res("r1", ("A5", "A6"))
try:
    r.seats = ("B1",)
except FrozenInstanceError:
    pass
assert not hasattr(r.seats, "append")


class Show:
    def __init__(self) -> None:
        self._lock = threading.Lock()   # 私有锁：只有本类的代码能拿到它
        self._taken: set[str] = set()

    def book(self, seats: tuple[str, ...]) -> bool:
        with self._lock:                # 检查与登记在同一个临界区
            if self._taken & set(seats):
                return False
            self._taken |= set(seats)
            return True


sh = Show()
out: list[bool] = []
ts = [threading.Thread(target=lambda: out.append(sh.book(("A5", "A6")))) for _ in range(100)]
for t in ts:
    t.start()
for t in ts:
    t.join()
assert out.count(True) == 1             # 100 个线程抢同一批座位，恰好一个成功
```
- **不可变省掉拷贝：** 持有者没法改它，就不用在构造和读取时各复制一次；还能放心地在线程之间共享。
- **私有锁：** 在 Java 里 `synchronized(this)` 锁的是对象本身，外部代码也能对同一个对象加锁，可能意外与内部互相阻塞甚至死锁；私有锁对象把"谁能参与这个锁"限定在类内。
- **代价：** 想"修改"订单只能创建新对象；订单很大且频繁改时要权衡。
- **何时不用：** 单线程脚本里加锁只增加复杂度。
