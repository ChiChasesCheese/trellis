---
id: hl-c07-concepts-code
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 10
---
## Q
写出：`Numeric` concept（整数或浮点）、一个带 requires 表达式的 `HasPrice` concept（要求 `t.price()` 可转成 `double`），以及使用它们的三种语法。

## A
```cpp
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
concept HasPrice = requires(const T& t) {
    { t.price() } -> std::convertible_to<double>;
};

template <Numeric T> T twice(T x) { return x + x; }       // 约束模板参数
auto triple(Numeric auto x) { return x * 3; }             // 缩写函数模板 (C++20)
template <typename T> requires HasPrice<T>                // requires 子句
double total(const std::vector<T>& xs);
```
- `requires` 表达式里写「必须合法的表达式」及其结果类型约束。
- 标准库预置了 `std::integral`、`std::floating_point`、`std::totally_ordered`、`std::copyable`、`std::invocable`、`std::ranges::range` 等。
