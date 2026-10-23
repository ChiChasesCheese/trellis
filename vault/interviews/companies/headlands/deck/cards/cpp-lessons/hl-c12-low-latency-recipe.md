---
id: hl-c12-low-latency-recipe
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 12
---
## Q
面试问：怎样在 C++ 里写低延迟代码？
Interview question: How do you write low-latency C++?

## A
- **热路径零分配**：池 / arena。
- **无锁数据结构**：如 SPSC 队列。
- **缓存行对齐**，避免伪共享（false sharing）。
- **数据局部性**：连续存放、SoA。
- 避免**系统调用与异常**。
- **线程绑核**、预热。
- 测量**尾延迟**，不要只看平均值。
