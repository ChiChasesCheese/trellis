---
id: hl-cq-q09-code-if-constexpr
node: cpp-questions.b-standards
type: qa
step: 18
---
## Q
补全代码：写一个模板函数 `describe(const T& x)`，用 `if constexpr` 在编译期判断：整型返回 `"integer " + to_string(x)`，否则返回 `"other"`。再写一个折叠表达式 lambda `sum_all`。

## A
```cpp
template <class T> auto describe(const T& x) {
    if constexpr (std::is_integral_v<T>)
        return std::string("integer ") + std::to_string(x);
    else
        return std::string("other");
}
auto sum_all = [](auto... xs) { return (xs + ...); };   // 折叠表达式
```
`if constexpr` 的弃用分支不会被实例化，所以可以写对该类型编译不过的代码。
