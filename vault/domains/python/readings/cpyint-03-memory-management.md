---
nodes: [memory.refcounting, memory.cyclic-gc, memory.allocator, memory.object-size]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 内存管理
---
# CPython Internals · 内存管理

这一部分讲 CPython 两层内存回收机制：引用计数负责大多数对象『归零即释放』，分代垃圾回收器专门处理引用计数处理不了的循环引用；也讲了 pymalloc 这个专门针对小对象的内存池分配器如何减少频繁 malloc/free 的系统调用开销。

**读时提取：**
- 引用计数归零立即释放，和分代 GC 定期扫描分别解决什么问题
- 循环引用为什么引用计数处理不了，必须靠可达性分析的分代 GC 清理
- pymalloc 分配器如何为小对象维护内存池，减少直接系统调用

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
