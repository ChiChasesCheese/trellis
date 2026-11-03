%% trellis:begin %%
# `dataclass`、`NamedTuple` 与 `__slots__`
*类、协议与元编程*

比较三种数据类构建器的可变性、内存与哈希语义，`frozen=True`、`field(default_factory=)`、`__post_init__` 校验，以及 `__slots__` 省内存并禁止动态属性的代价。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/classes.pythonic-object|Pythonic 对象：`__init__`、`__repr__`、`__eq__`、`classmethod` vs `staticmethod`]], [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]]

**Unlocks:** [[domains/python/map/craft.patterns.notify-outside-the-lock|锁内记事件、锁外派发（collect under lock, dispatch outside）]], [[domains/python/map/craft.patterns.append-only-log-derived-state|只追加日志 + 派生状态：事实不可变，余额/视图可重算（event-sourced state）]], [[domains/python/map/craft.patterns.immutable-snapshot-publish|不可变快照 + 整体替换发布（copy-on-write publish）]], [[domains/python/map/craft.patterns.recursive-descent-parsing|递归下降解析：优先级 = 调用层次，分词与求值分离]], [[domains/python/map/craft.patterns.make-unmake-undo-log|可逆变更：make/unmake、撤销日志、Edit.invert]], [[domains/python/map/craft.idioms.frozen-value-objects|不可变值对象（frozen + slots dataclass as value object）]], [[domains/python/map/craft.idioms.validated-construction|构造即校验与规范化（__post_init__ + object.__setattr__）]], [[domains/python/map/craft.idioms.read-only-views-and-snapshots|只读视图与快照返回（MappingProxyType / tuple / frozenset）]], [[domains/python/map/craft.idioms.heapq-tuple-ordering|heapq 的元组序与 tie-break：计数器、负号、dataclass(order=True)]], [[domains/python/map/craft.idioms.match-structural|结构化模式匹配：对 dataclass 与枚举的 match / case]], [[domains/python/map/craft.idioms.replace-for-state-change|用 dataclasses.replace 整体替换，而不是原地改（immutable record swap）]], [[domains/python/map/craft.idioms.kw-only-positional-only|参数形态：仅位置 `/`、仅关键字 `*`、kw_only dataclass]], [[domains/python/map/craft.idioms.slots-and-memory|__slots__ 与 slots=True：该用在哪、不能用在哪]], [[domains/python/map/craft.idioms.namedtuple-for-keys|NamedTuple 做复合键与轻量返回值]], [[domains/python/map/craft.architecture.entity-vs-value-object|实体 vs 值对象：身份、可变性与谁拥有状态]], [[domains/python/map/craft.architecture.command-event-fact|命令、事件与事实：过去式、自带全部信息、不可变]], [[domains/python/map/craft.architecture.extension-points-worth-paying-for|扩展点值得付费的地方：数据代替代码、从第一天就预留的字段]], [[domains/python/map/craft.architecture.unit-of-inventory-modeling|库存的单位怎么选：房型夜、车的行程段、场次座位、航班实例]]

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
