# C06 · 算法、lambda 与 ranges

> 目标：会用 `<algorithm>`/`<numeric>` 写出短而对的代码；理解 lambda 的捕获与生命周期；知道 C++20 ranges 是什么、和 Java Stream 有何不同。

## 1. Java 对照

| Java | C++ |
|---|---|
| `Collections.sort(list, cmp)` | `std::sort(v.begin(), v.end(), cmp)` |
| `Collections.binarySearch` | `std::lower_bound` / `upper_bound` / `binary_search` |
| `list.stream().filter().map().collect()` | `v \| views::filter(..) \| views::transform(..)`（C++20） |
| `Comparator.comparing(...)` | lambda 或 ranges 的**投影**（projection） |
| 匿名内部类 / lambda | lambda（可显式选择按值/按引用捕获） |

C++ 算法接受**迭代器区间** `[first, last)`，不依赖具体容器，且与 lambda 一起会被**内联**，没有装箱、没有虚调用。

## 2. 常用算法速览

```cpp
std::vector<Trade> ts{{"MSFT", 50, 410.0}, {"AAPL", 100, 187.5}, {"NVDA", 10, 900.0}, {"AAPL", 20, 188.0}};
std::sort(ts.begin(), ts.end(), [](const Trade& a, const Trade& b) {
    if (a.sym != b.sym) return a.sym < b.sym;        // must be a strict weak ordering: never use <=
    return a.qty * a.px > b.qty * b.px;              // then by notional, descending
});
for (auto& t : ts) std::cout << "  " << t.sym << " " << t.qty << " @ " << t.px << "\n";
```

* `sort` 平均 O(n log n)，不稳定；要稳定用 `stable_sort`。比较器必须是**严格弱序**（`a<b` 不能写成 `a<=b`）。

```cpp
std::vector<int> v{1, 3, 3, 5, 8, 13, 21};            // sorted
auto lo = std::lower_bound(v.begin(), v.end(), 3);    // first element >= 3
auto hi = std::upper_bound(v.begin(), v.end(), 3);    // first element >  3
std::cout << "  lower_bound(3) index " << lo - v.begin() << ", upper_bound(3) index " << hi - v.begin()
          << ", count " << hi - lo << ", binary_search(8)=" << std::binary_search(v.begin(), v.end(), 8) << "\n";
```

* 二分只用于**已排序**区间：`lower_bound` 返回第一个 `>= x`，`upper_bound` 返回第一个 `> x`；两者之差就是相等元素个数。

```cpp
std::vector<int> big(10, 1'000'000'000);
// std::accumulate(big.begin(), big.end(), 0) would sum in INT (init's type) and overflow: see c06_accumulate_ub.cpp
long long right = std::accumulate(big.begin(), big.end(), 0LL);     // init type decides the accumulator type
std::cout << "  sum with 0LL init: " << right << "\n";
```

* **`accumulate` 的累加器类型 = 初值的类型**。`accumulate(first, last, 0)` 用 `int` 累加，元素较大时溢出（有符号溢出是 UB）：

```cpp
// C06: std::accumulate's accumulator type is the TYPE OF THE INIT VALUE, not the element type or the destination.
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> big(10, 1'000'000'000);
    long long wrong = std::accumulate(big.begin(), big.end(), 0);      // 0 is an int: every partial sum is an int
    std::cout << "sum with int init: " << wrong << "  (signed overflow = undefined behaviour)\n";
}
```

```text
/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__numeric/accumulate.h:30:32: runtime error: signed integer overflow: 2000000000 + 1000000000 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1/__numeric/accumulate.h:30:32 
```

```cpp
std::vector<int> w{9, 4, 7, 1, 8, 2, 6};
std::nth_element(w.begin(), w.begin() + 3, w.end());                 // O(n): w[3] is the 4th smallest, rest partitioned
std::cout << "  4th smallest via nth_element: " << w[3] << "\n";
std::partial_sort(w.begin(), w.begin() + 3, w.end());                // smallest 3, sorted
show("first three sorted", std::vector<int>(w.begin(), w.begin() + 3));
auto mid = std::stable_partition(w.begin(), w.end(), [](int x) { return x % 2 == 0; });
std::cout << "  evens before odds, " << mid - w.begin() << " evens\n";
```

* `nth_element` O(n) 找第 k 小；`partial_sort` 只排前 k 个；`partition` 按谓词分组。求 top-k、中位数别全排序。

```cpp
std::vector<int> u{1, 1, 2, 2, 2, 3, 1};
u.erase(std::unique(u.begin(), u.end()), u.end());                   // removes CONSECUTIVE duplicates only
show("unique", u);
std::vector<int> seq(5);
std::iota(seq.begin(), seq.end(), 10);
std::vector<int> prefix(seq.size());
std::partial_sum(seq.begin(), seq.end(), prefix.begin());
show("iota", seq); show("prefix sums", prefix);
auto [mn, mx] = std::minmax_element(seq.begin(), seq.end());
std::cout << "  min " << *mn << " max " << *mx << "\n";
std::string perm = "abc";
std::cout << "  permutations:";
do { std::cout << " " << perm; } while (std::next_permutation(perm.begin(), perm.end()));
std::cout << "\n";
```

* `unique` 只去**相邻**重复，通常先 `sort`；`erase(unique(...), end)` 才真正删。`iota` 填递增序列，`partial_sum` 前缀和，`next_permutation` 枚举排列。

```cpp
std::priority_queue<int> maxheap;                                      // C++ default is a MAX-heap (Java's is a min-heap)
for (int x : {5, 1, 9, 3}) maxheap.push(x);
std::cout << "  maxheap top " << maxheap.top();
std::priority_queue<int, std::vector<int>, std::greater<int>> minheap;  // Java's PriorityQueue default
for (int x : {5, 1, 9, 3}) minheap.push(x);
std::cout << ", minheap top " << minheap.top() << "\n";
auto cmp = [](const Trade& a, const Trade& b) { return a.qty * a.px > b.qty * b.px; };   // "greater" => min-heap by notional
std::priority_queue<Trade, std::vector<Trade>, decltype(cmp)> top3(cmp);
for (auto& t : ts) { top3.push(t); if (top3.size() > 3) top3.pop(); }  // keep the 3 largest notionals
std::cout << "  top-3 notional kept, smallest of them: " << top3.top().sym << " " << top3.top().qty * top3.top().px << "\n";
```

* **`priority_queue` 默认大顶堆**（Java 的 `PriorityQueue` 默认小顶堆）。自定义比较器的含义是"**谁排在下面**"：传 `greater` 得小顶堆。保持 k 个最大值用小顶堆，满了就弹堆顶。

```text
  AAPL 100 @ 187.5
  AAPL 20 @ 188
  MSFT 50 @ 410
  NVDA 10 @ 900
  lower_bound(3) index 1, upper_bound(3) index 3, count 2, binary_search(8)=1
  sum with 0LL init: 10000000000
  4th smallest via nth_element: 6
  first three sorted: 1 2 4
  evens before odds, 4 evens
  unique: 1 2 3 1
  iota: 10 11 12 13 14
  prefix sums: 10 21 33 46 60
  min 10 max 14
  permutations: abc acb bac bca cab cba
  maxheap top 9, minheap top 1
  top-3 notional kept, smallest of them: NVDA 9000
```

## 3. lambda

lambda 是**编译器生成的匿名函数对象类**：`[捕获](参数){ 函数体 }`。每个 lambda 有独一无二的类型，所以 `auto` 或模板参数接收它时可以完全内联；`std::function` 则把类型擦除，换来统一类型但多一次间接调用（可能还有堆分配）。

```cpp
void captures() {
    int x = 10;
    auto by_val = [x] { return x; };              // copies x at creation: later changes are invisible
    auto by_ref = [&x] { return x; };             // refers to the live x: dangles if the lambda outlives x
    x = 20;
    std::cout << "  by value " << by_val() << ", by reference " << by_ref() << "\n";

    int counter = 0;
    auto inc = [counter]() mutable { return ++counter; };   // mutable: modify the lambda's own copy
    inc(); inc();
    std::cout << "  outer counter still " << counter << ", lambda's copy is at " << inc() << "\n";

    auto owned = std::make_unique<int>(5);
    auto taker = [p = std::move(owned)] { return *p * 2; };  // init-capture (C++14): move-only capture
    std::cout << "  moved-in capture: " << taker() << ", owned is " << (owned ? "set" : "null") << "\n";
}
```

* `[x]` 按值：创建时复制，之后外部改变不可见；`[&x]` 按引用：看得到外部变化，但 lambda 活得比 `x` 久就**悬空**；`[=]`/`[&]` 全部按值/按引用（容易误捕获 `this`，不推荐滥用）。
* 按值捕获的变量在 lambda 里默认是 `const`；`mutable` 允许改**lambda 自己的副本**。
* 初始化捕获 `[p = std::move(owned)]`（C++14）是把 move-only 对象（`unique_ptr`）放进 lambda 的唯一办法。

```cpp
void generic_and_recursion() {
    auto add = [](auto a, auto b) { return a + b; };         // generic lambda (C++14): a template operator()
    std::cout << "  " << add(1, 2) << " " << add(1.5, 2.25) << " " << add(std::string("a"), std::string("b")) << "\n";
    auto fact = [](auto&& self, int n) -> long { return n <= 1 ? 1 : n * self(self, n - 1); };   // recursion without std::function
    std::cout << "  10! = " << fact(fact, 10) << "\n";
    int v = [] { return 6 * 7; }();                          // immediately-invoked: initialise a const with logic
    std::cout << "  IIFE " << v << "\n";
}
```

* 参数写 `auto` = 泛型 lambda（编译器生成模板化的 `operator()`）。
* 递归 lambda：把自己作为参数传入（上面 `fact(fact, 10)`），避免 `std::function`。

```cpp
void what_a_lambda_is() {
    int a = 1, b = 2;
    auto empty = [] { return 1; };
    auto two = [a, b] { return a + b; };
    auto big = [arr = std::vector<int>(100)] { return arr.size(); };
    std::function<int()> f = two;
    std::cout << "  sizeof: empty lambda " << sizeof(empty) << ", [a,b] " << sizeof(two) << ", [vector] " << sizeof(big)
              << ", std::function " << sizeof(f) << "\n";
    // A lambda has its own unique type, so a template parameter or `auto` call inlines it. std::function erases the
    // type behind an indirect call (and may heap-allocate a large capture): use it to STORE callbacks, not in hot loops.
}
```

```cpp
std::function<int()> make_counter() {
    int n = 0;
    return [n]() mutable { return ++n; };          // by VALUE: safe to return. [&n] here would dangle (UB).
}
```

```text
  by value 10, by reference 20
  outer counter still 0, lambda's copy is at 3
  moved-in capture: 10, owned is null
  3 3.75 ab
  10! = 3628800
  IIFE 42
  sizeof: empty lambda 1, [a,b] 8, [vector] 24, std::function 32
  returned counter: 3
```

* 无捕获 lambda 大小为 1（空类）；每个捕获占相应字节；`std::function` 在这个标准库里是 32 字节（带小对象缓冲，大小因实现而异）。
* **返回 lambda 一定按值捕获**；`[&n]` 返回局部变量引用 = 悬空。

## 4. ranges（C++20）

* **range** = 任何有 `begin()/end()` 的东西；**view** = 轻量、**惰性**的 range，不拥有元素也不分配。`|` 把它们串成管线，只在遍历时才一个元素一个元素地计算（和 Java Stream 类似，但没有装箱、没有中间集合）。
* `std::ranges::sort(v)` 等算法直接收容器；**投影**参数让你按成员排序而不写比较器。

```cpp
std::vector<int> v{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
auto pipeline = v | rv::filter([](int x) { return x % 2 == 0; })
                  | rv::transform([](int x) { return x * x; })
                  | rv::take(3);                          // NOTHING has run yet: views are lazy descriptions
std::cout << "  squares of the first three evens:";
for (int x : pipeline) std::cout << " " << x;             // the work happens here, element by element, no temp vectors
std::cout << "\n";
```

```cpp
long total = 0;
for (long i : rv::iota(1, 1'000'001) | rv::filter([](long i) { return i % 3 == 0; })) total += i;   // no vector of 1M ints
std::cout << "  sum of multiples of 3 up to 1,000,000: " << total << "\n";
```

```cpp
std::vector<Fill> fills{{"MSFT", 50}, {"AAPL", 100}, {"NVDA", 10}};
rg::sort(fills, {}, &Fill::qty);                          // sort by a member: comparator-free projection
std::cout << "  by qty:";
for (auto& f : fills) std::cout << " " << f.sym;
auto it = rg::find(fills, "AAPL", &Fill::sym);
std::cout << "; AAPL at index " << it - fills.begin() << "\n";
auto mx = rg::max_element(fills, {}, &Fill::qty);
std::cout << "  max qty: " << mx->sym << "\n";
```

```cpp
auto bad = rg::find(std::vector<int>{1, 2, 3}, 2);        // temporary container: result is rg::dangling, not an iterator
static_assert(std::is_same_v<decltype(bad), rg::dangling>);
std::cout << "  find on a temporary returns ranges::dangling (use of it will not compile)\n";
```

```cpp
std::string csv = "AAPL,MSFT,NVDA";
std::cout << "  split:";
for (auto part : csv | rv::split(',')) std::cout << " [" << std::string(part.begin(), part.end()) << "]";
std::cout << "\n  reversed keys:";
for (int x : v | rv::reverse | rv::take(3)) std::cout << " " << x;
std::cout << "\n";
```

```text
  squares of the first three evens: 4 16 36
  sum of multiples of 3 up to 1,000,000: 166666833333
  by qty: NVDA MSFT AAPL; AAPL at index 2
  max qty: AAPL
  find on a temporary returns ranges::dangling (use of it will not compile)
  split: [AAPL] [MSFT] [NVDA]
  reversed keys: 10 9 8
```

注意：C++20 的 views 不含 `zip`/`enumerate`/`to<vector>`（C++23 才有）；视图遍历期间底层容器不能被修改；视图上的 `filter` 缓存 `begin()`，多次遍历的复杂度要小心。

## 5. 坑

1. 比较器不是严格弱序（用了 `<=`、或比较浮点 NaN）→ `sort` 越界崩溃/死循环。
2. `accumulate` 初值类型决定累加类型（`0` vs `0LL` vs `0.0`；对 `double` 用 `0` 会逐步截断成整数）。
3. 对**未排序**区间用 `lower_bound`/`binary_search` = 结果无意义。
4. `remove`/`unique` 只是把要保留的元素前移，不改变容器大小，必须配 `erase`。
5. lambda 按引用捕获后离开作用域再调用（线程、回调、返回值）→ 悬空。
6. `priority_queue` 的比较器方向与直觉相反。
7. 对临时容器用 ranges 算法返回 `dangling` 迭代器。

## 6. 面试官接着会问

**Q：lambda 是什么？和函数指针、`std::function` 的区别？**
要点：编译器生成的函数对象类；独有类型、可内联、可带状态；函数指针无状态；`std::function` 类型擦除（可存任意可调用对象，间接调用，大捕获可能堆分配）。热路径用模板参数/`auto`，存回调用 `std::function`。

**Q：值捕获和引用捕获的风险？**
要点：悬空；线程中尤甚；`this` 的隐式捕获；`[=]` 不会复制成员变量而是捕获 `this`。

**Q：`std::sort` 为什么比 `qsort` 快？**
要点：比较器在编译期已知，可内联；`qsort` 通过函数指针对每次比较做间接调用。

**Q：ranges 比 Stream 好在哪里？**
要点：惰性视图零分配；与迭代器兼容；编译期展开；但调试/报错更难读，C++20 缺少一些视图。

**Q：怎么求 top-k？**
要点：小顶堆维护 k 个，O(n log k)；或 `nth_element` O(n) 平均。

## 7. 自测

1. `std::accumulate(v.begin(), v.end(), 0.0)` 与 `0` 有何不同？
2. `[=]` 在成员函数里捕获了什么？有什么风险？
3. `sort` 的比较器写成 `a <= b` 会怎样？
4. 如何得到小顶堆 `priority_queue<int>`？

<details><summary>答案</summary>

1. 累加器类型：`0.0` 用 double，`0` 用 int（对 double 元素逐次截断）。
2. 捕获 `this` 指针（成员实际按引用访问）；对象销毁后调用 lambda = 悬空。C++20 起 `[=]` 隐式捕获 `this` 已被弃用，应写 `[this]` 或 `[*this]`。
3. 违反严格弱序，相等元素比较返回 true，可能越界读写或崩溃（UB）。
4. `std::priority_queue<int, std::vector<int>, std::greater<int>>`。

</details>
