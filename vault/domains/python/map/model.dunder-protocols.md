%% trellis:begin %%
# 特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`
*对象模型：名字、对象与数据模型（data model）*

理解解释器如何通过特殊方法实现 `len()`、`for`、`in`、`+`、调用等语法，`__repr__` 与 `__str__` 的分工，以及为什么应实现协议而不是继承内建类型。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.names-objects|名字绑定、对象身份与 `is` vs `==`]]

**Unlocks:** [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]], [[domains/python/map/iteration.iterator-protocol|可迭代对象与迭代器：`__iter__`、`__next__`、`StopIteration`]], [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[domains/python/map/classes.operator-overloading|运算符重载：`__add__`/`__radd__`、就地运算符与比较运算]]

## Readings
- [[fluent-01-data-model|Fluent Python 2e · 第 1 章 Python 数据模型]]
- [[fluent-12-special-methods-sequences|Fluent Python 2e · 第 12 章 序列的特殊方法]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]

## Cards (6)
1. [[call-protocol-no-base-class-needed]]
2. [[dunder-protocol-vs-inherit-builtin]]
3. [[getitem-sequence-vs-mapping-and-slice]]
4. [[len-bool-fallback-and-maxsize]]
5. [[missing-contains-degrades-to-linear-scan]]
6. [[repr-str-division-of-labor]]
%% trellis:end %%

## Notes
