---
nodes:
- model.dict-set-internals
- memory.object-size
title: dict 的键值分离设计：为什么同一个类的实例能共享一张键表
corpus: cpython-internals
section: 016-dict-implementation-notes
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# dict 的键值分离设计：为什么同一个类的实例能共享一张键表

这份笔记讲的是紧凑 dict（3.6+）背后的取舍：dict 由 dictobject 本体、一份 keys 对象（键+哈希）、一份 values 数组三部分组成，拆开后同一个类的所有实例可以共享同一张键表（split table），只各自保留自己的 values 数组，官方估算能省下约 60% 的内存——这正是“百万级对象为什么该考虑 `__slots__`”这类问题的另一面：普通实例字典其实已经在用共享键表省内存，`__slots__` 是进一步连字典都不要了。笔记也讲了调节稀疏度的参数（`USABLE_FRACTION`、`GROWTH_RATE`）如何在“减少哈希冲突”和“遍历/清空的固定开销”之间权衡，以及为什么尝试利用 CPU 缓存局部性去顺带探测相邻槽位反而会增加冲突、没有被采用。读完能把“字典哈希表怎么定位槽位、为什么装载因子触发扩容”这些结论和“键共享省内存”这个常被面试问到的优化点连起来。
