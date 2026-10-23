# hc09 · 按 notional 取 top-k 成交 / ticker（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

一天里交易所产生很多成交事件（trade event），以三个**平行数组**（parallel arrays）给出：第 `i` 个事件是 `(tickers[i], prices[i], volumes[i])`。一个事件的 **notional**（名义金额）= `price × volume`。价格是整数 tick（比如 1 tick = 1 美分），数量是整数股数，所以 notional 是精确的 `long long`，没有浮点误差。价格、数量 ≥ 0；乘法和累加**溢出就报错**，绝不静默回绕。

| Part | 内容 |
|---|---|
| 1 | top-k **事件**：大小为 k 的堆 + 完整 tie-break + 溢出检查；再对比 `partial_sort` / `nth_element` / 整体排序 |
| 2 | 按 ticker 聚合后取 top-k；一趟遍历同时算「总额」和「最大事件」 |
| 3 | 流式：成交按时间到达，只看滑动窗口内的，旧成交过期，随时报 top-k ticker |
| 4 | 两千万条数据怎么用多核：切块并行聚合，最后合并；异常、取消、溢出 |

排序规则（Part 1）：notional **大**的在前；notional 相同，ticker 字典序**升序**；再相同，下标升序。三条合起来是**全序**（total order），结果唯一、可复现。

| 下标 | ticker | price | volume | notional |
|---|---|---|---|---|
| 0 | AAPL | 18000 | 10 | 180000 |
| 1 | MSFT | 40000 | 3 | 120000 |
| 2 | AAPL | 18100 | 5 | 90500 |
| 3 | GOOG | 14000 | 9 | 126000 |
| 4 | MSFT | 40000 | 3 | 120000 |
| 5 | TSLA | 25000 | 8 | 200000 |

* top 3 事件：`[TSLA(i=5, 200000), AAPL(i=0, 180000), GOOG(i=3, 126000)]`
* top 4 事件：第 4 名是 i=1 不是 i=4：notional 与 ticker 都相同（MSFT, 120000），下标小的在前。
* top 2 ticker：`[AAPL 270500, MSFT 240000]`（TSLA 200000、GOOG 126000 落选）。

注意：最大的**事件**（TSLA）不属于最大的 **ticker**（AAPL）。两个问题，两个答案。

## 2. Part 1：top-k 事件

### 2.1 为什么取最大的 k 个要用「最小」堆

堆（heap）是一棵数组存的树，**堆顶永远是「最大」的那个**——这里「大」由比较器决定。我们让比较器把「更差」的事件当作「更大」，于是堆顶就是**目前保留的 k 个里最差的**。

* 来了一个新事件：如果它连堆顶（最差的保留者）都不如，直接丢掉——这是**快速拒绝**（fast reject），只花一次整数比较；
* 如果比堆顶好：弹出堆顶，压入新事件，`O(log k)`；
* 扫完 n 个事件，总共 `O(n log k)` 时间、`O(k)` 空间。随机顺序下绝大多数事件连堆都进不去。

手算样例 k = 3：依次看 `180000, 120000, 90500`（堆满，堆顶 = 90500）→ `126000 > 90500`，换掉 90500 → `120000`（i=4）不如堆顶 120000（i=1）（notional 同、ticker 同、下标 4 > 1，所以 i=4 更差）→ 丢掉 → `200000` 比堆顶 120000（i=1）好，换掉 → 最终 {200000, 180000, 126000}。

C++ 的 `std::priority_queue<T, Container, Compare>`：`Compare(a, b)` 为真表示「a 排在 b **前面**」，`top()` 返回排在**最后**的元素（默认 `std::less` 下就是最大值）。我们把 `better(a, b)`（a 比 b 好）当作 `Compare` 传进去，于是排在最后的——`top()`——是**最差的保留者**，正是要的。

### 2.2 tie-break 必须写全：全序

只按 notional 比较，notional 相同的事件谁留谁走取决于**到达顺序**——同一批数据换个顺序，答案就变了。下面用 3 个 notional 都是 100 的事件、只能留 2 个：

```cpp
// A comparator that ignores ties makes top-k depend on the order the data arrives in.  A full order does not.
#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

struct Event { int index; std::string ticker; long long notional; };

// Keep the 2 best by notional only (larger is better): the heap top is the worst kept event.
std::vector<int> top2_notional_only(const std::vector<Event>& events) {
    auto better = [](const Event* a, const Event* b) { return a->notional > b->notional; };
    std::priority_queue<const Event*, std::vector<const Event*>, decltype(better)> heap(better);
    for (const Event& e : events) {
        if (heap.size() < 2) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top()->index); heap.pop(); }
    std::sort(out.begin(), out.end());
    return out;
}

// Same, with the full order: notional descending, then ticker ascending, then index ascending.
std::vector<int> top2_full_order(const std::vector<Event>& events) {
    auto better = [](const Event* a, const Event* b) {
        if (a->notional != b->notional) return a->notional > b->notional;
        if (a->ticker != b->ticker) return a->ticker < b->ticker;
        return a->index < b->index;
    };
    std::priority_queue<const Event*, std::vector<const Event*>, decltype(better)> heap(better);
    for (const Event& e : events) {
        if (heap.size() < 2) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top()->index); heap.pop(); }
    std::sort(out.begin(), out.end());
    return out;
}

void show(const char* label, const std::vector<int>& v) {
    std::cout << label;
    for (int i : v) std::cout << " " << i;
    std::cout << "\n";
}

int main() {
    // Three events tie at notional 100; only two can stay.
    std::vector<Event> forward = {{0, "AAA", 100}, {1, "BBB", 100}, {2, "CCC", 100}};
    std::vector<Event> reversed = {{2, "CCC", 100}, {1, "BBB", 100}, {0, "AAA", 100}};
    show("notional only, forward :", top2_notional_only(forward));
    show("notional only, reversed:", top2_notional_only(reversed));
    show("full order,    forward :", top2_full_order(forward));
    show("full order,    reversed:", top2_full_order(reversed));
}
```

输出：

```text
notional only, forward : 0 1
notional only, reversed: 1 2
full order,    forward : 0 1
full order,    reversed: 0 1
```

只按 notional 时，正序和倒序输入留下的集合**不同**；加上 ticker、下标（全序）之后一致。面试时一句话：**top-k 的比较器必须是全序，否则结果取决于输入顺序，没法测试也没法复现。**

ticker 的比较是**按字节（unsigned char）字典序**：`std::string` / `std::string_view` 的 `compare` 把每个字节当无符号数比，所以 UTF-8 的 `"\xC3\xA9"` 排在 `"Z"` 之后；空串排最前；字符串里嵌入的 `'\0'` 是名字的一部分（`string_view` 带长度，`strcmp` 不带——别用 `strcmp`）。

### 2.3 溢出：`__builtin_mul_overflow`

`price * volume` 对两个 `long long` 是**有符号溢出 = 未定义行为**（UB），不是「回绕成负数」——编译器可以假设它不发生。检查必须在乘法**之前或同时**完成：clang/gcc 的 `__builtin_mul_overflow(a, b, &r)` 做乘法并告诉你是否溢出，不触发 UB。

```cpp
// Signed overflow is undefined behaviour; unsigned wraps.  __builtin_mul_overflow reports the overflow without invoking UB.
#include <climits>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error(std::to_string(a) + " * " + std::to_string(b));
    return r;
}

int main() {
    const long long a = LLONG_MAX, b = 2;
    // The wrong way, made visible without UB: do the product in unsigned 64-bit arithmetic and reinterpret.
    const auto wrapped = static_cast<long long>(static_cast<unsigned long long>(a) * static_cast<unsigned long long>(b));
    std::cout << "LLONG_MAX * 2 wrapped to " << wrapped << " (a negative notional)\n";
    // The right way.
    try {
        (void)mul_exact(a, b);
    } catch (const std::overflow_error& e) {
        std::cout << "mul_exact threw overflow_error: " << e.what() << "\n";
    }
    std::cout << "3037000499^2 = " << mul_exact(3037000499LL, 3037000499LL) << "\n";
    try {
        (void)mul_exact(3037000500LL, 3037000500LL);
    } catch (const std::overflow_error&) {
        std::cout << "3037000500^2 overflows\n";
    }
    // int * int is also signed: price (int) * volume (int) overflows at 46341 * 46341, even if the result is stored in a long long.
    const int p = 46341, v = 46341;
    int as_int;
    std::cout << "46341 * 46341 overflows int: " << (__builtin_mul_overflow(p, v, &as_int) ? "yes" : "no") << "\n";
    std::cout << "as long long: " << static_cast<long long>(p) * v << "\n";
}
```

```text
LLONG_MAX * 2 wrapped to -2 (a negative notional)
mul_exact threw overflow_error: 9223372036854775807 * 2
3037000499^2 = 9223372030926249001
3037000500^2 overflows
46341 * 46341 overflows int: yes
as long long: 2147488281
```

`floor(sqrt(LLONG_MAX)) = 3037000499`：它的平方能装下，`3037000500` 的平方不行——面试官爱用这个边界。还要注意 `int * int` 在被转成 `long long` **之前**就已经溢出（最后两行）。

另一条规则：**每个事件都要校验、都要算 notional，即使它进不了 top-k**。否则排在最后的那个溢出事件会被漏掉。负的价格/数量在乘法**之前**拒绝（`LLONG_MIN * -1` 也是 UB）。

### 2.4 代码（类型、校验、Part 1）

输入是 `std::span<const std::string_view>` 和两个 `std::span<const long long>`：`span` 是「指针 + 长度」的视图，`vector` 可以直接传进去，**不复制**；`string_view` 同理，函数只在调用期间**借用**文本。结果里的 `Trade` / `TickerTotal` 持有自己的 `std::string`，所以调用方可以在结果还活着的时候销毁输入。

```cpp
#include <algorithm>
#include <array>
#include <climits>
#include <cstddef>
#include <deque>
#include <exception>
#include <functional>
#include <future>
#include <mutex>
#include <optional>
#include <queue>
#include <set>
#include <span>
#include <stdexcept>
#include <stop_token>
#include <string>
#include <string_view>
#include <thread>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace toptrades {

// The three parallel arrays.  string_view: the caller owns the text, the functions only borrow it for the call.
using Strings = std::span<const std::string_view>;
using Longs = std::span<const long long>;

inline long long mul_exact(long long a, long long b) {
    long long r;
    if (__builtin_mul_overflow(a, b, &r)) throw std::overflow_error("multiplication overflow: " + std::to_string(a) + " * " + std::to_string(b));
    return r;
}
inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow: " + std::to_string(a) + " + " + std::to_string(b));
    return r;
}

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

/// One trade.  The constructor validates, so an existing Trade never has a negative field or an overflowing notional.
struct Trade {
    int index;
    std::string ticker;  // owned copy: results outlive the input arrays
    long long price, volume;

    Trade(int index, std::string ticker, long long price, long long volume)
        : index(index), ticker(std::move(ticker)), price(price), volume(volume) {
        if (index < 0) throw std::invalid_argument("index must be >= 0: " + std::to_string(index));
        if (price < 0) throw std::invalid_argument("negative price: " + std::to_string(price));
        if (volume < 0) throw std::invalid_argument("negative volume: " + std::to_string(volume));
        mul_exact(price, volume);
    }
    long long notional() const { return mul_exact(price, volume); }
    friend bool operator==(const Trade&, const Trade&) = default;
};

struct TickerTotal {
    std::string ticker;
    long long notional;
    TickerTotal(std::string ticker, long long notional) : ticker(std::move(ticker)), notional(notional) {
        if (notional < 0) throw std::invalid_argument("negative notional: " + std::to_string(notional));
    }
    friend bool operator==(const TickerTotal&, const TickerTotal&) = default;
};

struct Summary {
    long long grand_total;
    std::optional<Trade> largest;
    friend bool operator==(const Summary&, const Summary&) = default;
};

/// "a goes before b": larger notional first, then ticker ascending (bytewise), then index ascending.  A strict total
/// order: no two different trades are equivalent, so every algorithm below returns the same, reproducible list.
struct BestFirst {
    bool operator()(const Trade& a, const Trade& b) const {
        const long long na = a.notional(), nb = b.notional();
        if (na != nb) return na > nb;
        if (const int c = a.ticker.compare(b.ticker); c != 0) return c < 0;
        return a.index < b.index;
    }
};

/// Same idea for ticker totals (tickers are unique in a table, so two criteria are a total order).
struct BestTickerFirst {
    bool operator()(const TickerTotal& a, const TickerTotal& b) const {
        if (a.notional != b.notional) return a.notional > b.notional;
        return a.ticker < b.ticker;
    }
};

/// Checks the arrays and k, returns the number of events.
inline std::size_t check_inputs(Strings tickers, Longs prices, Longs volumes, int k) {
    if (tickers.size() != prices.size() || prices.size() != volumes.size())
        throw std::invalid_argument("length mismatch: " + std::to_string(tickers.size()) + " tickers, " +
                                    std::to_string(prices.size()) + " prices, " + std::to_string(volumes.size()) + " volumes");
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    if (tickers.size() > static_cast<std::size_t>(INT_MAX)) throw std::invalid_argument("too many events for an int index");
    return tickers.size();
}

/// Notional of event i: non-negative inputs, multiplication overflow -> std::overflow_error.
inline long long notional_at(Strings, Longs prices, Longs volumes, std::size_t i) {
    if (prices[i] < 0) throw std::invalid_argument("negative price at " + std::to_string(i) + ": " + std::to_string(prices[i]));
    if (volumes[i] < 0) throw std::invalid_argument("negative volume at " + std::to_string(i) + ": " + std::to_string(volumes[i]));
    return mul_exact(prices[i], volumes[i]);
}
```

下面是 Part 1：堆版本、整体排序基线、`partial_sort`、`nth_element`。

```cpp
namespace detail {

struct Key {  // what the heap stores: 16 bytes, no string copy
    long long notional;
    int index;
};

inline Trade make_trade(Strings t, Longs p, Longs v, int i) {
    return Trade(i, std::string(t[static_cast<std::size_t>(i)]), p[static_cast<std::size_t>(i)], v[static_cast<std::size_t>(i)]);
}

/// All notionals (validating every event) plus the full-order comparison on event indices: O(n) space, used by the
/// sort-based variants.
struct Ranked {
    Strings tickers;
    std::vector<long long> notional;
    Ranked(Strings t, Longs p, Longs v) : tickers(t) {
        notional.reserve(t.size());
        for (std::size_t i = 0; i < t.size(); ++i) notional.push_back(notional_at(t, p, v, i));
    }
    bool better(int a, int b) const {
        const long long na = notional[static_cast<std::size_t>(a)], nb = notional[static_cast<std::size_t>(b)];
        if (na != nb) return na > nb;
        if (const int c = tickers[static_cast<std::size_t>(a)].compare(tickers[static_cast<std::size_t>(b)]); c != 0) return c < 0;
        return a < b;
    }
    std::vector<int> indices() const {
        std::vector<int> idx(notional.size());
        for (std::size_t i = 0; i < idx.size(); ++i) idx[i] = static_cast<int>(i);
        return idx;
    }
};

inline std::vector<Trade> materialize(const std::vector<int>& idx, std::size_t m, Strings t, Longs p, Longs v) {
    std::vector<Trade> out;
    out.reserve(m);
    for (std::size_t i = 0; i < m; ++i) out.push_back(make_trade(t, p, v, idx[i]));
    return out;
}

}  // namespace detail

/// The k best events, best first.  A bounded heap whose top is the WORST event kept so far: O(n log k) time, O(k) space.
/// Every event is validated and its notional computed, even when it cannot make the top k.
inline std::vector<Trade> top_events(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const auto cap = static_cast<std::size_t>(k);
    auto better = [&](const detail::Key& a, const detail::Key& b) {  // "a is better than b"
        if (a.notional != b.notional) return a.notional > b.notional;
        if (const int c = tickers[static_cast<std::size_t>(a.index)].compare(tickers[static_cast<std::size_t>(b.index)]); c != 0) return c < 0;
        return a.index < b.index;
    };
    // priority_queue's top() is the element that compares greatest.  "Greatest" under `better` = the worst event.
    std::vector<detail::Key> storage;
    storage.reserve(std::min(cap, n));  // never reserve k itself: k may be INT_MAX
    std::priority_queue<detail::Key, std::vector<detail::Key>, decltype(better)> heap(better, std::move(storage));
    for (std::size_t i = 0; i < n; ++i) {
        const long long notional = notional_at(tickers, prices, volumes, i);
        if (cap == 0) continue;
        if (heap.size() == cap && notional < heap.top().notional) continue;  // fast reject: no allocation, no string compare
        const detail::Key cand{notional, static_cast<int>(i)};
        if (heap.size() < cap) {
            heap.push(cand);
        } else if (better(cand, heap.top())) {
            heap.pop();
            heap.push(cand);
        }
    }
    std::vector<int> worst_first;
    worst_first.reserve(heap.size());
    while (!heap.empty()) { worst_first.push_back(heap.top().index); heap.pop(); }
    std::reverse(worst_first.begin(), worst_first.end());
    return detail::materialize(worst_first, worst_first.size(), tickers, prices, volumes);
}

/// Baseline: sort every event index, take the prefix.  O(n log n) time, O(n) space.
inline std::vector<Trade> top_events_sorted(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    std::sort(idx.begin(), idx.end(), [&](int a, int b) { return r.better(a, b); });
    return detail::materialize(idx, std::min(static_cast<std::size_t>(k), n), tickers, prices, volumes);
}

/// std::partial_sort: a heap of the first m, sifted by the rest, then sorted.  O(n log m) time, O(n) space for the indices.
inline std::vector<Trade> top_events_partial_sort(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    const std::size_t m = std::min(static_cast<std::size_t>(k), n);
    std::partial_sort(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m), idx.end(), [&](int a, int b) { return r.better(a, b); });
    return detail::materialize(idx, m, tickers, prices, volumes);
}

/// std::nth_element (introselect, O(n) average) puts the m best in front in ANY order; then sort just that prefix.
inline std::vector<Trade> top_events_nth_element(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    const detail::Ranked r(tickers, prices, volumes);
    auto idx = r.indices();
    const std::size_t m = std::min(static_cast<std::size_t>(k), n);
    auto cmp = [&](int a, int b) { return r.better(a, b); };
    if (m > 0 && m < n) std::nth_element(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m - 1), idx.end(), cmp);
    std::sort(idx.begin(), idx.begin() + static_cast<std::ptrdiff_t>(m), cmp);
    return detail::materialize(idx, m, tickers, prices, volumes);
}
```

要点：

1. 堆里放的是 16 字节的 `Key{notional, index}`，**不是** `Trade`：`Trade` 带一个 `std::string`，移动/比较都更贵；比较 ticker 时通过下标回到 `tickers[]` 里查。
2. `storage.reserve(std::min(cap, n))`——**绝不能 `reserve(k)`**：`k` 可以是 `INT_MAX`，那是几十 GB。
3. `std::priority_queue` 没有「替换堆顶」，只能 `pop` + `push`（两次下沉/上浮）。想省一次可以直接对 `std::vector` 用 `std::pop_heap` / `std::push_heap` 或手写 sift-down——面试里提一句即可。
4. 校验在 `if (cap == 0) continue;` **之前**：`k == 0` 时每个事件仍要校验。
5. `Trade` 的构造函数把所有不变量（非负、不溢出）检查一遍：只要对象存在，`notional()` 就是安全的。

### 2.5 `partial_sort` / `nth_element` / 整体排序

| 方法 | 时间 | 额外空间 | 特点 |
|---|---|---|---|
| 大小为 k 的堆 | `O(n log k)` | `O(k)` | **流式**：数据可以一个一个到，不用全放内存 |
| `std::partial_sort(first, first+m, last)` | `O(n log m)` | 需要全部 n 个下标 | 内部就是「大小 m 的堆，扫剩下的，最后堆排序」 |
| `std::nth_element` + 排前缀 | 平均 `O(n)` + `O(m log m)` | 需要全部 n 个下标 | introselect；前 m 个**无序**但都是最好的 m 个，所以还要把前缀排一下 |
| `std::sort` 全排 + 截断 | `O(n log n)` | 需要全部 n 个下标 | 最笨，用来对拍 |

对比（2,000,000 个随机 notional，单位毫秒）：

```cpp
// Four ways to take the k best of n events: bounded heap, partial_sort, nth_element + sort of the prefix, full sort.
// Every variant uses the same strict total order (notional descending, then index ascending), so the answers are identical.
// Build with -O2 and no sanitizers for meaningful timings.
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <vector>

struct Key { long long notional; int index; };
inline bool better(const Key& a, const Key& b) { return a.notional != b.notional ? a.notional > b.notional : a.index < b.index; }

template <class F> double ms(F&& f) {
    const auto t0 = std::chrono::steady_clock::now();
    f();
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

std::vector<Key> heap_topk(const std::vector<Key>& all, std::size_t k) {
    std::priority_queue<Key, std::vector<Key>, decltype(&better)> heap(&better);
    for (const Key& e : all) {
        if (heap.size() == k && e.notional < heap.top().notional) continue;  // fast reject
        if (heap.size() < k) heap.push(e);
        else if (better(e, heap.top())) { heap.pop(); heap.push(e); }
    }
    std::vector<Key> out;
    while (!heap.empty()) { out.push_back(heap.top()); heap.pop(); }
    std::reverse(out.begin(), out.end());
    return out;
}
std::vector<Key> partial_sort_topk(std::vector<Key> v, std::size_t k) {
    std::partial_sort(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k), v.end(), better);
    v.resize(k);
    return v;
}
std::vector<Key> nth_element_topk(std::vector<Key> v, std::size_t k) {
    std::nth_element(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k - 1), v.end(), better);
    std::sort(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(k), better);
    v.resize(k);
    return v;
}
std::vector<Key> sort_topk(std::vector<Key> v, std::size_t k) {
    std::sort(v.begin(), v.end(), better);
    v.resize(k);
    return v;
}

int main() {
    const int n = 2'000'000;
    std::mt19937_64 rnd(1);
    std::vector<Key> events(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) events[static_cast<std::size_t>(i)] = {static_cast<long long>(rnd() % 1'000'000'000), i};
    std::cout << "n = " << n << ", milliseconds\n";
    std::cout << "      k    heap  partial_sort  nth_element    sort\n";
    for (std::size_t k : {std::size_t{10}, std::size_t{1000}, std::size_t{100000}, std::size_t{1000000}}) {
        std::vector<Key> a, b, c, d;
        const double th = ms([&] { a = heap_topk(events, k); });
        const double tp = ms([&] { b = partial_sort_topk(events, k); });
        const double tn = ms([&] { c = nth_element_topk(events, k); });
        const double ts = ms([&] { d = sort_topk(events, k); });
        const bool same = std::equal(a.begin(), a.end(), b.begin(), [](const Key& x, const Key& y) { return x.index == y.index; }) &&
                          std::equal(a.begin(), a.end(), c.begin(), [](const Key& x, const Key& y) { return x.index == y.index; }) &&
                          std::equal(a.begin(), a.end(), d.begin(), [](const Key& x, const Key& y) { return x.index == y.index; });
        std::cout << std::fixed << std::setprecision(1) << std::setw(7) << k << std::setw(8) << th << std::setw(14) << tp << std::setw(13) << tn
                  << std::setw(8) << ts << (same ? "" : "  MISMATCH") << "\n";
    }
}
```

```text
n = 2000000, milliseconds
      k    heap  partial_sort  nth_element    sort
     10     0.9           3.3         13.2   113.8
   1000     1.0           2.2         12.3   111.5
 100000    28.6          25.8         15.8   111.3
1000000   198.2         203.1         66.5   118.6
```

读法：k 小时堆最快（绝大多数事件被一次比较拒绝）；k 接近 n 时 `nth_element` 最快（线性选择不关心 k）；整体排序永远是最慢的。**答题模板**：「k 小、数据流式 → 堆；数据已在内存且 k 大 → `nth_element`；要简单 → `sort`」。`nth_element` 和 `partial_sort` 要求比较器是**严格弱序**，且想要可复现的结果就必须是**全序**——否则 notional 相同的事件进哪个集合由算法内部细节决定。

## 3. Part 2：按 ticker 聚合后取 top-k

**聚合**（aggregate）和**选择**（select）是两件事：先把每个 ticker 的 notional 加起来（哈希表，`O(n)`），再从 m 个不同 ticker 里选 top-k（堆，`O(m log k)`）。累加用 `add_exact`：**每个事件都不溢出，合起来也可能溢出**，要报。出现过但总额为 0 的 ticker 存在（排在最后）。

两个 C++ 细节：

* `std::unordered_map<std::string, long long>` 用 `string_view` 查找会先构造一个临时 `std::string`。C++20 的**异构查找**（heterogeneous lookup）：给哈希器加 `using is_transparent = void;` 并把相等比较换成 `std::equal_to<>`，`find(std::string_view)` 就不再分配（`StringHash` / `Totals`）。
* 表是**节点式**（node-based）的：元素地址在 rehash 后**不变**。`top_of` 的堆里放 `const Entry*`（指向节点），最后才把选中的 k 个复制成 `TickerTotal`。如果换成 `vector<pair<...>>` 或开放寻址哈希表就不能这么做。

`top_tickers_sorted` 是「把所有节点指针 `partial_sort`」的对照写法——更短，常数更大（Java 版用 `groupingBy + sorted().limit(k)`）。`summarize` 一趟遍历同时算两个互不相关的聚合（Java 的 `teeing`）：循环里一边累加总额，一边记**最大事件的下标**，最后才构造一个 `Trade`。

```cpp
/// Hash of string_view so that map.find(std::string_view) needs no temporary std::string (C++20 heterogeneous lookup).
struct StringHash {
    using is_transparent = void;
    std::size_t operator()(std::string_view s) const noexcept { return std::hash<std::string_view>{}(s); }
};
using Totals = std::unordered_map<std::string, long long, StringHash, std::equal_to<>>;

/// totals[ticker] += amount, checked.  Throws before touching the table.
inline void add_to(Totals& totals, std::string_view ticker, long long amount) {
    if (auto it = totals.find(ticker); it != totals.end()) it->second = add_exact(it->second, amount);
    else totals.emplace(std::string(ticker), amount);
}

/// Top k of a ticker -> total table (bounded heap of pointers into the table's nodes: no string copies until the end).
inline std::vector<TickerTotal> top_of(const Totals& totals, int k) {
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    const auto cap = static_cast<std::size_t>(k);
    if (cap == 0) return {};
    using Entry = Totals::value_type;
    auto better = [](const Entry* a, const Entry* b) {
        if (a->second != b->second) return a->second > b->second;
        return a->first < b->first;
    };
    std::vector<const Entry*> storage;
    storage.reserve(std::min(cap, totals.size()));
    std::priority_queue<const Entry*, std::vector<const Entry*>, decltype(better)> heap(better, std::move(storage));
    for (const Entry& e : totals) {
        if (heap.size() < cap) heap.push(&e);
        else if (better(&e, heap.top())) { heap.pop(); heap.push(&e); }
    }
    std::vector<TickerTotal> out;
    out.reserve(heap.size());
    while (!heap.empty()) { out.emplace_back(heap.top()->first, heap.top()->second); heap.pop(); }
    std::reverse(out.begin(), out.end());
    return out;
}

/// Aggregate per ticker, then take the top k.  O(n) hashing + O(m log k) selection.
inline std::vector<TickerTotal> top_tickers(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    Totals totals;
    for (std::size_t i = 0; i < n; ++i) add_to(totals, tickers[i], notional_at(tickers, prices, volumes, i));
    return top_of(totals, k);
}

/// Same answer by sorting: partial_sort of all m entries' pointers.  O(m log k) too, but with a bigger constant than the heap.
inline std::vector<TickerTotal> top_tickers_sorted(Strings tickers, Longs prices, Longs volumes, int k) {
    const std::size_t n = check_inputs(tickers, prices, volumes, k);
    Totals totals;
    for (std::size_t i = 0; i < n; ++i) add_to(totals, tickers[i], notional_at(tickers, prices, volumes, i));
    using Entry = Totals::value_type;
    std::vector<const Entry*> all;
    all.reserve(totals.size());
    for (const Entry& e : totals) all.push_back(&e);
    const std::size_t m = std::min(static_cast<std::size_t>(k), all.size());
    std::partial_sort(all.begin(), all.begin() + static_cast<std::ptrdiff_t>(m), all.end(), [](const Entry* a, const Entry* b) {
        if (a->second != b->second) return a->second > b->second;
        return a->first < b->first;
    });
    std::vector<TickerTotal> out;
    for (std::size_t i = 0; i < m; ++i) out.emplace_back(all[i]->first, all[i]->second);
    return out;
}

/// One pass, two independent aggregates: the grand total and the best single event (built once, at the end).
inline Summary summarize(Strings tickers, Longs prices, Longs volumes) {
    const std::size_t n = check_inputs(tickers, prices, volumes, 0);
    long long grand = 0;
    std::optional<std::size_t> best;
    long long best_notional = 0;
    for (std::size_t i = 0; i < n; ++i) {
        const long long nt = notional_at(tickers, prices, volumes, i);
        grand = add_exact(grand, nt);
        // strictly better only: on a full tie the earlier index (already in `best`) wins
        if (!best || nt > best_notional || (nt == best_notional && tickers[i] < tickers[*best])) {
            best = i;
            best_notional = nt;
        }
    }
    if (!best) return Summary{grand, std::nullopt};
    return Summary{grand, detail::make_trade(tickers, prices, volumes, static_cast<int>(*best))};
}
```

## 4. Part 3：流式滑动窗口 top-k

成交按时间顺序到达，只关心最近 `window` 个时间单位：`now - time < window` 的成交是活的，**恰好差 `window` 就过期**，活跃区间是 `(now - window, now]`。

窗口 W = 10，k = 2，输入：

```
F 1 AAPL 100 2
F 3 MSFT 50 10
F 5 AAPL 100 3
Q 5
F 12 TSLA 10 10
Q 12
Q 15
Q 40
```

| 查询 | 输出 | 说明 |
|---|---|---|
| `Q 5` | `[AAPL 500, MSFT 500]` | 并列按 ticker 升序 |
| `Q 12` | `[MSFT 500, AAPL 300]` | t=1 的 AAPL 200 已过期（12-1=11 >= 10） |
| `Q 15` | `[TSLA 100]` | MSFT(t=3)、AAPL(t=5) 都过期（15-5=10 >= 10，边界算过期） |
| `Q 40` | `[]` | |

### 4.1 为什么只用 `priority_queue` 不行

一个 ticker 的总额会**变大**（新成交）也会**变小**（旧成交过期），即「修改任意一个元素的键」。`std::priority_queue` 只能看堆顶、弹堆顶，找不到也改不了中间的元素。解法有两种：**懒删除**（lazy deletion，旧条目留在堆里，弹出时发现过期/不一致再丢；空间会涨）；或者用一个**有序容器**——`std::set`，键 `(总额降序, ticker 升序)`，「删旧键、插新键」各 `O(log m)`，取前 k 名是顺序遍历 `O(log m + k)`。这里用后者。

三个结构配合：

| 结构 | 作用 |
|---|---|
| `std::deque<Fill> live_` | 活跃成交，按到达（=时间）顺序；**只有队头会过期** |
| `unordered_map<ticker, {total, count}> acc_` | 每个 ticker 在窗口内的总额和还活着的成交笔数 |
| `std::set<Rank> ranking_` | 所有活跃 ticker，按 (总额降序, ticker 升序) 排好 |

每个成交最多进、出各一次：`O(log m)` 摊还。

### 4.2 `set` 里放 `string_view`：指向 map 节点里的键

`Rank{total, ticker}` 里的 `ticker` 是 `std::string_view`，**指向 `acc_` 节点里的 key**——不复制字符串。这依赖三条规则：

1. `unordered_map` 的节点不会因 rehash 而移动，所以视图一直有效；
2. 某个 ticker 的节点要被 `erase` 时，**先把 `ranking_` 里的条目删掉**，再删 map 节点（否则 `ranking_` 里留着悬空视图，比较时读已释放内存）；
3. 这个类**不能拷贝也不能移动**（`= delete`）：拷贝会让新对象的 `ranking_` 指向旧对象的节点。

下面的程序演示视图为什么「看起来没事」却是陷阱：vector 重新分配之后，短字符串的字符是**存在 `std::string` 对象内部**的，会跟着搬走，旧视图指向的地址已经不是它了（程序只比较地址，从不通过过期视图读数据）。

```cpp
// A string_view into a std::vector<std::string> element goes stale when the vector reallocates and the strings move (short
// strings keep their characters INSIDE the std::string object).  The program only compares addresses; it never reads through
// a stale view.
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

int main() {
    std::vector<std::string> names;
    names.reserve(1);
    names.push_back("AAPL");  // short string: characters live inside the std::string object
    const std::string_view view = names[0];
    const char* before = view.data();
    names.push_back("MSFT");  // exceeds capacity 1: reallocation moves the strings
    const char* after = names[0].data();
    std::cout << "view still points at element 0's characters: " << (before == after ? "yes" : "no") << "\n";

    // The safe pattern for this problem: build ALL the strings first (or keep them in a deque / a reserved vector), then take views.
    std::vector<std::string> stable = {"AAPL", "MSFT", "GOOG"};
    std::vector<std::string_view> views(stable.begin(), stable.end());
    std::cout << "views taken after the vector is complete: " << views[0] << " " << views[1] << " " << views[2] << "\n";
}
```

```text
view still points at element 0's characters: no
views taken after the vector is complete: AAPL MSFT GOOG
```

### 4.3 更新键：相等键陷阱与 node handle

Java 的做法是 `ranking.remove(old); ranking.add(new)`。C++ 里这样写有两个问题：

* **旧键和新键相等**时（一笔 notional 为 0 的成交：总额不变），「先 insert 新的、再 erase 旧的」会 insert 不进去（已存在），然后 erase 把**唯一的条目**删掉；
* 在 `erase` 和 `insert` 之间如果分配内存失败（`bad_alloc`），状态就坏了。

C++17 的 **node handle**：`auto node = set.extract(key);` 把节点从树里摘出来（不释放、不分配），`node.value()` 给出可修改的键，改完 `set.insert(std::move(node))` 放回去。无论新旧键是否相等都对，而且不会抛异常。

```cpp
// Updating a std::set key: "erase the old key, insert the new one" is wrong when old == new, and allocation can throw
// between the two steps.  A node handle edits the key in place and never allocates.
#include <iostream>
#include <set>
#include <string>
#include <utility>

using Key = std::pair<long long, std::string>;  // (total, ticker)

int main() {
    std::set<Key> ranking = {{10, "A"}, {7, "B"}};

    // Wrong when the total does not change (a zero-notional trade): insert finds the key already there, then erase removes it.
    {
        auto wrong = ranking;
        const Key old_key{10, "A"}, new_key{10, "A"};
        wrong.insert(new_key);  // no-op: equal key exists
        wrong.erase(old_key);   // removes the only entry for A
        std::cout << "insert-then-erase with old == new keeps " << wrong.size() << " of 2 entries\n";
    }

    // Right: extract the node, change the key through the node handle, put it back.  No allocation, any old/new relation.
    {
        auto right = ranking;
        auto node = right.extract(Key{10, "A"});
        node.value().first = 10;  // unchanged total
        right.insert(std::move(node));
        auto node2 = right.extract(Key{10, "A"});
        node2.value().first = 3;  // changed total: A moves behind B
        right.insert(std::move(node2));
        std::cout << "extract / edit / insert keeps " << right.size() << " entries; smallest is (" << right.begin()->first << ", "
                  << right.begin()->second << ")\n";
    }
}
```

```text
insert-then-erase with old == new keeps 1 of 2 entries
extract / edit / insert keeps 2 entries; smallest is (3, A)
```

### 4.4 代码

溢出的原子性：`add` 先算出 `new_total`（`add_exact` 溢出就抛），**这时还没动任何结构**；然后依次做可能失败的操作（`push_back`、新建节点、`insert`），任何一步抛异常都撤销前面的步骤；最后只剩 `noexcept` 的修改。

```cpp
struct Fill {
    long long time;
    std::string ticker;
    long long price, volume;
    Fill(long long time, std::string ticker, long long price, long long volume)
        : time(time), ticker(std::move(ticker)), price(price), volume(volume) {
        if (time < 0) throw std::invalid_argument("negative time: " + std::to_string(time));
        if (price < 0) throw std::invalid_argument("negative price: " + std::to_string(price));
        if (volume < 0) throw std::invalid_argument("negative volume: " + std::to_string(volume));
        mul_exact(price, volume);
    }
    long long notional() const { return mul_exact(price, volume); }
    friend bool operator==(const Fill&, const Fill&) = default;
};
struct Tick { long long time; friend bool operator==(const Tick&, const Tick&) = default; };
struct Ask { long long time; friend bool operator==(const Ask&, const Ask&) = default; };
using Feed = std::variant<Fill, Tick, Ask>;

struct Answer {
    long long time;
    std::vector<TickerTotal> top;
    friend bool operator==(const Answer&, const Answer&) = default;
};

/// Top-k tickers over the last `window` time units.  A fill at time t is live while now - t < window.
///
/// Why not a heap alone: a ticker's total changes in both directions (new fills, expiries), i.e. "change the key of
/// an arbitrary element", and a priority_queue cannot find or edit anything but its top.  std::set can: erase the old
/// (total, ticker) key, insert the new one, O(log m) each.
///
/// ranking_ stores string_views into the keys of acc_ (unordered_map nodes never move), so this class is neither copyable nor
/// movable, and a ranking entry is always erased BEFORE its acc_ node is.
class SlidingTopK {
public:
    SlidingTopK(long long window, int k) : window_(window), k_(k) {
        if (window < 1) throw std::invalid_argument("window must be >= 1: " + std::to_string(window));
        if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    }
    SlidingTopK(const SlidingTopK&) = delete;
    SlidingTopK& operator=(const SlidingTopK&) = delete;

    /// Advance the clock to f.time (expiring old fills), then count f.  Overflow -> std::overflow_error, state unchanged.
    void add(const Fill& f) {
        advance_to(f.time);
        auto it = acc_.find(std::string_view(f.ticker));
        const long long old_total = it == acc_.end() ? 0 : it->second.total;
        const long long new_total = add_exact(old_total, f.notional());  // overflow_error here: nothing has been touched
        live_.push_back(f);                                              // bad_alloc here: nothing else has been touched
        if (it == acc_.end()) {
            try {
                it = acc_.try_emplace(f.ticker).first;
                ranking_.insert(Rank{new_total, it->first});
            } catch (...) {
                if (it != acc_.end()) acc_.erase(it);
                live_.pop_back();
                throw;
            }
        } else {
            rekey(it->first, old_total, new_total);
        }
        it->second.total = new_total;
        ++it->second.count;
    }

    /// Move the clock to t (t < now throws) and expire every fill with now - time >= window.
    void advance_to(long long t) {
        if (t < now_) throw std::invalid_argument("time went backwards: " + std::to_string(t) + " < " + std::to_string(now_));
        now_ = t;
        while (!live_.empty() && now_ - live_.front().time >= window_) {
            const Fill& f = live_.front();
            auto it = acc_.find(std::string_view(f.ticker));
            if (it->second.count == 1) {
                ranking_.erase(Rank{it->second.total, it->first});  // erase the view's entry before its owner dies
                acc_.erase(it);
            } else {
                const long long nt = it->second.total - f.notional();
                rekey(it->first, it->second.total, nt);
                it->second.total = nt;
                --it->second.count;
            }
            live_.pop_front();
        }
    }

    /// Current top k, best first (total descending, ticker ascending).
    std::vector<TickerTotal> top() const {
        std::vector<TickerTotal> out;
        std::size_t left = static_cast<std::size_t>(k_);
        for (auto it = ranking_.begin(); it != ranking_.end() && left > 0; ++it, --left) out.emplace_back(std::string(it->ticker), it->total);
        return out;
    }
    long long total_of(std::string_view ticker) const {
        auto it = acc_.find(ticker);
        return it == acc_.end() ? 0 : it->second.total;
    }
    int live_events() const { return static_cast<int>(live_.size()); }
    int distinct_tickers() const { return static_cast<int>(acc_.size()); }
    long long now() const { return now_; }

    /// Process a feed; every Ask yields one Answer.  std::visit over the variant: a missing overload is a compile error.
    static std::vector<Answer> replay(long long window, int k, const std::vector<Feed>& feed) {
        SlidingTopK w(window, k);
        std::vector<Answer> answers;
        for (const Feed& item : feed) {
            std::visit(overloaded{
                           [&](const Fill& f) { w.add(f); },
                           [&](const Tick& t) { if (t.time != w.now()) w.advance_to(t.time); },
                           [&](const Ask& a) {
                               w.advance_to(a.time);
                               answers.push_back(Answer{a.time, w.top()});
                           }},
                       item);
        }
        return answers;
    }

private:
    struct Acc { long long total = 0; int count = 0; };
    struct Rank {
        long long total;
        std::string_view ticker;  // points into the key of an acc_ node
    };
    struct RankOrder {
        bool operator()(const Rank& a, const Rank& b) const {
            if (a.total != b.total) return a.total > b.total;
            return a.ticker < b.ticker;
        }
    };

    /// Change one ranking key without allocating: extract the node, edit the key (C++17 node handles allow it), re-insert.
    /// Also correct when the key does not change (a zero-notional fill): erase+insert of equal keys would be a trap.
    void rekey(std::string_view ticker, long long from, long long to) {
        auto node = ranking_.extract(Rank{from, ticker});
        node.value().total = to;
        ranking_.insert(std::move(node));
    }

    long long window_;
    int k_;
    std::deque<Fill> live_;  // arrival order = time order: only the front can expire
    std::unordered_map<std::string, Acc, StringHash, std::equal_to<>> acc_;
    std::set<Rank, RankOrder> ranking_;
    long long now_ = 0;
};
```

`replay` 用 `std::visit` + `overloaded`（把几个 lambda 合成一个函数对象）分派 `std::variant<Fill, Tick, Ask>`——少写一个分支，编译不过，对应 Java 的 sealed + 模式匹配 `switch`。`Tick` 在当前时间是空操作；`Tick` / `Ask` 回退时间由 `advance_to` 抛 `invalid_argument`。

## 5. Part 4：切块并行聚合

两千万条数据，单线程太慢：**切成块，每块各自聚合成一张表，最后合并**。

### 5.1 为什么合并是对的

1. 整数加法满足**结合律和交换律**：怎么切、按什么顺序合并，结果都一样（浮点数不满足，所以价格用整数 tick）；
2. 每块的表只被一个线程写，**没有共享可变状态**——不需要锁，也没有数据竞争（data race）；
3. 所有 notional 非负，部分和单调不减：只要任何一块、任何一次合并溢出，真实总和就一定超过 `LLONG_MAX`——所以「是否溢出」**与分块方式无关**。总额恰好等于 `LLONG_MAX` 必须通过，多 1 必须报。

### 5.2 线程、异常、取消

* 一个异常如果从 `std::thread` 的函数体里逃出来，会直接 `std::terminate`（整个进程死）。所以每个工作线程**自己 `catch (...)`，把 `std::current_exception()` 存起来**，主线程 join 之后再 `rethrow_exception`。
* `std::jthread`（C++20）的析构函数会 `request_stop()` 然后 `join()`——线程不会泄漏，`vector<jthread>` 离开作用域就全部 join。
* **取消是协作式的**：一块失败后调用共享的 `std::stop_source::request_stop()`，其它块每处理 4096 个事件看一次 `stop_requested()`，发现就退出。

```cpp
// Worker threads, exceptions and cooperative cancellation: an exception must not leave a thread body.
#include <atomic>
#include <chrono>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <stop_token>
#include <thread>
#include <vector>

int main() {
    constexpr int workers = 4;
    std::vector<std::exception_ptr> errors(workers);
    std::vector<long long> steps(workers, 0);
    std::stop_source stop;
    {
        std::vector<std::jthread> threads;
        for (int w = 0; w < workers; ++w)
            threads.emplace_back([&, w] {
                try {
                    for (long long i = 0; i < 50'000'000; ++i) {
                        if ((i & 0xFFF) == 0 && stop.stop_requested()) return;  // look at the flag every 4096 steps
                        if (w == 0 && i == 100'000) throw std::overflow_error("chunk 0 failed");
                        ++steps[static_cast<std::size_t>(w)];
                    }
                } catch (...) {
                    errors[static_cast<std::size_t>(w)] = std::current_exception();  // never let it escape the thread
                    stop.request_stop();
                }
            });
    }  // all jthreads joined here
    for (const auto& e : errors) {
        if (!e) continue;
        try { std::rethrow_exception(e); } catch (const std::exception& ex) { std::cout << "rethrown after join: " << ex.what() << "\n"; }
        break;
    }
    long long others = 0;
    for (int w = 1; w < workers; ++w) others += steps[static_cast<std::size_t>(w)];
    std::cout << "other workers stopped early: " << (others < 3LL * 50'000'000 ? "yes" : "no") << "\n";
}
```

```text
rethrown after join: chunk 0 failed
other workers stopped early: yes
```

### 5.3 三种实现

| 函数 | 做法 | 点评 |
|---|---|---|
| `totals_chunked` | 每块一个 `jthread`，每块一张私有表，最后合并 | 推荐：无共享、无锁 |
| `totals_recursive` | 对半切，左半边 `std::async`，右半边自己算 | Java 的 ForkJoin 形状；**标准库没有线程池**，每次切分都起一个线程，`threshold` 太小会起成千上万个线程 |
| `totals_sharded` | 对照组：所有线程往同一张表里加 | 标准库**没有**并发哈希表：自己按 `hash % 16` 分成 16 片，每片一个 `std::mutex`。热点 ticker 上所有线程排队 |

* 16 个分片的 `Shard` 用 `alignas(64)`：每片占自己的缓存行（cache line），避免**伪共享**（false sharing）——两个线程写同一缓存行里的不同变量，缓存行在核之间来回抢。下面的程序量一量：

```cpp
// Two counters updated by two threads: in the same cache line they fight over it ("false sharing"); on separate lines they do not.
// Build with -O2 and no sanitizers.  The numbers depend on the machine; the gap is what matters.
#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>

struct Shared { std::atomic<long long> a{0}, b{0}; };                     // a and b in one 16-byte neighbourhood
struct Padded { alignas(64) std::atomic<long long> a{0}; alignas(64) std::atomic<long long> b{0}; };  // 64 bytes apart

template <class T> double run(T& counters) {
    constexpr int iterations = 20'000'000;
    const auto t0 = std::chrono::steady_clock::now();
    {
        std::jthread x([&] { for (int i = 0; i < iterations; ++i) counters.a.fetch_add(1, std::memory_order_relaxed); });
        std::jthread y([&] { for (int i = 0; i < iterations; ++i) counters.b.fetch_add(1, std::memory_order_relaxed); });
    }
    return std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
}

int main() {
    Shared s;
    Padded p;
    std::cout << "same cache line:      " << run(s) << " ms\n";
    std::cout << "separate cache lines: " << run(p) << " ms\n";
}
```

```text
same cache line:      273.9 ms
separate cache lines: 27.4 ms
```

* C++17 的并行算法（`std::execution::par`）在 libstdc++ 里要链接 TBB，在 libc++ 里默认没有；面试里说「我会手写切块 + 合并，因为可控」比依赖它更稳。
* `std::vector<std::exception_ptr>` 每个线程写**不同的元素**，没有竞争；`vector<bool>` 才会因为位压缩让相邻元素共享一个字节，多线程写它们会竞争。

```cpp
namespace detail {

struct Cancelled {};  // thrown inside a worker when a sibling failed; never escapes a worker

/// Add events [from, to) into m.  Looks at the stop token every 4096 events: cooperative cancellation.
inline void accumulate(Totals& m, Strings t, Longs p, Longs v, std::size_t from, std::size_t to, const std::stop_token& stop = {}) {
    for (std::size_t i = from; i < to; ++i) {
        if ((i & 0xFFF) == 0 && stop.stop_requested()) throw Cancelled{};
        add_to(m, t[i], notional_at(t, p, v, i));
    }
}

/// Merge two tables (small into large).  Both belong to the caller, who must not use them afterwards.
inline Totals merge_into(Totals a, Totals b) {
    if (a.size() < b.size()) a.swap(b);
    for (auto& [ticker, amount] : b) add_to(a, ticker, amount);
    return a;
}

/// Start of chunk c: n * c / chunks computed in 64 bits.
inline std::size_t boundary_impl(std::size_t n, int chunks, int c) {
    return static_cast<std::size_t>(static_cast<unsigned long long>(n) * static_cast<unsigned long long>(c) / static_cast<unsigned long long>(chunks));
}

/// Run body(c, from, to, stop) on one jthread per chunk.  A worker that throws records its exception and asks the others
/// to stop; after all workers are joined the lowest-numbered recorded exception is rethrown.  Exceptions never escape
/// a thread body (that would call std::terminate).
template <class Body>
void run_chunks(std::size_t n, int chunks, Body body) {
    std::vector<std::exception_ptr> errors(static_cast<std::size_t>(chunks));
    std::stop_source stop;
    {
        std::vector<std::jthread> workers;
        workers.reserve(static_cast<std::size_t>(chunks));
        try {
            for (int c = 0; c < chunks; ++c) {
                workers.emplace_back([&, c] {
                    try {
                        body(c, boundary_impl(n, chunks, c), boundary_impl(n, chunks, c + 1), stop.get_token());
                    } catch (const Cancelled&) {
                    } catch (...) {
                        errors[static_cast<std::size_t>(c)] = std::current_exception();
                        stop.request_stop();
                    }
                });
            }
        } catch (...) {  // could not start a thread: stop the ones already running, join them (vector dtor), rethrow
            stop.request_stop();
            throw;
        }
    }  // every jthread is joined here
    for (const auto& e : errors)
        if (e) std::rethrow_exception(e);
}

inline Totals sum_range(Strings t, Longs p, Longs v, std::size_t from, std::size_t to, std::size_t threshold) {
    if (to - from <= threshold) {
        Totals m;
        accumulate(m, t, p, v, from, to);
        return m;
    }
    const std::size_t mid = from + (to - from) / 2;  // not (from + to) / 2: that can overflow
    auto left = std::async(std::launch::async, [=] { return sum_range(t, p, v, from, mid, threshold); });
    Totals right = sum_range(t, p, v, mid, to, threshold);  // if this throws, ~future waits for the left task
    return merge_into(left.get(), std::move(right));
}

}  // namespace detail

inline std::size_t boundary(std::size_t n, int chunks, int c) { return detail::boundary_impl(n, chunks, c); }

inline Totals totals_sequential(Strings t, Longs p, Longs v) {
    const std::size_t n = check_inputs(t, p, v, 0);
    Totals m;
    detail::accumulate(m, t, p, v, 0, n);
    return m;
}

/// One jthread per chunk, one private table per chunk (nothing shared, no lock), merge at the end.
inline Totals totals_chunked(Strings t, Longs p, Longs v, int chunks) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (chunks < 1) throw std::invalid_argument("chunks must be >= 1: " + std::to_string(chunks));
    std::vector<Totals> parts(static_cast<std::size_t>(chunks));
    detail::run_chunks(n, chunks, [&](int c, std::size_t from, std::size_t to, const std::stop_token& stop) {
        detail::accumulate(parts[static_cast<std::size_t>(c)], t, p, v, from, to, stop);
    });
    Totals acc = std::move(parts[0]);
    for (std::size_t c = 1; c < parts.size(); ++c) acc = detail::merge_into(std::move(acc), std::move(parts[c]));
    return acc;
}

/// Divide and conquer (the fork/join shape): halves until the range is <= threshold, the left half on std::async.
/// No thread pool in the standard library: this starts roughly n / threshold threads, so threshold must not be tiny.
inline Totals totals_recursive(Strings t, Longs p, Longs v, int threshold) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (threshold < 1) throw std::invalid_argument("threshold must be >= 1: " + std::to_string(threshold));
    return detail::sum_range(t, p, v, 0, n, static_cast<std::size_t>(threshold));
}

/// Control group: every thread adds into one shared table.  The standard library has no concurrent hash map, so the
/// table is split into 16 shards (hash % 16), each with its own mutex.  Correct, but hot tickers serialize on a lock.
inline Totals totals_sharded(Strings t, Longs p, Longs v, int chunks) {
    const std::size_t n = check_inputs(t, p, v, 0);
    if (chunks < 1) throw std::invalid_argument("chunks must be >= 1: " + std::to_string(chunks));
    struct alignas(64) Shard {  // one cache line each: no false sharing between shard mutexes
        std::mutex mutex;
        Totals map;
    };
    std::array<Shard, 16> shards;
    detail::run_chunks(n, chunks, [&](int, std::size_t from, std::size_t to, const std::stop_token& stop) {
        for (std::size_t i = from; i < to; ++i) {
            if ((i & 0xFFF) == 0 && stop.stop_requested()) throw detail::Cancelled{};
            const long long amount = notional_at(t, p, v, i);
            Shard& s = shards[StringHash{}(t[i]) % shards.size()];
            std::lock_guard<std::mutex> lock(s.mutex);
            add_to(s.map, t[i], amount);
        }
    });
    Totals all;
    for (Shard& s : shards) all.merge(s.map);  // shards hold disjoint keys: node splice, no rehash of values
    return all;
}

inline std::vector<TickerTotal> top_tickers_parallel(Strings t, Longs p, Longs v, int k, int chunks) {
    if (k < 0) throw std::invalid_argument("k must be >= 0: " + std::to_string(k));
    return top_of(totals_chunked(t, p, v, chunks), k);
}

}  // namespace toptrades
```

`run_chunks` 里「线程启动失败」的路径也处理了：`emplace_back` 抛异常时，先 `request_stop()`，再让 `vector<jthread>` 的析构去 join 已经起来的线程。多个块同时失败时，抛出编号最小的**已记录**的异常（被取消的块不会记录异常）。

## 6. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| `ArithmeticException`（`Math.multiplyExact`） | `std::overflow_error` + `__builtin_*_overflow` | 有符号溢出在 C++ 是 UB，必须用内建函数或先判断 |
| `String[]`，`null` ticker → NPE | `span<const string_view>`，没有 null | 值类型；「null」这一类错误在类型里就不存在了 |
| 返回 `List.copyOf`（不可变） | 返回 `std::vector<Trade>`（值） | 调用方拥有结果；不可变用 `const` 表达 |
| `PriorityQueue` 存 `Trade` 对象 | `priority_queue` 存 16 字节 `Key`，需要时再查数组 | 没有 GC，复制字符串有真实成本 |
| `TreeSet.remove` + `add` | `set::extract` + `insert(node)` | 相等键陷阱 + 不分配 |
| `parallel()` 流 / ForkJoin / `StructuredTaskScope` | `jthread` + `stop_source`、`std::async`、手写分片 | 标准库没有线程池/并发 map/结构化并发 |
| 取消 = 中断标志 `Thread.interrupt` | `std::stop_token` | 同样是协作式 |
| 字符串比较 UTF-16 码元 | 字节（unsigned char）字典序 | 语言的字符串模型不同 |
| 垃圾回收保证 `String` 一直有效 | `string_view` 可能悬空 | 生命周期要自己管：视图借用，结果拥有 |

## 7. 陷阱

1. **比较器不是全序**：top-k 结果取决于输入顺序（2.2）。
2. **`priority_queue` 的 `top()` 是 Compare 下「最大」的**：传错方向，堆顶就成了最好的，整个算法反了。
3. **`reserve(k)`**：k 可以是 `INT_MAX`。
4. **`price * volume` 不检查**：UB，不是「回绕」。`int * int` 先溢出再转型。
5. **只校验进堆的事件**：后面排在最末的溢出事件被漏掉。
6. **`string_view` 悬空**：指向临时 `std::string`、指向会重新分配的 `vector<string>`、指向已销毁的输入——结果里要放 `std::string`。
7. **`set` 更新键用 insert 后 erase**：新旧键相等时丢条目（4.3）。
8. **先删 map 节点、后删 set 条目**：`set` 里留下悬空视图。
9. **异常从线程函数体里逃出**：`std::terminate`。
10. **`std::async` 递归切到 `threshold = 1`**：n 个事件起 n 个线程。
11. **`vector<T>::resize` 需要默认构造**：`TickerTotal` 没有默认构造函数——截断用 `erase(begin()+k, end())`。

## 8. 面试官会追问什么（senior）

**Q1. 为什么堆要用「最差者在顶」？** 因为每个新元素只需要和「当前最差的保留者」比；比它还差就不可能进 top-k。最大堆要全扫才知道谁最差。

**Q2. `nth_element` 什么时候比堆好？** 数据全在内存、k 很大（接近 n）：线性选择不关心 k。堆的优势是流式和 `O(k)` 空间。

**Q3. 如果数据放不进内存？** 按 ticker 哈希分片，每片各自聚合 / 取 top-k，最后 k 路归并；或者流式堆（Part 1 的堆本来就是流式）。

**Q4. 窗口 top-k 能更快吗？** 可以用懒删除的堆（均摊 `O(log n)`，但空间随更新数涨）；`set` 精确且空间是 `O(m)`。如果 m 很小，每次查询直接扫描 `unordered_map` 也可以。

**Q5. 并行为什么不用共享哈希表？** 热点 ticker 上锁争用；伪共享；扩展性差。「各算各的，最后合并」正确性靠结合律，且没有同步成本。

**Q6. 浮点价格怎么办？** 先转成整数 tick；或用定点数；`double` 累加不满足结合律，并行结果会随分块变化。

**Q7. `std::jthread` 相比 `std::thread`？** 析构自动 `join`（`std::thread` 在可 join 状态析构 = `terminate`），并内置 `stop_token`。

## 9. 自测

1. 为什么 top-k 的比较器必须是全序？
2. `priority_queue<Key, vector<Key>, decltype(better)>` 中 `better(a, b)` 表示「a 比 b 好」，堆顶是谁？
3. `k = INT_MAX`、`n = 6` 时，`reserve` 应该传什么？
4. `LLONG_MAX * 2` 在 C++ 里「回绕成 -2」吗？
5. `ranking_` 里放 `string_view`，为什么先 `ranking_.erase(...)` 再 `acc_.erase(...)`？
6. 一笔 notional 为 0 的成交打到一个已有 ticker 上，「insert 新键、erase 旧键」会怎样？
7. 工作线程里抛出的异常没人 catch 会怎样？应该怎么传回主线程？
8. 为什么合并两块的表时溢出与分块方式无关？

<details><summary>答案</summary>

1. notional 相同的事件进哪个集合，否则取决于到达顺序或算法内部细节：同一批数据结果不同，没法复现和测试。
2. 最差的保留者（`top()` 是 Compare 下最大的 = 排在最后的）。
3. `min(k, n)`。
4. 不是——有符号溢出是未定义行为；用 `__builtin_mul_overflow`（或先转无符号再比较）才能得到确定行为。
5. `ranking_` 的条目持有指向 `acc_` 节点键的视图；先删节点会让条目悬空，之后的比较读到已释放内存。
6. 总额不变，新旧键相等：`insert` 因为已存在而什么也没做，随后 `erase` 把唯一的条目删掉，这个 ticker 从排名里消失。用 `extract` / 改键 / `insert(node)`。
7. 直接 `std::terminate`，整个进程退出。线程函数体里 `catch (...)`，保存 `std::current_exception()`，join 之后 `rethrow_exception`。
8. 所有 notional 非负，部分和单调不减：若任意一块或任意一次合并溢出，则真实总和 > `LLONG_MAX`，顺序实现也会溢出；反之总和不超过 `LLONG_MAX` 时，所有部分和都不超过。
</details>

**练习**：在 `ParallelNotional` 的基础上加每线程缓存（thread-local 聚合 + 批量合并）并量一量吞吐。
