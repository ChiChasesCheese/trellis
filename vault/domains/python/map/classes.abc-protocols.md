%% trellis:begin %%
# 鸭子类型、抽象基类（ABC）与 `typing.Protocol`
*类、协议与元编程*

理解鸭子类型靠行为而非继承、`collections.abc` 的虚拟子类与 `register`、`@abstractmethod` 阻止实例化，以及 Protocol 提供的结构化子类型（structural subtyping）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]

**Unlocks:** [[domains/python/map/types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]]

## Readings
- [[effective-07-classes-interfaces|Effective Python 3e · 第 7 章 类与接口]]
- [[fluent-13-interfaces-protocols-abc|Fluent Python 2e · 第 13 章 接口、协议与抽象基类]]
- [[peps-pep3119-abstract-base-classes|PEP 3119：引入抽象基类（ABC）]]
- [[peps-pep544-protocols|PEP 544：Protocol 与结构化子类型]]
- [[pydocs-abc-module|abc 模块：抽象基类机制]]
- [[pydocs-collections-abc|collections.abc：容器的抽象基类]]

## Cards (7)
1. [[abc-mixin-minimal-methods]]
2. [[abc-three-ways-to-satisfy-issubclass]]
3. [[abstractmethod-blocks-instantiation]]
4. [[abstractmethod-doesnt-affect-virtual-subclass]]
5. [[protocol-structural-vs-nominal-subtyping]]
6. [[runtime-checkable-only-checks-presence]]
7. [[subclasshook-customizes-issubclass]]
%% trellis:end %%

## Notes
