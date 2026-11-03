---
id: craft-dunder-protocols-that-pay-1-bool-keeps-old-callers-working
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 1
---
## Q
**特殊方法 · 为什么限流结果要写 __bool__**｜写法

限流器的 `allow(key)` 原来返回 `bool`，调用处都是 `if limiter.allow(k):`。现在要让它同时返回「还剩多少额度、多久后重试」，改成一个 `Decision` 对象。如果不做额外处理，没改过的旧调用点会发生什么？`__bool__` 怎样解决，又有什么代价？

## A
**要点。** Python 判断 `if x:` 时，普通对象一律为真。把 `bool` 换成结果对象而没写 `__bool__`，被拒绝的请求也会让 `if` 成立：旧调用点悄悄放行了本该拒绝的请求，没有任何报错。`__bool__` 让对象的真值等于 `allowed`，于是返回类型可以从裸值升级成结构化结果，旧代码一行不用改。

```python
from dataclasses import dataclass

class Limiter:
    def __init__(self, left: int) -> None:
        self.left = left
    def allow(self, key: str) -> bool:                 # 旧版：裸 bool
        if self.left > 0:
            self.left -= 1
            return True
        return False

@dataclass(frozen=True)
class Decision:                                        # 新版：结构化结果
    allowed: bool
    retry_after: float

class Limiter2(Limiter):                               # 升级了，但没写 __bool__
    def allow(self, key: str):
        return Decision(super().allow(key), 0.0 if self.left else 30.0)

@dataclass(frozen=True)
class DecisionB(Decision):
    def __bool__(self) -> bool:                        # 让旧调用点继续成立
        return self.allowed

class Limiter3(Limiter):
    def allow(self, key: str):
        return DecisionB(super().allow(key), 0.0 if self.left else 30.0)

def handle(limiter) -> str:                            # 没改过的旧调用点
    return "放行" if limiter.allow("u1") else "拒绝"

print(handle(Limiter(0)), handle(Limiter2(0)), handle(Limiter3(0)))
d = Limiter3(0).allow("u1")
print(d.allowed, d.retry_after)                        # 新代码读字段
```

实际输出：

```
拒绝 放行 拒绝
False 30.0
```

中间那个 `放行` 就是漏洞：限流器已经拒绝了，旧代码却放行。

**代价。** `if decision:` 读起来像在问「是否成功」，会让新代码忽略 `retry_after` 之类的字段；真值也只适用于「有一个明确的好/坏」的类型。有多种结果（成功、部分成功、需要重试）时，用枚举字段，不要给它写 `__bool__`。
