---
id: hl-cq-q36-alloc-free-hot-path
node: cpp-questions.i-low-latency
type: qa
step: 1
---
## Q
面试题：在 C++ 里怎么让热路径不做堆分配？
How do you keep the hot path allocation-free in C++?

## A
热路径上 `malloc` / `new` 的耗时**不可预测**：要锁、可能向内核要内存、可能缺页。办法：
- **启动时预分配**：`reserve`、对象池、固定容量容器；
- **竞技场（arena）分配器**：`std::pmr::monotonic_buffer_resource`；
- 避免会隐式分配的东西：`std::string` 拼接、`std::function`、`shared_ptr`、`std::list`、`map`；
- 预触碰池内存，避免第一次使用时缺页。
