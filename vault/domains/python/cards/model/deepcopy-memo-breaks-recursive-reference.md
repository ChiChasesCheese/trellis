---
id: deepcopy-memo-breaks-recursive-reference
node: model.copy
type: qa
source: python-docs
---
## Q
`copy.deepcopy()` 在递归复制对象时，如何避免因为循环引用（对象直接或间接引用自身）而陷入无限递归？

## A
`deepcopy()` 在一次拷贝过程中维护一个 `memo` 字典，用已复制对象的 id 作为键，记录它对应的副本；再次遇到同一个对象时直接从 `memo` 取出已经建好的副本，而不是重新递归复制，从而打断了循环引用导致的无限递归。
