%% trellis:begin %%
# dict 与 set 的实现：哈希表、开放寻址、紧凑布局与插入序
*对象模型：名字、对象与数据模型（data model）*

理解哈希表如何用哈希值定位槽位并处理冲突（开放寻址、扰动探测）、3.6+ 紧凑 dict 为何保序、装载因子触发扩容，以及平均 O(1) 与最坏 O(n) 的来源。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.hash-eq|`__hash__` 与 `__eq__` 的契约]]

**Unlocks:** [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]]

## Readings
- [[cpy-dict-notes|dict 的键值分离设计：为什么同一个类的实例能共享一张键表]]
- [[cpyint-05-objects-types|CPython Internals · 对象与类型]]
- [[effective-04-dictionaries|Effective Python 3e · 第 4 章 字典]]
- [[fluent-03-dict-set|Fluent Python 2e · 第 3 章 字典与集合]]
- [[hpp-04-dicts-sets|High Performance Python 2e · 第 4 章 字典与集合]]
- [[pydocs-builtin-types|内建类型（Built-in Types）完整参考]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]

## Drills
- [[model-predict-identity-and-aliasing|Drill：六段代码，逐段预测输出并解释机制]]

## Cards (6)
1. [[collision-probing-rejects-cache-locality]]
2. [[dict-resize-only-on-growth-path]]
3. [[dict-three-part-data-layout]]
4. [[sparser-hashtable-hurts-iteration]]
5. [[split-table-key-null-vs-dummy-null]]
6. [[split-table-shared-key-table]]
%% trellis:end %%

## Notes
