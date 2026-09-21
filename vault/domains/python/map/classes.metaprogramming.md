%% trellis:begin %%
# 类装饰器、`__init_subclass__` 与元类（metaclass）
*类、协议与元编程*

理解类本身是 `type` 的实例、类体执行完后由元类创建类对象、`__init_subclass__` 与类装饰器在多数场景下足以替代元类，以及元类的典型用途（注册、校验、ORM）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.inheritance-mro|继承、多重继承、MRO（C3 线性化）与 `super()`]]

## Readings
- [[effective-08-metaclasses-attributes|Effective Python 3e · 第 8 章 元类与属性]]
- [[fluent-24-class-metaprogramming|Fluent Python 2e · 第 24 章 类元编程]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]

## Cards (6)
1. [[class-creation-order-setname-then-initsubclass]]
2. [[init-subclass-implicit-classmethod-kwargs]]
3. [[init-subclass-vs-class-decorator-scope]]
4. [[metaclass-typical-uses]]
5. [[most-derived-metaclass-selection]]
6. [[zero-arg-super-needs-classcell]]
%% trellis:end %%

## Notes
