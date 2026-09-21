%% trellis:begin %%
# 弱引用：`weakref`、`WeakValueDictionary` 与缓存
*内存管理与垃圾回收*

掌握弱引用不增加引用计数、对象被回收后弱引用失效，以及用弱引用字典实现不阻止回收的缓存与观察者列表。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

## Readings
- [[fluent-06-references-mutability|Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收]]
- [[pydocs-weakref-module|weakref 模块：弱引用]]

## Cards (5)
1. [[not-all-types-support-weakref]]
2. [[slots-disables-weakref-by-default]]
3. [[weakref-does-not-keep-alive]]
4. [[weakref-proxy-vs-ref-failure-mode]]
5. [[weakvaluedict-cache-vs-plain-dict]]
%% trellis:end %%

## Notes
