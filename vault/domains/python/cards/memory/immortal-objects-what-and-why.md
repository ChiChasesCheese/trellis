---
id: immortal-objects-what-and-why
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
PEP 683（Python 3.12）里的「不朽对象」（immortal objects）具体做了什么？它要解决的根本问题是什么？

## A
把对象的引用计数（reference count）固定设为一个特殊的巨大值，CPython 的 C API 和运行时此后都不再修改这个值（`Py_INCREF`/`Py_DECREF` 对它是空操作），只有解释器整体关闭时才真正释放。要解决的问题是：像 `None`、`True`、小整数这类「值上看起来不可变」的对象，此前每次被引用或丢弃都要改写它头部的引用计数，这个「运行时可变状态」让它们其实并不是真正意义上的不可变对象。
