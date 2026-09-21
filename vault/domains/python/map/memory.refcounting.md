%% trellis:begin %%
# 引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`
*内存管理与垃圾回收*

理解每个对象头部的引用计数如何随赋值/作用域退出增减、归零即释放的确定性，以及引用计数无法处理循环引用的原因。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/model.names-objects|名字绑定、对象身份与 `is` vs `==`]]

**Unlocks:** [[domains/python/map/memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]], [[domains/python/map/memory.allocator|pymalloc：arena / pool / block 与为何内存不还给操作系统]], [[domains/python/map/memory.interning-immortal|驻留（interning）与不朽对象（immortal objects，PEP 683）]], [[domains/python/map/memory.weakref|弱引用：`weakref`、`WeakValueDictionary` 与缓存]], [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

## Readings
- [[cpy-gc-design|循环垃圾回收器：分代、可达性扫描与销毁顺序]]
- [[cpyint-03-memory-management|CPython Internals · 内存管理]]
- [[fluent-06-references-mutability|Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收]]
- [[py-pydocs-data-model|数据模型（Data Model）参考]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]

## Drills
- [[memory-debug-the-growing-worker|Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位]]

## Cards (5)
1. [[free-threading-split-refcount]]
2. [[getrefcount-plus-one]]
3. [[refcount-cannot-clear-self-cycle]]
4. [[refcount-deterministic-vs-gc]]
5. [[refcount-inc-dec-triggers]]
%% trellis:end %%

## Notes
