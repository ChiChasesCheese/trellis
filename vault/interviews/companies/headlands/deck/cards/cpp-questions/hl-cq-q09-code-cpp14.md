---
id: hl-cq-q09-code-cpp14
node: cpp-questions.b-standards
type: qa
step: 16
---
## Q
写出 C++14 的三个常用写法：泛型 lambda `add`（两个 `auto` 参数求和）、创建装着 7 的 `unique_ptr<int>`、浮点常量变量模板 `pi_v<T>`。

## A
```cpp
auto add = [](auto a, auto b) { return a + b; };            // 泛型 lambda
auto u = std::make_unique<int>(7);                          // make_unique
template <class T> constexpr T pi_v = T(3.14159265358979L); // 变量模板
```
