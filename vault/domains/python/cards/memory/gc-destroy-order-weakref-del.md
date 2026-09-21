---
id: gc-destroy-order-weakref-del
node: memory.cyclic-gc
type: qa
source: cpython-internals
---
## Q
循环 GC 确认一批对象不可达之后，销毁它们的顺序是什么？`__del__`（旧式终结器）和弱引用（weak reference）分别在哪一步被处理？

## A
顺序是：①处理带回调的弱引用（只有弱引用对象本身可达时才会调用其回调，两边都不可达则跳过回调）；②若对象有旧式终结器（legacy `tp_del`）就把它挪进 `gc.garbage` 列表，不再自动回收；③调用新式终结器（`tp_finalize`，即 `__del__`）并标记已终结，避免对象被复活（resurrect）后重复调用；④若有对象在终结过程中被复活，重新跑一遍不可达检测；⑤清空所有还指向不可达对象的弱引用（置为 `None`）；⑥最后调用每个对象的 `tp_clear` 断开内部引用，引用计数（reference count）归零，对象真正被释放。
