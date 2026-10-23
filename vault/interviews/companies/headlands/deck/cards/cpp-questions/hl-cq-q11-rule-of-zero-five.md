---
id: hl-cq-q11-rule-of-zero-five
node: cpp-questions.c-memory-ownership
type: qa
step: 3
---
## Q
C++ 的零法则（Rule of Zero）和五法则（Rule of Five）分别是什么？析构函数里能抛异常吗？

## A
- **零法则**：成员都用 RAII 类型（`vector`、`string`、`unique_ptr`），就不需要自己写析构、拷贝、移动。
- **五法则**：自己管资源时，五个特殊成员——析构、拷贝构造、拷贝赋值、移动构造、移动赋值——要么都写，要么都删。例如 `FileHandle` 在构造里 `fopen`、析构里 `fclose`，并删除拷贝（只能有一个所有者）。
- **析构函数不能抛异常**：析构默认 `noexcept`，在异常展开期间再抛一个会 `std::terminate`。
