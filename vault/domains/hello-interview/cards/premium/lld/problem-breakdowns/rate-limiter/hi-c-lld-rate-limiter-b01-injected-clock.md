---
id: hi-c-lld-rate-limiter-b01-injected-clock
node: lld.problem-breakdowns.rate-limiter.beyond
type: qa
step: 2
---
## Q
**限流器 · Python：注入时钟与单调时钟**｜拓展 · 加分

为什么限流器的时间源要作为参数传进去？墙钟倒退会怎样？测试里怎么拨快时间？

## A
**模式。** 注入时钟：把"现在是几点"当作依赖传进来，而不是在类里直接调用全局函数。

```python
import time
from dataclasses import dataclass


@dataclass
class FakeClock:                                 # 测试替身：时间只在你拨的时候走
    now_ms: float = 0.0

    def __call__(self) -> float:
        return self.now_ms

    def advance(self, ms: float) -> None:
        self.now_ms += ms


def wall_ms() -> float:
    return time.time() * 1000                    # 墙钟：NTP 校时、手动改时间都会让它跳变


# 墙钟倒退 5 秒时，令牌桶的 elapsed 变成负数，令牌被"反向补充"，桶被扣成负数
elapsed = (1_000_000 - 5_000) - 1_000_000
tokens = min(10, 3 + elapsed * 2 / 1000)         # 容量 10，每秒 2 个，当前 3 个
print(tokens)                                    # 3 - 10 = -7：之后很长时间全部被拒绝

clk = FakeClock()
clk.advance(500)
assert clk() == 500
```
- **注入的好处：** 测试时用 `FakeClock` 手动 `advance`，不用 `sleep`，结果确定且瞬间完成；核心实现里的令牌桶就是 `TokenBucket(10, 1, clock)` 这样把时钟传进去的。
- **默认值用单调时钟：** `time.monotonic()` 保证不倒退，不受 NTP 或手动改时间影响；`time.time()` 是日历时间，会跳变。
- **可调用对象：** 用带 `__call__` 的类（或 `lambda`）都行，类型只需 `Callable[[], float]`。
- **何时不用：** 一次性脚本里直接调用 `time.monotonic()` 就够，不要为了模式而注入。
