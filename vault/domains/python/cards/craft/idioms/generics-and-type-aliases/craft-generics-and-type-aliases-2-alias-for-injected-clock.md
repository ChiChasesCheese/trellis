---
id: craft-generics-and-type-aliases-2-alias-for-injected-clock
node: craft.idioms.generics-and-type-aliases
type: qa
step: 2
---
## Q
**泛型与类型别名 · 为什么要给 Clock 起一个类型别名**｜写法

限流器、缓存都接受一个注入的时钟，参数类型写成 `Callable[[], float]`。几十个类各自重复写，而且有的写成返回 `float` 秒，有的返回 `datetime`。别名统一了什么？它能挡住怎样的错误？

## A
**要点。** 类型别名（type alias）给一个类型起名：`Clock = Callable[[], float]`。作用有两个：把「时钟是什么」的约定写在一处（单调秒数、无参），读签名时看到 `Clock` 就知道含义；以及让检查器在约定被破坏时报错，例如把返回 `datetime` 的函数传给要求 `float` 秒的位置。别名只是同一个类型的另一个名字，运行时没有任何开销。

```python
from collections.abc import Callable
from datetime import datetime, timezone

Clock = Callable[[], float]                 # 约定：单调秒数；永远从外部注入

class Limiter:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock
    def now(self) -> float:
        return self._clock()

def utc_now() -> datetime:                  # 另一个解法里的口径：datetime
    return datetime.now(timezone.utc)

fake = [100.0]
print(Limiter(lambda: fake[0]).now())       # 测试里注入假时钟
print(type(Limiter(utc_now).now()).__name__)   # 运行时不报错，now() 却返回了 datetime
```

实际输出：

```
100.0
datetime
```

把上面的代码存成 `g2.py`，mypy 的检查结果：

```
g2.py:17: error: Argument 1 to "Limiter" has incompatible type "Callable[[], datetime]"; expected "Callable[[], float]"  [arg-type]
```

**为什么。** 第二行输出是不报错的 bug：`now()` 本该返回秒数，却返回了日期对象，后面做加减时才会炸。别名加检查器，让这个错误在传入时就暴露。

**取舍。** 一个共享的别名模块能避免各处重写和口径漂移，代价是多一个依赖；约定值得统一时（所有时钟都是单调秒数）才共享。确实需要两种口径（单调秒数用于时长、墙上时间用于日历规则），就起两个名字，不要用同一个名字装两种含义。
