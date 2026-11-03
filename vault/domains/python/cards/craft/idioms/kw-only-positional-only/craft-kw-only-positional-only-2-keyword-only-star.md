---
id: craft-kw-only-positional-only-2-keyword-only-star
node: craft.idioms.kw-only-positional-only
type: qa
step: 2
---
## Q
**参数形态 · 熔断器的配置参数为什么放在 `*` 之后**｜写法

熔断器的构造函数有一串同类型的数值参数：`failure_threshold`（几次失败后断开）、`open_timeout`（断开多少秒后试探）、`half_open_max_calls`。调用方写 `CircuitBreaker(30, 5)`，本意是「5 次失败、30 秒」，却写反了。类型检查器看不出来，运行时也不报错。怎样让这种错误当场暴露？

## A
**要点。** 同类型的位置参数是静默出错的高发区：顺序对调后类型依然匹配。`*` 之后的参数是仅关键字（keyword-only）的，调用方必须写名字，位置调换就不可能发生，而且代码读起来自带注释：`failure_threshold=5, open_timeout=30`。经验是：一串同类型的配置参数，一律放在 `*` 之后。

```python
class Breaker:
    def __init__(self, failure_threshold: int = 5, open_timeout: float = 30.0,
                 half_open_max_calls: int = 1) -> None:
        self.failure_threshold, self.open_timeout = failure_threshold, open_timeout
        self.half_open_max_calls = half_open_max_calls

class Breaker2:
    def __init__(self, *, failure_threshold: int = 5, open_timeout: float = 30.0,
                 half_open_max_calls: int = 1) -> None:
        self.failure_threshold, self.open_timeout = failure_threshold, open_timeout
        self.half_open_max_calls = half_open_max_calls

b = Breaker(30, 5)                                  # 想写 5 次失败 / 30 秒，写反了
print(b.failure_threshold, b.open_timeout)          # 不报错：类型也都对得上
try:
    Breaker2(30, 5)
except TypeError as e:
    print("TypeError:", e)
b2 = Breaker2(failure_threshold=5, open_timeout=30)
print(b2.failure_threshold, b2.open_timeout)
```

实际输出：

```
30 5
TypeError: Breaker2.__init__() takes 1 positional argument but 3 were given
5 30
```

**为什么。** 第一行是危险的：阈值成了 30 次、超时成了 5 秒，程序照常运行，只是行为不对，要到线上出事才发现。仅关键字把这类错误从运行期的行为异常变成调用时的立刻报错。

**取舍。** 并非所有参数都该这样。最核心、顺序天然明确的一两个参数（`Rect(width, height)` 之类）保留位置形式更自然；可选的、数量多的、同类型的，放到 `*` 之后。
