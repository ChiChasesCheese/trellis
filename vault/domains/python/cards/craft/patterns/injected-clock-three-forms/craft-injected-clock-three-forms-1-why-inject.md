---
id: craft-injected-clock-three-forms-1-why-inject
node: craft.patterns.injected-clock-three-forms
type: qa
step: 1
---
## Q
**注入时钟 · 为什么测试「恰好到点」不能靠 sleep**｜模式

冷却器规定每个用户 10 秒内只放行一次。要测「第 10 秒整的那一刻」的行为，直接在 `allow` 里调 `time.monotonic()` 的话怎么测？注入时钟又是怎么解决的？默认值怎么选？

## A
**要点。** 把时间变成输入。类不自己读时钟，而是通过构造参数拿一个返回当前时间的函数（Clock）。生产代码用默认的真实时钟，测试传一个手动拨动的假时钟，于是边界可以精确到某一个值，不会因机器慢而偶发失败，也不用真的等 10 秒。

```python
Clock = Callable[[], float]

class Cooldown:
    """每个 key 每 10 秒最多放行一次。"""

    def __init__(self, clock: Clock = time.monotonic) -> None:   # 默认单调时钟；测试传假的
        self._clock = clock                 # 默认单调时钟，测试传假的
        self._last: dict[str, float] = {}

    def allow(self, key: str) -> bool:
        now = self._clock()
        last = self._last.get(key)
        if last is not None and now - last < 10:
            return False
        self._last[key] = now
        return True

class FakeClock:
    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t

fake = FakeClock()
c = Cooldown(fake)
print(c.allow("u"))          # t=0
fake.t = 9.999
print(c.allow("u"))             # 差一点点
fake.t = 10.0
print(c.allow("u"))             # 恰好到点：不用 sleep，一行就测到

# 陷阱：默认参数在 def 时就绑定了，事后替换 time.monotonic 不起作用
time.monotonic = lambda: 1e9    # type: ignore[assignment]
c2 = Cooldown()
t0 = c2._clock()
print("补丁后默认时钟读数是否为 1e9:", t0 == 1e9)
```

实际输出（前三行依次是 t=0、9.999、10.0 的结果，最后一行是下面说的陷阱）：

```
True
False
True
补丁后默认时钟读数是否为 1e9: False
```

**易错。** 默认参数在 `def` 时就绑定了：事后用 `time.monotonic = ...` 替换并不会影响已经绑定的默认值，所以补丁时钟走不通，必须真正把时钟作为参数传入。

**为什么。** 默认选 `time.monotonic` 而不是 `time.time`：墙上时钟会被校时（NTP）、手动改时间而跳变甚至倒退，算时长应该用单调时钟。
