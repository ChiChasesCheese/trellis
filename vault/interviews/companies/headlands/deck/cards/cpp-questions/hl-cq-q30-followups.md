---
id: hl-cq-q30-followups
node: cpp-questions.g-concurrency
type: qa
step: 16
---
## Q
三个追问：“良性”数据竞争可以接受吗？双重检查锁（double-checked locking）怎么写才对？`atomic<int>` 上的 `i++` 是什么？

## A
- **良性竞争**：标准 C++ 里不行，它是 UB，编译器可以做出出乎意料的变换。
- **双重检查锁**：没有原子 / acquire-release 就是错的；用 `std::call_once`，或函数内的局部 `static`（C++11 起初始化是线程安全的）。
- **`atomic<int>` 上的 `i++`**：原子的读-改-写，等价于 `fetch_add(1)`。
