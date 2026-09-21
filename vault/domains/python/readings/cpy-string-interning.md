---
nodes:
- memory.interning-immortal
- model.names-objects
title: 字符串驻留与不朽对象：is 比较为什么能又快又准
corpus: cpython-internals
section: 013-string-interning
url: https://github.com/python/cpython/blob/main/InternalDocs/string_interning.md
tags:
- canonical
---

# 字符串驻留与不朽对象：is 比较为什么能又快又准

驻留（interning）的本质是维护一个“同内容只留一份”的字符串集合，好处是驻留过的字符串可以直接用指针比较（`is`）代替逐字符比较，被大量用在 dict/属性查找的快速路径上。CPython 用两套机制：一是单字符 latin-1 字符串和编译期已知的标识符（`_Py_ID`/`_Py_STR`）在运行时启动阶段就被静态驻留进全局表；二是普通字符串在运行时按需驻留进一个解释器级别的 dict。驻留过的字符串还分“会死”和“不朽”（immortal）：3.12 引入的不朽对象机制让 `None`/`True`/小整数以及这类常驻字符串不再参与引用计数的加减——省掉了多核下对同一块内存反复写引用计数带来的缓存行竞争，也对 `fork` 后的写时复制更友好，因为不朽对象永远不会因为引用计数变化而被“写”。读完能把“小整数/短字符串驻留只是实现细节”这句话背后的具体机制和它为什么对多核有意义讲清楚。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/string_interning.md)

## Archived copy
![[cpy-string-interning-clip]]
%% trellis:end %%
