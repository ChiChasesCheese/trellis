---
id: hl-cq-q11-stack-vs-heap
node: cpp-questions.c-memory-ownership
type: qa
step: 5
---
## Q
追问：栈分配和堆分配的成本差在哪？什么会造成栈溢出？Linux 主线程的栈通常多大？
Stack vs heap cost? Stack overflow?

## A
- **栈分配**：移动一下栈指针，而且缓存是热的。
- **堆分配**：要经过分配器，可能加锁，还可能触发缺页。
- **栈溢出**：深递归或很大的局部数组；Linux 主线程的栈通常是 **8 MB**。
