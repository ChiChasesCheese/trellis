---
id: hi-c-lld-design-principles-b03-inject-clock
node: lld.in-a-hurry.design-principles.beyond
type: qa
step: 3
---
## Q
**设计原则 · Python：注入时钟让依赖可测**｜拓展 · 加分

DIP 最实用的一个落点是时间。代码里直接调用 `time.time()` 有什么代价，注入一个可调用的时钟怎么写？

## A
**模式。** 注入时钟（injected clock）：时间是依赖，由外部传入。

```python
import time
from typing import Callable


class Session:
    def __init__(self, ttl: float, clock: Callable[[], float] = time.monotonic) -> None:
        self._ttl, self._clock = ttl, clock       # 默认值给生产用
        self._born = clock()

    def expired(self) -> bool:
        return self._clock() - self._born >= self._ttl


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


c = FakeClock()
s = Session(10, c)
assert not s.expired()
c.now = 10
assert s.expired()          # 不用 sleep，瞬间完成且确定
```
- **直接调用的代价：** 测试要 `sleep` 或打补丁，慢且偶发失败
- **为什么用 `monotonic`：** 计算时间间隔要用不会倒退的时钟；墙上时间会被校时调整
- **何时不用：** 一次性脚本不需要；只有被测逻辑真依赖时间时才注入
