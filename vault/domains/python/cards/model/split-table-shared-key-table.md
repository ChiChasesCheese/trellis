---
id: split-table-shared-key-table
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
CPython 的 dict 为什么能让同一个类的所有实例共享同一份键表（key-table）？这样做大约省了多少内存？

## A
CPython 把 dict 的哈希表拆成两部分：一份存键（key）和对应哈希值的 key-table，另一份是单独的 values 数组，这种结构称为拆分表（split table）。当多个字典的键集合完全相同时（最典型的场景是同一个类的多个实例各自的 `__dict__`），它们可以共享同一份 key-table，各自只保留自己的 values 数组；这种共享让这类字典整体节省了约 60% 的内存。
