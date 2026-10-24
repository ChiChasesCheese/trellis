---
id: pl-abstraction-typeclasses-philosophy-python-runtime-retrofit
node: abstraction.typeclasses
type: qa
step: 9
---
## Q
Python 没有类型类，却能在运行时为 `int`、第三方类补充能力。`singledispatch` 和 `ABC.register` 是怎样做到的，它们与 Rust 的 trait 有什么本质差别？

## A
Python 的类型都是运行时对象，随时可以被注册。两个标准库工具在做类型类式的事：

**`functools.singledispatch`**：把一个函数变成按第一个参数的类型分派的「泛函数」，之后可以从任何地方为任何类型登记实现：

```python
from functools import singledispatch
@singledispatch
def describe(x): return "something"
@describe.register
def _(x: int): return f"int {x}"
@describe.register
def _(x: list): return "[" + ", ".join(describe(i) for i in x) + "]"
print(describe(5), describe([1, "a"]))   # int 5 [int 1, something]
```

`describe` 的定义里不需要知道 `int` 和 `list`，登记可以写在任何模块，包括对第三方类型。没有登记的类型（`"a"`）落到默认实现。这就是类型类的「实例声明」，只是在运行时才起作用，查找依据是对象的类及其父类（MRO）。

**`ABC.register`**：把一个与抽象基类毫无继承关系的类声明为它的「虚拟子类」：

```python
from abc import ABC, abstractmethod
class Closeable(ABC):
    @abstractmethod
    def close(self): ...
class Foreign:
    def close(self): pass
isinstance(Foreign(), Closeable)   # False
Closeable.register(Foreign)
isinstance(Foreign(), Closeable)   # True
```

和 Rust 的差别：

1. **何时检查**：Rust 在编译期保证每个调用都有实例，缺了就编译失败；Python 在运行时才知道，缺了抛 `TypeError`（或落到默认实现）。
2. **一致性**：Rust 保证全局唯一；Python 里两个库可以对同一个类型各登记一次，后注册的覆盖先注册的，行为取决于导入顺序。
3. **分派位置**：Rust 的实例由类型决定，可以按返回类型分派；`singledispatch` 只按第一个参数的运行时类型。

两者都是「能力在类型之外」，选择不同是因为语言目标不同：Rust 需要证明，Python 需要灵活。
