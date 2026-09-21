%% trellis:begin %%
# 属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`
*类、协议与元编程*

理解 `obj.x` 的查找顺序（数据描述符→实例 `__dict__`→类→非数据描述符→`__getattr__`），`__getattribute__` 拦截一切的风险，以及惰性属性的实现方式。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]

**Unlocks:** [[domains/python/map/classes.properties-descriptors|`property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）]]

## Readings
- [[effective-08-metaclasses-attributes|Effective Python 3e · 第 8 章 元类与属性]]
- [[fluent-22-dynamic-attributes-properties|Fluent Python 2e · 第 22 章 动态属性与特性]]
- [[pydocs-descriptor-guide|描述符指南（Descriptor Guide）]]
- [[pydocs-tutorial-classes|Python 教程第 9 章：类]]

## Cards (6)
1. [[attr-lookup-precedence-chain]]
2. [[class-lookup-uses-mro-not-instance-dict]]
3. [[getattr-invoked-by-dot-not-getattribute]]
4. [[getattr-vs-getattribute-trigger]]
5. [[lazy-attribute-via-getattr]]
6. [[override-getattribute-recursion-risk]]
%% trellis:end %%

## Notes
