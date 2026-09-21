%% trellis:begin %%
# `property` 与描述符协议（`__get__`/`__set__`/`__set_name__`）
*类、协议与元编程*

掌握 property 是描述符的特例、数据描述符与非数据描述符的优先级差异、用描述符复用校验逻辑，以及 `__set_name__` 如何拿到属性名。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.attribute-lookup|属性查找：实例字典、类字典、`__getattr__` 与 `__getattribute__`]]

## Readings
- [[effective-08-metaclasses-attributes|Effective Python 3e · 第 8 章 元类与属性]]
- [[fluent-22-dynamic-attributes-properties|Fluent Python 2e · 第 22 章 动态属性与特性]]
- [[fluent-23-attribute-descriptors|Fluent Python 2e · 第 23 章 属性描述符]]
- [[pydocs-descriptor-guide|描述符指南（Descriptor Guide）]]

## Drills
- [[classes-design-a-money-value-object|Drill：写一个不可变 `Money` 值对象，再用描述符复用校验]]

## Cards (6)
1. [[data-vs-nondata-descriptor-priority]]
2. [[descriptor-reuse-validation-across-attrs]]
3. [[functions-are-nondata-descriptors]]
4. [[orm-descriptor-indirection]]
5. [[property-is-data-descriptor]]
6. [[set-name-when-called]]
%% trellis:end %%

## Notes
