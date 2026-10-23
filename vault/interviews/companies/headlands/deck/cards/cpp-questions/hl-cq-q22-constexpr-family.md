---
id: hl-cq-q22-constexpr-family
node: cpp-questions.e-templates
type: qa
step: 11
---
## Q
面试题：`constexpr` 是什么？它和 `const`、`consteval`、`static_assert` 有什么区别？什么是 CRTP？
What's `constexpr`? How is it different from `const`, `consteval` and `static_assert`? What is CRTP?

## A
- **`const`**：运行期不可修改。
- **`constexpr`**：可以（且在需要常量的地方必须）**在编译期求值**。
- **`consteval`**（C++20）：**必须**在编译期求值。
- **`static_assert`**：编译期断言，错了就编译失败。
- 用途：把查找表和配置算在编译期，运行时零成本。
- **CRTP** 是用模板实现的静态多态。
