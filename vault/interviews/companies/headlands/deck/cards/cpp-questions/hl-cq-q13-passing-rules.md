---
id: hl-cq-q13-passing-rules
node: cpp-questions.c-memory-ownership
type: qa
step: 15
---
## Q
C++ 函数参数里什么时候传 `T&` / `T*`、什么时候按值传 `unique_ptr`、什么时候传 `shared_ptr`？只读用 `shared_ptr` 怎么传？

## A
- 函数只是**使用**对象：传 `T&` 或 `T*`（裸指针 / 引用表示“不拥有”）。
- 要**接管所有权**：按值传 `unique_ptr`。
- 要**共享**：传 `shared_ptr`；只读时用 `const shared_ptr&`，避免多余的原子加减。
- 延迟敏感路径尽量避免 `shared_ptr`，因为引用计数是原子操作。
