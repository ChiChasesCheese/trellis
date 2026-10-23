---
id: hl-cq-q10-code-span-bit-format
node: cpp-questions.b-standards
type: qa
step: 25
---
## Q
写出这几个 C++20 小件的用法：接受数组或 `vector` 都能传的 `sum` 函数参数类型；删除 `v` 里所有能被 3 整除的元素；`<bit>` 的 popcount / 前导零 / 向上取 2 的幂 / 循环左移；`std::format` 格式化；自动 join 的线程。

## A
```cpp
int sum(std::span<const int> s);                       // 指针 + 长度，数组、vector 都能传
std::erase_if(v, [](int x) { return x % 3 == 0; });
std::popcount(255u); std::countl_zero(1u);
std::bit_ceil(100u); std::rotl(0x80000001u, 1);
std::format("{:>6} | {:08b} | {:.2f}", "px", 37u, 3.14159);
std::jthread t([] { /* ... */ });                      // 析构时自动 join
```
