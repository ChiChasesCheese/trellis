---
id: cc-python-classes-slots
node: python.classes
type: qa
---
## Q
10^6 record objects blow the memory budget. What does `__slots__` change, and what does it cost you?

## A
**`__slots__` removes the per-instance `__dict__`**, storing attributes in a fixed array — typically 40–50 % less memory per object, plus slightly faster attribute access.

```python
class Row:
    __slots__ = ("day", "user", "amount")
```

- `@dataclass(slots=True)` (3.10+) writes it for you.
- Costs: no ad-hoc attributes, no `__weakref__` unless you list it, and every class in an inheritance chain must declare slots or the dict comes back.
- A tuple or `NamedTuple` is still smaller. Reach for `__slots__` when you need **named, mutable** fields and the object count runs into the millions ([[cc-performance-memory-object-cost]]).

## Q zh
10^6 个记录对象把内存预算撑爆了。`__slots__` 改变了什么？它让你付出什么代价？

## A zh
**`__slots__` 去掉了每个实例的 `__dict__`**，把属性存进一个定长数组 —— 通常每个对象省 40–50% 内存，属性访问也略快。

```python
class Row:
    __slots__ = ("day", "user", "amount")
```

- `@dataclass(slots=True)`（3.10+）会替你写好。
- 代价：不能临时加属性；不列出 `__weakref__` 就没有弱引用；继承链上每个类都必须声明 slots，否则 dict 会回来。
- tuple 或 `NamedTuple` 仍然更小。只有当你需要**具名且可变**的字段、且对象数量以百万计时才动用 `__slots__`（[[cc-performance-memory-object-cost]]）。
