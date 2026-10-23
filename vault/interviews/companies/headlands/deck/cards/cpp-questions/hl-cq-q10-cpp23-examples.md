---
id: hl-cq-q10-cpp23-examples
node: cpp-questions.b-standards
type: qa
step: 26
---
## Q
C++23 的 `std::expected`、显式 `this`、`ranges::to`、`std::println` 各怎么用？

## A
- `std::expected<int, Err>`：返回“值或错误”，失败时 `return std::unexpected(Err::Empty);`。
- 显式 this：`int get(this const Counter& self)`。
- `... | std::ranges::to<std::vector>()`：把惰性管道**物化**成 `vector`。
- `std::println("{}", v)`：直接打印容器。
- 编译选项用 `-std=c++23`。
