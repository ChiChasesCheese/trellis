---
id: hl-cq-q22-code-constexpr-table
node: cpp-questions.e-templates
type: qa
step: 12
---
## Q
写出一个 `constexpr` 函数，生成 16 个数的 popcount 表，并把它放进编译期常量 `kTable`，再用 `static_assert` 检查 `kTable[15] == 4`。再用循环版 `constexpr` 斐波那契函数 `fib` 在编译期算 `fib(50)`，结果是多少？

## A
```cpp
constexpr std::array<int, 16> make_popcount_table() {
    std::array<int, 16> t{};
    for (int i = 0; i < 16; ++i) { int c = 0; for (int b = i; b; b >>= 1) c += b & 1; t[i] = c; }
    return t;
}
constexpr auto kTable = make_popcount_table();       // 编译器算好，放在只读数据段
static_assert(kTable[15] == 4 && kTable[8] == 1);    // 错了就编译失败
constexpr auto kFib50 = fib(50);                     // 编译期算出 12586269025
```
编译期循环从 C++14 起允许。
