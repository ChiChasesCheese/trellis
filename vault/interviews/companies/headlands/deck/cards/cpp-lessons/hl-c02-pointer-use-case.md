---
id: hl-c02-pointer-use-case
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 14
---
## Q
自测：什么时候函数参数该用指针而不是引用？

## A
三种情况：
1. 参数"**可以没有**"：用 `nullptr` 表示没有。
2. 需要在函数里**重新指向**别的对象。
3. 与 **C API** 交互。

其他情况默认用引用（"一定有"）。指针本身不应表示所有权；需要所有权时用 `unique_ptr`。
