%% trellis:begin %%
# 循环垃圾回收：分代（generations）、阈值与增量回收
*内存管理与垃圾回收*

掌握 `gc` 模块如何追踪容器对象、通过"试减引用"找出不可达环、分代假设与触发阈值，3.12+ 增量回收的变化，以及 `__del__` 与弱引用在环中的处理。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

**Unlocks:** [[domains/python/map/memory.leaks-tracemalloc|长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`]]

## Readings
- [[cpy-gc-design|循环垃圾回收器：分代、可达性扫描与销毁顺序]]
- [[cpyint-03-memory-management|CPython Internals · 内存管理]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]
- [[pydocs-gc-module|gc 模块：垃圾回收器接口]]

## Drills
- [[memory-debug-the-growing-worker|Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位]]

## Cards (5)
1. [[gc-destroy-order-weakref-del]]
2. [[gc-full-collection-cost]]
3. [[gc-generations-thresholds]]
4. [[gc-only-tracks-containers]]
5. [[gc-trial-subtraction]]
%% trellis:end %%

## Notes
