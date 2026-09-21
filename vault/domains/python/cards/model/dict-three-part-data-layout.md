---
id: dict-three-part-data-layout
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
一个 CPython dict 对象在内存里由哪三个部分组成？

## A
由三部分组成：dict 对象本身的结构体（dictobject struct，保存元数据并指向另外两部分）；一个 dict-keys 对象（保存所有键和它们的哈希值）；以及一个单独的 values 数组（按相同顺序保存每个键对应的值）。把键和值拆成两个独立结构，是支持拆分表（split table）在多个字典间共享 key-table 的前提。
