---
id: hi-c-lld-oop-concepts-b01-py-encapsulation
node: lld.in-a-hurry.oop-concepts.beyond
type: qa
step: 1
---
## Q
**面向对象概念 · Python：封装并不强制**｜拓展 · 加分

Python 的"私有"在底层是什么？返回内部集合时，复制和只读视图各自的代价是什么？

## A
**模式。** 防御性复制（defensive copy）与只读视图。

```python
from types import MappingProxyType


class Lot:
    def __init__(self) -> None:
        self._spots = ["A1", "A2"]
        self._prices = {"car": 5}

    @property
    def spots(self) -> tuple[str, ...]:
        return tuple(self._spots)                # 复制：O(n)，调用方改不到内部

    @property
    def prices(self) -> MappingProxyType:
        return MappingProxyType(self._prices)    # 只读视图：O(1)，但随内部变化


class Acct:
    def __init__(self) -> None:
        self.__bal = 0                           # 名称改写成 _Acct__bal


lot = Lot()
try:
    lot.prices["bus"] = 9
except TypeError:
    pass
assert Acct()._Acct__bal == 0                    # 只是改名，并非真私有
```
- **单下划线：** 只是约定；**双下划线：** 名称改写，目的是避免子类意外冲突，不是安全机制
- **`@property`：** 是描述符，读取时调用函数，所以可以先加校验、以后不改调用方
- **选哪个：** 集合小或调用不频繁用复制；大集合且调用方只读用视图，但要接受它"活着"
