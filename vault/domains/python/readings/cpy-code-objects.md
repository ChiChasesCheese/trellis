---
nodes:
- runtime.compile-bytecode
- runtime.exceptions
title: 代码对象：字节码之外还带着什么
corpus: cpython-internals
section: 005-code-objects
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# 代码对象：字节码之外还带着什么

`CodeObject` 是编译器产出的成品：除了字节码本身，还携带常量表、变量名表、以及一张压缩过的“源码位置表”（`co_linetable`），记录每条指令对应源码里的起止行号和列号。代码对象名义上不可变，会被 `marshal` 协议序列化写到磁盘（也就是 `__pycache__` 里 `.pyc` 文件的真身），下次导入时直接反序列化跳过重新编译。读这篇的价值有两点：一是理解“字节码缓存”到底缓存的是什么对象、为什么改了源码时间戳/哈希就要重新编译；二是理解异常发生时 traceback 上的行号是怎么来的——`tb_lasti`（最后执行的指令位置）配合位置表被懒惰地换算成行号，而不是解释器执行时时刻都在维护一个行号变量。知道位置表存在，能解释为什么 3.11 之后的报错能精确定位到表达式内的某个子部分而不只是整行。
