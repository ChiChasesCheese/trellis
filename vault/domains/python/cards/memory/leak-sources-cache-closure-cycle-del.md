---
id: leak-sources-cache-closure-cycle-del
node: memory.leaks-tracemalloc
type: cloze
source: python-docs
---
长驻 Python 进程常见的内存泄漏来源包括：{{c1::没有上限或没有过期策略的全局缓存（含 `lru_cache` 装饰的函数缓存）}}、{{c2::闭包或回调一直持有对大对象的引用不释放}}、{{c3::循环引用（reference cycle）让引用计数永不归零，只能等循环垃圾回收器（cyclic GC）按阈值触发才释放（3.4 起带 `__del__` 的循环也能回收，只有旧式 C 终结器会进 `gc.garbage`）}}，以及 C 扩展自己管理、Python 侧看不见的内存。
