# C07 · 模板、`constexpr` 与 concepts 入门

> 目标：理解模板是「编译期代码生成」而不是 Java 的擦除泛型；会读写基本模板、可变参数模板、`if constexpr`、`constexpr` 函数、C++20 concepts。

## 1. Java 对照

Java 泛型在编译后**擦除**为 `Object`：`List<Integer>` 里是装箱对象的引用，运行时没有 `T`，不能 `new T()`，不能用基本类型。
C++ 模板对每个实际用到的类型**生成一份专门的代码**（实例化，monomorphisation）：`vector<int>` 是真正连续的 `int`，`T` 在编译期完全已知，可以内联、可以用基本类型、可以用非类型参数（如数组大小）。代价：编译慢、二进制变大、报错信息长。

## 2. 函数模板、类模板

```cpp
template <typename T>
T clamp_to(T v, T lo, T hi) { return v < lo ? lo : (v > hi ? hi : v); }   // one definition, one instance per T used
```

编译器根据实参推导 `T`（`clamp_to(15, 0, 10)` → `T=int`）；推导不出时显式写 `clamp_to<long>(3, 5, 9)`。**模板定义必须在头文件/同一个文件里**（实例化时编译器要看到完整代码）。

```cpp
template <typename T, std::size_t N>             // non-type parameter: N is a compile-time constant
class RingBuffer {
    T data_[N];                                  // inline storage, sized at compile time: no heap, no pointer
    std::size_t head_ = 0, size_ = 0;
public:
    bool push(const T& v) {
        if (size_ == N) return false;
        data_[(head_ + size_++) % N] = v;
        return true;
    }
    bool pop(T& out) {
        if (size_ == 0) return false;
        out = data_[head_]; head_ = (head_ + 1) % N; --size_;
        return true;
    }
    static constexpr std::size_t capacity() { return N; }
};
```

* `std::size_t N` 是**非类型模板参数**：编译期常量，数组大小成为类型的一部分，无需堆分配。
* C++17 的 CTAD（类模板参数推导）：`std::pair p{1, std::string("x")}`、`std::vector v{1,2,3}` 不用写 `<int>`。

## 3. 可变参数模板与折叠表达式

```cpp
template <typename... Ts>
auto sum_all(Ts... xs) { return (xs + ...); }               // fold expression (C++17): ((x1 + x2) + x3) ...

template <typename... Args>
void log_line(const char* tag, Args&&... args) {
    std::cout << "  [" << tag << "]";
    ((std::cout << ' ' << std::forward<Args>(args)), ...);   // fold over the comma operator: print each argument
    std::cout << "\n";
}
```

`typename... Ts` 是**参数包**；`(xs + ...)` 是折叠表达式（C++17），展开为 `x1 + x2 + x3`。`std::forward<Args>(args)...` 完美转发（保持左值/右值性）是 `emplace`、`make_unique` 的实现基础。

## 4. 编译期分支：`if constexpr`

```cpp
template <typename T>
std::string describe(const T& v) {
    if constexpr (std::is_integral_v<T>)             // chosen at COMPILE time; the other branches are not even compiled for T
        return "integer " + std::to_string(v);
    else if constexpr (std::is_floating_point_v<T>)
        return "float " + std::to_string(v);
    else
        return "something else: " + std::string(v);  // would be a compile error for int if this were a plain `if`
}
```

普通 `if` 两个分支都必须能编译；`if constexpr` 在编译期选分支，**未选中的分支不会被实例化**，替代了 C++11 时代复杂的 SFINAE（"替换失败不是错误"）技巧。`<type_traits>` 提供 `is_integral_v<T>`、`is_trivially_copyable_v<T>` 等编译期谓词。

## 5. 特化（specialization）

```cpp
template <typename T> struct Name { static const char* get() { return "other"; } };
template <> struct Name<int> { static const char* get() { return "int"; } };          // full specialisation
template <typename T> struct Name<T*> { static const char* get() { return "pointer"; } };   // partial specialisation
```

全特化针对某个具体类型，偏特化针对一类类型（所有指针）。函数模板不支持偏特化，用重载或 `if constexpr`。

```text
10 -1 5
  push 1 -> 1
  push 2 -> 1
  push 3 -> 1
  push 4 -> 0
  popped 1, capacity 3, sizeof 32
6 6.5 ab
  [fill] AAPL 100 187.5
  integer 42; float 2.500000; something else: hi
  other int pointer
  CTAD: pair<int,string>=1 vector<int>=1
```

## 6. `constexpr`、`consteval`、`constinit`

* `constexpr` 函数：**可以**在编译期求值（实参是常量时），也可以在运行期被正常调用。
* `constexpr` 变量：必须在编译期算出来，值烙进二进制。
* `static_assert`：编译期断言。
* C++20：`consteval` 函数**必须**在编译期求值；`constinit` 变量保证静态初始化（避免初始化顺序问题）但允许之后修改；`constexpr` 里可用 `std::vector`/`std::string`（但结果不能带到运行期）。

```cpp
constexpr std::uint64_t fib(int n) {                   // an ordinary function that MAY run at compile time
    std::uint64_t a = 0, b = 1;
    for (int i = 0; i < n; ++i) { auto t = a + b; a = b; b = t; }
    return a;
}
static_assert(fib(50) == 12586269025ULL, "checked by the compiler, costs nothing at run time");
```

```cpp
constexpr std::array<std::uint32_t, 16> make_squares() {     // a lookup table baked into the binary
    std::array<std::uint32_t, 16> t{};
    for (std::uint32_t i = 0; i < t.size(); ++i) t[i] = i * i;
    return t;
}
constexpr auto kSquares = make_squares();
static_assert(kSquares[15] == 225);

constexpr bool is_prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; ++d) if (n % d == 0) return false;
    return true;
}
constexpr int count_primes_below(int n) { int c = 0; for (int i = 2; i < n; ++i) c += is_prime(i); return c; }
constexpr int kPrimesBelow1000 = count_primes_below(1000);     // evaluated by the compiler
```

```cpp
consteval int must_be_compile_time(int x) { return x * 2; }    // C++20: calling at run time is a compile error
constinit int g_counter = 100;                                  // C++20: constant-initialised, but mutable (no init-order fiasco)
```

```text
fib(50)=12586269025 (also usable with run-time n: fib(10)=55)
squares[7]=49 primes below 1000: 168
consteval gave 42, constinit counter 101
runtime_n=0 fib=0
```

用途：查表（正弦表、CRC 表、质数表）、配置校验、把运行期开销挪到编译期；`static_assert(sizeof(Msg) == 64)` 守住协议结构体的大小。

## 7. Concepts（C++20）

问题：模板对 `T` 的要求只写在文档里，传错类型就是几百行模板内部报错。**concept** 是命名的编译期谓词，写在模板头上，相当于 Java 的 `<T extends Comparable<T>>`，但可以表达"这段代码能编译"。

```cpp
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
concept HasPrice = requires(const T& t) {              // a requires-expression: "this code must compile"
    { t.price() } -> std::convertible_to<double>;
};
```

```cpp
template <Numeric T>                                    // constrained template parameter
T twice(T x) { return x + x; }

auto triple(Numeric auto x) { return x * 3; }           // abbreviated function template (C++20)

template <typename T>
    requires HasPrice<T>                                // requires-clause
double total(const std::vector<T>& xs) {
    double s = 0;
    for (const auto& x : xs) s += x.price();
    return s;
}

template <typename T>
concept Sortable = std::totally_ordered<T> && std::copyable<T>;

template <Sortable T>
T max_of(const T& a, const T& b) { return a < b ? b : a; }
```

```cpp
void print_kind(std::integral auto) { std::cout << "  integral overload\n"; }          // more constrained wins ...
void print_kind(std::floating_point auto) { std::cout << "  floating overload\n"; }
void print_kind(auto) { std::cout << "  generic overload\n"; }
```

```text
42 2.5 15
200.75
abd 9
  integral overload
  floating overload
  generic overload
```

`requires` 表达式里写"必须合法的表达式"及其结果类型约束。标准库预置了 `std::integral`、`std::floating_point`、`std::totally_ordered`、`std::copyable`、`std::invocable`、`std::ranges::range` 等。**约束更强的重载优先**（`integral` 版本胜过无约束 `auto`）。

传错类型时，错误直接指出被违反的约束：

```cpp
// C07: the payoff of concepts: the error names the violated requirement instead of 80 lines of template internals.
#include <concepts>
#include <string>

template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <Numeric T>
T twice(T x) { return x + x; }

int main() {
    return twice(std::string("oops")).size();      // std::string is not Numeric
}
```

```text
C07/c07_concept_bad.cpp:13:12: error: no matching function for call to 'twice'
   13 |     return twice(std::string("oops")).size();      // std::string is not Numeric
      |            ^~~~~
C07/c07_concept_bad.cpp:10:3: note: candidate template ignored: constraints not satisfied [with T = std::string]
   10 | T twice(T x) { return x + x; }
      |   ^
C07/c07_concept_bad.cpp:9:11: note: because 'std::string' does not satisfy 'Numeric'
    9 | template <Numeric T>
      |           ^
C07/c07_concept_bad.cpp:7:19: note: because 'std::string' does not satisfy 'integral'
    7 | concept Numeric = std::integral<T> || std::floating_point<T>;
```

## 8. 坑

1. **模板代码膨胀**：每个类型一份副本，指令缓存压力；公共部分抽成非模板函数。
2. **报错极长**：从最上面的 `error:` 和第一个 `note: candidate` 读起；concepts 能显著缩短。
3. **ODR/头文件**：模板的定义要对所有使用它的翻译单元可见。
4. **依赖名需要 `typename`**：`typename T::value_type`。
5. `constexpr` 不等于"一定在编译期执行"：用在需要常量的上下文（`constexpr` 变量、`static_assert`、数组大小、`consteval`）才强制。
6. 模板里的 `auto` 返回类型推导不到 `void`/不同分支类型不一致会报错。

## 9. 面试官接着会问

**Q：C++ 模板与 Java 泛型的区别？**
要点：编译期实例化 vs 类型擦除；基本类型直接可用、无装箱、可内联、支持非类型参数和特化；代价是代码膨胀与编译时间；Java 是单份代码+装箱+运行期类型信息缺失。

**Q：什么是 SFINAE？现在怎么写？**
要点：替换失败不是错误——重载解析时某个模板实参替换出错就悄悄丢弃该候选；现代写法用 `if constexpr` 和 concepts。

**Q：`constexpr` 与 `const`？**
要点：`const` 是运行期不可变；`constexpr` 要求编译期可求值，可用于常量表达式。

**Q：concepts 解决什么？**
要点：把模板要求写进接口、更好的错误信息、基于约束的重载选择。

**Q：模板为什么说是零开销抽象？**
要点：全部在编译期解析，没有虚表/装箱，与手写特化版本等价。

## 10. 自测

1. `template <std::size_t N> struct Buf { char d[N]; };` 里的 `N` 是什么？`Buf<16>` 和 `Buf<32>` 是同一类型吗？
2. `if constexpr` 与普通 `if` 在模板里的关键区别？
3. 折叠表达式 `(xs + ...)` 展开 `sum_all(1, 2, 3)` 得到什么？
4. `consteval` 函数能用运行期值调用吗？

<details><summary>答案</summary>

1. 非类型模板参数（编译期常量）；不同的类型。
2. 未选中的分支不会被编译/实例化，因此可以包含对该类型非法的代码。
3. `1 + (2 + 3)`（右折叠），结果 6。
4. 不能，编译错误。

</details>
