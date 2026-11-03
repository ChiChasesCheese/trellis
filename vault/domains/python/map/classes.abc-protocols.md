%% trellis:begin %%
# 鸭子类型、抽象基类（ABC）与 `typing.Protocol`
*类、协议与元编程*

理解鸭子类型靠行为而非继承、`collections.abc` 的虚拟子类与 `register`、`@abstractmethod` 阻止实例化，以及 Protocol 提供的结构化子类型（structural subtyping）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]]

**Unlocks:** [[domains/python/map/types.protocols-generics|`Protocol`、`TypeVar`、`ParamSpec` 与泛型类]], [[domains/python/map/craft.patterns.policy-seam|策略接缝：把会变的规则做成注入的纯函数/对象]], [[domains/python/map/craft.patterns.predicate-algebra-three-valued|谓词代数与三值逻辑：可组合的小对象 + NULL 传播]], [[domains/python/map/craft.idioms.protocol-callable-abc|策略接口三选一：Callable / Protocol / ABC]], [[domains/python/map/craft.architecture.dependency-direction-consumer-owns-interface|依赖方向：接口由使用方定义，核心不依赖基础设施]], [[domains/python/map/craft.architecture.interface-only-when-earned|接口是挣来的：什么时候不抽象]], [[domains/python/map/craft.architecture.composition-of-independent-axes|独立变化轴的组合：N×M 个组合只写 N+M 个小类]]

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
