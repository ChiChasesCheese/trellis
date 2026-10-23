---
id: hl-c08-cpp14-code
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 6
---
## Q
写出 C++14 的：放宽 `constexpr` 阶乘、泛型 lambda、初始化捕获 `unique_ptr`、`std::exchange`。

## A
```cpp
constexpr int factorial(int n) {          // 允许循环和局部变量
    int r = 1;
    for (int i = 2; i <= n; ++i) r *= i;
    return r;
}
static_assert(factorial(5) == 120);

auto gen = [](auto a, auto b) { return a * b; };    // gen(3,4)=12, gen(1.5,2)=3
auto owned = std::make_unique<int>(9);
auto use = [p = std::move(owned)] { return *p + 1; };   // 10

auto old = std::exchange(v, std::vector<int>{9});  // 设新值，拿回旧值
```
- `std::exchange(v, new)`：把 `v` 换成新值并返回旧值（上例旧 size 3，新 size 1）。
