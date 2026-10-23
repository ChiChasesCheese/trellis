---
id: hl-cq-q09-ifconstexpr-variant-optionalref
node: cpp-questions.b-standards
type: qa
step: 21
---
## Q
三个追问：`if constexpr` 和普通 `if` 差在哪？`std::variant` 的开销是什么？可以写 `std::optional<T&>` 吗？
`if constexpr` vs `if`? Cost of `std::variant`? `optional<T&>`?

## A
- **`if constexpr`**：没被选中的分支甚至**不会被实例化**，所以里面可以有对该类型编译不过的代码；普通 `if` 两个分支都要能编译。
- **`variant` 的开销**：最大备选类型的大小加一个标签；`visit` 是跳转表或 switch，没有堆分配，也没有间接调用。
- **`optional<T&>`**：不允许；用指针，或 `optional<std::reference_wrapper<T>>`。
