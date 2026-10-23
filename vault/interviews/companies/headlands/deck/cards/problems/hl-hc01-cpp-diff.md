---
id: hl-hc01-cpp-diff
node: problems.hc01-stock-trading-dp
type: qa
step: 21
---
## Q
买卖股票的 C++20 实现和 Java 版在输入类型、溢出、状态机、动作类型、结果类型上有哪些差异？

## A
- **输入**：Java 是 `long[]`（可为 null → `NullPointerException`）；C++ 是 `std::span<const long long>`，不可能为 null、不拷贝、不修改。
- **溢出**：Java 用 `Math.addExact` 抛 `ArithmeticException`；C++ 有符号溢出是 **UB**，用 `__builtin_add_overflow`，或像这里从上界保证不溢出。
- **`k + 1`**：Java 回绕成负数 → `NegativeArraySizeException`；C++ 是 UB，先 `k >= n/2` 分流。
- **大小**：Java `int length`；C++ `size_t` 无符号，`size() - 1` 会回绕，格子数用 `long long`。
- **不确定的结果**：Java 抛异常；C++ 用 `std::optional`（`try_plan`，格子数超限返回 `nullopt`，价格越界仍抛异常）。
- **状态机**：Java `enum` + 方法；C++ `enum class` + 自由函数，注意 `enum class` 可以容纳非法整数值。
- **动作类型**：`sealed interface` + record + 模式匹配 vs `std::variant` + `std::visit(overloaded{...})`，同样编译期穷尽。
- **哨兵**：`pendingSell = -1` vs `std::optional<int>`；**逆序遍历**：`list.reversed()` vs `views::reverse`。
