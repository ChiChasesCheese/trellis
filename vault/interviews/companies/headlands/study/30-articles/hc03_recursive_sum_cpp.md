# hc03 · 递归求和 1..n（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

面试官说："写个函数，**递归**求 `1 + 2 + … + n`。"一分钟写完。真正的题目是接下来的一连串"如果……呢？"，每一问试探一个层面：

| 追问 | 在测什么 | 对应 |
|---|---|---|
| 结果放 `int` 还是 `long long`？溢出怎么办？ | 整数表示、未定义行为、返回类型设计 | Part 1 |
| `n = 一百万` 会怎样？能不能不爆栈？尾递归？ | 调用栈、编译器优化、trampoline | Part 2 |
| 有公式 `n(n+1)/2`，为什么不直接用？区间 `[a, b]` 呢？ | 中间量溢出、`__int128` | Part 3 |
| 数组里一亿个数，怎么并行求和？ | 线程、结合律、伪共享 | Part 4 |

手算：`sum(4) = 4 + sum(3) = 4 + (3 + (2 + (1 + sum(0)))) = 10`；`sum(0) = 0` 是递归出口（base case）。

## 2. Part 1：把"可能溢出"写进类型

返回裸 `long long` 时，装不下只有三种坏选择：抛异常（调用者会忘记 catch）、返回 `-1`（区间有负数时 `-1` 是合法的和）、静默回绕（最糟：答案错了没人知道）。所以返回一个**封闭的结果类型**：

```cpp
#include <algorithm>
#include <atomic>
#include <bit>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <future>
#include <optional>
#include <pthread.h>
#include <span>
#include <stdexcept>
#include <string>
#include <thread>
#include <unistd.h>
#include <utility>
#include <variant>
#include <vector>

namespace recsum {

struct Ok {
    long long value;
    friend bool operator==(const Ok&, const Ok&) = default;
};
struct Overflow {
    __int128 exact;
    friend bool operator==(const Overflow&, const Overflow&) = default;
};
using SumResult = std::variant<Ok, Overflow>;
```

`std::variant<Ok, Overflow>` 是 C++ 的"和类型"（sum type）；用 `std::visit` 取值时漏掉一个分支**编译不过**。`__int128` 是 clang / gcc 的 128 位整数，在这里扮演 Java 的 `BigInteger`：这题所有精确值的绝对值都小于 2^127，装得下。

接着是位宽和**检查加法**。`Width::Int` 让溢出在 `n = 65536` 就发生（`1+…+65535 = 2147450880 ≤ INT_MAX`，再加 65536 是 `2147516416`），测试不必跑几十亿步；`Width::Long` 的溢出点是 `n = 4294967296`。

```cpp
enum class Width { Int, Long };  // accumulator width; Int makes the overflow happen at n = 65536

/// Checked addition in the given width; std::nullopt means "does not fit".  Operands must already fit the width.
/// Signed overflow is UNDEFINED BEHAVIOUR in C++, so the check has to be done by the builtin, never "after the fact".
inline std::optional<long long> add(Width w, long long a, long long b) {
    long long s;
    if (__builtin_add_overflow(a, b, &s)) return std::nullopt;
    if (w == Width::Int && (s < INT_MIN || s > INT_MAX)) return std::nullopt;
    return s;
}
```

**为什么必须用 builtin？** C++ 里**有符号整数溢出是未定义行为**（UB）：不是回绕，不是异常。编译器可以假设它永远不发生——`if (a + b < a)` 这种"溢出之后再检查"可能被整个优化掉。有符号整数的检查加法有三种正确写法（面试里说出 builtin 最好）：

```cpp
// Signed overflow is undefined behaviour in C++.  Three correct ways to add with a check.
#include <climits>
#include <iostream>
#include <optional>

// 1. The compiler builtin (clang, gcc): the best answer.
std::optional<long long> add_builtin(long long a, long long b) {
    long long s;
    if (__builtin_add_overflow(a, b, &s)) return std::nullopt;
    return s;
}

// 2. Test BEFORE adding, using only operations that cannot overflow.
std::optional<long long> add_precheck(long long a, long long b) {
    if (b > 0 && a > LLONG_MAX - b) return std::nullopt;
    if (b < 0 && a < LLONG_MIN - b) return std::nullopt;
    return a + b;
}

// 3. Widen: the exact sum of two long longs always fits __int128.
std::optional<long long> add_wide(long long a, long long b) {
    __int128 s = static_cast<__int128>(a) + b;
    if (s < LLONG_MIN || s > LLONG_MAX) return std::nullopt;
    return static_cast<long long>(s);
}

int main() {
    for (auto f : {add_builtin, add_precheck, add_wide}) {
        auto r1 = f(LLONG_MAX, 1), r2 = f(LLONG_MIN, -1), r3 = f(LLONG_MAX, LLONG_MIN);
        std::cout << r1.has_value() << r2.has_value() << (r3 ? *r3 : 0) << "\n";   // 0 0 -1
    }
}
```

递归本体。`exact_to` 给出精确值：`n*(n+1) < 2^126` 对所有 `n ≤ LLONG_MAX` 成立，`__int128` 装得下。

```cpp
/// Exact 1+2+...+n.  n*(n+1) < 2^126 for every n <= LLONG_MAX, so it fits __int128.
inline __int128 exact_to(long long n) {
    const __int128 bn = n;
    return bn * (bn + 1) / 2;
}

inline void require_non_negative(long long n) {
    if (n < 0) throw std::invalid_argument("n must be >= 0: " + std::to_string(n));
}

namespace detail {
// The addition happens AFTER the recursive call returns, so every frame must stay alive: this is not a tail call.
inline std::optional<long long> add_up(long long n, Width w) {
    if (n == 0) return 0;
    std::optional<long long> rest = add_up(n - 1, w);
    if (!rest) return std::nullopt;
    return add(w, n, *rest);
}
}  // namespace detail

/// sum(n) = n + sum(n-1).  Stack depth = n.  A stack overflow is a SIGSEGV in C++, not an exception: it cannot be caught.
inline SumResult sum_recursive(long long n, Width w) {
    require_non_negative(n);
    if (auto r = detail::add_up(n, w)) return Ok{*r};
    return Overflow{exact_to(n)};
}
```

注意 `add_up` 里的加法发生在**递归返回之后**（`add(w, n, *rest)`），每一层都必须等子调用回来，栈帧不能丢——这**不是**尾递归。

## 3. Part 2：栈深

### 3.1 栈帧，以及"栈溢出不是异常"

每次函数调用在线程的**调用栈**上压一个**栈帧**（参数、局部变量、返回地址），返回时弹出。栈的大小固定（Linux 主线程默认 8 MiB；macOS 主线程 8 MiB，其他线程 512 KiB），`n` 层递归就要 `n` 个帧。超出时：

* Java：抛 `StackOverflowError`，可以 catch。
* **C++：访问越过栈末尾的保护页，进程收到 `SIGSEGV` 直接死掉，没有异常可抓。**

所以在 C++ 里：

* "量一量能递归多深"不能递归到崩，要在离栈末尾还有 32 KiB 时停下来报告深度；
* "确认它真的会爆栈"只能放在**子进程**里验证（崩的是子进程）。

量深度：`__builtin_frame_address(0)` 取当前帧地址，和起点的差就是已用的栈字节数；线程栈大小要用 pthread 属性指定（`std::thread` 没有这个选项）。

```cpp
namespace detail {
struct Probe {
    const char* base;
    std::size_t budget;
};
// noinline + the asm barrier after the call keep this a genuine non-tail recursion; otherwise -O2 turns it into a loop.
[[gnu::noinline]] inline int dive(const Probe& p, int depth) {
    const char* here = static_cast<const char*>(__builtin_frame_address(0));
    if (static_cast<std::size_t>(p.base - here) >= p.budget) return depth;
    int deepest = dive(p, depth + 1);
    asm volatile("" ::: "memory");
    return deepest;
}
struct Job {
    std::function<void()> fn;
};
}  // namespace detail

/// Run fn on a new thread whose stack is `bytes` big.  std::thread cannot choose its stack size; pthread attributes can.
inline void run_with_stack(std::size_t bytes, std::function<void()> fn) {
    detail::Job job{std::move(fn)};
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    const auto page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    pthread_attr_setstacksize(&attr, (bytes + page - 1) / page * page);
    pthread_t th;
    int rc = pthread_create(&th, &attr, [](void* p) -> void* { static_cast<detail::Job*>(p)->fn(); return nullptr; }, &job);
    pthread_attr_destroy(&attr);
    if (rc != 0) throw std::runtime_error("pthread_create failed: " + std::to_string(rc));
    pthread_join(th, nullptr);
}

/// How deep can plain recursion go on a thread with `stack_bytes` of stack?  We cannot recurse until the crash (a stack
/// overflow kills the process), so we stop 32 KiB (or half the stack, if smaller) before the end and report the depth.
inline int measure_depth(std::size_t stack_bytes) {
    const std::size_t margin = std::min<std::size_t>(32 * 1024, stack_bytes / 2);
    int depth = 0;
    run_with_stack(stack_bytes, [&] {
        const char* base = static_cast<const char*>(__builtin_frame_address(0));
        depth = detail::dive(detail::Probe{base, stack_bytes - margin}, 0);
    });
    return depth;
}
```

`noinline` 加末尾的 `asm volatile("" ::: "memory")` 是为了让 `dive` **保持是递归**——否则编译器会把它变成循环（见 3.2）。

### 3.2 编译器会把递归变成循环吗？

```cpp
// Does the compiler turn recursion into a loop?  Try:  ./a.out tail|musttail|plain 100000000
//   -O0: tail and plain crash (stack overflow), musttail works.   -O2: all three print the sum.
// The standard promises none of this; [[clang::musttail]] (clang only) makes the tail call mandatory.
#include <cstdlib>
#include <iostream>
#include <string>

long long sum_tail(long long n, long long acc) {
    if (n == 0) return acc;
    return sum_tail(n - 1, acc + n);          // last action of the function: a tail call
}

long long sum_musttail(long long n, long long acc) {
    if (n == 0) return acc;
    [[clang::musttail]] return sum_musttail(n - 1, acc + n);   // compile error if it cannot be a jump
}

long long sum_plain(long long n) {            // NOT a tail call: the add happens after the call returns
    if (n == 0) return 0;
    return n + sum_plain(n - 1);
}

int main(int argc, char** argv) {
    std::string mode = argc > 1 ? argv[1] : "tail";
    long long n = argc > 2 ? std::atoll(argv[2]) : 1000;
    if (mode == "tail") std::cout << sum_tail(n, 0) << "\n";
    else if (mode == "musttail") std::cout << sum_musttail(n, 0) << "\n";
    else std::cout << sum_plain(n) << "\n";
}
```

运行 `./a.out tail|musttail|plain 100000000`（一亿层）的结果（clang）：

| | `tail`（尾调用） | `musttail` | `plain`（`n + f(n-1)`） |
|---|---|---|---|
| `-O0` | 栈溢出崩溃 | 正常 | 栈溢出崩溃 |
| `-O2` | 正常 | 正常 | **正常** |

* `-O2` 下 clang 连 `n + sum_plain(n-1)` 都变成了循环（加法满足结合律，编译器自动引入累加器）。**标准不保证任何一种结果**：靠"优化器会帮我消除递归"写出来的代码，换个编译选项就崩。
* `[[clang::musttail]]` 让尾调用成为**强制**的（做不到就编译报错），代价是不可移植（clang 专有）。
* 这里的 `sum_recursive` 带溢出检查（返回后还要判断 `optional`），编译器没法把它变成循环，所以 `-O2` 下依旧会爆栈。
* 可以直接说出口的结论：**C++ 里不要依赖尾调用消除；需要稳定的栈深就写循环，或者用 trampoline。**

### 3.3 迭代版

```cpp
/// Iterative version: O(1) stack.  One local (acc) is all the "waiting" state the recursion kept in its frames.
inline SumResult sum_iterative(long long n, Width w) {
    require_non_negative(n);
    long long acc = 0;
    for (long long i = 1; i <= n; ++i) {
        auto next = add(w, acc, i);
        if (!next) return Overflow{exact_to(n)};
        acc = *next;
    }
    return Ok{acc};
}
```

循环里没有"等待子调用返回"的状态：一个局部变量 `acc` 就是递归在每个栈帧里保存的全部东西。

### 3.4 Trampoline（蹦床）：把栈换成堆

想法：函数不递归调用自己，而是**返回一个"下一步该做什么"的对象**（栈帧立刻弹出）；由一个 `while` 循环取出来执行。栈深永远是常数，代价是每步构造一个小对象。

```cpp
/// Trampoline: either finished (done) or "here is the next step" (more).  Every step returns immediately (its frame is
/// popped) and hands back a small heap-or-inline object; run() loops.  Stack depth is constant.
template <class T>
class Trampoline {
public:
    using Next = std::function<Trampoline()>;  // std::function<R()> may name a still-incomplete R

    static Trampoline done(T value) { return Trampoline(std::in_place_index<0>, std::move(value)); }
    static Trampoline more(Next next) { return Trampoline(std::in_place_index<1>, std::move(next)); }

    bool is_done() const { return state_.index() == 0; }
    T take() && { return std::move(std::get<0>(state_)); }
    Trampoline step() const { return std::get<1>(state_)(); }

private:
    // Not a variadic `Trampoline(A&&...)`: that would out-compete the copy constructor for non-const lvalues.
    template <std::size_t I, class A>
    Trampoline(std::in_place_index_t<I> tag, A&& a) : state_(tag, std::forward<A>(a)) {}
    std::variant<T, Next> state_;
};

/// Run a trampoline: a loop, no recursion.  `cur = cur.step()` is safe: step() has returned before the assignment
/// destroys the std::function it was called through.
template <class T>
T run(Trampoline<T> cur) {
    while (!cur.is_done()) cur = cur.step();
    return std::move(cur).take();
}
```

三个 C++ 细节：

1. `std::function<Trampoline()>`：返回类型 `Trampoline` 在类内还是**不完整类型**，对 `std::function` 的声明来说没问题（调用时才要求完整）。
2. 构造函数不能写成 `template <class... A> Trampoline(A&&...)`：对非 const 左值，它比拷贝构造函数更匹配，会**劫持拷贝**。所以用带 `in_place_index_t` 标签的构造函数。
3. `cur = cur.step()`：`step()` 调用了存放在 `cur` 里的 `std::function`，**返回之后**才赋值（销毁旧的 function），所以安全；如果一个 lambda 在自己还在执行时被销毁，才是 UB。

用它写求和（尾递归形式：累加器 `acc` 当参数）、互递归 `is_even` / `is_odd`（连"自己调自己"都不是，编译器不可能替你消除），以及作对照的"普通尾递归写法"：

```cpp
namespace detail {
using SumTramp = Trampoline<std::optional<long long>>;
// Tail-recursive form: `acc` carries the sum so far, the recursive call is the last thing that happens.
inline SumTramp step(long long n, long long acc, Width w) {
    if (n == 0) return SumTramp::done(acc);
    auto next = add(w, acc, n);
    if (!next) return SumTramp::done(std::nullopt);
    return SumTramp::more([n, w, a = *next] { return step(n - 1, a, w); });
}
inline Trampoline<bool> odd(long long n);
inline Trampoline<bool> even(long long n) {
    return n == 0 ? Trampoline<bool>::done(true) : Trampoline<bool>::more([n] { return odd(n - 1); });
}
inline Trampoline<bool> odd(long long n) {
    return n == 0 ? Trampoline<bool>::done(false) : Trampoline<bool>::more([n] { return even(n - 1); });
}
// Plain tail recursion.  Clang/GCC at -O1+ usually turn this into a loop; the standard does not promise it.
inline std::optional<long long> tail(long long n, long long acc, Width w) {
    if (n == 0) return acc;
    auto next = add(w, acc, n);
    if (!next) return std::nullopt;
    return tail(n - 1, *next, w);
}
}  // namespace detail

inline SumResult sum_trampoline(long long n, Width w) {
    require_non_negative(n);
    if (auto r = run(detail::step(n, 0, w))) return Ok{*r};
    return Overflow{exact_to(n)};
}

/// Mutual recursion is_even/is_odd: not even a self tail call, a trampoline handles it all the same.
inline bool is_even(long long n) {
    require_non_negative(n);
    return run(detail::even(n));
}

/// Tail-recursive source form, left to the optimiser.  Correct everywhere; stack-safe only if the compiler says so.
inline SumResult sum_tail_recursive(long long n, Width w) {
    require_non_negative(n);
    if (auto r = detail::tail(n, 0, w)) return Ok{*r};
    return Overflow{exact_to(n)};
}
```

## 4. Part 3：闭式公式与区间 `[a, b]`

"为什么不直接 `n*(n+1)/2`？"——因为 `n*(n+1)` 先溢出。`n = 2^32 - 1` 时 `n*(n+1) = 2^64 - 2^32`，装不进 `long long`，得到负数，再除 2 是 `-2^31`，没有任何报错。（在 C++ 里这个**有符号**乘法本身是 UB，所以下面的"错误写法"用无符号乘法把回绕写明白，只用来对比。）

```cpp
/// The classic wrong answer, made well-defined: in Java `n * (n + 1) / 2` wraps; in C++ the same signed expression is
/// UB, so the wrap is spelled out with unsigned arithmetic (modular since forever) and a conversion that is modular
/// since C++20.  n = 2^32 - 1: n*(n+1) = 2^64 - 2^32 wraps to a negative long long, and the result is -2^31.
inline long long naive_closed_form(long long n) {
    const auto un = static_cast<unsigned long long>(n);
    const auto wrapped = static_cast<long long>(un * (un + 1));
    return wrapped / 2;
}
```

正确做法：区间 `a..b` 的和 = `(a+b) * (b-a+1) / 2`。三个要点：

1. `(a+b)` 和 `(b-a+1)` **一奇一偶**，所以乘积一定是偶数，除 2 是精确的。
2. 中间量溢出 ≠ 结果溢出：`MIN..MAX` 里 `b-a+1 = 2^64` 装不进 `long long`，但和恰好是 `LLONG_MIN`。所以别急着在中间量溢出时报 `Overflow`。
3. 用 `__int128` 一次乘法就够了：`|(a+b)*(b-a+1)| ≤ 2^126 + 2^63 < 2^127`。

```cpp
/// Exact a+(a+1)+...+b.  |(a+b)*(b-a+1)| <= 2^126 + 2^63 < 2^127, so one __int128 multiplication cannot overflow, and the
/// product is always even (one factor is even), so the division by 2 is exact.
inline __int128 range_sum_exact(long long a, long long b) {
    if (a > b) throw std::invalid_argument("a > b: " + std::to_string(a) + " > " + std::to_string(b));
    return (static_cast<__int128>(a) + b) * (static_cast<__int128>(b) - a + 1) / 2;
}

inline SumResult range_sum(long long a, long long b) {
    const __int128 exact = range_sum_exact(a, b);
    if (exact >= LLONG_MIN && exact <= LLONG_MAX) return Ok{static_cast<long long>(exact)};
    return Overflow{exact};
}
```

没有 `__int128` 的平台（MSVC）怎么办？先把偶数那个因子除 2 再用 `__builtin_mul_overflow`，溢出时用两个 64 位拼 128 位。拼 128 位累加器的完整写法（`hi` 有符号、`lo` 无符号，`lo` 相加后比原值小说明进位）：

```cpp
// A 128-bit accumulator from two 64-bit halves: what to write when __int128 does not exist (MSVC).
#include <cassert>
#include <climits>
#include <cstdint>
#include <iostream>
#include <random>

struct Wide {
    std::int64_t hi = 0;       // signed high half
    std::uint64_t lo = 0;      // unsigned low half

    Wide plus(std::int64_t x) const {
        std::uint64_t nlo = lo + static_cast<std::uint64_t>(x);            // unsigned: wraps, well defined
        std::uint64_t carry = nlo < lo ? 1 : 0;                           // wrapped => carry into hi
        std::uint64_t sign_ext = x < 0 ? ~std::uint64_t{0} : 0;           // high half of the sign-extended x
        return {static_cast<std::int64_t>(static_cast<std::uint64_t>(hi) + sign_ext + carry), nlo};
    }
    Wide merge(const Wide& o) const {
        std::uint64_t nlo = lo + o.lo;
        std::uint64_t carry = nlo < lo ? 1 : 0;
        return {static_cast<std::int64_t>(static_cast<std::uint64_t>(hi) + static_cast<std::uint64_t>(o.hi) + carry), nlo};
    }
    bool fits_long() const {                       // hi must be the sign extension of lo
        return hi == (static_cast<std::int64_t>(lo) < 0 ? -1 : 0);
    }
    __int128 to_i128() const { return (static_cast<__int128>(hi) << 64) | lo; }   // only for checking here
};

int main() {
    std::mt19937_64 rnd(1);
    Wide w;
    __int128 ref = 0;
    for (int i = 0; i < 1'000'000; ++i) {
        std::int64_t x = rnd() % 3 == 0 ? static_cast<std::int64_t>(rnd()) : (rnd() % 2 ? LLONG_MAX : LLONG_MIN);
        w = w.plus(x);
        ref += x;
        assert(w.to_i128() == ref);
        assert(w.fits_long() == (ref >= LLONG_MIN && ref <= LLONG_MAX));
    }
    Wide a = Wide{}.plus(LLONG_MAX).plus(LLONG_MAX), b = Wide{}.plus(LLONG_MIN);
    assert(a.merge(b).to_i128() == static_cast<__int128>(LLONG_MAX) * 2 + LLONG_MIN);
    std::cout << "portable Wide agrees with __int128 on 1,000,000 random adds\n";
}
```

## 5. Part 4：并行求和

对象是 `std::span<const long long>`（指针 + 长度，不拷贝，`vector`、数组、子区间都能传）。

**为什么要 128 位累加器 `Wide`？** 逐步检查加法的结果取决于求和**顺序**：`{MAX, 1, -1}` 顺序加在第二步就溢出，而真实总和是 `MAX`。并行时每块的边界是任意的，同一份数据换个切法就可能"溢出"或"不溢出"。128 位加法永远不溢出且满足结合律，怎么切块、怎么合并结果都一样，最后只判一次"放不放得进 `long long`"。

```cpp
/// 128-bit accumulator.  Addition is associative, so any chunking and any merge order give the same answer; the
/// overflow decision is taken once, at the end.  (Per-step checked adds depend on the order: {MAX, 1, -1}.)
struct Wide {
    __int128 v = 0;
    static Wide zero() { return {}; }
    Wide plus(long long x) const { return Wide{v + x}; }
    Wide merge(const Wide& o) const { return Wide{v + o.v}; }
    bool fits_long() const { return v >= LLONG_MIN && v <= LLONG_MAX; }
    __int128 exact() const { return v; }
    SumResult to_result() const { return fits_long() ? SumResult{Ok{static_cast<long long>(v)}} : SumResult{Overflow{v}}; }
    friend bool operator==(const Wide&, const Wide&) = default;
};

/// Hot loop: a local __int128 lives in two registers; no objects, no calls.
inline Wide sum_chunk(std::span<const long long> data) {
    __int128 acc = 0;
    for (long long x : data) acc += x;
    return Wide{acc};
}

inline SumResult checked_sum(std::span<const long long> data) { return sum_chunk(data).to_result(); }
```

热循环里 `acc` 是局部 `__int128`，住在寄存器里，不分配对象。

### 5.1 分治（fork-join）

Java 有 `ForkJoinPool`（work-stealing，任务便宜）。C++ 标准库**没有**：每个 `std::async(std::launch::async, …)` 是一个真正的 OS 线程。`threshold = 1` 时朴素的"每个节点一个线程"要创建十万个线程，所以只让最上面几层（约 `2 × 核数` 个任务）开线程，下面用普通递归：

```cpp
namespace detail {
inline Wide fork_join(std::span<const long long> d, std::size_t threshold, int spawn_levels) {
    if (d.size() <= threshold) return sum_chunk(d);
    const std::size_t mid = d.size() / 2;  // size_t cannot go negative; with `int` indices (lo + hi) / 2 overflows on big arrays
    const auto left = d.first(mid), right = d.subspan(mid);
    if (spawn_levels <= 0) return fork_join(left, threshold, 0).merge(fork_join(right, threshold, 0));
    // No work-stealing pool in the standard library: a thread per node would be 100,000 threads for threshold = 1,
    // so only the top levels get a thread (about 2 * cores tasks); below that it is plain recursion.
    auto spawned = std::async(std::launch::async, [=] { return fork_join(left, threshold, spawn_levels - 1); });
    const Wide mine = fork_join(right, threshold, spawn_levels - 1);
    return spawned.get().merge(mine);  // get() rethrows a worker's exception here
}
}  // namespace detail

inline std::size_t hardware_threads() { return std::max(1u, std::thread::hardware_concurrency()); }

inline SumResult parallel_sum_fork_join(std::span<const long long> data, std::size_t threshold) {
    if (threshold < 1) throw std::invalid_argument("threshold < 1");
    const int levels = std::bit_width(hardware_threads());
    return detail::fork_join(data, threshold, levels).to_result();
}
```

`mid = d.size() / 2` 用 `size_t`，不会像 `int` 的 `(lo + hi) / 2` 那样在大数组上溢出。`spawned.get()` 会把工作线程里的异常重新抛出来。

### 5.2 每块一个 `std::async`

```cpp
namespace detail {
inline std::span<const long long> chunk_of(std::span<const long long> d, std::size_t chunk, std::size_t size) {
    const std::size_t from = std::min(d.size(), chunk * size), to = std::min(d.size(), (chunk + 1) * size);
    return d.subspan(from, to - from);
}
inline std::size_t ceil_div(std::size_t a, std::size_t b) { return a / b + (a % b != 0); }
}  // namespace detail

/// One std::async per chunk, hardware_threads()*4 chunks (the parallel-stream analogue).
inline SumResult parallel_sum_async(std::span<const long long> data) {
    const std::size_t chunks = hardware_threads() * 4;
    const std::size_t size = detail::ceil_div(data.size(), chunks);
    std::vector<std::future<Wide>> parts;
    parts.reserve(chunks);
    for (std::size_t i = 0; i < chunks; ++i)
        parts.push_back(std::async(std::launch::async, [=] { return sum_chunk(detail::chunk_of(data, i, size)); }));
    Wide total = Wide::zero();
    for (auto& p : parts) total = total.merge(p.get());
    return total.to_result();
}
```

### 5.3 固定数量的工作线程 + 原子计数器

Java 21 可以"每块一个虚拟线程"，因为虚拟线程很便宜。C++ 没有：一个 OS 线程要几十微秒创建、占用一块栈，一万个线程是灾难。C++ 的做法是自己定池子大小（核数个线程），线程从一个 `std::atomic` 计数器里领块号：

```cpp
namespace detail {
struct JoinAll {  // a joinable std::thread destroyed without join() calls std::terminate: join on every exit path
    std::vector<std::thread> threads;
    ~JoinAll() { for (auto& t : threads) if (t.joinable()) t.join(); }
};
}  // namespace detail

/// `chunks` pieces of work, at most hardware_threads() OS threads pulling chunk numbers from an atomic counter.
/// This is what "a virtual thread per chunk" becomes in C++: there are no cheap threads, so you size the pool yourself.
inline SumResult parallel_sum_workers(std::span<const long long> data, std::size_t chunks) {
    if (chunks < 1) throw std::invalid_argument("chunks < 1");
    const std::size_t size = detail::ceil_div(data.size(), chunks);
    std::vector<Wide> parts(chunks);  // slot i is written by exactly one worker: no data race, no lock
    std::atomic<std::size_t> next{0};
    {
        detail::JoinAll pool;
        const std::size_t workers = std::min(chunks, hardware_threads());
        for (std::size_t w = 0; w < workers; ++w)
            pool.threads.emplace_back([&] {
                for (std::size_t i; (i = next.fetch_add(1, std::memory_order_relaxed)) < chunks;)
                    parts[i] = sum_chunk(detail::chunk_of(data, i, size));
            });
    }  // ~JoinAll joins; thread join() is the synchronisation that makes `parts` visible to us
    Wide total = Wide::zero();
    for (const Wide& p : parts) total = total.merge(p);
    return total.to_result();
}

}  // namespace recsum
```

* `fetch_add(1, relaxed)`：计数器只需要"每个块号只被领走一次"，不需要给其他数据排序，`relaxed` 足够。
* 每个 `parts[i]` 只被一个线程写 → 没有数据竞争，不需要锁；`join()` 提供 happens-before，主线程随后读到的就是最终值。
* **伪共享（false sharing）**：`parts` 里相邻的槽在同一条缓存线上（x86 64 字节，Apple 芯片 128 字节），两个线程写相邻槽会让整条线在核之间来回失效。这里每块很大、写得很少，影响小；如果每个线程要频繁写自己的槽，要么把槽补齐到整条缓存线，要么在局部变量里累加、最后写一次：

```cpp
// Per-thread partial sums.  Adjacent slots share a cache line: every write by one thread invalidates the line in the
// others' caches ("false sharing").  Pad each slot to a full line (128 bytes covers Apple silicon and x86), or keep the
// partial sum in a local variable and write the slot once at the end.
#include <iostream>
#include <numeric>
#include <thread>
#include <vector>

struct alignas(128) Slot {
    long long value = 0;
};
static_assert(sizeof(Slot) == 128, "one slot per cache line");

int main() {
    std::vector<long long> data(4'000'000);
    std::iota(data.begin(), data.end(), 1);

    constexpr int threads = 4;
    std::vector<Slot> slots(threads);                       // padded: no two threads touch the same line
    std::vector<std::thread> pool;
    const std::size_t part = data.size() / threads;
    for (int t = 0; t < threads; ++t)
        pool.emplace_back([&, t] {
            long long local = 0;                            // the hot loop touches only a register ...
            for (std::size_t i = t * part; i < (t + 1) * part; ++i) local += data[i];
            slots[t].value = local;                         // ... and the shared slot is written once
        });
    for (auto& th : pool) th.join();                        // join makes the slots visible to this thread

    long long total = 0;
    for (const Slot& s : slots) total += s.value;
    std::cout << total << "\n";                             // 8000002000000
}
```

* `JoinAll`：一个仍可 `join` 的 `std::thread` 被析构会调用 `std::terminate`。用 RAII 保证任何路径（包括抛异常）都 join。
* 裸 `std::thread` 的函数体里逃出异常也会 `std::terminate`；`std::async` 的 `future::get()` 才会把异常带回来。

## 6. 陷阱

1. **有符号溢出是 UB。** 不是回绕。`-fsanitize=undefined` 能抓到；想要回绕就用无符号类型。
2. **指望尾调用消除。** 见 3.2：`-O0` / `-O2` 结果不同，标准不保证。
3. **栈溢出当成可捕获的错误。** 它是信号，不是异常。
4. **`n * (n + 1) / 2`。** 先乘后除，中间量溢出。先把偶数因子除 2，或者用 `__int128`。
5. **用 `double` 并行求和。** 浮点加法不满足结合律，不同切法得到不同结果（并行结果会"抖"）。要确定性就固定切块方式和合并顺序，或用补偿求和（Kahan）。
6. **`std::execution::par`。** `std::reduce(std::execution::par, …)` 在 libstdc++ 里依赖 TBB，在 libc++ 里还是实验性的；面试里说"标准有这个接口，但可用性取决于标准库实现"，然后手写 `std::async` / `std::thread` 版。
7. **`std::async` 的 future 析构会阻塞。** 返回值被丢弃的 `std::async(...)` 会立刻同步执行完——看起来像并行，其实是串行。

## 7. 面试官会追问什么（senior）

**Q1. 为什么不用递归？** 栈深 O(n)，`n` 大了崩；每层有调用开销。迭代 O(1) 栈；或者直接用公式 O(1)。

**Q2. `-O2` 会不会把它优化成循环？** 可能：clang/gcc 对简单的 `n + f(n-1)` 和尾调用都会做。但标准不保证，`-O0` 不做，带检查的版本做不了。要保证就写循环，或在 clang 里用 `[[clang::musttail]]`。

**Q3. 怎么检测溢出？** `__builtin_add_overflow`（clang/gcc）；或者先用 `__int128` 加宽再判断；或者加之前用 `LLONG_MAX - b` 比较。注意 C++26 的 `std::add_sat` 是饱和运算，不会告诉你发生了溢出。

**Q4. 不用 `__int128` 怎么办？** 两个 64 位拼成 128 位（`lo` 无符号加法回绕，回绕了就给 `hi` 进位）——第 4 节的 `wide_portable.cpp`。

**Q5. 并行加速比能到多少？为什么常常比顺序还慢？** 求和是内存带宽受限的：一个核就能吃满大部分带宽，再多的核收益有限；数据小的时候线程创建（几十微秒）比计算本身还贵。

**Q6. 线程数怎么选？** CPU 密集任务：`std::thread::hardware_concurrency()`（核数）；阻塞 I/O：可以更多。

**Q7. `memory_order_relaxed` 为什么够？** 计数器只负责分发块号，不用它去发布别的数据；数据的可见性由 `join()` 保证。

## 8. 自测

1. `int x = INT_MAX; x + 1` 会得到什么？`unsigned u = UINT_MAX; u + 1` 呢？
2. `sum_recursive(1'000'000, Width::Long)` 在 512 KiB 的栈上会怎样？能 `try/catch` 吗？
3. 为什么 `{MAX, 1, -1}` 用逐步检查加法会报溢出，而真实总和并没有溢出？
4. `std::async(std::launch::async, f);`（不保存返回值）有什么问题？
5. 为什么 `Trampoline` 的构造函数不能写成可变参数模板 `Trampoline(A&&...)`？
6. `n * (n + 1) / 2` 在 `n = 2^32` 时，用 `__int128` 怎么修？用 `long long` 又怎么修？

<details><summary>答案</summary>

1. `INT_MAX + 1` 是未定义行为（可能回绕成负数，也可能被优化器利用）；`UINT_MAX + 1` 是定义良好的回绕，结果 0。
2. 进程收到 `SIGSEGV` 崩溃；栈溢出不是异常，不能 catch。
3. 逐步加：`MAX + 1` 先超过 `LLONG_MAX`，后面 `-1` 不能"撤销"一次已经报告的溢出。真实总和只有一个，与顺序无关。用 128 位累加，最后判一次。
4. 返回的临时 `future` 在表达式结束时析构，析构会**等待任务完成**，所以调用点同步阻塞，没有并行。
5. 对非 const 左值（`Trampoline t2 = t1;`），模板 `A&&`（`A = Trampoline&`）比 `const Trampoline&` 的拷贝构造函数更匹配，被选中后去构造 `variant` 而编译失败。用带标签的构造函数避免。
6. `__int128 n = ...; n * (n + 1) / 2`（乘积 < 2^127）；`long long` 的话先把 `n` 和 `n+1` 中的偶数除 2 再相乘，并用 `__builtin_mul_overflow` 检测。

</details>
