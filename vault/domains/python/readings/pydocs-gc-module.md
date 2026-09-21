---
nodes:
- memory.cyclic-gc
title: gc 模块：垃圾回收器接口
corpus: python-docs
section: 39-gc
url: https://docs.python.org/3/library/gc.html
tags:
- canonical
---

# gc 模块：垃圾回收器接口

gc 模块是操作 CPython 循环垃圾回收器的接口，补充引用计数处理不了的循环引用场景。核心 API：gc.disable() 可以完全关掉自动回收（如果确信代码不产生循环引用，能省下扫描开销）；gc.collect(generation) 手动触发指定代（0/1/2）的回收，不传参数则做一次全量回收；gc.set_debug(gc.DEBUG_LEAK) 能让回收不掉的对象保留在 gc.garbage 里供检查，是定位为什么内存一直涨的常用手段。这个模块和分代假设（大多数对象活得很短，所以新对象所在的第 0 代扫描最频繁）直接对应，是理解 CPython 内存管理策略之后能立刻上手排查内存问题的实操工具，比单纯读理论文章更有用。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/gc.html)

## Archived copy
![[pydocs-gc-module-clip]]
%% trellis:end %%
