---
id: hl-c07-if-constexpr
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 5
---
## Q
`if constexpr` 和普通 `if` 在模板里的关键区别是什么？它取代了什么技巧？写出示例。

## A
- 普通 `if`：两个分支都必须能编译。
- `if constexpr`：**编译期选分支**，未选中的分支不会被实例化，所以可以包含对该类型非法的代码。
- 取代了 C++11 时代复杂的 **SFINAE**（替换失败不是错误）技巧。`<type_traits>` 提供 `is_integral_v<T>`、`is_trivially_copyable_v<T>` 等编译期谓词。

```cpp
template <typename T>
std::string describe(const T& v) {
    if constexpr (std::is_integral_v<T>)       return "integer " + std::to_string(v);
    else if constexpr (std::is_floating_point_v<T>) return "float " + std::to_string(v);
    else return "something else: " + std::string(v);   // 对 int 若用普通 if 会编译失败
}
```
