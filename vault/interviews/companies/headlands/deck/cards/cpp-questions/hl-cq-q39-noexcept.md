---
id: hl-cq-q39-noexcept
node: cpp-questions.i-low-latency
type: qa
step: 18
---
## Q
C++ 的 `noexcept` 有什么作用？异常从 `noexcept` 函数里逃出来会怎样？

## A
- `noexcept` 声明函数不抛异常，编译器可以省去展开信息。
- 移动构造函数标 `noexcept`，`vector` 扩容时才会使用它。
- `noexcept` 函数里抛出异常会直接 `std::terminate`。
- 相关规则：析构函数不要抛异常；靠 RAII 做异常安全。
