---
id: hl-c03-make-shared
node: cpp-lessons.c03-smart-pointers
type: qa
step: 7
---
## Q
面试问：`std::make_shared<T>()` 比 `std::shared_ptr<T>(new T)` 好在哪？有什么代价？
Interview question: What are the benefits and costs of `make_shared`?

## A
- **好处**：把对象和控制块放在**一次**分配里（`shared_ptr<T>(new T)` 是两次分配），更快、更省、缓存更友好；同时异常安全，例如旧标准下 `f(shared_ptr<A>(new A), g())` 若 `g()` 抛异常可能泄漏。
- **代价**：①不能用自定义删除器；②只要还有 `weak_ptr`，整块内存（包括已析构对象占的空间）不能回收。
- 实测分配次数：`shared_ptr(new T)` 2 次，`make_shared` 1 次，`make_unique` 1 次（没有控制块）。
