---
id: hl-cq-q30-compiler-hoist-flag
node: cpp-questions.g-concurrency
type: qa
step: 15
---
## Q
线程里写 `while (!done) {}`，`done` 是普通 `bool`，别的线程会把它置 true。除了竞争，编译器优化还可能带来什么问题？`volatile` 能修吗？正确做法是什么？

## A
- 编译器可以假设没有别的线程改普通变量，所以把 `done` 的读取**提到循环外**，变成死循环。
- `volatile` 能阻止这种优化，但仍然不保证**别的数据**的可见顺序。
- 正确做法：`std::atomic<bool>`。
- 用 **ThreadSanitizer** 来检查。
