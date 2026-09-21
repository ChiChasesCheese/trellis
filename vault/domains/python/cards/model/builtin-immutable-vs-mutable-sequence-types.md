---
id: builtin-immutable-vs-mutable-sequence-types
node: model.sequences
type: qa
source: python-docs
---
## Q
Python 内建的不可变序列（immutable sequence）和可变序列（mutable sequence）类型分别包括哪些？这个划分和「能不能当字典键」有什么关系？

## A
内建的不可变序列有 str（字符串）、tuple（元组）、bytes（字节串）；内建的可变序列有 list（列表）、bytearray（可变字节数组）。不可变序列一旦创建内容就不能改变，天然满足哈希值恒定的要求，因此可以被哈希、可以做字典键或放进 set（前提是内部元素也都可哈希）；可变序列的内容随时可能改变，哈希值无法保持稳定，所以 list、bytearray 都不可哈希，不能作为字典键或 set 元素。
