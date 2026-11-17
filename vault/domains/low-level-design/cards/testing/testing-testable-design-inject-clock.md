---
id: testing-testable-design-inject-clock
node: testing.testable-design
type: qa
step: 1
---
## Q
一个令牌 60 秒后过期，测试想验证「第 59.9 秒还有效，第 60 秒失效」。直接在类里调用 `time.time()`，测试怎么写？为什么不用 `time.sleep(60)`？

## A
**把时钟当参数传进去，测试里换成假时钟**

- **`sleep` 的代价**：测试跑一分钟；机器忙时睡眠时长有误差，边界上的断言时对时错，这就是不稳定测试；
- **注入（injection）**：构造函数接一个返回当前时间的可调用对象，默认是 `time.time`；测试传一个返回变量的 lambda；
- **用起来**：测试里把变量设成几，「现在」就是几，边界上的两个时刻各一行断言；
- **只在一处读时钟**：所有判断都走这个可调用对象；漏掉一处直接调 `time.time()`，那处就测不了；
- **过期不存成列**：存 `expires_at`，每次询问时用当前时间现算，不要存一个「是否过期」的布尔值，它会越存越旧。

```python
import time
from typing import Callable

class Token:
    def __init__(self, ttl: float, clock: Callable[[], float] = time.time):
        self._clock = clock
        self.expires_at = clock() + ttl
    def expired(self) -> bool:
        return self._clock() >= self.expires_at

now = [1000.0]
tok = Token(60, clock=lambda: now[0])
now[0] = 1059.9; print(tok.expired())     # False
now[0] = 1060.0; print(tok.expired())     # True
```

<details class="pt"><summary>延伸</summary>

只在进程内量时长（超时、限速）应该用 `time.monotonic`：它不受系统改时间影响。要存进数据库或发给别的机器的过期时间才用墙钟（`time.time`）。两种时钟都以同样方式注入。

</details>

**知识点：**可测的设计（Design for Testability）
