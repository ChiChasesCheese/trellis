---
id: craft-slots-and-memory-2-what-slots-takes-away
node: craft.idioms.slots-and-memory
type: qa
step: 2
---
## Q
**__slots__ 与内存 · slots 带来的限制和一个意外的好处**｜写法

给类加上 slots 后，哪些原来能做的事不能做了？继承时有哪些容易踩的坑？它有没有顺带的好处？

## A
**要点。** 去掉 `__dict__` 意味着：不能临时添加属性，默认没有弱引用支持（需要的话要显式加），继承时子类若不声明 `__slots__` 就会把 `__dict__` 带回来，两个都有非空 slots 的父类不能同时继承。好处也来自此：拼错的属性名会立刻报 `AttributeError`，而不是悄悄新增一个属性。

```python
import weakref
from dataclasses import dataclass

@dataclass(slots=True)
class P:
    x: int

p = P(1)
try:
    p.y = 2                                  # 拼错/乱加属性：直接报错
except AttributeError as e:
    print("AttributeError")
try:
    weakref.ref(p)
except TypeError as e:
    print("TypeError:", e)

@dataclass(slots=True, weakref_slot=True)    # 3.11+：需要弱引用就显式要
class W:
    x: int
print(weakref.ref(W(1)) is not None)

class Base:
    __slots__ = ("a",)
class Child(Base):                           # 子类忘了写 __slots__：__dict__ 又回来了
    pass
class Child2(Base):
    __slots__ = ("b",)
print(hasattr(Child(), "__dict__"), hasattr(Child2(), "__dict__"))

class A: __slots__ = ("a",)
class B: __slots__ = ("b",)
try:
    class C(A, B): pass                       # 两个基类都有非空 slots：布局冲突
except TypeError as e:
    print("TypeError:", e)
```

实际输出：

```
AttributeError
TypeError: cannot create weak reference to 'P' object
True
True False
TypeError: multiple bases have instance lay-out conflict
```

**为什么。** 弱引用（weakref）需要对象里有一个 `__weakref__` 槽，缓存和观察者常用它，所以 slots 类要用时得显式要。子类忘了写 `__slots__`，只是回到有 `__dict__` 的状态，不会报错，但省下的内存也全没了，而且没人发现。

**信号。** 类属于「数据很多、字段固定、不需要动态属性和弱引用」的节点和记录：用 slots。需要弱引用、多重继承、反射式地加属性：不要。
