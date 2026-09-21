---
nodes:
- concurrency.free-threading
title: 自由线程构建里，读操作为什么能不加锁
corpus: cpython-internals
section: 012-quiescent-state-based-reclamation
url: https://github.com/python/cpython/blob/main/InternalDocs/qsbr.md
tags:
- canonical
---

# 自由线程构建里，读操作为什么能不加锁

去掉 GIL 之后有一个新麻烦：多个线程可能正在无锁地读一个 dict/list 的内部数组，这时候另一个线程把它 resize 了、旧数组该什么时候真正释放？释放早了会踩上正在读它的线程，释放晚了内存又降不下来。CPython 的自由线程（free-threaded）构建用了一种叫 QSBR（Quiescent-State Based Reclamation）的方案：每个线程定期在“安全点”（eval breaker 处）汇报一次“我现在没有持有任何可能被回收的共享引用”，全局维护一个所有线程都已经越过的“最小安全序号”，只有序号早于这个值的待释放对象才会被真正 free。读这篇不需要记实现细节，只要建立一个认识：`--disable-gil` 构建能让读操作不加锁，不是没有代价，而是把代价换成了一套后台的、批量化的内存延迟回收机制，这也是回答“free-threading 的成熟度/工程复杂度”这类问题时更有说服力的素材。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/qsbr.md)

## Archived copy
![[cpy-qsbr-reclaim-clip]]
%% trellis:end %%
