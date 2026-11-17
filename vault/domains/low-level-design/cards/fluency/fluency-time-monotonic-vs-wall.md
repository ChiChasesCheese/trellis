---
id: fluency-time-monotonic-vs-wall
node: fluency.time-numbers
type: qa
step: 4
---
## Q
限流器要算“距离上次放行过了多少毫秒”，同事用 `time.time()` 相减，再 `int(秒 * 1000)`。这里有哪两个问题？哪种时钟、什么类型更合适？

## A
**间隔用单调时钟 + 整数纳秒**

- **墙钟（wall clock）`time.time()`、`datetime.now()`**：能被 NTP 校时、手动调整拨回去，相减可能得到负数；只用来表示“什么时候发生”，要存库或展示；
- **单调时钟（monotonic）`time.monotonic()`**：只增不减，不受系统时间调整影响；但起点不确定，不能存库、不能跨进程比较，只用来量“过了多久”；
- **浮点秒会丢精度**：纳秒量级的时刻用 `float` 秒表示后相减，差值本该是整毫秒，乘 1000 后却是 `…457.9999`，`int()` 截断少 1 毫秒；
- **内部用整数**：`time.monotonic_ns()` 返回 `int`，相减、整除都是精确的；对外要毫秒时用 `// 1_000_000`（向 0 截断，要四舍五入是另一个需求，要写明）；
- **测试**：时钟作为参数传进来（`clock=time.monotonic_ns`），测试里换成假时钟，不要在测试里 `sleep`。

```python
import time

class Stopwatch:
    def __init__(self, clock=time.monotonic_ns):
        self._clock = clock
        self._start = clock()

    def elapsed_ms(self) -> int:
        return (self._clock() - self._start) // 1_000_000   # 整数纳秒，精确整除

a, b = 4419269212589083, 4422791670589083          # 真实差值正好 3522458 ms
print((b - a) // 1_000_000)                         # 3522458
print(int((b / 1e9 - a / 1e9) * 1000))              # 3522457：浮点相减少了 1 ms
```

<details class="pt"><summary>延伸</summary>

多个服务实例共用一个限额时，各机器的时钟互不一致，“现在”要取共享存储（Redis、数据库）服务端的时间，不要取各实例自己的时钟。

</details>

**知识点：**时间与数字（Time & Numbers）
