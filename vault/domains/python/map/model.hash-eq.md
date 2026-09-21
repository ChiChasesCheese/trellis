%% trellis:begin %%
# `__hash__` 与 `__eq__` 的契约
*对象模型：名字、对象与数据模型（data model）*

掌握相等的对象必须有相同哈希、定义 `__eq__` 会让 `__hash__` 变 None、可哈希对象为何必须不可变，以及自定义类做字典键时的常见错误。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.dunder-protocols|特殊方法与语言协议：`__repr__`、`__len__`、`__getitem__`、`__call__`]]

**Unlocks:** [[domains/python/map/model.dict-set-internals|dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Readings
- [[fluent-03-dict-set|Fluent Python 2e · 第 3 章 字典与集合]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]

## Drills
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[hash-eq-contract-basic]]
2. [[hash-truncated-to-py-ssize-t]]
3. [[inherit-hash-explicit-assignment]]
4. [[mutable-eq-should-not-define-hash]]
5. [[override-eq-implicit-hash-none]]
6. [[str-bytes-hash-salted-random]]
%% trellis:end %%

## Notes
