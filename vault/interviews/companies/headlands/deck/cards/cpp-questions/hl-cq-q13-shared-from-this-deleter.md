---
id: hl-cq-q13-shared-from-this-deleter
node: cpp-questions.c-memory-ownership
type: qa
step: 17
---
## Q
追问：`enable_shared_from_this` 是做什么的？智能指针的自定义删除器（deleter）怎么写，`unique_ptr` 和 `shared_ptr` 的实现有什么不同？

## A
- **`enable_shared_from_this`**：让对象能安全地交出一个指向自己的 `shared_ptr`，并共用已有的控制块。
- **自定义删除器**：`unique_ptr<FILE, decltype(&fclose)>` 可以包装 C 资源，删除器是类型的一部分；`shared_ptr` 的删除器被**类型擦除**，存进控制块。
