---
id: hi-c-lld-bookmyshow-b02-py-bitmask
node: lld.problem-breakdowns.bookmyshow.beyond
type: qa
step: 4
---
## Q
**电影票预订 · Python：用一个整数表示 546 个座位**｜拓展 · 加分

怎么把"检查多个座位都没被占"做成一次按位运算？这种表示的代价是什么？

## A
**模式。** 位图（bitmap）：每个座位一位，集合运算变成位运算。

```python
import threading

COLS = 21


def bit(seat: str) -> int:
    return 1 << ((ord(seat[0]) - 65) * COLS + int(seat[1:]))   # A0 是第 0 位，Z20 是第 545 位


def mask(seats: list[str]) -> int:
    m = 0
    for s in seats:
        m |= bit(s)
    return m


class MShow:
    def __init__(self) -> None:
        self.booked = 0                  # 一个整数装下 546 个座位的状态
        self._lock = threading.Lock()

    def book(self, seats: list[str]) -> int:
        want = mask(seats)               # 锁外先算好
        with self._lock:
            if self.booked & want:       # 一次按位与：任何一个座位被占就非零
                raise ValueError("taken")
            self.booked |= want          # 一次按位或：全部占上
            return want

    def cancel(self, want: int) -> None:
        with self._lock:
            self.booked &= ~want         # 清掉这笔订单的位


m = MShow()
a = m.book(["A5", "A6"])
try:
    m.book(["A6", "A7"])                 # A6 冲突：整笔失败
except ValueError:
    pass
assert m.booked == mask(["A5", "A6"])    # A7 没有被占
m.cancel(a)
assert m.booked == 0
```
- **底层：** Python 的 `int` 是任意精度，内部按每 30 位一个数字（digit）存放，546 位约占 19 个数字；按位运算对整个数逐个数字处理，一次就覆盖所有座位。
- **好处：** 全有或全无的检查和修改各是一个表达式，临界区极短；内存小；可用座位数是 `546 - bin(booked).count("1")`。
- **代价：** 状态与订单列表是两份数据，取消时要精确清掉这笔订单的位，重复座位会让位运算与订单脱节（所以输入要先去重）；座位 id 到位号的映射写死了布局。
- **何时不用：** 面试里默认用订单列表推可用性；被追问性能时讲位图，并说明要同步维护。
