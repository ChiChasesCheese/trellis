---
id: dict-resize-only-on-growth-path
node: model.dict-set-internals
type: qa
source: cpython-internals
---
## Q
CPython 的 dict 什么时候才会检查是否需要扩容（resize）？用 `.pop()` 反复清空一个字典的过程会触发扩容吗？

## A
dict 只在可能「增长」的操作（插入新键）路径上才检查是否需要扩容，纯删除操作不做这个检查。这样设计让只涉及单个键的操作在不触发扩容检查的前提下保持 O(1)，也避免了「扩容抖动」（反复扩容又收缩浪费性能）——例如用 `.pop()` 循环清空一个字典，整个过程都不会检查扩容，因为字典只会变小，从不需要更大的表。
