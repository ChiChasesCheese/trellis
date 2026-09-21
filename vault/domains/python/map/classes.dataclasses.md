%% trellis:begin %%
# `dataclass`、`NamedTuple` 与 `__slots__`
*类、协议与元编程*

比较三种数据类构建器的可变性、内存与哈希语义，`frozen=True`、`field(default_factory=)`、`__post_init__` 校验，以及 `__slots__` 省内存并禁止动态属性的代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]]

## Readings
- [[effective-07-classes-interfaces|Effective Python 3e · 第 7 章 类与接口]]
- [[fluent-05-dataclass-builders|Fluent Python 2e · 第 5 章 数据类构造器]]
- [[peps-pep557-dataclasses|PEP 557：数据类（Data Classes）]]
- [[pydocs-dataclasses-module|dataclasses 模块：数据类完整参考]]

## Drills
- [[classes-design-a-money-value-object|Drill：写一个不可变 `Money` 值对象，再用描述符复用校验]]

## Cards (7)
1. [[dataclass-eq-field-by-field]]
2. [[dataclass-frozen-mechanism-cost]]
3. [[dataclass-hash-generation-rules]]
4. [[dataclass-mutable-default-raises]]
5. [[namedtuple-vs-dataclass-mutability-memory]]
6. [[post-init-when-called]]
7. [[slots-tradeoff-dynamic-attrs]]
%% trellis:end %%

## Notes
