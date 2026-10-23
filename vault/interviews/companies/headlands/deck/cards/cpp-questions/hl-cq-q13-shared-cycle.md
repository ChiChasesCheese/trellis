---
id: hl-cq-q13-shared-cycle
node: cpp-questions.c-memory-ownership
type: qa
step: 14
---
## Q
两个对象互相持有 `shared_ptr` 会发生什么？怎么修？

## A
- **循环引用**：引用计数永远不会归零，析构函数不运行，内存泄漏（Linux 上 LeakSanitizer 会报告）。
- 实测：两个节点互指，离开作用域后 `a.use_count` 仍是 2，一行 `~Leaky` 都不输出。
- 修法：其中一边改成 `weak_ptr`（“反向 / 观察”关系），就能正常析构。
