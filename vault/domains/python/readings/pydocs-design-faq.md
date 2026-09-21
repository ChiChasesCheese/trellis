---
nodes:
- model.numbers
- memory.allocator
- memory.refcounting
- memory.cyclic-gc
- model.dict-set-internals
- memory.object-size
title: 设计与历史 FAQ：CPython 内部实现精选问答
corpus: python-docs
section: 20-design
url: https://docs.python.org/3/faq/design.html
tags:
- canonical
---

# 设计与历史 FAQ：CPython 内部实现精选问答

这篇 FAQ 用一问一答的形式回答了大量为什么 Python 是这样设计的，其中几组问答直接对应 CPython 实现细节：内存管理用的是引用计数为主、可选循环检测为辅的混合方案，而不是传统标记清除或分代 GC，因为大多数对象生命周期短、引用归零就能立刻确定性释放，不需要等一整轮扫描；CPython 退出时不一定释放所有内存，因为清理顺序和 C 扩展持有的资源不受保证；列表底层会过量分配（over-allocate）以摊薷 append 的成本，这也是为什么 list 和 tuple 要分成两种类型（一个为追加优化，一个为不可变值优化）；字典底层是哈希表，要求键的哈希值在生命周期内不变，这正是字典键必须不可变（或可哈希）的根本原因。这些问答比读源码省时间得多，是面试被追问 CPython 底层怎么实现时最省力的复习材料。
