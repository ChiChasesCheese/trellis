# C16 · CoderPad 生存指南：单文件、`main`、`assert` 测试、读懂编译错误

> 目标：在共享编辑器里限时写 C++ 时，能快速搭骨架、写自测、读懂编译器的报错、避开常见陷阱。

## 1. 环境预期

* **单个文件**，你自己写 `main`；通常没有构建系统、不能链接第三方库、不能加 sanitizer。
* 先确认语言标准（`-std=c++17`? `c++20`?）：先写一个小的 C++20 特性（比如 `std::span` / `contains`）试编译，失败就退回 17 的写法。
* 头文件**逐个 include**。`<bits/stdc++.h>` 只有 GCC 有，Clang/Apple 环境没有；而且某个头文件"碰巧"被另一个头间接包含并不可靠（换编译器就消失）。
* 面试官希望看到：先澄清需求和边界 → 说方案与复杂度 → 写代码 → 用例子走查 → 测试。大声说出你在做什么。

## 2. 骨架：解法 + 自测 + `main`

下面是一个可以直接粘贴的模板：三个小题（两数之和、按成交额取 top-k、订单簿最优价），带 `CHECK` 宏自测。

```cpp
#define CHECK(cond) do { if (!(cond)) { std::cerr << "FAILED line " << __LINE__ << ": " #cond "\n"; std::exit(1); } } while (0)
#define CHECK_EQ(a, b) do { auto va = (a); auto vb = (b); if (!(va == vb)) { std::cerr << "FAILED line " << __LINE__ << ": " #a " == " #b "  (" << va << " vs " << vb << ")\n"; std::exit(1); } } while (0)
```

* 为什么自己写 `CHECK` 而不是 `assert`：`assert` 在定义了 `NDEBUG`（常见于 release/`-O2` 构建配置）时**整个消失**，测试就成了空操作；自己的宏总是执行，并且能打印行号和表达式。

```cpp
std::optional<std::pair<int, int>> two_sum(const std::vector<int>& a, int target) {
    std::unordered_map<int, int> seen;                    // value -> index
    for (int i = 0; i < static_cast<int>(a.size()); ++i) {
        if (auto it = seen.find(target - a[i]); it != seen.end()) return std::pair{it->second, i};
        seen.emplace(a[i], i);
    }
    return std::nullopt;
}
```

```cpp
struct Trade { std::string sym; long qty; long px_cents; };

std::vector<Trade> top_k(const std::vector<Trade>& trades, std::size_t k) {
    auto notional = [](const Trade& t) { return t.qty * t.px_cents; };
    auto worse = [&](const Trade& a, const Trade& b) { return notional(a) > notional(b); };   // "greater" => smallest on top
    std::priority_queue<Trade, std::vector<Trade>, decltype(worse)> heap(worse);
    for (const auto& t : trades) {
        heap.push(t);
        if (heap.size() > k) heap.pop();                  // drop the smallest of the k+1
    }
    std::vector<Trade> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    std::reverse(out.begin(), out.end());                 // largest first
    return out;
}
```

```cpp
class Book {
    std::map<long, long, std::greater<long>> bids_;       // price -> qty, best (highest) first
    std::map<long, long> asks_;                           // best (lowest) first
public:
    void add(bool buy, long px, long qty) { (buy ? bids_[px] : asks_[px]) += qty; }
    void cancel(bool buy, long px, long qty) {
        auto erase_from = [&](auto& m) {
            auto it = m.find(px);
            if (it == m.end()) return;
            it->second -= qty;
            if (it->second <= 0) m.erase(it);             // never leave empty levels behind
        };
        if (buy) erase_from(bids_); else erase_from(asks_);
    }
    std::optional<long> best_bid() const { return bids_.empty() ? std::nullopt : std::optional(bids_.begin()->first); }
    std::optional<long> best_ask() const { return asks_.empty() ? std::nullopt : std::optional(asks_.begin()->first); }
};
```

```cpp
void run_tests() {
    auto r = two_sum({2, 7, 11, 15}, 9);
    CHECK(r.has_value());
    CHECK_EQ(r->first, 0);
    CHECK_EQ(r->second, 1);
    CHECK(!two_sum({1, 2}, 100).has_value());
    CHECK(!two_sum({}, 0).has_value());                   // edge: empty input

    std::vector<Trade> ts{{"A", 10, 100}, {"B", 5, 1000}, {"C", 1, 50}, {"D", 20, 100}};
    auto top = top_k(ts, 2);
    CHECK_EQ(top.size(), 2u);
    CHECK_EQ(top[0].sym, "B");                            // 5000
    CHECK_EQ(top[1].sym, "D");                            // 2000
    CHECK_EQ(top_k(ts, 0).size(), 0u);                    // edge: k == 0
    CHECK_EQ(top_k(ts, 99).size(), 4u);                   // edge: k > n

    Book b;
    CHECK(!b.best_bid().has_value());
    b.add(true, 100, 5); b.add(true, 101, 3); b.add(false, 103, 4); b.add(false, 102, 1);
    CHECK_EQ(*b.best_bid(), 101L);
    CHECK_EQ(*b.best_ask(), 102L);
    b.cancel(true, 101, 3);
    CHECK_EQ(*b.best_bid(), 100L);
}
```

```text
all tests passed
```

测试习惯：先写正常例子，再写**边界**——空输入、`k=0`、`k>n`、单元素、重复值、负数、最大值溢出、已空的订单簿。

## 3. 读懂编译错误

规则：**从第一个 `error:` 往下读，只看前几行**；后面的错误常是第一个错误的连锁反应；先修第一个再重新编译。`note:` 行告诉你候选是什么、模板在哪里实例化。

### 缺分号（类定义后）

```text
C16/c16_bad_missing_semicolon.cpp:3:27: error: expected ';' after struct
    3 | struct Point { int x, y; }                             // missing ';' after the class definition
      |                           ^
      |                           ;
1 error generated.

```

### 缺头文件

```text
C16/c16_bad_missing_include.cpp:6:23: error: no member named 'accumulate' in namespace 'std'
    6 |     std::cout << std::accumulate(v.begin(), v.end(), 0) << "\n";   // <numeric> not included
      |                       ^~~~~~~~~~
1 error generated.
```

→ `no member named 'accumulate' in namespace 'std'` 几乎一定是缺 `#include <numeric>`（同理 `setw` → `<iomanip>`，`sort` → `<algorithm>`）。

### 对 `const` 引用调用非 `const` 成员函数

```text
C16/c16_bad_const.cpp:5:30: error: 'this' argument to member function 'inc' has type 'const Counter', but function is not marked const
    5 | void use(const Counter& c) { c.inc(); }                // calling a non-const member on a const reference
      |                              ^
C16/c16_bad_const.cpp:4:34: note: 'inc' declared here
    4 | struct Counter { int n = 0; void inc() { ++n; } };
      |                                  ^
```

### 拷贝 `unique_ptr`

```text
C16/c16_bad_deleted_copy.cpp:6:26: error: call to implicitly-deleted copy constructor of 'std::unique_ptr<int>'
    6 |     std::unique_ptr<int> b = a;                        // copying a unique_ptr: the copy constructor is deleted
      |                          ^   ~
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__memory/unique_ptr.h:209:55: note: copy constructor is implicitly deleted because 'unique_ptr<int>' has a user-declared move constructor
```

→ 要转移所有权用 `std::move`。

### 参数类型不匹配

```text
C16/c16_bad_no_match.cpp:7:12: error: no matching function for call to 'add'
    7 |     return add(v, 2);                                  // vector<int> is not an int
      |            ^~~
C16/c16_bad_no_match.cpp:4:5: note: candidate function not viable: no known conversion from 'std::vector<int>' to 'int' for 1st argument
    4 | int add(int a, int b) { return a + b; }
```

### 花括号初始化的窄化

```text
C16/c16_bad_narrowing.cpp:5:11: error: non-constant-expression cannot be narrowed from type 'long' to 'int' in initializer list [-Wc++11-narrowing]
    5 |     int x{big};                                        // brace initialisation forbids narrowing conversions
      |           ^~~
C16/c16_bad_narrowing.cpp:5:11: note: insert an explicit cast to silence this issue
```

### `sort` 一个 `list`

（完整报错有几十行，这里只保留第一条 error 和提到你自己文件的行）

```text
In file included from C16/c16_bad_sort_list.cpp:2:
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__algorithm/make_heap.h:37:31: error: invalid operands to binary expression ('std::__list_iterator<int, void *>' and 'std::__list_iterator<int, void *>')
C16/c16_bad_sort_list.cpp:6:10: note: in instantiation of function template specialization 'std::sort<std::__list_iterator<int, void *>>' requested here
In file included from C16/c16_bad_sort_list.cpp:2:
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__algorithm/partial_sort.h:43:85: error: invalid operands to binary expression ('std::__list_iterator<int, void *>' and 'std::__list_iterator<int, void *>')
C16/c16_bad_sort_list.cpp:6:10: note: in instantiation of function template specialization 'std::sort<std::__list_iterator<int, void *>>' requested here
In file included from C16/c16_bad_sort_list.cpp:2:
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__algorithm/sort_heap.h:39:37: error: invalid operands to binary expression ('std::__list_iterator<int, void *>' and 'std::__list_iterator<int, void *>')
C16/c16_bad_sort_list.cpp:6:10: note: in instantiation of function template specialization 'std::sort<std::__list_iterator<int, void *>>' requested here
In file included from C16/c16_bad_sort_list.cpp:2:
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__algorithm/sort.h:867:86: error: invalid operands to binary expression ('std::__list_iterator<int, void *>' and 'std::__list_iterator<int, void *>')
C16/c16_bad_sort_list.cpp:6:10: note: in instantiation of function template specialization 'std::sort<std::__list_iterator<int, void *>>' requested here
```

→ 错误来自标准库内部（`__last - __first`），但真正原因在带你文件名的那一行（`requested here`）：`list` 迭代器不支持随机访问，用 `l.sort()`。模板错误的读法：找出带你的文件名的那一行。

## 4. 开着警告写

CoderPad 一般看不到警告，但本地要 `-Wall -Wextra`，每个警告都值得处理：

```cpp
// C16: -Wall -Wextra warnings worth fixing during the interview: each one usually points at a real bug.
#include <iostream>
#include <vector>

int sum_to(const std::vector<int>& v, int n) {
    int total = 0;
    for (int i = 0; i < v.size(); ++i)        // -Wsign-compare: int vs size_t
        total += v[i];
    int unused = 0;                           // -Wunused-variable
    if (n > 0)
        return total;
}                                             // -Wreturn-type: control reaches end of non-void function (UB if n <= 0)

int main(int argc, char**) {                  // -Wunused-parameter would fire for named but unused params
    int x;
    if (argc > 5) x = 1;
    std::cout << x << " " << sum_to({1, 2}, 1) << "\n";   // -Wsometimes-uninitialized
}
```

编译器输出：

```text
C16/c16_warnings.cpp:10:9: warning: unused variable 'unused' [-Wunused-variable]
C16/c16_warnings.cpp:8:23: warning: comparison of integers of different signs: 'int' and 'size_type' (aka 'unsigned long') [-Wsign-compare]
C16/c16_warnings.cpp:13:1: warning: non-void function does not return a value in all control paths [-Wreturn-type]
C16/c16_warnings.cpp:17:9: warning: variable 'x' is used uninitialized whenever 'if' condition is false [-Wsometimes-uninitialized]
```

对应关系：`-Wsign-compare`（`int` 与 `size_t` 比较）、`-Wunused-variable`、`-Wreturn-type`（缺 `return`，走到末尾是 UB）、`-Wsometimes-uninitialized`（可能读未初始化变量）。

## 5. 高频陷阱

```cpp
std::vector<int> v{10, 20, 30};
// for (size_t i = v.size() - 1; i >= 0; --i)   // TRAP: size_t is unsigned, i >= 0 is always true, wraps to 2^64-1
for (std::size_t i = v.size(); i-- > 0;) std::cout << v[i] << " ";           // safe reverse loop with an unsigned index
std::cout << "\n";
std::vector<int> empty;
// empty.size() - 1 is 18446744073709551615, not -1
std::cout << "empty.size() - 1 = " << empty.size() - 1 << "; as int: " << static_cast<int>(empty.size()) - 1 << "\n";
```

```cpp
int lo = 2'000'000'000, hi = 2'100'000'000;
// int mid = (lo + hi) / 2;                      // TRAP: lo + hi overflows int (UB)
int mid = lo + (hi - lo) / 2;                    // safe midpoint
std::cout << "mid = " << mid << "\n";
```

```cpp
std::cout << "7/2 = " << 7 / 2 << ", 7.0/2 = " << 7.0 / 2 << ", -7/2 = " << -7 / 2 << ", -7%3 = " << -7 % 3
          << " (C++ truncates toward zero; % keeps the dividend's sign)\n";
long cents = 1999;
double dollars = cents / 100;                     // TRAP: integer division first -> 19
double right = cents / 100.0;
std::cout << "cents/100 = " << dollars << ", cents/100.0 = " << right << "\n";
```

```cpp
char c = '7';
int digit = c - '0';                              // char arithmetic: '7' is the number 55
std::string s = "ab";
std::cout << "digit " << digit << ", 'a'+1 = " << 'a' + 1 << " (an int!), static_cast<char>('a'+1) = " << static_cast<char>('a' + 1)
          << ", s + 'c' = " << s + 'c' << "\n";
```

```cpp
std::map<std::string, int> m;
if (m["x"] == 0) std::cout << "m[\"x\"] == 0, but size is now " << m.size() << " (operator[] inserted)\n";
std::cout << "count() does not insert: " << m.count("y") << ", size " << m.size() << "\n";
```

```cpp
std::vector<int> a(3, 7);                         // 3 elements of 7
std::vector<int> b{3, 7};                         // 2 elements: 3 and 7 (braces prefer the initializer_list constructor)
int uninit;                                       // TRAP: indeterminate value; reading it is UB
int zero{};                                       // value-initialised to 0
uninit = 5;
std::cout << "vector(3,7).size()=" << a.size() << " vector{3,7}.size()=" << b.size() << " zero=" << zero << " uninit=" << uninit << "\n";
```

```text
30 20 10 
empty.size() - 1 = 18446744073709551615; as int: -1
mid = 2050000000
7/2 = 3, 7.0/2 = 3.5, -7/2 = -3, -7%3 = -1 (C++ truncates toward zero; % keeps the dividend's sign)
cents/100 = 19, cents/100.0 = 19.99
digit 7, 'a'+1 = 98 (an int!), static_cast<char>('a'+1) = b, s + 'c' = abc
m["x"] == 0, but size is now 1 (operator[] inserted)
count() does not insert: 0, size 1
vector(3,7).size()=3 vector{3,7}.size()=2 zero=0 uninit=5
```

* `size_t` 是无符号：`v.size() - 1` 在空容器上是 18446744073709551615，`i >= 0` 对无符号永远为真。倒序用 `for (size_t i = n; i-- > 0;)`，或转成 `int`。
* 中点：`lo + (hi - lo) / 2`。
* 整数除法截断；金额用整数分。
* `'a' + 1` 是 `int`；`s + 'c'` 才是字符串拼接。
* `map::operator[]` 查询会插入；只查用 `find`/`count`/`contains`。
* `vector<int>(3, 7)` vs `vector<int>{3, 7}`。

## 6. 时间管理与沟通

* 先写**最直接可行的解**（哪怕 O(n²)），说出复杂度，再优化；先让测试过。
* 变量命名清楚；在容器类型和复杂度上口头说明理由（"用 `unordered_map` 是因为只需要点查，平均 O(1)"）。
* 用 `auto`、范围 `for`、结构化绑定减少样板，但类型不明显时写出来。
* 卡住时：把问题缩小到一个小例子手算；询问提示不丢分。
* 不要和编译器较劲超过一两分钟：换更简单的写法（例如回退到传统 `for`）。

## 7. 面试官接着会问

**Q：你的解法复杂度？空间？能优化吗？**
要点：先答 O(·)；再说瓶颈（哈希 vs 排序 vs 堆）；"k 很小用堆，k 接近 n 用排序/`nth_element`"。

**Q：为什么用 `unordered_map` 不用 `map`？反之？**
要点：只需点查 → `unordered_map` 平均 O(1)；要有序遍历/范围查询/最小最大 → `map` O(log n)；自定义 key 要提供哈希和 `==`。

**Q：这段代码有什么 UB 风险？**
要点：越界、迭代器失效、整数溢出、悬空引用、未初始化。

**Q：怎么测试你的代码？**
要点：正常 / 边界 / 大输入 / 对拍（暴力解对比）。

**Q：如果输入很大，会怎么改？**
要点：快速 I/O、`reserve`、避免拷贝（`const&`、`move`）、选择连续容器。

## 8. 自测

1. 编译报了 20 个错误，从哪里开始？
2. 为什么自己写 `CHECK` 宏比 `assert` 安全？
3. `for (size_t i = n - 1; i >= 0; --i)` 错在哪？
4. `std::sort(l.begin(), l.end())` 对 `std::list` 为什么编译失败？

<details><summary>答案</summary>

1. 第一个 `error:`；其余多半是连锁错误；修完重编。
2. `NDEBUG` 下 `assert` 被移除，测试变成空操作；`CHECK` 总是执行。
3. `size_t` 无符号，`i >= 0` 永远为真，且 `n==0` 时 `n-1` 回绕；写 `for (size_t i = n; i-- > 0;)`。
4. `std::sort` 需要随机访问迭代器；`list` 只有双向迭代器，应使用 `l.sort()`。

</details>
