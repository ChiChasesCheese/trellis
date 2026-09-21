%% trellis:begin %%
# Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`
*类、协议与元编程*

掌握一个类应实现的基本协议、`@classmethod` 作为备选构造器、`@staticmethod` 的定位，以及为什么 `__repr__` 应该能重建对象。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]]

**Unlocks:** [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]], [[domains/python/map/classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]], [[domains/python/map/classes.abc-protocols|鸭子类型、抽象基类（ABC）与 `typing.Protocol`]], [[domains/python/map/classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]]

## Readings
- [[effective-07-classes-interfaces|Effective Python 3e · 第 7 章 类与接口]]
- [[fluent-01-data-model|Fluent Python 2e · 第 1 章 Python 数据模型]]
- [[fluent-11-pythonic-object|Fluent Python 2e · 第 11 章 符合 Python 风格的对象]]
- [[pydocs-descriptor-guide|描述符指南（Descriptor Guide）]]
- [[pydocs-tutorial-classes|Python 教程第 9 章：类]]

## Drills
- [[classes-design-a-money-value-object|Drill：写一个不可变 `Money` 值对象，再用描述符复用校验]]

## Cards (6)
1. [[classmethod-alternate-constructor]]
2. [[classmethod-vs-staticmethod-binding]]
3. [[eq-default-identity-and-hash]]
4. [[eq-notimplemented-fallback]]
5. [[hash-truncation-width]]
6. [[repr-reconstructs-object]]
%% trellis:end %%

## Notes
