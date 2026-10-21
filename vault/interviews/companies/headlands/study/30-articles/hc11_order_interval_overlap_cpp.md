# hc11 · 订单区间最大重叠 + 按买 / 卖方撤单（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

交易系统里每张订单（order）有一个**生命周期**：`start` 时刻进入订单簿，`end` 时刻离开。建模成**左闭右开**区间 `[start, end)`：`start` 那一刻已经「活着」，`end` 那一刻已经「不活了」。时间是**非负整数**（`long long`），可以接近 `LLONG_MAX`（纳秒时间戳），所以实现里**只做比较，不做 `end - start`、`end + 1` 或 `(a + b) / 2`**。

| Part | 内容 |
|---|---|
| 1 | 同时活着的订单数的最大值（以及最早出现的时刻）：扫描线 + 「同一时刻先结束后开始」 |
| 2 | 买、卖两个方向各自的峰值；`Cancel` 把区间截短；`std::variant` 事件 + `std::visit` |
| 3 | 在线：订单和撤单按时间到达，随时回答「到现在为止的最大重叠」和「t 时刻有几张」 |
| 4 | 坐标高达 10^18、更新顺序任意：坐标压缩 + 懒标记线段树 |

```
[[1,5],[2,6],[4,8]]          → 3，最早在 t=4
[[1,3],[3,5]]                → 1     （闭区间 [s,e] 的版本 → 2）
[[0,10],[2,3],[2,3],[5,7]]   → 3，最早在 t=2
[]                           → 0，Peak(0, 0)
```

* `[1,3)` 与 `[3,5)` **不重叠**：时刻 3 是交接，旧单已死、新单刚生。
* `start == end` 的空区间从没活过，忽略。输入可以乱序、有重复。
* Java 版的输入是 `long[][]`（要检查「行长度不是 2」）；C++ 版用 `struct Interval { long long start, end; }`，这类错误在类型里就不存在了。

## 2. Part 1：最大重叠

### 2.1 扫描线（sweep line）

把「区间」变成「事件」：区间 `[s, e)` 变成两个事件——`s` 处 **+1**（开始），`e` 处 **−1**（结束）。把所有事件按时间排好，从左到右扫一遍，维护当前活着的个数 `live`，记录最大值。最大值只可能出现在某个**开始**事件之后（只有开始会让 `live` 变大）。

**最关键的细节：同一时刻，结束要排在开始前面。** `[1,3)` 和 `[3,5)` 在时刻 3 各有一个事件：`−1`（第一个结束）和 `+1`（第二个开始）。先 `+1` 再 `−1`，`live` 会短暂变成 2，答案错成 2；先 `−1` 再 `+1`，`live` 始终是 1。只按时间排序而不管同时刻的先后，结果由排序的稳定性/输入顺序决定——「有时对有时错」。

```cpp
// The tie rule of a sweep line: at the same time, an END must be processed before a START ([1,3) and [3,5) do not overlap).
// With std::pair<time, delta> the default order (-1 < +1) is already right; sorting only by time leaves it to chance.
#include <algorithm>
#include <iostream>
#include <utility>
#include <variant>
#include <vector>

using Event = std::pair<long long, int>;  // (time, +1 start / -1 end)

int sweep(std::vector<Event> events, bool by_time_only) {
    if (by_time_only) {
        // Wrong: events with equal times keep whatever relative order they had (here: all starts were appended before all ends).
        std::stable_sort(events.begin(), events.end(), [](const Event& a, const Event& b) { return a.first < b.first; });
    } else {
        std::sort(events.begin(), events.end());  // (time, delta): -1 sorts before +1
    }
    int live = 0, best = 0;
    for (const auto& [time, delta] : events) {
        (void)time;
        live += delta;
        best = std::max(best, live);
    }
    return best;
}

struct Close { long long time; };
struct Open { long long time; };

int main() {
    // [1,3) and [3,5): the answer must be 1.
    std::vector<Event> events = {{1, +1}, {3, +1}, {3, -1}, {5, -1}};  // starts of both intervals, then their ends
    std::cout << "time only, ties in insertion order: " << sweep(events, true) << "   (wrong: start at 3 came before the end at 3)\n";
    std::cout << "(time, delta) pairs:                " << sweep(events, false) << "\n";

    // The same rule as the ORDER OF A VARIANT's alternatives: Close is alternative 0, Open is alternative 1.
    using SweepEvent = std::variant<Close, Open>;
    std::vector<SweepEvent> ev = {Open{1}, Open{3}, Close{3}, Close{5}};
    auto time_of = [](const SweepEvent& e) { return std::visit([](const auto& x) { return x.time; }, e); };
    std::sort(ev.begin(), ev.end(), [&](const SweepEvent& a, const SweepEvent& b) { return std::pair(time_of(a), a.index()) < std::pair(time_of(b), b.index()); });
    for (const auto& e : ev) std::cout << (e.index() == 0 ? "Close@" : "Open@") << time_of(e) << " ";
    std::cout << "\n";
}
```

```text
time only, ties in insertion order: 2   (wrong: start at 3 came before the end at 3)
(time, delta) pairs:                1
Open@1 Close@3 Open@3 Close@5 
```

第一行就是「只按时间排」的错误结果，第二行是 `(time, delta)` 的 `pair`：`pair` 的默认比较先比 time，再比 delta，而 `−1 < +1`，所以结束天然排在开始前面。最后一行用了另一种写法：把规则编码进 `std::variant<Close, Open>` **备选类型的顺序**——`Close` 是第 0 个，`Open` 是第 1 个，按 `(time, index())` 排序，同一时刻 `Close` 在前。想要闭区间 `[s,e]`（`[1,3]` 与 `[3,5]` 在 3 重叠）就把两个类型的顺序换过来。

### 2.2 三种写法

**(a) 两个各自排序的数组 + 双指针**（`peak`，主解）。把所有开始排成 `starts`，所有结束排成 `ends`，第 `i` 个开始时，已结束的个数 `j` = `ends` 中满足 `ends[j] <= s`（半开）的个数；`live = (i + 1) − j`。不需要真的建「事件」。

手算 `[[1,5],[2,6],[4,8]]`：`starts = [1,2,4]`，`ends = [5,6,8]`。`s=1`：没有结束，`live=1`；`s=2`：`live=2`；`s=4`：`ends[0]=5 <= 4`？否，`live=3` → 最大 3，时刻 4。`[[1,3],[3,5]]`：`s=3` 时 `ends[0]=3 <= 3` 成立，`j=1`，`live=2−1=1`。闭区间只把条件换成 `ends[j] < s`。

**(b) 一个事件数组**（`peak_events`）：`std::vector<std::variant<Close, Open>>`，按 `(time, index())` 排序。

**(c) `std::map` 当差分数组**（`peak_diff_map`）：`++delta[start]; --delta[end];`，然后按键从小到大累加。同一个键上的 `+1` 和 `−1` 先合并成**净增量**再用，所以同时刻的规则自动成立；缺点是 `map` 比排序的 `vector` 慢得多、内存大。

闭区间不能用 (c)：`[s, e]` 转成 `[s, e+1)` 会在 `e = LLONG_MAX` 时**有符号溢出**。正确做法是不做运算，只比较：

```cpp
// Turning a closed [s, e] into a half-open [s, e + 1) breaks at e = LLONG_MAX: e + 1 is signed overflow (undefined behaviour).
// Compare instead of converting: a closed end happened only if it is strictly before the start being considered.
#include <climits>
#include <iostream>

int main() {
    const long long e = LLONG_MAX;
    long long plus_one;
    const bool overflow = __builtin_add_overflow(e, 1LL, &plus_one);
    std::cout << "LLONG_MAX + 1 overflows: " << (overflow ? "yes" : "no") << " (wrapped value would be " << plus_one << ")\n";

    // closed: has the interval [?, e] ended before time s?   e < s   (no arithmetic)
    // half-open: has [?, e) ended by time s?                 e <= s
    const long long s = LLONG_MAX;
    std::cout << "closed end LLONG_MAX happened before s = LLONG_MAX: " << (e < s ? "yes" : "no") << "\n";
    std::cout << "half-open end LLONG_MAX happened by s = LLONG_MAX: " << (e <= s ? "yes" : "no") << "\n";
}
```

```text
LLONG_MAX + 1 overflows: yes (wrapped value would be -9223372036854775808)
closed end LLONG_MAX happened before s = LLONG_MAX: no
half-open end LLONG_MAX happened by s = LLONG_MAX: yes
```

### 2.3 排序比较器必须是严格弱序

`std::sort` 要求比较器 `comp(a, b)` 是**严格弱序**（strict weak ordering）：`comp(x, x)` 必须为 `false`。写成 `<=` 的比较器（「时间相同也算排前面」）违反这一条；元素有很多相等值时，`std::sort` 的内部循环可能越界读写——是**未定义行为**，不是「结果有点乱」。

```cpp
// std::sort needs a STRICT weak order: comp(x, x) must be false.  `<=` is not one; with many equal keys it can make std::sort
// read past the end of the array.  This program only checks the property; it never sorts with the bad comparator.
#include <iostream>

int main() {
    auto good = [](long long a, long long b) { return a < b; };
    auto bad = [](long long a, long long b) { return a <= b; };
    std::cout << "good(5, 5) = " << good(5, 5) << "   (irreflexive: required)\n";
    std::cout << "bad(5, 5)  = " << bad(5, 5) << "   (violates the requirement: undefined behaviour inside std::sort)\n";
    // Two equal elements would each claim to come before the other:
    std::cout << "bad(5, 5) && bad(5, 5) says 5 is before 5, and 5 is before 5, at once\n";
}
```

```text
good(5, 5) = 0   (irreflexive: required)
bad(5, 5)  = 1   (violates the requirement: undefined behaviour inside std::sort)
bad(5, 5) && bad(5, 5) says 5 is before 5, and 5 is before 5, at once
```

### 2.4 代码（类型 + Part 1）

```cpp
#include <algorithm>
#include <array>
#include <climits>
#include <iterator>
#include <cstddef>
#include <map>
#include <span>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace overlap {

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

enum class Side : unsigned char { Buy, Sell };

/// Largest number of simultaneously live orders and the EARLIEST time it is reached.  (0, 0) when nothing was ever live.
struct Peak {
    int count;
    long long time;
    friend bool operator==(const Peak&, const Peak&) = default;
};

/// A half-open lifetime [start, end).  No subtraction anywhere: times may be close to LLONG_MAX.
struct Interval {
    long long start, end;
    friend bool operator==(const Interval&, const Interval&) = default;
};

/// Place: planned lifetime [start, end).  end == start is legal (never live).
struct Place {
    long long id;
    Side side;
    long long start, end;
    Place(long long id, Side side, long long start, long long end) : id(id), side(side), start(start), end(end) {
        if (side != Side::Buy && side != Side::Sell) throw std::invalid_argument("invalid side");  // an enum can hold any value of its type
        if (start < 0) throw std::invalid_argument("negative start: " + std::to_string(start));
        if (end < start) throw std::invalid_argument("end < start: " + std::to_string(end) + " < " + std::to_string(start));
    }
    friend bool operator==(const Place&, const Place&) = default;
};

/// Cancel: from `time` on the order is no longer live (its interval becomes [start, min(end, time))).
struct Cancel {
    long long id;
    long long time;
    Cancel(long long id, long long time) : id(id), time(time) {
        if (time < 0) throw std::invalid_argument("negative time: " + std::to_string(time));
    }
    friend bool operator==(const Cancel&, const Cancel&) = default;
};

/// Closed hierarchy of events: std::visit with `overloaded` does not compile if a case is missing.
using OrderEvent = std::variant<Place, Cancel>;

struct Report {
    Peak buy, sell, all;
    friend bool operator==(const Report&, const Report&) = default;
};

namespace detail {

/// Core of the two-vector sweep.  Sort all starts and all ends separately; for the i-th start (ascending), j counts the
/// ends that already happened.  Half-open: an end at or before s has happened (end first, then start, at the same time).
/// Closed: only an end strictly before s has happened.  live = (i + 1) - j.  A maximum can only appear at a start.
inline Peak peak_of(std::vector<long long> starts, std::vector<long long> ends, bool inclusive) {
    if (starts.empty()) return {0, 0};
    std::sort(starts.begin(), starts.end());
    std::sort(ends.begin(), ends.end());
    int best = 0;
    long long best_time = 0;
    std::size_t j = 0;
    for (std::size_t i = 0; i < starts.size(); ++i) {
        const long long s = starts[i];
        while (j < ends.size() && (inclusive ? ends[j] < s : ends[j] <= s)) ++j;
        const int live = static_cast<int>(i + 1 - j);
        if (live > best) {  // strictly greater: among equal maxima keep the earliest time
            best = live;
            best_time = s;
        }
    }
    return {best, best_time};
}

inline Peak sweep(std::span<const Interval> intervals, bool inclusive) {
    std::vector<long long> starts, ends;
    starts.reserve(intervals.size());
    ends.reserve(intervals.size());
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (!inclusive && iv.end == iv.start) continue;  // an empty half-open interval was never live
        starts.push_back(iv.start);
        ends.push_back(iv.end);
    }
    return peak_of(std::move(starts), std::move(ends), inclusive);
}

}  // namespace detail

/// Peak of simultaneously live orders for half-open [start, end).  Unsorted input and duplicates are fine.
inline Peak peak(std::span<const Interval> intervals) { return detail::sweep(intervals, false); }
inline int max_overlap(std::span<const Interval> intervals) { return peak(intervals).count; }
/// Closed [start, end]: [1,3] and [3,5] overlap at 3; [5,5] is a single live point.
inline int max_overlap_inclusive(std::span<const Interval> intervals) { return detail::sweep(intervals, true).count; }

/// Variant two: ONE vector of events, sorted by (time, kind).  The tie rule "end before start" is the alternative order
/// of the variant: Close is index 0, Open is index 1.
struct Close { long long time; };
struct Open { long long time; };
using SweepEvent = std::variant<Close, Open>;

inline Peak peak_events(std::span<const Interval> intervals) {
    std::vector<SweepEvent> events;
    events.reserve(intervals.size() * 2);
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (iv.end == iv.start) continue;
        events.emplace_back(Open{iv.start});
        events.emplace_back(Close{iv.end});
    }
    auto time_of = [](const SweepEvent& e) { return std::visit([](const auto& x) { return x.time; }, e); };
    std::sort(events.begin(), events.end(), [&](const SweepEvent& a, const SweepEvent& b) {
        return std::pair(time_of(a), a.index()) < std::pair(time_of(b), b.index());  // strict weak order: < never <=
    });
    int live = 0, best = 0;
    long long best_time = 0;
    for (const SweepEvent& e : events) {
        std::visit(overloaded{[&](const Close&) { --live; },
                              [&](const Open& o) {
                                  if (++live > best) { best = live; best_time = o.time; }
                              }},
                   e);
    }
    return {best, best_time};
}

/// Variant three: a difference array in an ordered map.  +1 at start, -1 at end; walking the keys in order and adding
/// the NET delta of each key makes the tie rule automatic: a +1 and a -1 on the same key cancel before anyone looks.
inline Peak peak_diff_map(std::span<const Interval> intervals) {
    std::map<long long, int> delta;
    for (const Interval& iv : intervals) {
        if (iv.start < 0) throw std::invalid_argument("negative start: " + std::to_string(iv.start));
        if (iv.end < iv.start) throw std::invalid_argument("end < start: " + std::to_string(iv.end) + " < " + std::to_string(iv.start));
        if (iv.end == iv.start) continue;
        ++delta[iv.start];
        --delta[iv.end];
    }
    int live = 0, best = 0;
    long long best_time = 0;
    for (const auto& [time, d] : delta) {
        live += d;
        if (live > best) { best = live; best_time = time; }
    }
    return {best, best_time};
}
```

要点：

1. `Peak` 的 `time` 是**最早**达到最大值的时刻：用 `live > best`（严格大于）更新。同一个 `s` 出现多次时，后面的 `live` 更大，`time` 仍然是 `s`。
2. `peak_of` 按值接收两个 `vector`（调用方 `std::move` 进来）：函数内部排序，不改调用方的数据；输入是 `span<const Interval>`，**不可能**被修改。
3. 每个区间都校验（`start < 0`、`end < start` → `std::invalid_argument`），包括空区间。
4. 空输入返回 `Peak{0, 0}`。

## 3. Part 2：买 / 卖方向 + 撤单

输入是一串 `OrderEvent`（顺序**无所谓**）：`Place(id, side, start, end)` 和 `Cancel(id, time)`——`time` 时刻起这张单不再活着，区间变成 `[start, min(end, time))`。

* 撤单时间 `<= start` → 从没活过；`>= end` → 无影响；同一个 `id` 多次撤单：**最早**的生效；
* 撤单的 `id` 没有对应的 `Place`、同一个 `id` 两次 `Place` → `std::invalid_argument`；
* 买方峰值和卖方峰值可以出现在不同时刻，`all.count` **不等于** `buy.count + sell.count`。

```
Place(1,BUY, 0,10)  Place(2,BUY, 2, 8)  Place(3,SELL,3, 6)  Place(4,SELL,4,12)  Place(5,BUY, 5, 9)
Cancel(2, 6)        Cancel(4, 5)

有效区间： 1 BUY [0,10)   2 BUY [2,6)   3 SELL [3,6)   4 SELL [4,5)   5 BUY [5,9)
buy  = Peak(3, 5)    t=5：订单 1、2、5
sell = Peak(2, 4)    t=4：订单 3、4
all  = Peak(4, 4)    t=4：1、2、3、4；t=5：1、2、3、5 也是 4，取最早
```

做法：先**把「撤单」翻译成「改区间」**（每个 id 的最早撤单时间），再按方向各收集一份 `starts / ends`，对每份调用 Part 1 的 `peak_of`。

C++ 里的三个点：

* `OrderEvent` 是 `std::variant<Place, Cancel>`（闭合的层级），用 `std::visit(overloaded{...}, event)` 分派。`overloaded` 把几个 lambda 合成一个有多个 `operator()` 的类型；少写一个分支**编译不过**——对应 Java 的 sealed interface + 模式匹配 `switch`。
* `Side` 是 `enum class`，但它**可以装下任何 `unsigned char` 值**：`static_cast<Side>(7)` 是合法值，下标访问 `lanes[7]` 就越界。所以 `Place` 的构造函数检查它。
* 订单 id 是任意 `long long`（包括 `LLONG_MIN`、负数）；放在 `unordered_map` 里没问题。

```cpp
/// Buy / sell / all peaks of a batch of Place and Cancel events (any order).  The effective interval of an order is
/// [start, min(end, earliest cancel)); a cancel at or before start means it never lived.
inline Report analyze(std::span<const OrderEvent> events) {
    std::unordered_map<long long, Place> places;
    std::unordered_map<long long, long long> cancel_at;
    for (const OrderEvent& e : events) {
        std::visit(overloaded{[&](const Place& p) {
                                  if (!places.emplace(p.id, p).second) throw std::invalid_argument("duplicate order id " + std::to_string(p.id));
                              },
                              [&](const Cancel& c) {
                                  auto [it, fresh] = cancel_at.try_emplace(c.id, c.time);
                                  if (!fresh) it->second = std::min(it->second, c.time);  // the earliest cancel wins
                              }},
                   e);
    }
    for (const auto& [id, time] : cancel_at) {
        (void)time;
        if (!places.contains(id)) throw std::invalid_argument("cancel of unknown order " + std::to_string(id));
    }
    std::vector<long long> buy_s, buy_e, sell_s, sell_e, all_s, all_e;
    for (const auto& [id, p] : places) {
        long long end = p.end;
        if (auto c = cancel_at.find(id); c != cancel_at.end()) end = std::min(end, c->second);
        if (end <= p.start) continue;  // empty, or cancelled before it began
        auto& s = p.side == Side::Buy ? buy_s : sell_s;
        auto& e = p.side == Side::Buy ? buy_e : sell_e;
        s.push_back(p.start);
        e.push_back(end);
        all_s.push_back(p.start);
        all_e.push_back(end);
    }
    return {detail::peak_of(std::move(buy_s), std::move(buy_e), false), detail::peak_of(std::move(sell_s), std::move(sell_e), false),
            detail::peak_of(std::move(all_s), std::move(all_e), false)};
}
```

## 4. Part 3：在线版

订单和撤单是一个个实时到的，不能先攒起来排序。每来一个事件都要能回答：到现在为止最大重叠是多少？`t` 时刻有几张单活着？

### 4.1 差分数组 + 有序 map

差分数组（difference array）：下单在 `start` 处 +1、在 `end` 处 −1，某时刻的活跃数 = 这个时刻及以前所有差分之和。事件按时间到达，所以**过去**的差分已经累加成确定的活跃数；只有**未来**的差分（订单的计划结束时间）需要等着。每个方向（买、卖、再加一个「全部」）各有一个 `Lane`：

| 成员 | 含义 |
|---|---|
| `expiries : map<end, count>` | 未来差分：在某个结束时间结束的订单数；`begin()` 就是最近的结束 |
| `history : map<time, live>` | 已确定的阶梯函数：从 `time` 起活跃数是 `live`；`upper_bound(t)` 的前一个元素回答「t 时刻有几张」 |
| `live`、`committed_max/time` | 当前活跃数；已「封账」的最大值及最早时刻 |

### 4.2 同一时间戳是一批：最大值何时才算数

同一时间戳内的事件视为一批。先 `place` 两张、再在**同一时刻** `cancel` 其中一张：那张的区间是空的，`maxSoFar` 要**追溯修正**，不能被瞬时的 2 污染。做法：时钟**离开**一个时间戳时，才把该时间戳的最终 `live` 并进 `committed_max`（`advance`）；`peak()` 再把当前还没封账的时间戳也算一个候选，相等时较早的（已封账的）赢。

```
place(1..5)   t=5 时 live=5     peak() = (5, 5)
cancel(4, 5)  同一时刻         live=4     peak() = (4, 4)   ← 最大值 4 最早出现在 t=4（已封账），不是被 t=5 的瞬时 5 污染
```

### 4.3 `std::map` 的两个坑

* `operator[]` 在键不存在时**插入**一个默认值。只读的 `live_at` 如果写成 `history[t]`，每次查询都让 `history` 变大，还给每个被查询的时刻「编造」一条记录。读路径用 `find` / `upper_bound`，并且让函数是 `const` 的——编译器就会拦住你。
* `upper_bound(t)` 如果等于 `begin()`，说明 `t` 在第一条记录之前（那时活跃数是 0）；这时 `std::prev(begin())` 是未定义行为，必须先判断。

```cpp
// std::map::operator[] INSERTS a default-constructed value for a missing key.  A "read" written with it grows the map.
#include <iostream>
#include <iterator>
#include <map>

int live_at_wrong(std::map<long long, int>& history, long long t) { return history[t]; }  // inserts (t, 0) when t is missing

int live_at_right(const std::map<long long, int>& history, long long t) {
    auto it = history.upper_bound(t);  // first step strictly after t
    return it == history.begin() ? 0 : std::prev(it)->second;  // the step at or before t; before the first step: 0
}

int main() {
    std::map<long long, int> history = {{5, 1}, {9, 0}};
    std::cout << "size before: " << history.size() << "\n";
    for (long long t = 0; t < 12; ++t) (void)live_at_right(history, t);
    std::cout << "after 12 correct reads: " << history.size() << "\n";
    for (long long t = 0; t < 12; ++t) (void)live_at_wrong(history, t);
    std::cout << "after 12 reads through operator[]: " << history.size() << "  (each inserted step claims the count dropped to 0)\n";
}
```

```text
size before: 2
after 12 correct reads: 2
after 12 reads through operator[]: 12  (each inserted step claims the count dropped to 0)
```

排空 `expiries` 用 `extract(begin())`：摘下节点，取走 `key()` / `mapped()`，节点随即销毁；循环里不保留任何指向已删节点的迭代器。

### 4.4 代码

```cpp
/// Online version: events arrive in time order (equal timestamps allowed) and every call is O(log n).
///
/// Per lane (buy, sell, all) it keeps a difference array in two ordered maps:
///   expiries  future decrements: planned end time -> how many orders end then (begin() = the next end);
///   history   settled step function: time -> live count from that time on (upper_bound + prev answers "live at t").
/// Events with the same timestamp form one batch: place two orders, cancel one of them at the same instant, and that order's
/// interval is empty, so the instantaneous 2 must not become the maximum.  Hence a timestamp's value is committed to
/// the running maximum only when the clock moves past it; peak() also looks at the still-open current timestamp.
class OnlineOverlap {
public:
    /// Order at time `start` (not before the last event), planned to end at `end` (exclusive).
    void place(long long id, Side side, long long start, long long end) {
        (void)Place(id, side, start, end);  // validation only: non-negative, end >= start, valid enum
        if (start < now_) throw std::invalid_argument("event out of order: " + std::to_string(start) + " < " + std::to_string(now_));
        if (orders_.contains(id)) throw std::invalid_argument("duplicate order id " + std::to_string(id));
        advance_to(start);
        orders_.emplace(id, Order{side, start, end});
        if (end > start) {  // an empty interval changes no count
            Lane& lane = lane_of(side);
            lane.open(end);
            all_.open(end);
            lane.stamp();
            all_.stamp();
        }
    }

    /// Cancel at `time`: true if it really shortened a live order; false if it had already ended or been cancelled.
    bool cancel(long long id, long long time) {
        auto it = orders_.find(id);
        if (it == orders_.end()) throw std::invalid_argument("cancel of unknown order " + std::to_string(id));
        if (time < now_) throw std::invalid_argument("event out of order: " + std::to_string(time) + " < " + std::to_string(now_));
        advance_to(time);
        Order& o = it->second;
        const bool effective = o.end > time;  // start <= now == time, so end > time means still live
        if (effective) {
            Lane& lane = lane_of(o.side);
            lane.cancel(o.end);
            all_.cancel(o.end);
            lane.stamp();
            all_.stamp();
            o.end = time;  // a second cancel (or the planned end) now sees "already ended"
        }
        return effective;
    }

    /// Dispatch a variant event.  Place -> true; Cancel -> the result of cancel().
    bool apply(const OrderEvent& e) {
        return std::visit(overloaded{[&](const Place& p) {
                                         place(p.id, p.side, p.start, p.end);
                                         return true;
                                     },
                                     [&](const Cancel& c) { return cancel(c.id, c.time); }},
                          e);
    }

    /// Move the clock without an event so that orders ending by `t` leave the live count.
    void advance_to(long long t) {
        if (t < now_) throw std::invalid_argument("time went backwards: " + std::to_string(t) + " < " + std::to_string(now_));
        if (t > now_) {
            for (Lane& l : lanes_) l.advance(t);
            all_.advance(t);
            now_ = t;
        }
    }

    long long now() const { return now_; }
    int live_now() const { return all_.live; }
    int live_now(Side s) const { return lane_of(s).live; }
    /// Live count at time t (0 <= t <= now).  Looking ahead is not supported.
    int live_at(long long t) const { check_past(t); return all_.live_at(t); }
    int live_at(Side s, long long t) const { check_past(t); return lane_of(s).live_at(t); }
    /// Maximum so far (including the current timestamp) and its earliest time.
    Peak peak() const { return all_.peak(); }
    Peak peak(Side s) const { return lane_of(s).peak(); }
    int max_so_far() const { return peak().count; }
    int max_so_far(Side s) const { return peak(s).count; }
    /// Number of recorded steps (all lanes); a read must never add one.
    std::size_t history_size() const { return all_.history.size() + lanes_[0].history.size() + lanes_[1].history.size(); }

private:
    struct Order {
        Side side;
        long long start, end;
    };

    struct Lane {
        std::map<long long, int> expiries;
        std::map<long long, int> history;
        int live = 0;
        int committed_max = 0;  // best value over timestamps the clock has already passed
        long long committed_time = 0;
        long long last_tick = 0;

        /// Clock moves from last_tick to `to` (> last_tick): commit last_tick's final value, fold in the ends <= to.
        void advance(long long to) {
            if (live > committed_max) { committed_max = live; committed_time = last_tick; }
            while (!expiries.empty() && expiries.begin()->first <= to) {
                auto node = expiries.extract(expiries.begin());
                live -= node.mapped();
                history.insert_or_assign(node.key(), live);  // the step down happens at the end time
            }
            last_tick = to;
        }
        void open(long long end) { ++live; ++expiries[end]; }
        void cancel(long long end) {
            --live;
            auto it = expiries.find(end);
            if (--it->second == 0) expiries.erase(it);
        }
        void stamp() { history.insert_or_assign(last_tick, live); }
        int live_at(long long t) const {
            auto it = history.upper_bound(t);  // first step strictly after t
            return it == history.begin() ? 0 : std::prev(it)->second;
        }
        Peak peak() const { return live > committed_max ? Peak{live, last_tick} : Peak{committed_max, committed_time}; }
    };

    Lane& lane_of(Side s) { return lanes_[static_cast<std::size_t>(s)]; }
    const Lane& lane_of(Side s) const { return lanes_[static_cast<std::size_t>(s)]; }
    void check_past(long long t) const {
        if (t < 0 || t > now_) throw std::invalid_argument("t must be in [0, now=" + std::to_string(now_) + "]: " + std::to_string(t));
    }

    std::unordered_map<long long, Order> orders_;
    std::array<Lane, 2> lanes_;
    Lane all_;
    long long now_ = 0;
};
```

其它语义：`place` 的 `start` 必须 ≥ 上一个事件的时间（相等允许）；`cancel` 返回 `true` 表示真的缩短了一张还活着的单（已自然结束 / 已撤过 → `false`；`id` 不存在、时间倒退 → `invalid_argument`）；失败的调用**不改变状态**（先校验、后修改）。`liveAt(t)` 只支持 `0 <= t <= now`，看未来（预测）不支持——因为未来的撤单还没发生。`OnlineOverlap` 是普通值类型，拷贝是深拷贝。

## 5. Part 4：坐标压缩 + 懒标记线段树

时间戳是纳秒，范围 10^18，数组开不出来；而且订单可能以任意顺序加入和撤销，还要问「某个时间段内的最大重叠」。

### 5.1 坐标压缩（coordinate compression）

活跃数只会在区间的**端点**处变化。把所有会用到的端点排序去重成 `c[0] < c[1] < … < c[m−1]`，相邻两个端点之间的 `[c[j], c[j+1])` 叫一个**基本段**（elementary segment），每个基本段内活跃数是常数。区间 `[s, e)` 恰好覆盖基本段 `idx(s) .. idx(e)−1`，`idx` 用二分查找（`std::lower_bound`）求。值域 10^18 的问题变成了只有 `m−1 ≤ 2n` 个格子的问题。二分只用比较，不做减法，所以接近 `LLONG_MAX` 也不会溢出。

### 5.2 线段树（segment tree）：区间加、区间最大

线段树把 `[0, size)` 的格子一分为二、递归，用数组 `mx[]`、`add[]` 存（堆的布局：结点 `i` 的孩子是 `2i` 和 `2i+1`）。

* `add[i]`：整段还欠着的加数，**永久保留**，不往下推（标记永久化）；
* `mx[i]`：这段里的最大值，已经含 `add[i]` 和子树里所有的加数，但不含祖先的 `add`。

更新一个区间时，被完全覆盖的结点只改自己的 `add` 和 `mx`，部分覆盖的递归下去，回来时 `mx[i] = add[i] + max(mx[左], mx[右])`。查询时一路把经过的结点的 `add` 累加起来。两种操作都是 `O(log m)`；查询是 `const` 的——不需要把标记下推。

下面的程序用 4 个基本段的小树，打印每次更新后的 `mx` 和 `add`（下标 1..7）：

```cpp
// A tiny lazy segment tree (range add, range max) with permanent tags, printed after every update.
// 4 elementary segments, leaves at nodes 4..7:           node 1  [0,3]
//                                                   node 2 [0,1]   node 3 [2,3]
//                                                 node 4 [0]  node 5 [1]  node 6 [2]  node 7 [3]
#include <algorithm>
#include <iostream>
#include <vector>

struct Tree {
    int size = 4;
    std::vector<int> mx = std::vector<int>(8, 0), add = std::vector<int>(8, 0);

    void range_add(int node, int nl, int nr, int l, int r, int delta) {
        if (l <= nl && nr <= r) { add[static_cast<std::size_t>(node)] += delta; mx[static_cast<std::size_t>(node)] += delta; return; }
        const int mid = nl + (nr - nl) / 2;
        if (l <= mid) range_add(2 * node, nl, mid, l, r, delta);
        if (r > mid) range_add(2 * node + 1, mid + 1, nr, l, r, delta);
        const auto n = static_cast<std::size_t>(node);
        mx[n] = add[n] + std::max(mx[2 * n], mx[2 * n + 1]);
    }
    int range_max(int node, int nl, int nr, int l, int r) const {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) return mx[n];
        const int mid = nl + (nr - nl) / 2;
        int best = -1'000'000;
        if (l <= mid) best = std::max(best, range_max(2 * node, nl, mid, l, r));
        if (r > mid) best = std::max(best, range_max(2 * node + 1, mid + 1, nr, l, r));
        return best + add[n];
    }
    void print(const char* what) const {
        std::cout << what << "\n  mx : ";
        for (int i = 1; i < 8; ++i) std::cout << mx[static_cast<std::size_t>(i)] << " ";
        std::cout << "\n  add: ";
        for (int i = 1; i < 8; ++i) std::cout << add[static_cast<std::size_t>(i)] << " ";
        std::cout << "\n";
    }
};

int main() {
    Tree t;
    t.range_add(1, 0, 3, 0, 3, 1);  // covers the whole root: only add[1] and mx[1] change
    t.print("add [0,3]");
    t.range_add(1, 0, 3, 1, 2, 1);  // splits: node 5 (segment 1) and node 6 (segment 2) get tagged, parents recompute
    t.print("add [1,2]");
    std::cout << "max over [0,0] = " << t.range_max(1, 0, 3, 0, 0) << ", over [1,1] = " << t.range_max(1, 0, 3, 1, 1)
              << ", over [0,3] = " << t.range_max(1, 0, 3, 0, 3) << "\n";
    std::cout << "the tag on the root (" << t.add[1] << ") was never pushed down; the query adds it on the way back up\n";
}
```

```text
add [0,3]
  mx : 1 0 0 0 0 0 0 
  add: 1 0 0 0 0 0 0 
add [1,2]
  mx : 2 1 1 0 1 1 0 
  add: 1 0 0 0 1 1 0 
max over [0,0] = 1, over [1,1] = 2, over [0,3] = 2
the tag on the root (1) was never pushed down; the query adds it on the way back up
```

第一次 `add [0,3]` 完整覆盖了根：只有 `add[1]` 和 `mx[1]` 变成 1，其余不动。第二次 `add [1,2]`：跨左右两棵子树，只给叶子 5、6 打标记，再回算父结点。查询 `[0,0]` 返回 1（= 根的标记），`[1,1]` 返回 2（叶子 5 的标记 + 根的标记）。

### 5.3 代码

```cpp
/// Interval counting over huge coordinates: coordinate compression + a lazy segment tree with "permanent" tags.
///
/// Compression: the live count only changes at endpoints.  Sort and dedupe them into c[0] < ... < c[m-1]; the gap
/// [c[j], c[j+1]) is an elementary segment with a constant count.  [s, e) covers segments idx(s) .. idx(e)-1.
/// Segment tree over those segments, stored in two std::vector<int> (heap layout, children of i are 2i and 2i+1):
///   add[i]  the amount still owed to the whole range of node i (never pushed down),
///   mx[i]   the maximum over node i's range, including add[i] and everything below, excluding ancestors' tags.
/// A query walks down and adds each visited node's tag on the way back up: no push-down, so queries stay const.
class IntervalIndex {
public:
    /// Every endpoint that will ever be used (any order, duplicates allowed).
    explicit IntervalIndex(std::span<const long long> coordinates) : coords_(coordinates.begin(), coordinates.end()) {
        std::sort(coords_.begin(), coords_.end());
        coords_.erase(std::unique(coords_.begin(), coords_.end()), coords_.end());
        segs_ = coords_.empty() ? 0 : static_cast<int>(coords_.size()) - 1;
        size_ = 1;
        while (size_ < std::max(1, segs_)) size_ <<= 1;
        mx_.assign(2 * static_cast<std::size_t>(size_), 0);
        add_.assign(2 * static_cast<std::size_t>(size_), 0);
    }

    /// Build from intervals: collect endpoints, compress, add each.
    static IntervalIndex of(std::span<const Interval> intervals) {
        std::vector<long long> pts;
        pts.reserve(intervals.size() * 2);
        for (const Interval& iv : intervals) { pts.push_back(iv.start); pts.push_back(iv.end); }
        IntervalIndex idx{std::span<const long long>(pts)};
        for (const Interval& iv : intervals) idx.add(iv.start, iv.end);
        return idx;
    }

    /// Part 1's answer through compression + segment tree; must equal the sweep.
    static int max_overlap(std::span<const Interval> intervals) { return of(intervals).max(); }

    void add(long long start, long long end) { update(start, end, 1); }
    /// Undo a previous add of the same interval (caller's responsibility).
    void remove(long long start, long long end) { update(start, end, -1); }

    int max() const { return segs_ == 0 ? 0 : mx_[1]; }

    /// Live count at time t; 0 outside all endpoints; the right end is exclusive.
    int live_at(long long t) const {
        const int j = floor_index(t);
        if (j < 0 || j >= segs_) return 0;
        return range_max(1, 0, size_ - 1, j, j);
    }

    /// Maximum live count at any time in [from, to).  to < from -> invalid_argument; to == from -> 0.
    int max_in(long long from, long long to) const {
        if (to < from) throw std::invalid_argument("to < from: " + std::to_string(to) + " < " + std::to_string(from));
        if (to == from || segs_ == 0) return 0;
        const int lo = std::max(0, floor_index(from));  // the segment containing `from` (or the first one)
        const int hi = std::min(segs_ - 1, lower_bound_index(to) - 1);  // the last segment starting before `to`
        if (lo > hi) return 0;
        return std::max(0, range_max(1, 0, size_ - 1, lo, hi));
    }

    int coordinate_count() const { return static_cast<int>(coords_.size()); }
    int segment_count() const { return segs_; }

private:
    void update(long long start, long long end, int delta) {
        if (end < start) throw std::invalid_argument("end < start: " + std::to_string(end) + " < " + std::to_string(start));
        const int lo = exact_index(start);
        const int hi = exact_index(end);
        if (lo == hi) return;  // empty interval
        range_add(1, 0, size_ - 1, lo, hi - 1, delta);
    }

    void range_add(int node, int nl, int nr, int l, int r, int delta) {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) {  // fully covered: tag this node only
            add_[n] += delta;
            mx_[n] += delta;
            return;
        }
        const int mid = nl + (nr - nl) / 2;
        if (l <= mid) range_add(2 * node, nl, mid, l, r, delta);
        if (r > mid) range_add(2 * node + 1, mid + 1, nr, l, r, delta);
        mx_[n] = add_[n] + std::max(mx_[2 * n], mx_[2 * n + 1]);
    }

    int range_max(int node, int nl, int nr, int l, int r) const {
        const auto n = static_cast<std::size_t>(node);
        if (l <= nl && nr <= r) return mx_[n];
        const int mid = nl + (nr - nl) / 2;
        int best = INT_MIN;  // at least one branch below runs (l <= r), so this is always replaced
        if (l <= mid) best = std::max(best, range_max(2 * node, nl, mid, l, r));
        if (r > mid) best = std::max(best, range_max(2 * node + 1, mid + 1, nr, l, r));
        return best + add_[n];  // this node's tag applies to its whole range and was never pushed down
    }

    // Binary searches use comparisons only: no subtraction, no overflow near LLONG_MAX.
    int exact_index(long long x) const {
        auto it = std::lower_bound(coords_.begin(), coords_.end(), x);
        if (it == coords_.end() || *it != x) throw std::invalid_argument("unknown coordinate: " + std::to_string(x));
        return static_cast<int>(it - coords_.begin());
    }
    /// Largest j with coords[j] <= x, or -1.
    int floor_index(long long x) const { return static_cast<int>(std::upper_bound(coords_.begin(), coords_.end(), x) - coords_.begin()) - 1; }
    /// Smallest j with coords[j] >= x, or coords.size().
    int lower_bound_index(long long x) const { return static_cast<int>(std::lower_bound(coords_.begin(), coords_.end(), x) - coords_.begin()); }

    std::vector<long long> coords_;
    int segs_ = 0;
    int size_ = 1;
    std::vector<int> mx_, add_;
};

}  // namespace overlap
```

要点：

1. 叶子数 `size_` 取 ≥ 基本段数的最小 2 的幂；多出来的叶子永远是 0，不会混进查询（查询只访问 `[0, segs)`）。
2. `update` 先对**两个端点**都调用 `exact_index`（未知端点 → `invalid_argument`），**再**改树：失败的调用不会留下「改了一半」的树。
3. `max_in(from, to)`：`lo` = `from` 所在的基本段（`from` 在最左端点之前就取第 0 段），`hi` = 最后一个起点 `< to` 的基本段；范围伸出所有端点之外的部分活跃数是 0，所以结果 `max(0, …)`。
4. `range_max` 里的 `INT_MIN` 初值：`l <= r` 保证至少一个分支会执行，所以 `INT_MIN + add` 不会真的发生（那会是有符号溢出）。
5. 下标计算 `nl + (nr - nl) / 2` 而不是 `(nl + nr) / 2`。这里数值不大，但养成习惯。

追问核心：**如果只要全局最大，为什么扫描线更好？** 扫描线 `O(n log n)`（只是排序），常数小、代码短；线段树在**需要动态更新/区间查询**时才值得：任意顺序的 `add` / `remove`、`maxIn(from, to)`、`liveAt(t)`。

## 6. 和 Java 版的差异（以及为什么）

| Java | C++ | 为什么 |
|---|---|---|
| `long[][] intervals`，检查 `length == 2`、`null` | `span<const Interval>` | 固定两个字段；`span` 只读视图，不能被修改，也不可能是 `null` |
| `IllegalArgumentException` | `std::invalid_argument` | 同样是「调用方错了」的异常 |
| `record` + 紧凑构造器校验 | `struct` + 构造函数里 `throw` | 对象存在就代表不变量成立 |
| `sealed interface` + `switch` 模式匹配 | `std::variant` + `std::visit(overloaded{...})` | 都是闭合层级 + 穷尽检查，C++ 在编译期检查 |
| `enum Side`（只有两个值） | `enum class Side`（可以装别的值） | C++ 的 enum 不保证值域；输入边界要自己检查 |
| `TreeMap.firstEntry()` / `floorEntry()` | `begin()` / `upper_bound` + `prev` | 要自己处理「没有」的情况（迭代器等于 `begin()` / `end()`） |
| `TreeMap.compute(...)` 删 0 计数 | `find` + 减一 + `erase` | `operator[]` 会插入 |
| `Arrays.sort(long[])` | `std::sort`（严格弱序的比较器） | 比较器写错是 UB，不是排序结果不对 |
| `int` 溢出静默回绕 | 有符号溢出是 UB | 所有 `end + 1`、`end - start` 都不能写 |
| 垃圾回收 | `OnlineOverlap` 深拷贝 / 移动 | 值语义：拷贝出来的在线对象互相独立 |

## 7. 陷阱

1. **同一时刻开始排在结束前面**：`[1,3)` + `[3,5)` 变成 2（2.1）。
2. **比较器写成 `<=`**：`std::sort` 未定义行为（2.3）。
3. **闭区间转半开 `end + 1`**：`LLONG_MAX` 处有符号溢出（2.2）。
4. **`end - start`、`(a + b) / 2`**：大时间戳溢出。
5. **`std::map::operator[]` 当读用**：查询把 map 变大、编造记录（4.3）。
6. **`prev(upper_bound(t))` 不检查 `begin()`**：在第一条记录之前查询是未定义行为。
7. **同一时间戳内 place 后 cancel 污染最大值**：最大值要等时间戳「过去」才算数（4.2）。
8. **`enum class` 当作只有枚举值**：`static_cast<Side>(7)` 越界下标。
9. **线段树「查询时下推标记」**：查询变成非 `const`，并发读也不安全；用永久化标记。
10. **`exact_index` 在改树之后才检查**：未知端点导致半更新的树。

## 8. 面试官会追问什么（senior）

**Q1. 「如果 `end` 是包含的呢？」** 开始排在结束前面（或双指针里 `ends[j] < s` 代替 `<=`）；不要转成 `end + 1`。

**Q2. 每张订单有数量（qty）呢？** `+1 / −1` 换成 `+qty / −qty`，求同时在簿的最大总量（用 `long long` 并注意溢出）。

**Q3. 买方在簿量 − 卖方在簿量的最大绝对值？** 带符号的差分：买 `+qty`、卖 `−qty`，扫一遍，同时记最大和最小前缀和。

**Q4. `t > now` 的预测查询为什么贵？** 未来可能还有撤单，答案不确定；要精确就得把「已知订单的计划结束」和「还会到来的撤单」分开建模，或者重建线段树。

**Q5. 在线版为什么每个事件 `O(log n)`？** `map` 的插入/删除/查找各 `O(log n)`；每个订单的结束事件最多被折叠进 `live` 一次。

**Q6. 线段树什么时候才值得？** 需要任意顺序的增删、区间最大查询；只要全局最大，排序 + 扫描线更简单更快。

**Q7. 为什么用「标记永久化」而不是 push-down？** 查询不用修改树，所以可以是 `const` 的、并发读安全；代码短；代价是查询要累加路径上的 `add`。

## 9. 自测

1. `[1,3)` 与 `[3,5)` 同一时刻有一个结束事件和一个开始事件，哪个先处理？为什么？
2. `std::sort(v.begin(), v.end(), [](auto a, auto b){ return a <= b; })` 有什么问题？
3. 闭区间 `[s, e]` 与半开区间 `[s, e)` 在双指针里的差别是什么？为什么不能用 `e + 1`？
4. `history[t]` 在 `const` 成员函数里能不能写？写了会怎样？
5. 同一时间戳内 `place` 两张、`cancel` 一张，`max_so_far` 为什么要「追溯修正」？
6. `static_cast<Side>(7)` 会造成什么问题？怎么防？
7. 线段树里 `add[i]` 与 `mx[i]` 分别是什么？查询时为什么要在回溯时加上 `add[node]`？
8. 为什么 `IntervalIndex::update` 要先对两个端点都做 `exact_index`，再修改树？

<details><summary>答案</summary>

1. 先处理结束。否则 `live` 会短暂变成 2，答案错成 2。
2. `<=` 不是严格弱序（`comp(x, x)` 为 `true`）；有很多相等元素时 `std::sort` 可能越界，是未定义行为。要用 `<`。
3. 半开：`ends[j] <= s` 算已结束；闭区间：`ends[j] < s` 才算已结束。`e + 1` 在 `e = LLONG_MAX` 时有符号溢出（UB）。
4. 不能：`operator[]` 是非 `const` 的（会插入）。在非 `const` 函数里写会给不存在的时刻插入一条记录，让 map 增长，并编造一个「活跃数为 0」的阶梯。
5. 被撤的那张订单的区间是空的，它从没真正活过；时间戳还没「过去」时最大值不是最终的，所以只在时钟离开该时间戳时才把它并进 `committed_max`。
6. 它是 `enum class` 的合法值，但没有对应的下标/分支：`lanes[7]` 越界。在构造函数/入口检查 `side` 是 `Buy` 或 `Sell`。
7. `add[i]`：整段还欠着的加数（永久，不下推）；`mx[i]`：该段最大值，含 `add[i]` 与子树，不含祖先。回溯时补上经过结点的 `add`，因为这些标记没有下推到孩子里。
8. 如果先改树、再发现第二个端点未知，调用虽然抛了异常，树却已经被改过；先把两个端点都校验完，失败的调用就不会留下任何痕迹。
</details>

## 延伸阅读

* LeetCode 253（Meeting Rooms II）是 Part 1 的原型；731 / 732（My Calendar II / III）是 Part 3 / 4 的原型。
