# C09 · 未定义行为（UB）与 Sanitizer

> 目标：说清什么是 UB、为什么 C++ 留着它、常见种类，并会用 AddressSanitizer / UndefinedBehaviorSanitizer / ThreadSanitizer 抓。

## 1. Java 对照

Java 的每个程序行为都有定义：整数溢出回绕、数组越界抛 `ArrayIndexOutOfBoundsException`、空引用抛 `NullPointerException`、数据竞争也只会读到"某个写过的值"。
C++ 的标准把一类错误标成**未定义行为（undefined behaviour）**：程序一旦执行到，**标准对整个程序不再有任何要求**——可能"碰巧正常"、崩溃、结果错，或者编译器因为"UB 不会发生"的假设把你的检查整个删掉。

## 2. 为什么要有 UB

标准把"程序员保证不会发生"的情况交给编译器当前提，从而不必生成检查代码：不做数组边界检查（快）、假设有符号整数不会溢出（循环可以向量化）、假设不同类型的指针不指向同一内存（可以重排读写）。**快是用"出错时不可预测"换来的。**

## 3. 常见 UB 清单

| UB | 例子 | Java 里 |
|---|---|---|
| 有符号整数溢出 | `INT_MAX + 1` | 回绕 |
| 越界访问 | `v[v.size()]`、`arr[5]` | 抛异常 |
| 悬空指针/引用、use-after-free、double free | `delete p; *p` | 不可能 |
| 空指针解引用 | `*nullptr` | NPE |
| 数据竞争 | 两线程无同步写同一变量 | 定义弱语义 |
| 读未初始化变量 | `int x; use(x)` | 不可能（局部变量必须赋值） |
| 严格别名违规 | `int*` 当 `float*` 读 | — |
| 移位过大/负数移位 | `1 << 32`（32 位 int） | 移位量取模 |
| `INT_MIN / -1`、除零 | | 除零抛异常 |
| 非 void 函数没有 return 就走到末尾 | | 编译错误 |
| 违反 `memcpy` 不重叠、`const` 对象被修改 | | — |

**最危险的特点**：UB 的表现取决于优化级别、编译器版本、周围代码。测试通过不代表没有。

## 4. 有符号溢出：编译器会删掉你的检查

```cpp
[[gnu::noinline]] bool overflows_signed_naive(int x) { return x + 1 < x; }                  // compiler: always false
[[gnu::noinline]] bool overflows_signed_safe(int x) { return x == INT_MAX; }                // test the BOUNDARY instead
[[gnu::noinline]] bool overflows_unsigned(std::uint32_t x) { return x + 1u < x; }           // defined wrap: check is real
[[gnu::noinline]] bool add_checked(int a, int b, int& out) { return __builtin_add_overflow(a, b, &out); }   // GCC/Clang builtin
```

```text
naive signed check on INT_MAX : false   (the overflow happened, the check says no)
boundary check on INT_MAX     : true
unsigned check on UINT32_MAX  : true
__builtin_add_overflow(INT_MAX,1): true (wrapped result -2147483648)
```

第一行是关键：`x + 1 < x` 对有符号 `int` "永远为假"（因为溢出是 UB，编译器假定不会发生），`-O2` 下整个函数变成 `return false`：

```asm
__Z22overflows_signed_naivei:
	mov	w0, #0
	ret
```

无符号溢出是**有定义的回绕**，检查有效。要安全地检测溢出：先检查边界（`x == INT_MAX`）、用更宽类型、或编译器内建 `__builtin_add_overflow`（GCC/Clang）。

UBSan 会在运行时直接指出：

```cpp
// C09: signed integer overflow is undefined behaviour; unsigned overflow wraps (defined). UBSan names the line.
#include <climits>
#include <cstdint>
#include <iostream>

int main(int argc, char**) {
    int x = INT_MAX - 1 + argc;                  // argc == 1 at run time, so x == INT_MAX
    std::uint32_t u = UINT32_MAX - 1 + static_cast<std::uint32_t>(argc);
    std::cout << "unsigned UINT32_MAX + 1 = " << u + 1u << " (defined: wraps to 0)\n";
    int y = x + 1;                               // UB: UBSan reports "signed integer overflow"
    std::cout << "signed INT_MAX + 1 = " << y << " (whatever the compiler happened to emit)\n";
}
```

```text
C09/c09_signed_overflow_ub.cpp:11:15: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior C09/c09_signed_overflow_ub.cpp:11:15 
```

## 5. 越界与生命周期

```cpp
// C09: out-of-bounds access. operator[] does not check. at() throws. Raw arrays and vectors both corrupt memory silently.
#include <iostream>
#include <stdexcept>
#include <vector>

int main(int argc, char**) {
    std::vector<int> v{10, 20, 30};
    try { std::cout << v.at(5) << "\n"; }
    catch (const std::out_of_range& e) { std::cout << "at(5) threw: " << e.what() << "\n"; }
    int idx = 2 + argc;                         // == 3, one past the end
    std::cout << "v[3] = " << v[idx] << "\n";   // heap-buffer-overflow (ASan), silent garbage without it
    int arr[4] = {1, 2, 3, 4};
    std::cout << "arr[4] = " << arr[idx + 1] << "\n";
}
```

```text
ERROR: AddressSanitizer: heap-buffer-overflow on address 0x… at pc 0x… bp 0x… sp 0x…
READ of size 4 at 0x… thread T0
0x… is located 0 bytes after 12-byte region [0x…,0x…)
SUMMARY: AddressSanitizer: heap-buffer-overflow (c09_bounds_ub:arm64+0x…) in main+0x364
```

`v.at(i)` 越界抛 `std::out_of_range`，`v[i]` 不检查。

```cpp
// C09: lifetime bugs: use-after-free, double free, returning the address of a local.
#include <iostream>

int* dangling_local() { int x = 7; return &x; }          // clang warns here (-Wreturn-stack-address)

int main(int argc, char**) {
    int* p = new int(5);
    delete p;
    if (argc == 1) std::cout << "after delete: " << *p << "\n";      // use-after-free
    int* q = dangling_local();
    std::cout << "returned local address is " << (q ? "non-null" : "null") << " (reading it would be UB)\n";
    delete p;                                                          // double free
}
```

```text
ERROR: AddressSanitizer: heap-use-after-free on address 0x… at pc 0x… bp 0x… sp 0x…
READ of size 4 at 0x… thread T0
0x… is located 0 bytes inside of 4-byte region [0x…,0x…)
freed by thread T0 here:
previously allocated by thread T0 here:
SUMMARY: AddressSanitizer: heap-use-after-free (c09_lifetime_ub:arm64+0x…) in main+0x174
```

编译器对返回局部变量地址的 `dangling_local` 本身就给了警告：

```text
C09/c09_lifetime_ub.cpp:5:44: warning: address of stack memory associated with local variable 'x' returned [-Wreturn-stack-address]
    5 | int* dangling_local() { int x = 7; return &x; }          // clang warns here (-Wreturn-stack-address)
      |                                            ^
```

## 6. 数据竞争

两个线程无同步地写同一个变量就是数据竞争，**即使每次结果都碰巧对**：

```cpp
// C09: a data race (two threads, one write, no synchronisation) is UB. ThreadSanitizer finds it; ASan/UBSan do not.
#include <iostream>
#include <thread>

int counter = 0;                                  // plain int: not atomic, not locked

int main() {
    std::thread a([] { for (int i = 0; i < 100000; ++i) ++counter; });
    std::thread b([] { for (int i = 0; i < 100000; ++i) ++counter; });
    a.join(); b.join();
    std::cout << "counter = " << counter << " (expected 200000)\n";
}
```

ThreadSanitizer 报告：

```text
WARNING: ThreadSanitizer: data race (pid=54615)
SUMMARY: ThreadSanitizer: data race (c09_data_race_ub:arm64+0x…) in void* std::__1::__thread_proxy[abi:nqe220106]<std::__1::tuple<std::__1::unique_ptr<std::__1::__thread_struct, std::__1::default_delete<std::__1::__thread_struct>>, main::$_1>>(void*)+0x68
```

修复：把计数器改成 `std::atomic<int>`，或用 `std::mutex` 保护。

## 7. 严格别名（strict aliasing）

规则：除少数例外（`char`/`unsigned char`/`std::byte`），通过**不相容类型**的指针读写同一块内存是 UB。编译器据此认为 `int*` 和 `float*` 不会指向同一处，可以不重新读取：

```cpp
[[gnu::noinline]] int store_both(int* i, float* f) {
    *i = 1;
    *f = 2.0f;          // compiler: "an int* and a float* cannot alias" ...
    return *i;          // ... so *i is still 1: it never reloads
}
```

我们把两个指针都指向同一块联合体存储来"撒谎"，结果：

```text
store_both returned 1 (a literal reading of the code would give 1073741824)
bits_memcpy(1.0f)=0x… bits_cast(1.0f)=0x…
```

函数返回 1，而不是 `2.0f` 的位模式 1073741824。汇编里能看到 `*i` 的值被直接当成常量 1 返回，根本没重新读内存：

```asm
__Z10store_bothPiPf:
	mov	w8, #1
	str	w8, [x0]
	mov	w8, #1073741824
	str	w8, [x1]
	mov	w0, #1
	ret
```

正确的"按位重解释"：`std::memcpy`（编译成一条 mov）或 C++20 `std::bit_cast`：

```cpp
std::uint32_t bits_memcpy(float f) { std::uint32_t u; std::memcpy(&u, &f, sizeof u); return u; }   // legal; compiles to one mov
std::uint32_t bits_cast(float f) { return std::bit_cast<std::uint32_t>(f); }                       // C++20, constexpr-friendly
// std::uint32_t bits_bad(float f) { return *reinterpret_cast<std::uint32_t*>(&f); }                // UB: strict aliasing violation
```

## 8. UBSan 一览

UBSan 报告后默认继续运行，所以一次能看到多种：

```cpp
// C09: a tour of what UBSan catches. UBSan keeps running after each report, so one run prints them all.
#include <climits>
#include <cstdint>
#include <cstring>
#include <iostream>

struct S { int field; };

int main(int argc, char**) {
    int n = 31 + argc;                        // 32 at run time
    std::cout << "shift: " << (1 << n) << "\n";                  // shift exponent 32 is too large for a 32-bit int
    int m = INT_MIN + argc - 1;               // INT_MIN
    std::cout << "division: " << m / (-argc) << "\n";            // INT_MIN / -1 overflows
    int zero = argc - 1;
    std::cout << "div by zero: " << 10 / zero << "\n";           // division by zero
    alignas(8) char buf[16] = {};
    std::cout << "misaligned: " << *reinterpret_cast<std::int64_t*>(buf + argc) << "\n";   // misaligned 8-byte load
    double d = 1e300 * argc;
    std::cout << "float->int: " << static_cast<int>(d) << "\n";  // out-of-range conversion
    bool b = false;
    unsigned char raw = static_cast<unsigned char>(2 + argc);
    std::memcpy(&b, &raw, 1);
    std::cout << "invalid bool: " << b << "\n";                   // a bool object holding 3
    S* sp = argc == 1 ? nullptr : new S{1};
    std::cout << "null member access: " << sp->field << "\n";    // reported by UBSan, then the SEGV kills us (so: last)
}
```

```text
C09/c09_ubsan_catalogue_ub.cpp:12:34: runtime error: shift exponent 32 is too large for 32-bit type 'int'
C09/c09_ubsan_catalogue_ub.cpp:14:36: runtime error: division of -2147483648 by -1 cannot be represented in type 'int'
C09/c09_ubsan_catalogue_ub.cpp:16:40: runtime error: division by zero
C09/c09_ubsan_catalogue_ub.cpp:18:36: runtime error: load of misaligned address 0x… for type 'std::int64_t' (aka 'long long'), which requires 8 byte alignment
C09/c09_ubsan_catalogue_ub.cpp:20:53: runtime error: 1e+300 is outside the range of representable values of type 'int'
C09/c09_ubsan_catalogue_ub.cpp:24:38: runtime error: load of value 3, which is not a valid value for type 'bool'
C09/c09_ubsan_catalogue_ub.cpp:26:48: runtime error: member access within null pointer of type 'S'
C09/c09_ubsan_catalogue_ub.cpp:26:48: runtime error: load of null pointer of type 'int'
```

注意程序自己的输出也说明了"UB 的结果是随机的"：`1 << 32` 得到 1，除零得到 0，`double` 转 `int` 得到饱和值。

## 9. Sanitizer 怎么用

| 选项 | 抓什么 | 开销 | 备注 |
|---|---|---|---|
| `-fsanitize=address` (ASan) | 越界、use-after-free、double free、栈/全局越界、new/delete 配对错误 | 约 2 倍 | 与 TSan 不能同时开 |
| `-fsanitize=undefined` (UBSan) | 有符号溢出、移位、对齐、null、bool/enum 非法值、float→int 溢出等 | 很小 | 默认报告后继续；`-fno-sanitize-recover` 让它直接终止 |
| `-fsanitize=thread` (TSan) | 数据竞争、锁序问题 | 5–15 倍 | 单独构建 |
| `-fsanitize=memory` (MSan) | 读未初始化内存 | — | 仅 Linux/clang |
| `-Wall -Wextra` + `-Werror` | 编译期可发现的：未使用、符号比较、缺 return、悬空 | 0 | 先把警告清零 |

推荐开发命令：`clang++ -std=c++20 -O1 -g -Wall -Wextra -fsanitize=address,undefined`。CoderPad 上通常不能加 sanitizer，所以要靠习惯：用 `at()` 调试越界、用 `size_t`/`int` 小心混用、不依赖未初始化值。

## 10. 防御清单

* 用 `vector`/`string`/`array` 与迭代器代替裸数组和指针算术；调试时用 `.at()`。
* 不手写 `new/delete`，用智能指针（悬空和 double free 大幅减少）。
* 变量声明即初始化（`int x{};`）。
* 溢出敏感处用 `long long`/`uint64_t`，或检查边界后再运算；`size()` 是无符号，倒序循环写 `for (size_t i = n; i-- > 0;)`。
* 多线程数据要么 `atomic`、要么 `mutex`、要么不共享。
* 位重解释用 `memcpy`/`bit_cast`。
* 所有警告都当作 bug 处理。

## 11. 面试官接着会问

**Q：什么是 UB？举几个例子。为什么不直接定义成崩溃/回绕？**
要点：标准不对程序行为做任何要求；列表第 3 节；检查有成本，语言选择让程序员负责，同时允许优化（向量化、别名分析、删死代码）。

**Q：有符号溢出和无符号溢出区别？**
要点：有符号 UB，无符号模 2^n 回绕；编译器会据此删掉 `x+1<x`。

**Q：UB 为什么"测试通过也不安全"？**
要点：编译器可以假设 UB 不发生并据此变换代码；升级编译器/改优化级别/加一行代码就可能变化。

**Q：数据竞争是什么？与竞态条件（race condition）一样吗？**
要点：数据竞争 = 两个线程无同步地访问同一内存且至少一个写，C++ 定义为 UB；竞态条件是逻辑上的时序错误，用了原子/锁也可能有。

**Q：你怎么在项目里发现这类问题？**
要点：Sanitizer（ASan/UBSan/TSan）、静态分析、`-Wall -Wextra -Werror`、模糊测试、Valgrind。

**Q：Java 为什么没有这些问题？代价是什么？**
要点：运行时做检查（边界、空、类型），GC 保证内存安全；代价是检查与运行时开销和不可预测的 GC 暂停。

## 12. 自测

1. `unsigned x = 0; x--;` 是 UB 吗？结果是多少？
2. 为什么 `if (x + 1 < x)` 不能用来检测 `int` 溢出？
3. `float f; int i = *(int*)&f;` 有什么问题？怎么写才对？
4. 数据竞争的程序"打印结果总是对的"说明没问题吗？

<details><summary>答案</summary>

1. 不是，无符号回绕有定义，结果 `UINT_MAX`（4294967295）。
2. 有符号溢出是 UB，编译器假设它不发生，把比较优化成常量 false。
3. 违反严格别名（UB）；用 `std::memcpy(&i, &f, sizeof i)` 或 `std::bit_cast<int>(f)`。
4. 不能：数据竞争本身就是 UB，当前编译器/CPU 恰好表现正常而已，TSan 仍会报告。

</details>
