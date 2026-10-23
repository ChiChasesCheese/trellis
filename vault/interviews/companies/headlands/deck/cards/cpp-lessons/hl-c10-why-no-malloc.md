---
id: hl-c10-why-no-malloc
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 10
---
## Q
面试问：为什么低延迟系统的热路径不用 `malloc`？
Interview question: Why do low-latency systems avoid `malloc` on the hot path?

## A
`malloc` 通用但有代价：
- 找合适的空闲块、元数据、多线程时的锁或线程缓存，**延迟不确定**。
- 可能触发**系统调用**（`mmap`、缺页）。
- **碎片化**，缓存局部性差。

做法：启动时一次性分配，热路径用预分配的**池 / arena**，分配 O(1) 且可预测。
