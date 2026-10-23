---
id: hl-c07-variadic-fold
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 4
---
## Q
可变参数模板（variadic template）的参数包和折叠表达式（fold expression）是什么？写出 `sum_all` 和打印所有参数的 `log_line`。

## A
```cpp
template <typename... Ts>
auto sum_all(Ts... xs) { return (xs + ...); }   // sum_all(1,2,3) = 1 + (2 + 3) = 6

template <typename... Args>
void log_line(const char* tag, Args&&... args) {
    std::cout << '[' << tag << ']';
    ((std::cout << ' ' << std::forward<Args>(args)), ...);   // 对逗号运算符折叠
}
```
- `typename... Ts` 是**参数包**；`(xs + ...)` 是折叠表达式（C++17），展开为 `x1 + x2 + x3`。
- `std::forward<Args>(args)...` 是**完美转发**，保持左值/右值性，是 `emplace`、`make_unique` 的实现基础。
