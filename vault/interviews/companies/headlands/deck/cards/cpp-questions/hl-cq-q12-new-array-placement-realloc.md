---
id: hl-cq-q12-new-array-placement-realloc
node: cpp-questions.c-memory-ownership
type: qa
step: 10
---
## Q
三个追问：`new[]` 比 `new` 多做了什么？placement new 什么场合用？C++ 对象能用 `realloc` 吗？

## A
- **`new[]`**：为 N 个对象分配空间、逐个构造，并记住 N，这样 `delete[]` 能把它们都析构。
- **placement new**：内存池、竞技场（arena）、共享内存——在已知地址上构造对象。
- **`realloc`**：只能用于可以按字节搬动的对象（trivially relocatable）；否则用 `vector`。
