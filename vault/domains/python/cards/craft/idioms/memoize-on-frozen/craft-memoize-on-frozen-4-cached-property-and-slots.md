---
id: craft-memoize-on-frozen-4-cached-property-and-slots
node: craft.idioms.memoize-on-frozen
type: qa
step: 4
---
## Q
**冻结与记忆化 · frozen + slots 的类怎么放派生值**｜写法

行程（Itinerary）是 `frozen=True, slots=True` 的数据类，有一个由航段算出的总价 `total`。很自然会想用 `@cached_property` 缓存它，实际上会失败。为什么？有哪几种替代做法？

## A
**要点。** `cached_property` 把算好的值写进实例的 `__dict__`。`slots=True` 的类没有 `__dict__`，所以访问时就抛 `TypeError`。三种选择：派生值便宜就用普通 `@property` 每次重算；值贵但创建时就能算，在 `__post_init__` 里用 `object.__setattr__` 设置（冻结类设字段的唯一正门）；真的要懒计算，去掉 `slots`，或者把缓存放在对象之外。

```python
from dataclasses import dataclass
from functools import cached_property

@dataclass(frozen=True, slots=True)
class Itinerary:
    legs: tuple[int, ...]
    @property
    def total(self) -> int:                   # 每次重算：便宜的派生值就这样
        return sum(self.legs)

print(Itinerary((1, 2, 3)).total)

try:
    @dataclass(frozen=True, slots=True)
    class Bad:
        legs: tuple[int, ...]
        @cached_property
        def total(self) -> int:
            return sum(self.legs)
    Bad((1, 2)).total
except TypeError as e:
    print("TypeError:", e)

@dataclass(frozen=True, slots=True)
class Pre:
    legs: tuple[int, ...]
    total: int = 0                            # 创建时算好
    def __post_init__(self) -> None:
        object.__setattr__(self, "total", sum(self.legs))   # frozen 里设值的唯一正门
print(Pre((1, 2, 3)).total)
```

实际输出：

```
6
TypeError: No '__dict__' attribute on 'Bad' instance to cache 'total' property.
6
```

**为什么。** 总价、首段起飞时间这类派生值，开销是几次属性读取，每次重算比引入缓存和失效逻辑都更简单可靠，因为对象不可变，派生值永远不会过期。`Pre` 的做法让 `total` 成了字段，会参与 `==` 和 `repr`，需要时加 `field(compare=False)`。

**易错。** 预计算的字段要从 `__init__` 参数里排除（`field(init=False)`）才不会被调用方传入一个与 `legs` 不一致的值。
