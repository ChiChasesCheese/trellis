---
id: hl-cq-q10-code-cpp20
node: cpp-questions.b-standards
type: qa
step: 24
---
## Q
补全 C++20 代码：用 concept `std::integral` 约束模板参数 `T` 的 `gcd_of`；给 `Version{int major, minor;}` 生成全部比较运算符；用指定初始化给 `Params` 的 `depth` 赋 5；用 ranges 管道对 `v` 先筛偶数再平方。

## A
```cpp
template <std::integral T> T gcd_of(T a, T b) { return b == 0 ? a : gcd_of(b, a % b); }

struct Version { int major, minor;
                 auto operator<=>(const Version&) const = default; };   // 生成全部比较运算符

Params p{.depth = 5};                                                   // 指定初始化

auto evens_squared = v | std::views::filter([](int x) { return x % 2 == 0; })
                       | std::views::transform([](int x) { return x * x; });   // 惰性管道
```
