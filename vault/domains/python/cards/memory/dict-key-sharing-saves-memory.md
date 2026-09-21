---
id: dict-key-sharing-saves-memory
node: memory.object-size
type: qa
source: cpython-internals
---
## Q
同一个类批量创建大量实例时，为什么这些实例各自的 `__dict__` 总内存占用，会比「每个实例都各自持有一份完整 key-value 哈希表」小得多？

## A
CPython 的 dict 支持「分裂表」（split table）：一个只存 key 和其 hash 值的 dict-keys 对象，可以被同一个类的所有实例的 `__dict__` 共享；每个实例自己只需要保留一份很小的 values 数组，按位置对应到共享的 key 表上取值。这样同一个类的全部实例共用一份 key 表，官方 dict 实现笔记里给出的估计是能省约 60% 的内存。
