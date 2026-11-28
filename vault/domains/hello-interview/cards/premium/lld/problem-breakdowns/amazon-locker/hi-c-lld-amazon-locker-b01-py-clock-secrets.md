---
id: hi-c-lld-amazon-locker-b01-py-clock-secrets
node: lld.problem-breakdowns.amazon-locker.beyond
type: qa
step: 2
---
## Q
**快递柜 · Python：注入时钟与不可预测的码**｜拓展 · 加分

怎样让过期逻辑可测，又让取件码不可预测？为什么不能用 `random`？

## A
**模式。** 注入时钟：时间是依赖，由外面传进来。

```python
import random
import secrets
from dataclasses import dataclass


class FakeClock:                      # 测试里手动拨时间
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:      # 可调用对象：和 time.time 接口一致
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


@dataclass(frozen=True)
class Token:                          # frozen：创建后不可改，码和过期时刻不会被误写
    expires_at: float

    def is_expired(self, now: float) -> bool:
        return now >= self.expires_at


clock = FakeClock()
tok = Token(expires_at=clock() + 7 * 86400)
clock.advance(7 * 86400 - 1)
assert not tok.is_expired(clock())    # 差 1 秒：有效
clock.advance(1)
assert tok.is_expired(clock())        # 恰好到点：过期

random.seed(1)
a = [random.randint(0, 999999) for _ in range(3)]
random.seed(1)
assert a == [random.randint(0, 999999) for _ in range(3)]   # 同一种子，同一串数：可复现即可预测
code = f"{secrets.randbelow(10**6):06d}"                    # 取自操作系统的随机源
```
- **注入的好处：** 业务类不依赖真实时间，测试不用等也不用打补丁（monkeypatch）。
- **代价：** 构造函数多一个参数；默认值给真实时钟，调用方无感。
- **`random` 的问题：** 它是确定性的伪随机数生成器，状态可以从输出推回；凭证必须用 `secrets`。
- **何时不用：** 一次性的脚本里直接用 `time.time()` 更简单。
