---
nodes:
- memory.weakref
title: weakref 模块：弱引用
corpus: python-docs
section: 40-weakref
url: https://docs.python.org/3/library/weakref.html
tags:
- canonical
---

# weakref 模块：弱引用

weakref 让你持有一个对象的引用而不增加它的引用计数，也就不会阻止这个对象被垃圾回收，这在实现缓存或观察者列表时特别关键：如果缓存本身持有强引用，被缓存的对象永远不会被回收，等于造成了逻辑上的内存泄漏。文档讲了 weakref.ref() 创建弱引用对象、调用它拿到目标对象（如果已被回收则返回 None）；WeakValueDictionary/WeakKeyDictionary 是最常用的场景化封装，字典里的键或值一旦在别处不再被强引用就会自动从字典中消失。weakref.finalize 提供了比 __del__ 更可靠的清理钩子注册方式，不依赖类本身定义析构方法，也能正确处理循环引用中的清理。这是写不阻止对象被回收的缓存或对象生命周期观察器时的标准工具，比自己维护引用计数逻辑安全得多。
