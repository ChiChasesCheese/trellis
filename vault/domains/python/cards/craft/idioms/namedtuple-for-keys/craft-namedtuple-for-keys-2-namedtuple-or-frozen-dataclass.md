---
id: craft-namedtuple-for-keys-2-namedtuple-or-frozen-dataclass
node: craft.idioms.namedtuple-for-keys
type: qa
step: 2
---
## Q
**NamedTuple 做键 · NamedTuple 与冻结数据类怎么选**｜写法

复合键 `(账户, 币种)` 既可以写成 `NamedTuple`，也可以写成 `@dataclass(frozen=True, slots=True)`。两者都可哈希、都有字段名。选哪个？NamedTuple 有哪些不那么明显的缺点？

## A
**要点。** NamedTuple 本质是元组：轻、可拆包、自带排序，但相等性按元组算，没有 `__post_init__` 可校验。冻结数据类是独立的类型：相等要求类型相同，可以校验，但不能拆包、不可排序（除非 `order=True`）。键和轻量返回值选 NamedTuple；需要校验或要与别的类型严格区分时选数据类。

```python
from dataclasses import dataclass
from typing import NamedTuple

class KeyNT(NamedTuple):
    account: str
    currency: str

@dataclass(frozen=True, slots=True)
class KeyDC:
    account: str
    currency: str
    def __post_init__(self) -> None:
        if len(self.currency) != 3:
            raise ValueError(f"currency must be 3 letters: {self.currency!r}")

class Point(NamedTuple):
    x: int
    y: int
class Size(NamedTuple):
    w: int
    h: int

print(KeyNT("a", "USD") == ("a", "USD"), KeyDC("a", "USD") == ("a", "USD"))
print(Point(1, 2) == Size(1, 2))                       # 毫不相干的两种东西相等
print(KeyNT("a", "US"))                                # 没有校验
try:
    KeyDC("a", "US")
except ValueError as e:
    print("ValueError:", e)
print({Point(1, 2): "pt"}.get(Size(1, 2)))             # 当键时互相命中
print(sorted([KeyNT("b", "USD"), KeyNT("a", "EUR")]))  # 字段顺序比较，白送
```

实际输出：

```
True False
True
KeyNT(account='a', currency='US')
ValueError: currency must be 3 letters: 'US'
pt
[KeyNT(account='a', currency='EUR'), KeyNT(account='b', currency='USD')]
```

**为什么。** `Point(1, 2) == Size(1, 2)` 为真，所以放进同一个字典，一种键能查到另一种键的值。键只在一处、类型唯一时没问题；多种键共用同一个字典或集合时，要用数据类（相等先比类型），或者在键里加一个标签字段。

**信号。** 只是「几个有名字的值打包一起走」（键、返回值、行）：NamedTuple。有约束要保证，或不同种类的键可能混在一起：冻结数据类。
