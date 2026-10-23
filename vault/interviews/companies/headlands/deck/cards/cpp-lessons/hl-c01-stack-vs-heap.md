---
id: hl-c01-stack-vs-heap
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 14
---
## Q
面试问：C++ 里栈（stack）和堆（heap）的区别？栈对象一定快吗？
Interview question: What is the difference between stack and heap in C++? Are stack objects always faster?

## A
- **栈（自动存储）**：分配只是移动栈指针，不碰分配器，缓存友好，离开作用域自动销毁。
- **堆**：要走 `malloc`/`new`（找空闲块、可能加锁），要自己或智能指针释放。
- 「栈上」说的是对象所在位置：`vector` 对象在栈上，元素在堆上。
- 栈空间小（默认几 MB），大数组放栈上会**栈溢出**（stack overflow）。
- 所以栈对象通常更快，但不是「一定」；大块数据应放堆（用 `vector`）。
