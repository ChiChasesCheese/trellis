---
id: hl-c07-constexpr-family
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 7
---
## Q
面试问：`const`、`constexpr`、`consteval`、`constinit` 和 `static_assert` 分别是什么？
Interview question: What is the difference between `const` and `constexpr`?

## A
- `const`：运行期不可变。
- `constexpr` **函数**：**可以**在编译期求值（实参是常量时），也可以运行期正常调用；`constexpr` **变量**必须编译期算出，值烙进二进制。
- `static_assert`：编译期断言，例如 `static_assert(sizeof(Msg) == 64)` 守住协议结构体大小。
- `consteval`（C++20）：函数**必须**在编译期求值，运行期调用是编译错误。
- `constinit`（C++20）：变量保证静态初始化（避开初始化顺序问题），但之后**可修改**。
- C++20 起 `constexpr` 里可用 `std::vector`/`std::string`（结果不能带到运行期）。
- 注意：`constexpr` 不等于"一定编译期执行"，用在需要常量的上下文才强制。
