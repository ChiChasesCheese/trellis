---
id: hl-c05-iterator-invalidation-def
node: cpp-lessons.c05-stl-containers
type: qa
step: 2
---
## Q
C++ 迭代器（iterator）是什么？`end()` 指向哪里？什么叫迭代器失效（invalidation），和 Java 的处理有何不同？

## A
- **迭代器**：指向容器元素的"广义指针"。`begin()` 指向第一个元素，`end()` 指向**最后一个元素之后**（不能解引用）。
- **失效**：容器变化后，旧的迭代器、指针、引用不再有效，继续使用是**未定义行为**。
- **Java**：会抛 `ConcurrentModificationException`；**C++ 不检查**，直接出错或读到垃圾。
- 所以必须记住每种容器的失效规则（见失效表）。
