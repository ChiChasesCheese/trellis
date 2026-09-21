%% trellis:begin %%
# 内存管理与垃圾回收

CPython 如何分配与回收对象：引用计数即时释放、分代式循环垃圾回收、pymalloc 的 arena/pool/block 分层，以及长驻进程中内存增长的来源与诊断。

## Topics
- [[domains/python/map/memory.refcounting|引用计数：`ob_refcnt`、即时释放与 `sys.getrefcount`]]
- [[domains/python/map/memory.cyclic-gc|循环垃圾回收：分代（generations）、阈值与增量回收]]
- [[domains/python/map/memory.allocator|pymalloc：arena / pool / block 与为何内存不还给操作系统]]
- [[domains/python/map/memory.object-size|对象的真实大小：`sys.getsizeof`、`__slots__`、int/str/list 的开销]]
- [[domains/python/map/memory.leaks-tracemalloc|长驻进程的内存泄漏：来源、`tracemalloc` 与 `gc.get_referrers`]]
- [[domains/python/map/memory.interning-immortal|驻留（interning）与不朽对象（immortal objects，PEP 683）]]
- [[domains/python/map/memory.weakref|弱引用：`weakref`、`WeakValueDictionary` 与缓存]]
%% trellis:end %%

## Notes
