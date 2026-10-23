---
id: hl-cq-q22-script
node: cpp-questions.e-templates
type: qa
step: 15
---
## Q
用英文 60 秒回答：What's `constexpr`? How is it different from `const`, `consteval` and `static_assert`? What is CRTP?

## A
结构：`const` 对 `constexpr` 对 `consteval` 对 `static_assert` → 用来在编译期建查找表和把不变量变成编译错误 → CRTP 静态多态：可内联、无 vtable，代价是派生类型互不相关。

- `const` means read-only at run time; **`constexpr`** means the value or function *can* be evaluated at **compile time**, and must be when a constant is required; `consteval` forces compile time; `static_assert` checks a condition during compilation.
- I use it to build **lookup tables** and constants at compile time - e.g. a popcount table is computed by the compiler and sits in read-only data - and to turn invariants into compile errors. Compile-time loops are allowed since C++14.
- **CRTP** is static polymorphism: the base class template calls into the derived class via a cast, so calls are resolved at compile time and can be inlined, with no vtable. The trade-off is that different derived types are unrelated types.
