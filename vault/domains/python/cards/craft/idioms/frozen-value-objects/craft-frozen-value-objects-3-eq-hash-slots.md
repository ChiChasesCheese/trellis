---
id: craft-frozen-value-objects-3-eq-hash-slots
node: craft.idioms.frozen-value-objects
type: qa
step: 3
---
## Q
**不可变值对象 · eq、frozen、hash 的组合，以及 slots 要付出什么**｜写法

`@dataclass` 不带参数时对象为什么不能放进 set？`frozen=True` 为什么一加就能？再加 `slots=True` 省了什么、又有哪些东西会失灵？

## A
**要点。** dataclass 生成 `__eq__` 之后必须决定 `__hash__`：相等的对象 hash 必须相同。`eq=True` 且可变时字段会变，hash 若跟着变，放进 set 的对象就找不回来了，所以 dataclass 直接把 `__hash__` 设为 `None`（不可哈希）。`eq=True` 且 `frozen=True` 才生成基于字段的 hash。`unsafe_hash=True` 是自担风险。

```python
@dataclass                                   # eq=True, frozen=False
class A:
    x: int

@dataclass(frozen=True)                      # eq=True, frozen=True
class B:
    x: int

@dataclass(eq=False)                         # 保留 object 的 identity 比较
class C:
    x: int

print("A.__hash__ =", A.__hash__)
print("B 可哈希:", hash(B(1)) == hash(B(1)))
print("C 相等吗:", C(1) == C(1), "| C 可哈希:", hash(C(1)) is not None)

# 为什么 A 不给 hash：可变对象的 hash 若随字段变，放进 set 之后就找不回来了
@dataclass(unsafe_hash=True)
class Risky:
    x: int

r = Risky(1)
s = {r}
r.x = 2                                      # 放进集合后改了字段
print("改字段后还在集合里吗:", r in s, "| 遍历仍有它:", r in list(s))
```

实际输出：

```
A.__hash__ = None
B 可哈希: True
C 相等吗: False | C 可哈希: True
改字段后还在集合里吗: False | 遍历仍有它: True
```

`slots=True` 让实例不再有 `__dict__`：每个对象更小，访问字段稍快，不能随手加属性。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Plain:
    a: int
    b: int

@dataclass(frozen=True, slots=True)
class Slotted:
    a: int
    b: int
```

```
有 __dict__: True | False
slots 不能加属性: AttributeError
slots 默认不能弱引用: cannot create weak reference to 'Slotted' object
slots + cached_property: TypeError No '__dict__' attribute on 'Cp' instance to cache 'double' property.
```

**代价。** slots 实例默认不能弱引用（要 `weakref_slot=True`，3.11 起可用），`functools.cached_property` 需要 `__dict__`，会失效。要缓存计算结果的值对象，别开 slots，或者自己在构造时算好存字段。
