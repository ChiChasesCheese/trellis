---
nodes: [model.dict-set-internals, model.names-objects, memory.interning-immortal]
url: https://realpython.com/products/cpython-internals-book/
tags: [book, no-archive]
title: CPython Internals · 对象与类型
---
# CPython Internals · 对象与类型

这一部分讲 CPython 里『一切皆对象』具体是怎么实现的：每个对象头部都带类型指针和引用计数，`type` 对象定义了实例的行为；也讲了小整数、短字符串这类『驻留'（interning）对象如何被缓存复用以省内存。

**读时提取：**
- 每个 Python 对象的 C 结构体头部都带哪两样东西（类型指针、引用计数）
- 小整数缓存池和字符串驻留如何让相同的字面量复用同一个对象
- 字典的键值分离存储如何让同一个类的实例共享一张键表省内存

%% trellis:begin %%
## Source
[Open the original ↗](https://realpython.com/products/cpython-internals-book/)
%% trellis:end %%
