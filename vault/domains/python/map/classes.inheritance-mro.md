%% trellis:begin %%
# 继承、多重继承、MRO（C3 线性化）与 `super()`
*类、协议与元编程*

掌握方法解析顺序如何由 C3 算法决定、`super()` 调用的是 MRO 中的下一个而非父类、mixin 的设计约束，以及为何 Fluent Python 建议优先组合。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]

**Unlocks:** [[domains/python/map/classes.metaprogramming|类装饰器、`__init_subclass__` 与元类（metaclass）]]

## Readings
- [[effective-07-classes-interfaces|Effective Python 3e · 第 7 章 类与接口]]
- [[fluent-14-inheritance|Fluent Python 2e · 第 14 章 继承：为了更好或更坏]]
- [[pydocs-mro-c3|方法解析顺序（MRO）：C3 算法]]
- [[pydocs-tutorial-classes|Python 教程第 9 章：类]]

## Drills
- [[classes-design-a-money-value-object|Drill：写一个不可变 `Money` 值对象，再用描述符复用校验]]

## Cards (6)
1. [[c3-linearization-formula]]
2. [[duplicate-base-class-error]]
3. [[local-precedence-ordering-design-rule]]
4. [[mro-conflict-raises-typeerror]]
5. [[mro-monotonicity-property]]
6. [[super-dispatches-to-mro-next-not-parent]]
%% trellis:end %%

## Notes
