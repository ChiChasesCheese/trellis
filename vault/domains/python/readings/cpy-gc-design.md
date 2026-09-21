---
nodes:
- memory.cyclic-gc
- memory.refcounting
title: 循环垃圾回收器：分代、可达性扫描与销毁顺序
corpus: cpython-internals
section: 010-garbage-collector-design
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# 循环垃圾回收器：分代、可达性扫描与销毁顺序

引用计数处理不了自引用的环（比如一个列表把自己装进自己），CPython 用单独的 `gc` 模块专门找这些环。算法思路是：先给每个容器对象记一份“临时引用计数”副本，扫描一遍把所有指向集合内部的引用都减掉，剩下计数大于 0 的就是能从外部直接到达的对象，再从这些对象出发做一次广度优先搜索把可达对象都捞回来，剩下的就真的不可达了。为了不用每次都扫全堆，对象按存活轮数分成 3 代（`gc.get_threshold()` 能看到触发阈值），新对象在第 0 代，扛过几轮回收才晋升。销毁顺序也有讲究：先处理弱引用回调，再调用 `__del__`/`tp_finalize`，如果对象在 finalizer 里“复活”还要重新跑一遍可达性分析。读完能把“循环引用为什么需要 GC”“分代假设”“weakref 回调什么时候执行”这几件事串成一条因果链，而不是零散的结论。
