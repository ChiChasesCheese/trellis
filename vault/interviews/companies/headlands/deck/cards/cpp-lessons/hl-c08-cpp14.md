---
id: hl-c08-cpp14
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 5
---
## Q
C++14 加了哪些特性？每个修复了 C++11 的什么限制？

## A
- **泛型 lambda**（`auto` 参数）、**初始化捕获**：C++11 的 lambda 不能泛型、不能捕获 move-only 对象。
- **函数返回类型推导** `auto f()`：少写重复类型。
- **放宽 `constexpr`**（允许循环、局部变量）：C++11 的 `constexpr` 只能一个 `return`。
- **变量模板**（`template <typename T> constexpr T kPi = ...`）、**`std::make_unique`**：补齐对称性与异常安全（C++11 只有 `make_shared`）。
- 二进制字面量 `0b1010'1010`、数字分隔符 `1'000'000`、`[[deprecated]]`、`std::exchange`、字符串字面量后缀 `"abc"s`：可读性。
