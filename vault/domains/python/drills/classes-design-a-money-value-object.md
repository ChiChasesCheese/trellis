---
nodes: [classes.dataclasses, classes.pythonic-object, classes.operator-overloading, classes.properties-descriptors, classes.inheritance-mro]
tags: [drill, interview]
---
# Drill：写一个不可变 `Money` 值对象，再用描述符复用校验

**限制与要求**
- 20 分钟内写完第 1、2 关，不许查文档。
- `Money` 必须真不可变（字段不能被重新赋值）、可哈希、能相加、`__repr__` 能看出怎么重建它。
- 描述符部分要能在两个以上字段上复用同一份校验逻辑，不许每个字段各写一遍 `if/raise`。
- 先说你选 `frozen dataclass` 还是手写 `__slots__` + 手写 dunder，再动手写。

**分关要求**
- 第 1 关（约 10 分钟）：写 `Money`（金额用整数分存储，`__eq__`/`__hash__`、`__add__`/`__radd__` 支持 `sum()`、`__repr__`、frozen）。
- 第 2 关（约 8 分钟）：写一个可复用的校验描述符（如 `PositiveInt`），用在一个可变的 `Account` 类的两个字段上。
- 第 3 关（约 5 分钟）：追问——`super().method()` 到底调的是谁？给一个菱形继承（diamond inheritance）的例子，让候选人说出 MRO 冲突时 Python 的行为。

**评分点（强答案会命中）**
- `frozen=True` 不是造出真正不可变对象，而是给类加了会抛 `FrozenInstanceError` 的 `__setattr__`/`__delattr__`；生成的 `__init__` 内部必须绕过它，用 `object.__setattr__` 赋值 [[dataclass-frozen-mechanism-cost]]
- `eq=True, frozen=False`（默认组合）会把 `__hash__` 显式设为 `None`；只有 `eq=True` 配 `frozen=True` 才会自动生成 `__hash__`，因为「不可变 + 可比较」才满足可哈希前提 [[dataclass-hash-generation-rules]]
- `@dataclass` 默认按字段顺序逐个比较生成 `__eq__`，且要求两边类型完全相同 [[dataclass-eq-field-by-field]]
- 二元运算符遇到不支持的类型要返回 `NotImplemented` 而不是自己 `raise`，否则剥夺了对方类型（比如 `int` 的 `0`）通过反射方法参与运算的机会 [[binary-op-return-notimplemented-not-raise]]
- `x + y` 只有在 `x.__add__(y)` 返回 `NotImplemented`，或 `type(y)` 是 `type(x)` 子类且重写了 `__radd__` 时，才会去调用 `y.__radd__(x)`；`sum()` 用 `0` 做初始值，所以 `__radd__` 要特殊处理 `other == 0` 的情况 [[radd-dispatch-conditions]]
- `property` 本质是内置的数据描述符（同时实现 `__get__`/`__set__`），数据描述符的优先级高于实例 `__dict__` 里的同名条目 [[property-is-data-descriptor]] [[data-vs-nondata-descriptor-priority]]
- 把校验逻辑写成独立的描述符类而不是每个字段各写一遍 `@property`，同一个描述符类可以实例化多次分别赋给不同属性名，靠 `__set_name__` 自动知道自己对应哪个属性名 [[descriptor-reuse-validation-across-attrs]] [[set-name-when-called]]
- `__set_name__` 是元类在类创建那一刻扫描类命名空间时调用的，之后动态挂上去的描述符不会自动触发它 [[set-name-when-called]]
- `super().method()` 调用的是实例 MRO 里紧跟在当前类之后的下一个类，不是源码字面上的父类；C3 算法找不出一致的线性化顺序时，Python 直接拒绝创建类并抛 `TypeError`，不会静默选一个不一致的顺序 [[super-dispatches-to-mro-next-not-parent]] [[mro-conflict-raises-typeerror]]

**参考答案**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int  # 以分为单位
    currency: str

    def __add__(self, other):
        if not isinstance(other, Money) or other.currency != self.currency:
            return NotImplemented
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        if other == 0:  # 支持 sum([...]) 的初始值 0
            return self
        return self.__add__(other)
```

`frozen=True` 自动生成的 `__eq__`/`__hash__` 按 `(amount, currency)` 逐字段比较/哈希；`__repr__` 由 dataclass 自动生成为 `Money(amount=..., currency=...)`，能直接重建对象。

```python
class PositiveInt:
    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, obj, owner=None):
        return getattr(obj, self._name)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self._name[1:]} must be >= 0")
        setattr(obj, self._name, value)


class Account:
    balance_cents = PositiveInt()
    daily_limit_cents = PositiveInt()

    def __init__(self, balance_cents, daily_limit_cents):
        self.balance_cents = balance_cents
        self.daily_limit_cents = daily_limit_cents
```

两个字段共享同一份 `PositiveInt` 校验逻辑，各自的存储位置由 `__set_name__` 在类创建时自动算出（`_balance_cents`、`_daily_limit_cents`），不需要为每个字段重复写 `if value < 0: raise`。

第 3 关：菱形继承例子——`class Base`，`class Left(Base)`，`class Right(Base)`，`class Child(Left, Right)`。`Child` 的 MRO 是 `[Child, Left, Right, Base, object]`；`Left.method` 里写的 `super().method()` 调的不是 `Base.method`，而是 MRO 中紧跟 `Left` 之后的 `Right.method`（如果 `Right` 重写了它），这正是协作式多继承（cooperative multiple inheritance）的关键。如果两个基类各自声明了互相矛盾的局部顺序（如 `class A(X, Y)`、`class B(Y, X)`，再 `class Z(A, B)`），C3 算法在 merge 阶段找不出满足两边局部顺序的表头，Python 会直接抛 `TypeError`，拒绝创建 `Z`，而不是随便选一个顺序凑合。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
