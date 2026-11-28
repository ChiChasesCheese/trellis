---
id: hi-c-sd-online-chess-b03-clock-injection
node: sd.problem-breakdowns.online-chess.beyond
type: qa
step: 3
---
## Q
**在线象棋 · 拓展：棋钟用单调时钟，并注入时钟便于测试**｜拓展 · 加分

服务端怎么实现棋钟才不受系统时间调整影响？怎么在不真等 3 分钟的情况下测试超时判负？

## A
**模式。** 注入时钟（injected clock）：时间作为参数传入，生产用单调时钟，测试用手动拨动的假时钟。

```python
import time
from typing import Callable


class ChessClock:
    def __init__(self, ms: int, now: Callable[[], float] = time.monotonic) -> None:
        self.left = {"w": ms, "b": ms}
        self.turn = "w"
        self.now = now                          # 注入：测试可替换，不依赖真实时间
        self.started = now()

    def remaining(self, side: str) -> int:
        if side != self.turn:
            return self.left[side]
        return self.left[side] - int((self.now() - self.started) * 1000)

    def press(self, credit_ms: int = 0) -> None:
        # 走子方：扣掉自己用的时间，再还给他估计的网络耗时 credit_ms
        self.left[self.turn] = self.remaining(self.turn) + credit_ms
        self.turn = "b" if self.turn == "w" else "w"
        self.started = self.now()

    def flagged(self) -> bool:
        return self.remaining(self.turn) <= 0


t = [0.0]
c = ChessClock(180_000, now=lambda: t[0])
t[0] += 5.2                                      # 白方想了 5.2 秒
c.press(credit_ms=100)
assert c.remaining("w") == 180_000 - 5_200 + 100
t[0] += 200                                      # 黑方想了 200 秒
assert c.flagged()                               # 不用真等就验证了超时
```
- **为什么用单调时钟：** 墙上时钟（`time.time()`）会被 NTP 或手动调整跳变，棋钟可能突然多出或少掉几秒；`time.monotonic()` 只增不减，适合量"经过了多久"。
- **状态存"剩余毫秒"：** 不要存"到点时间戳"，因为不同机器的时钟互不可比；换服务器接手时只能依靠这类相对量。
- **代价：** 单调时钟的起点因机器而异，不能写进库或发给别的机器；跨机器只传剩余时间。
