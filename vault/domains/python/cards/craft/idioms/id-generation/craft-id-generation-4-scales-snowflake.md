---
id: craft-id-generation-4-scales-snowflake
node: craft.idioms.id-generation
type: qa
step: 4
---
## Q
**ID 生成 · 从进程内计数器到多实例唯一 ID**｜写法

电子钱包的分录编号用 `itertools.count(1)`，单进程里没问题。服务扩成多个实例后，每个实例都从 1 开始，编号会冲突。分布式系统里 ID 常见的三种做法是什么，各自的取舍？

## A
**要点。** 三种取舍：数据库序列（集中发号，唯一且有序，但每次要访问数据库，成为瓶颈）；随机 UUIDv4（各实例独立生成，不用协调，但无序，作为主键会让 B 树索引的插入落到随机位置）；时间有序的 ID（雪花 ID 类的「时间戳 + 机器号 + 序号」，各实例独立生成，大致按时间有序）。Python 标准库的 `uuid.uuid7()` 到 3.14 才有，3.11–3.13 需要第三方库或自己实现。

```python
import time
from collections.abc import Callable

EPOCH_MS = 1_700_000_000_000          # 自选纪元，41 位时间戳可以用得更久

class Snowflake:
    """64 位：41 位毫秒时间戳 | 10 位机器号 | 12 位毫秒内序号。"""
    def __init__(self, worker: int, clock_ms: Callable[[], int] = lambda: time.time_ns() // 1_000_000):
        assert 0 <= worker < 1024
        self.worker, self.clock_ms = worker, clock_ms
        self.last_ms, self.seq = -1, 0
    def next(self) -> int:
        ms = self.clock_ms()
        if ms < self.last_ms:
            raise RuntimeError("时钟回拨，拒绝发号")        # 回拨会发出重复 ID
        if ms == self.last_ms:
            self.seq = (self.seq + 1) & 0xFFF
            if self.seq == 0:                              # 这一毫秒 4096 个用完了
                while ms <= self.last_ms:
                    ms = self.clock_ms()                   # 等到下一毫秒
        else:
            self.seq = 0
        self.last_ms = ms
        return ((ms - EPOCH_MS) << 22) | (self.worker << 12) | self.seq

t = [EPOCH_MS + 5]
a, b = Snowflake(1, lambda: t[0]), Snowflake(2, lambda: t[0])   # 两台机器，同一毫秒
ids = [a.next(), a.next(), b.next(), b.next()]
print(ids)
print(len(set(ids)))
t[0] += 1
print(a.next() > max(ids))
t[0] -= 5
try: a.next()
except RuntimeError as e: print(e)
```

实际输出：

```
[20975616, 20975617, 20979712, 20979713]
4
True
时钟回拨，拒绝发号
```

**为什么。** 同一毫秒里两台机器不冲突，靠的是机器号占了固定的位；同一台机器同一毫秒靠序号；时间戳在高位，所以 ID 整体按时间增长。代价全在时钟：时钟回拨会让「时间戳 + 序号」重复，必须拒绝或等待；机器号要有人分配且不重复。

**信号。** 需要 ID 在多个写入方之间无需协调就唯一，且希望近似按时间排序（便于分页、索引局部性）：时间有序 ID。只需要唯一、不关心顺序：UUIDv4。
