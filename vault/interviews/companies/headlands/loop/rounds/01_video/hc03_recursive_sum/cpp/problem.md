# hc03 · 递归求和 1..n（C++20 版）

面试官先让你写一个递归函数，算 1 到 n 的和，一分钟就能写完。真正的考点在后面一连串追问：结果放不放得下、递归多深会把栈撑爆、能不能直接用公式、能不能并行。C++ 版的每个追问都落到同一件事上：**有符号溢出是未定义行为**（undefined behavior，UB），而栈溢出是进程直接崩溃，不是能 catch 的异常。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `recsum`）。

## 读题前你需要知道

- **调用栈和栈帧**（call stack / stack frame）：每次函数调用在线程栈上压一帧（参数、局部变量、返回地址），返回时弹出。n 层递归就要 n 帧。栈的大小是固定的：macOS 主线程 8 MiB，其他线程默认 512 KiB。
- **栈溢出**（stack overflow）：在 C++ 里表现为 `SIGSEGV` / `SIGBUS`，进程被杀掉，`try/catch` 接不住。所以测试只能在子进程里观察它。
- **有符号溢出是 UB**：`long long` 加法越界后，编译器可以假设它从没发生，然后照这个前提去优化。所以只能**在加之前或者借助内建函数**判断，不能先加完再看结果是不是变成了负数。
- **`__int128`**：clang / gcc 提供的 128 位整数，在这套题里充当 Java 的 `BigInteger`。

## 公共类型（starter 已给出）

```cpp
struct Ok       { long long value; };
struct Overflow { __int128 exact; };          // 数学上的精确值
using SumResult = std::variant<Ok, Overflow>; // 只有两种结果，std::visit 必须两种都处理
enum class Width { Int, Long };               // 累加器位宽；Int 让溢出在 n = 65536 就发生
```

溢出的语义统一为：**数学上的真实和放不进该位宽，就返回 `Overflow{exact}`**，`exact` 是精确值。永远不要返回回绕后的错误数字。

## Part 1 · 朴素递归 + 带检查的加法

| 签名 | 要求 |
|---|---|
| `std::optional<long long> add(Width, long long a, long long b)` | 带检查的加法：放不进该位宽就返回 `std::nullopt`。`Int` 位宽还要判断是否超出 `int` 范围 |
| `__int128 exact_to(long long n)` | 精确的 1+…+n |
| `SumResult sum_recursive(long long n, Width)` | `sum(n) = n + sum(n-1)`；`n < 0` 抛 `std::invalid_argument`；溢出返回 `Overflow{exact_to(n)}`；不要试图捕获栈溢出 |

- `Int`：`n = 65535` 得 `Ok{2147450880}`；`n = 65536` 得 `Overflow{2147516416}`。
- 65536 层递归在 512 KiB 的线程栈上放不下，所以这两个测试跑在 64 MiB 栈的线程里。**栈比整数先出事**，这是 Part 2 的伏笔。
- C++ 专属测试：`add` 在 `LLONG_MAX + 1`、`LLONG_MIN - 1`、`INT_MAX + 1` 这些边界上不能触发 UB（UBSan 开着，一触发就终止）；`exact_to(LLONG_MAX)` 要精确，等于 (2^63 − 1) · 2^62。

## Part 2 · 栈深：编译器会不会帮你消掉递归，怎么办

| 签名 | 要求 |
|---|---|
| `void run_with_stack(std::size_t bytes, std::function<void()>)` | **已给出**：用 pthread 属性指定栈大小起一个线程（`std::thread` 做不到） |
| `int measure_depth(std::size_t stack_bytes)` | 在这么大的栈上，普通递归能走多深。栈溢出接不住，所以离栈底还剩约 32 KiB 时就停下，返回深度 |
| `SumResult sum_iterative(long long n, Width)` | 迭代版，栈空间 O(1)，语义同 Part 1 |
| `template<class T> T run(Trampoline<T>)` | 用循环把 trampoline 跑完（`Trampoline` 类型已给出：`done(value)` / `more(next)`） |
| `SumResult sum_trampoline(long long n, Width)` | 尾递归形式（带累加器参数）+ trampoline |
| `bool is_even(long long n)` | 互递归 `is_even / is_odd`，走 trampoline；n < 0 抛 `invalid_argument` |
| `SumResult sum_tail_recursive(long long n, Width)` | 普通的尾递归写法；编译器可能、也可能不把它变成循环，测试只查结果对不对 |

- `measure_depth(64 MiB)` 必须比 `measure_depth(512 KiB)` 深 4 倍以上；512 KiB 上至少 1000 层。
- 在 512 KiB 栈上：`sum_recursive(50'000'000)` 必须让子进程崩溃；`sum_trampoline(1'000'000)` 和 `sum_iterative(1'000'000)` 必须返回 `Ok{500000500000}`。
- `is_even(2'000'000)` 要在 512 KiB 栈上跑完。
- C++ 专属测试：`Trampoline` 能被拷贝（包括拷贝一个非 const 左值）；结果是只能移动的类型（`std::unique_ptr`）时，`run` 要把它移出来，不能拷贝。
- 提示：测深度时要阻止编译器把递归变成循环，可以用 `[[gnu::noinline]]`、在递归调用之后加一点工作，再用 `__builtin_frame_address(0)` 看栈用了多少。

## Part 3 · 区间 [a, b]：负数、中间量溢出、闭式公式

| 签名 | 要求 |
|---|---|
| `__int128 range_sum_exact(long long a, long long b)` | 精确值；`a > b` 抛 `invalid_argument`。提示：用一次 `__int128` 乘法就够，而且这次乘法本身不会溢出（先证明它） |
| `SumResult range_sum(long long a, long long b)` | 放得进 `long long` 返回 `Ok`，否则返回 `Overflow{exact}` |
| `long long naive_closed_form(long long n)` | **已给出**的错误写法 `n*(n+1)/2`（用无符号运算写出回绕），测试拿它做对比 |

- `naive_closed_form(4294967295)` 得 `-2147483648`：n·(n+1) = 2^64 − 2^32，放不进有符号 64 位。真实答案 `range_sum(1, 4294967295)` 是 `Ok{9223372034707292160}`。
- **中间量溢出不等于结果溢出**：`range_sum(LLONG_MIN, LLONG_MAX)` 是 `Ok{LLONG_MIN}`（项数 2^64 放不进 `long long`，和却放得进）；`range_sum(LLONG_MAX, LLONG_MAX)` 是 `Ok{LLONG_MAX}`（`a + b` 溢出，和就是 a）。
- `range_sum(LLONG_MAX - 1, LLONG_MAX)` 是 `Overflow{2^64 − 3}`，真的放不下。
- C++ 专属测试：在一组角落值组成的网格上，所有 (a, b) 组合都不能触发有符号溢出，结果和 oracle 一致。

## Part 4 · 并行求和（输入 `std::span<const long long>`）

| 签名 | 要求 |
|---|---|
| `struct Wide { __int128 v; plus(long long) · merge(Wide) · fits_long() }` | 128 位累加器：满足结合律，块怎么切、按什么顺序合并，结果都一样 |
| `SumResult checked_sum(std::span<const long long>)` | 顺序基线：**只有真实总和放不进 `long long` 时**才返回 `Overflow`。`{MAX, 1, -1}` 是 `Ok{MAX}` |
| `SumResult parallel_sum_fork_join(span, std::size_t threshold)` | 分治：长度 ≤ threshold 直接算，否则左半交给另一个线程（`std::async`），右半自己算；`threshold < 1` 抛 `invalid_argument` |
| `SumResult parallel_sum_async(span)` | 切成 `hardware_concurrency() * 4` 块，每块一个 `std::async` |
| `SumResult parallel_sum_workers(span, std::size_t chunks)` | 切成 `chunks` 块，最多 `hardware_concurrency()` 个线程从一个 `std::atomic` 计数器领块号；`chunks < 1` 抛 `invalid_argument` |

- 每种并行实现对同一个输入，结果必须和 `checked_sum` 完全相等（包括 `Overflow.exact`）。
- `threshold = 1` 时 fork-join 不能真的一个节点起一个线程：10 万个元素就是 10 万个线程。
- 4000 个元素、前一半 `LLONG_MAX`、后一半 `LLONG_MIN`：单看每块会溢出，总和 `-2000` 放得下，所以答案是 `Ok{-2000}`。
- 6 个线程同时调用三种并行实现，所有结果都要一致；1000 万个元素要在 2 秒内算完。
- C++ 专属测试：`span` 可以指向数组的一段（从奇数下标开始）、`std::array`、C 数组、空 span。

## 边界清单

- `n = 0`、`n = 1`、`n < 0`、`n = LLONG_MIN`
- `Int` 位宽 `65535 / 65536`；`Long` 位宽 `4294967295 / 4294967296`
- `add`：`MAX + 1`、`MIN − 1`、`MAX + MIN`、`INT_MAX + 1`、`INT_MIN + INT_MAX`
- 区间：单点、`a == b == 0`、全负、跨 0、`MIN..MAX`、`MAX−1..MAX`、`MIN..0`、`a > b`
- 数组：空、单元素、块数多于元素数、`threshold = 1`、块内溢出但总和不溢出
- 栈：512 KiB / 64 MiB 的线程栈；100 万步的 trampoline 链；200 万层互递归

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc03_recursive_sum          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc03_recursive_sum                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 「不用公式」→「现在用公式」→「n 很大怎么办」：Part 1 → Part 3。
- 「改成 `double`」：浮点加法不满足结合律，并行结果会抖。
- 「求 1..n 的平方和」：闭式 n(n+1)(2n+1)/6，要先除 2 再除 3，运算顺序同样重要。
