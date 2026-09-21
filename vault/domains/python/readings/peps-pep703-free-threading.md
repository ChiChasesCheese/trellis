---
nodes:
- concurrency.free-threading
title: PEP 703：让 GIL 可选（Making the GIL Optional）
corpus: peps
section: 01-pep-0703
url: https://peps.python.org/pep-0703/
tags:
- canonical
---

# PEP 703：让 GIL 可选（Making the GIL Optional）

这是 free-threading 构建（--disable-gil）的原始设计文档。面试常追问“为什么不干脆用读写锁保护 dict/list”——PEP 给出明确答案：读写锁在小临界区上扩展性差，改用类似 RCU 的乐观无锁访问加延迟回收（mimalloc 分页粒度）。要带走三点：一是用有偏引用计数（biased reference counting）替代朴素原子计数，配合 immortalization 和 deferred refcounting 减少多核缓存失效；二是为什么弃用分代 GC 只保留老年代——分代链表在无 GIL 下难以做到线程安全，且 CPython 因引用计数已提前回收大部分“年轻”对象，分代假设不像 Java 那样成立；三是动机部分的真实案例（PyTorch、DeepMind、scikit-learn/joblib）说明为何多线程在 GIL 下不可扩展、多进程又受 IPC/pickle 成本所限。读完能回答“GIL 保护的到底是什么、去掉它要动哪些子系统”。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0703/)

## Archived copy
![[peps-pep703-free-threading-clip]]
%% trellis:end %%
