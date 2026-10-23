---
id: hl-c07-constexpr-code
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 8
---
## Q
写出：一个能在编译期求值的 `fib`（用 `static_assert` 验证 `fib(50)`），以及编译期生成的平方表 `kSquares`（16 个元素）。

## A
```cpp
constexpr std::uint64_t fib(int n) {
    std::uint64_t a = 0, b = 1;
    for (int i = 0; i < n; ++i) { auto t = a + b; a = b; b = t; }
    return a;
}
static_assert(fib(50) == 12586269025ULL);   // 编译器检查，运行期零成本

constexpr std::array<std::uint32_t, 16> make_squares() {
    std::array<std::uint32_t, 16> t{};
    for (std::uint32_t i = 0; i < t.size(); ++i) t[i] = i * i;
    return t;
}
constexpr auto kSquares = make_squares();   // 查表烙进二进制
static_assert(kSquares[15] == 225);
```
- 同一个 `fib` 也能用运行期的 `n` 调用（`fib(10) == 55`）。
- 用途：查表（正弦表、CRC 表、质数表）、配置校验，把运行期开销挪到编译期。例：`count_primes_below(1000)` 编译期得 168。
