%% trellis:begin %%
# pymalloc：arena / pool / block 与为何内存不还给操作系统
*内存管理与垃圾回收*

理解小对象（≤512 字节）走 pymalloc 的三层分配器、大对象走系统 malloc、arena 只有全空才释放导致 RSS 居高不下，以及碎片化的影响。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]

**Unlocks:** [[domains/python/map/memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]]

## Readings
- [[cpyint-03-memory-management|CPython Internals · 内存管理]]
- [[hpp-11-using-less-ram|High Performance Python 2e · 第 11 章 减少内存占用]]
- [[pydocs-design-faq|设计与历史 FAQ：CPython 内部实现精选问答]]

## Drills
- [[memory-debug-the-growing-worker|Drill：长驻 worker 的 RSS 每小时涨 200 MB，怎么定位]]

## Cards (5)
1. [[pymalloc-arena-not-freed]]
2. [[pymalloc-fragmentation-mitigation]]
3. [[pymalloc-size-threshold]]
4. [[pymalloc-three-tiers]]
5. [[pymalloc-vs-raw-malloc]]
%% trellis:end %%

## Notes
