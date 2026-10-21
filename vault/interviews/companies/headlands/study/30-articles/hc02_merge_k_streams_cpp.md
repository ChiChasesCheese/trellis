# hc02 · 合并 K 个有序数据流（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。下面所有代码块按顺序拼起来就是一份能编译、能通过全部测试的完整实现。

## 1. 题目

给你 k 个各自**升序**（允许相等）的序列，合并成一个升序序列。然后面试官一路追问：

| Part | 内容 |
|---|---|
| 1 | 合并 k 个 `vector`。相等元素按**序列编号小的在前**（稳定）；序列可以为空、k 可以为 0；某个序列不是升序要报错并说出位置；比较不能写 `a - b` |
| 2 | **惰性**：构造时不碰任何 source；source 可以是无限的；输出一个元素后，那个序列的下一个元素等到下一次调用才去取 |
| 3 | 现实里 source 是会阻塞的 client：每个 source 一个生产者线程 + 一个有界队列；`try_next()` 立刻返回，`next()` 阻塞；`close()`；source 出错要传播 |
| 4 | 一次性合并并返回全部结果；任何一个 source 失败 → 取消其余 → 抛异常；离开函数时所有线程都已结束 |

```
[[1,4,7],[2,5,8],[3,6,9]]  →  [1,2,3,4,5,6,7,8,9]
[[1,4,5],[1,3,4],[2,6]]    →  [1,1,2,3,4,4,5,6]
```

## 2. Part 1：堆合并

### 2.1 从最笨的解法推导

* **全部拼起来再排序**：O(N log N)（N = 元素总数）。没有用上"每个序列已经有序"这个条件。
* **两两合并**：合并 k−1 次，每次扫描当前已合并的全部元素，最坏 O(N·k)。
* **堆**：每个序列只有"当前最小的未用元素"（队首）有资格成为下一个输出，所以全局最小值一定在 k 个队首里。把 k 个队首放进最小堆，弹出堆顶就是答案，再把它所在序列的下一个元素补进堆。每个元素进堆、出堆各一次，每次 O(log k)，总共 **O(N log k)**，堆里永远只有 k 个元素。

手算 `[[1,4,5],[1,3,4],[2,6]]`（括号里是序列编号）：

| 步 | 堆里的队首 | 弹出 | 补进 |
|---|---|---|---|
| 1 | 1(0) 1(1) 2(2) | 1(0) | 4(0) |
| 2 | 4(0) 1(1) 2(2) | 1(1) | 3(1) |
| 3 | 4(0) 3(1) 2(2) | 2(2) | 6(2) |
| 4 | 4(0) 3(1) 6(2) | 3(1) | 4(1) |
| 5 | 4(0) 4(1) 6(2) | 4(0) | 5(0) |
| … | | 4(1) 5(0) 6(2) | |

第 1 步里 `1(0)` 和 `1(1)` 值相等，序列 0 先出——这是**稳定**要求，比较键必须是 `(值, 序列编号)`。

### 2.2 `std::priority_queue` 的四个事实

1. **它是大顶堆。** `top()` 是按比较器"最大"的元素。想让最小的先出来，比较器要表达"a 排在 b **后面**"。
2. **它不稳定。** 值相等的元素以什么顺序出堆，标准没有规定，所以序列编号必须写进比较器。
3. **`top()` 返回 `const&`，`pop()` 之后这个引用就悬空了。** 先把需要的小结构拷出来再 `pop()`。
4. **只能依赖 `<`。** 元素类型可能只有 `operator<`：判断相等要写 `!less(a, b) && !less(b, a)`，不要用 `==`、`>`，更不要用 `a - b`。

```cpp
// std::priority_queue pops the LARGEST element under its comparator, and it is not stable.
#include <iostream>
#include <queue>
#include <vector>

struct Head {
    int value;
    int stream;
};

template <class Cmp>
void drain(const char* label, Cmp cmp) {
    std::priority_queue<Head, std::vector<Head>, Cmp> pq(cmp);
    for (int s = 0; s < 6; ++s) pq.push({1, s});  // six equal values from streams 0..5
    for (int s = 0; s < 3; ++s) pq.push({0, s});  // three smaller ones
    std::cout << label;
    while (!pq.empty()) {
        std::cout << pq.top().value << ':' << pq.top().stream << ' ';
        pq.pop();
    }
    std::cout << '\n';
}

int main() {
    std::priority_queue<int> by_default;  // default comparator std::less: a MAX-heap
    for (int x : {1, 5, 3}) by_default.push(x);
    std::cout << "default top: " << by_default.top() << "   (largest first)\n";

    // "a comes later than b" -> the smallest value comes out first.  Ties: whatever the heap internals give.
    drain("value only        : ", [](const Head& a, const Head& b) { return a.value > b.value; });
    // Add the stream index to the comparator and the order is fully determined: lower stream first.
    drain("value, then stream: ", [](const Head& a, const Head& b) {
        if (a.value != b.value) return a.value > b.value;
        return a.stream > b.stream;
    });
}
```

输出：第一行是 `5`（默认比较器 `std::less` 给出大顶堆）；"只比较值"那一行里，值为 1 的六个元素这次按序列编号 `3 1 2 5 4 0` 出来（标准不保证任何顺序）；加上序列编号之后固定为 `0 1 2 3 4 5`。

### 2.3 `merge`

```cpp
/// An input sequence is not ascending.  `stream` = index of the sequence, `position` = index of the offending element in it.
class UnsortedInputException : public std::runtime_error {
public:
    UnsortedInputException(int stream, std::size_t position)
        : std::runtime_error("stream " + std::to_string(stream) + " is not sorted at position " + std::to_string(position)),
          stream_(stream), position_(position) {}
    int stream() const noexcept { return stream_; }
    std::size_t position() const noexcept { return position_; }

private:
    int stream_;
    std::size_t position_;
};
```

`UnsortedInputException` 带两个字段：序列编号和违规元素在该序列里的下标。

```cpp
/// Merge k sorted vectors.  Equal elements come out in stream order (stable).  Only `less` is used: no ==, no >, no a - b.
/// The heap holds (stream, position) pairs, never copies of elements; the only copy of each element is the one into the result.
template <class T, class Less = std::less<T>>
std::vector<T> merge(const std::vector<std::vector<T>>& lists, Less less = {}) {
    struct Head {
        int stream;
        std::size_t pos;
    };
    // std::priority_queue pops the LARGEST element under its comparator, so the comparator says "a comes LATER than b".
    auto later = [&](const Head& a, const Head& b) {
        const T& x = lists[a.stream][a.pos];
        const T& y = lists[b.stream][b.pos];
        if (less(y, x)) return true;
        if (less(x, y)) return false;
        return a.stream > b.stream;  // tie: the smaller stream index wins; priority_queue itself is not stable
    };
    std::priority_queue<Head, std::vector<Head>, decltype(later)> heap(later);
    std::size_t total = 0;
    for (std::size_t s = 0; s < lists.size(); ++s) {
        total += lists[s].size();
        if (!lists[s].empty()) heap.push({static_cast<int>(s), 0});
    }
    std::vector<T> out;
    out.reserve(total);
    while (!heap.empty()) {
        const Head h = heap.top();  // copy the 16 bytes: pop() destroys the element top() refers to
        heap.pop();
        const auto& list = lists[h.stream];
        out.push_back(list[h.pos]);
        if (h.pos + 1 < list.size()) {
            if (less(list[h.pos + 1], list[h.pos])) throw UnsortedInputException(h.stream, h.pos + 1);
            heap.push({h.stream, h.pos + 1});
        }
    }
    return out;
}
```

要点：

* **堆里放 `(stream, pos)`，不放元素。** 元素留在原 `vector` 里，堆元素只有 16 字节；元素类型再大也不会被拷进拷出。整个函数对每个元素只拷贝一次：`out.push_back(list[h.pos])`。
* `later` 先看值，再看序列编号：`a.stream > b.stream` 表示"编号大的排在后面"，所以编号小的先出。
* `const Head h = heap.top();` 先拷再 `pop()`（事实 3）。
* 顺序检查在"取下一个元素"时做：`less(next, current)` 才算乱序，相等不算。位置是下一个元素的下标。
* `reserve(total)`：只分配一次，`push_back` 不会触发扩容搬运。
* 输入是 `const&`，函数不会修改它。

### 2.4 `merge_longs`：不拷贝、不装箱的堆

```cpp
/// Performance version: a hand-written heap of stream indices over the original arrays.  No element is copied into the heap.
inline std::vector<long long> merge_longs(const std::vector<std::vector<long long>>& arrays) {
    const std::size_t k = arrays.size();
    std::size_t total = 0;
    for (const auto& a : arrays) total += a.size();
    std::vector<long long> out;
    out.reserve(total);
    std::vector<std::size_t> pos(k, 0);
    std::vector<int> heap;
    heap.reserve(k);
    for (std::size_t s = 0; s < k; ++s)
        if (!arrays[s].empty()) heap.push_back(static_cast<int>(s));

    auto less = [&](int a, int b) {
        const long long va = arrays[a][pos[a]], vb = arrays[b][pos[b]];
        return va < vb || (va == vb && a < b);  // compare, never subtract: LLONG_MAX - LLONG_MIN overflows
    };
    auto sift_down = [&](std::size_t i, std::size_t n) {
        if (n == 0) return;
        const int s = heap[i];
        for (;;) {
            std::size_t child = 2 * i + 1;
            if (child >= n) break;
            if (child + 1 < n && less(heap[child + 1], heap[child])) ++child;
            if (!less(heap[child], s)) break;
            heap[i] = heap[child];
            i = child;
        }
        heap[i] = s;
    };
    std::size_t n = heap.size();
    for (std::size_t i = n / 2; i-- > 0;) sift_down(i, n);  // bottom-up heapify, O(k); `i-- > 0` is the safe unsigned loop
    while (n > 0) {
        const int s = heap[0];
        const long long v = arrays[s][pos[s]];
        out.push_back(v);
        if (++pos[s] < arrays[s].size()) {
            if (arrays[s][pos[s]] < v) throw UnsortedInputException(s, pos[s]);
        } else {
            heap[0] = heap[--n];  // stream exhausted: move the last heap entry to the top
        }
        sift_down(0, n);
    }
    return out;
}
```

* 堆里是 `int` 序列号，比较时回到原数组取值：数据按顺序读，对 CPU 缓存友好。
* **比较用 `<`，不用 `va - vb < 0`。** `LLONG_MAX - LLONG_MIN` 是**有符号溢出，C++ 里是未定义行为**（UB），不只是"结果错"。
* `for (std::size_t i = n / 2; i-- > 0;)`：倒着数无符号下标的安全写法。`for (size_t i = n/2 - 1; i >= 0; --i)` 永远不会结束，`n == 0` 时 `n/2 - 1` 还会回绕成 `SIZE_MAX`：

```cpp
// Counting down with an unsigned index: `i >= 0` is always true, and n / 2 - 1 wraps when n == 0.
#include <cstddef>
#include <iostream>

int main() {
    const std::size_t n = 7;
    // for (std::size_t i = n / 2 - 1; i >= 0; --i) { ... }   // never ends: after 0 comes 18446744073709551615
    std::cout << "indices n/2-1 .. 0:";
    for (std::size_t i = n / 2; i-- > 0;) std::cout << ' ' << i;  // test, THEN decrement
    std::cout << "\n";

    const std::size_t empty = 0;
    std::cout << "empty / 2 - 1 = " << (empty / 2 - 1) << "   (wrapped)\n";
    std::size_t visited = 0;
    for (std::size_t i = empty / 2; i-- > 0;) ++visited;  // n == 0 is handled without a special case
    std::cout << "visited " << visited << "\n";
}
```

* 自底向上建堆是 O(k)；序列用完时把堆尾搬到堆顶再下沉（`heap[0] = heap[--n]`）。

## 3. Part 2：惰性与手写迭代器

### 3.1 为什么要惰性

数据可能在网络上、可能是无限的。如果构造时就把每个 source 的第一个元素取出来，慢的 source 会拖慢整个构造；如果输出 `x` 之后**马上**去取 `x` 所在序列的下一个元素，调用者拿到 `x` 之前就要白等一次。规则：

1. 构造时不取任何东西；
2. 第一次 `has_next()` / `next()` 才每个 source 取一个队首；
3. 输出一个元素后，它所在序列的**补位推迟到下一次调用**。

结论（测试会数）：消费 n 个元素后，source 被取元素的总次数 ≤ k + n − 1。

### 3.2 `Source` 与 `from_range`

```cpp
/// A pull source: each call yields the next element, or std::nullopt at the end.  Calling it again after the end is
/// not allowed (the merger never does).
template <class T>
using Source = std::function<std::optional<T>()>;

/// Adapt any input range to a Source.  An lvalue range is borrowed (the caller keeps it alive); an rvalue range is
/// moved in and owned.  The state lives on the heap so that copying/moving the std::function cannot invalidate the iterator.
template <std::ranges::viewable_range R>
auto from_range(R&& r) {
    using View = std::views::all_t<R>;
    using V = std::ranges::range_value_t<View>;
    struct State {
        View view;
        std::ranges::iterator_t<View> it;
        explicit State(View v) : view(std::move(v)), it(std::ranges::begin(view)) {}
    };
    auto st = std::make_shared<State>(std::views::all(std::forward<R>(r)));
    return Source<V>([st]() -> std::optional<V> {
        if (st->it == std::ranges::end(st->view)) return std::nullopt;
        std::optional<V> v(*st->it);
        ++st->it;
        return v;
    });
}
```

`Source<T>` 是一个"拉取函数"：每次调用返回下一个元素，结束时返回 `std::nullopt`。这是手写生成器（generator）最小的形状。`from_range` 把任何 range 适配成 `Source`：

* `std::views::all` 对**左值** range 给出 `ref_view`（借用，调用者必须让它活着），对**右值**给出 `owning_view`（把 range 移进来，自己拥有）；
* 迭代器放在 `shared_ptr` 管理的堆对象里：`std::function` 被拷贝或移动时，迭代器不会指向已经搬走的 range。

### 3.3 `Merger`

```cpp
/// Lazy k-way merge, written by hand as an input range.  Nothing is pulled at construction; the first has_next()/next()
/// pulls one head per source; the source that just produced the output is refilled only on the NEXT call.
/// After a source (or the order check) throws, the merger is finished: every later call rethrows the same exception.
/// Requires T to be copy-constructible (the previous element of each stream is kept for the order check).
template <class T, class Less = std::less<T>>
class Merger {
public:
    struct sentinel {};

    class iterator {
    public:
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        iterator() = default;
        explicit iterator(Merger* m) : m_(m) { fetch(); }
        const T& operator*() const { return *cur_; }
        iterator& operator++() { fetch(); return *this; }
        void operator++(int) { fetch(); }
        friend bool operator==(const iterator& it, sentinel) { return !it.cur_.has_value(); }

    private:
        void fetch() { cur_ = m_->has_next() ? std::optional<T>(m_->next()) : std::nullopt; }
        Merger* m_ = nullptr;
        std::optional<T> cur_;
    };

    explicit Merger(std::vector<Source<T>> sources, Less less = {})
        : src_(std::move(sources)), head_(src_.size()), prev_(src_.size()), count_(src_.size(), 0),
          less_(std::move(less)), heap_(ByHead{this}) {}

    // The heap's comparator holds `this`: copying or moving a Merger would leave it pointing at the old object.
    Merger(const Merger&) = delete;
    Merger& operator=(const Merger&) = delete;

    bool has_next() {
        prime();
        return !heap_.empty();
    }

    T next() {
        prime();
        if (heap_.empty()) throw std::out_of_range("merge exhausted");
        const int s = heap_.top();
        heap_.pop();
        T out = *head_[s];
        prev_[s] = std::move(head_[s]);  // remembered for the order check; also the stream to refill on the next call
        head_[s].reset();
        refill_ = s;
        return out;
    }

    iterator begin() { return iterator(this); }
    sentinel end() { return {}; }

private:
    // "a comes later than b" (priority_queue pops the largest): value first, then the stream index
    struct ByHead {
        const Merger* m;
        bool operator()(int a, int b) const {
            const T& x = *m->head_[a];
            const T& y = *m->head_[b];
            if (m->less_(y, x)) return true;
            if (m->less_(x, y)) return false;
            return a > b;
        }
    };

    void prime() {
        if (failure_) std::rethrow_exception(failure_);
        try {
            if (!started_) {
                started_ = true;
                for (int s = 0; s < static_cast<int>(src_.size()); ++s)
                    if (advance(s)) heap_.push(s);
            }
            if (refill_ >= 0) {
                const int s = refill_;
                refill_ = -1;
                if (advance(s)) heap_.push(s);
            }
        } catch (...) {
            failure_ = std::current_exception();
            throw;
        }
    }

    bool advance(int s) {
        std::optional<T> v = src_[s]();
        if (!v) return false;
        if (prev_[s] && less_(*v, *prev_[s])) throw UnsortedInputException(s, count_[s]);
        ++count_[s];
        head_[s] = std::move(v);
        return true;
    }

    std::vector<Source<T>> src_;
    std::vector<std::optional<T>> head_;   // the current head of each stream (empty if exhausted or just emitted)
    std::vector<std::optional<T>> prev_;   // the last element emitted from each stream
    std::vector<std::size_t> count_;       // elements pulled from each stream so far
    Less less_;
    bool started_ = false;
    int refill_ = -1;
    std::exception_ptr failure_;
    std::priority_queue<int, std::vector<int>, ByHead> heap_;
};
```

要点：

* **比较器里存了 `this`**（`ByHead{this}`），所以对象不能拷贝也不能移动：拷贝出来的堆还指着旧对象。这里直接 `= delete`，`static_assert(!std::is_move_constructible_v<Merger<int>>)` 在测试里钉住。
* 堆里放 `int` 序列号，比较时去 `head_` 里取值，规则和 `merge` 一样：值、再序列编号。
* `prev_[s]`：每个序列**上一个已输出**的元素，只用来检查顺序。所以 `T` 必须可拷贝；每个元素在这里拷贝一次（`T out = *head_[s]`），然后把 `head_[s]` 移进 `prev_[s]`。
* `refill_`：刚输出的那个序列，下一次调用时才补位（3.1 的规则 3）。
* **粘性失败**：source 抛异常、或顺序检查失败，异常存进 `failure_`，之后每次调用都原样重抛。否则异常之后再调用，会悄悄跳过那个坏元素。
* `iterator` + `sentinel`：C++20 的 **input range**。`begin()` 取第一个元素，`operator*` 返回缓存的当前元素，`operator==(iterator, sentinel)` 在"没有下一个"时为真。有了它，`for (int x : merged)`、`merged | std::views::take(10)` 都能用，并且满足 `std::input_iterator`。`i++` 返回 `void` 是 input iterator 允许的。

```cpp
// The finished lazy merger on two infinite ranges.  `reference.hpp` is the code of the lecture.
#include <iostream>
#include <ranges>
#include <vector>

#include "../../../../loop/rounds/01_video/hc02_merge_k_streams/cpp/reference.hpp"

int main() {
    using namespace mergek;
    auto evens = from_range(std::views::iota(0) | std::views::transform([](int x) { return 2 * x; }));
    auto threes = from_range(std::views::iota(0) | std::views::transform([](int x) { return 3 * x; }));

    std::vector<Source<int>> sources;
    sources.push_back(std::move(evens));
    sources.push_back(std::move(threes));
    Merger<int> merged(std::move(sources));  // nothing is pulled yet; Merger is an input range

    for (int x : merged | std::views::take(10)) std::cout << x << ' ';
    std::cout << "\n";
}
```

输出 `0 0 2 3 4 6 6 8 9 10`：两个无限序列 `0,2,4,…` 和 `0,3,6,…` 的前十个，没有预读任何多余的东西。

## 4. Part 3：多线程、非阻塞、有界

### 4.1 为什么不能"先到先出"

source A 已经有 5，source B 还没数据。B 稍后可能给出 1：现在输出 5 就错了。所以规则只有一条：

> **每一条还活着的流都有队首时，才能决定谁最小。**

只要有一条活流没有队首，结果就是 **`Pending`**——它的意思是"现在无法安全地决定"，不是"没有数据"。三种结果：

| 结果 | 含义 |
|---|---|
| `Ready{value, stream}` | 输出这个元素，来自第 `stream` 条流 |
| `Pending` | 有活流还没给出队首（`try_next()` 才会返回） |
| `Done` | 所有流都结束了 |

### 4.2 结构

```
source 0 ──▶ [producer 0 jthread] ──▶ bounded queue 0 ─┐
source 1 ──▶ [producer 1 jthread] ──▶ bounded queue 1 ─┼──▶ Combiner ──▶ try_next() / next()
source 2 ──▶ [producer 2 jthread] ──▶ bounded queue 2 ─┘
```

* **有界队列 = 背压（backpressure）**：消费者不取，队列满了生产者就阻塞在 `push` 上；内存有界，每个 source 最多被读出 `capacity + 1` 个元素（队列里 `capacity` 个，加生产者手里正拿着的 1 个）。
* **终止标记**：每个生产者结束时一定留下 `End` 或 `Failed`。合并器永远不会无限等一个已经死掉的生产者。
* **取消靠协作**：C++ 里不能杀线程。`std::stop_token` 传给 source 和每一次等待，`request_stop()` 之后阻塞的等待会醒来。

### 4.3 类型与有界队列

```cpp
template <class T>
struct Ready {
    T value;
    int stream;
};
struct Pending {};
struct Done {};
/// try_next() result.  Pending = some live stream has no head yet, so no element can be output safely.
template <class T>
using Poll = std::variant<Ready<T>, Pending, Done>;

/// A source failed (it threw, or its stream is not sorted).  cause() is the original exception.
class MergeException : public std::runtime_error {
public:
    MergeException(int stream, std::exception_ptr cause)
        : std::runtime_error("stream " + std::to_string(stream) + " failed: " + describe(cause)), stream_(stream),
          cause_(std::move(cause)) {}
    int stream() const noexcept { return stream_; }
    const std::exception_ptr& cause() const noexcept { return cause_; }

private:
    static std::string describe(const std::exception_ptr& p) {
        if (!p) return "unknown";
        try {
            std::rethrow_exception(p);
        } catch (const std::exception& e) {
            return e.what();
        } catch (...) {
            return "non-std exception";
        }
    }
    int stream_;
    std::exception_ptr cause_;
};

/// A source that may block.  It receives the stop token and must return std::nullopt promptly once stop is requested.
template <class T>
using BlockingSource = std::function<std::optional<T>(std::stop_token)>;

namespace detail {

template <class... Ts>
struct overloaded : Ts... {
    using Ts::operator()...;
};
```

* `MergeException` 保存失败流的编号和原始异常（`std::exception_ptr`），`what()` 里带上原因的文字。
* `BlockingSource` 比 `Source` 多一个 `std::stop_token`：约定是**收到停止请求后尽快返回 `std::nullopt`**。
* `overloaded` 是 `std::visit` 的惯用工具：把几个 lambda 合成一个函数对象。它和下面的队列、消息、生产者、线程组、合并核心都在 `namespace detail` 里（到 `ConcurrentMerge` 之前结束）：这是实现细节，不是接口。

```cpp
/// Bounded blocking queue.  Every blocking call also wakes up when the stop token fires (condition_variable_any).
template <class M>
class BoundedQueue {
public:
    explicit BoundedQueue(std::size_t capacity) : cap_(capacity) {}

    /// Blocks while full.  Returns false if cancelled before the message could be enqueued.
    bool push(M m, std::stop_token st) {
        std::unique_lock lk(mu_);
        if (!not_full_.wait(lk, st, [&] { return q_.size() < cap_; })) return false;
        q_.push_back(std::move(m));
        lk.unlock();
        not_empty_.notify_one();
        return true;
    }

    std::optional<M> try_pop() {
        std::unique_lock lk(mu_);
        if (q_.empty()) return std::nullopt;
        return take(lk);
    }

    /// Blocks while empty.  Returns std::nullopt if cancelled while waiting.
    std::optional<M> pop(std::stop_token st) {
        std::unique_lock lk(mu_);
        if (!not_empty_.wait(lk, st, [&] { return !q_.empty(); })) return std::nullopt;
        return take(lk);
    }

private:
    M take(std::unique_lock<std::mutex>& lk) {
        M m = std::move(q_.front());
        q_.pop_front();
        lk.unlock();
        not_full_.notify_one();
        return m;
    }

    std::mutex mu_;
    std::condition_variable_any not_full_, not_empty_;
    std::deque<M> q_;
    const std::size_t cap_;
};
```

`std::condition_variable_any::wait(lock, stop_token, pred)` 在 `pred()` 为真**或停止被请求**时返回，返回值是 `pred()` 的结果。普通 `std::condition_variable` 没有这个重载：一个阻塞在空队列上的线程，没人通知它就永远醒不过来。

```cpp
// condition_variable_any::wait(lock, stop_token, pred) wakes up when stop is requested; a plain wait would sleep forever.
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>

int main() {
    std::mutex mu;
    std::condition_variable_any cv;
    bool has_item = false;  // nobody ever sets it

    std::stop_source stop;
    std::jthread worker([&, token = stop.get_token()] {
        std::unique_lock lock(mu);
        const bool got = cv.wait(lock, token, [&] { return has_item; });
        std::cout << "worker woke up, predicate true? " << std::boolalpha << got << ", stop requested? " << token.stop_requested() << "\n";
    });

    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    stop.request_stop();  // the worker is released although the predicate is still false
    worker.join();
}
```

### 4.4 生产者与线程组

```cpp
template <class T>
struct Item {
    T value;
};
struct End {};
struct Failed {
    std::exception_ptr cause;
};
/// Every producer ends with End or Failed, so the consumer never waits for a producer that is already dead.
template <class T>
using Msg = std::variant<Item<T>, End, Failed>;
template <class T>
using Queue = BoundedQueue<Msg<T>>;

/// Pull from `src`, check the order, push into `q`.  Returns normally at the end of the source and when cancelled;
/// throws when the source throws or is unsorted (the caller decides what a failure means).
template <class T, class Less>
void produce(int idx, const BlockingSource<T>& src, Queue<T>& q, std::stop_token st, const Less& less) {
    std::optional<T> prev;
    std::size_t pos = 0;
    for (;;) {
        std::optional<T> v = src(st);
        if (!v) {
            if (!st.stop_requested()) q.push(End{}, st);
            return;
        }
        if (prev && less(*v, *prev)) throw UnsortedInputException(idx, pos);
        prev = *v;
        if (!q.push(Item<T>{std::move(*v)}, st)) return;
        ++pos;
    }
}
```

* 生产者正常结束和被取消都是**返回**；source 抛异常、或顺序不对，是**抛出**——怎么处理失败由调用者决定（Part 3 把它变成 `Failed` 消息，Part 4 把它记下来并取消其余）。
* **线程函数里的异常不能漏出去**：漏出去就是 `std::terminate`，整个进程退出。必须在线程里 `catch (...)`，用 `std::exception_ptr` 把异常带出来，在别的线程里 `rethrow_exception`：

```cpp
// An exception that leaves a thread body calls std::terminate.  Catch it in the thread, carry it out as an exception_ptr.
#include <exception>
#include <iostream>
#include <stdexcept>
#include <thread>

int main() {
    std::exception_ptr failure;
    std::thread t([&] {
        try {
            throw std::runtime_error("the source failed");
        } catch (...) {
            failure = std::current_exception();  // without this catch: std::terminate(), the whole process dies
        }
    });
    t.join();  // join() orders the write to `failure` before the read below
    try {
        if (failure) std::rethrow_exception(failure);
    } catch (const std::exception& e) {
        std::cout << "main rethrew: " << e.what() << "\n";
    }
}
```

```cpp
/// Owns the stop source and the threads.  Destruction = request stop, then join every thread (jthread's destructor):
/// no producer can outlive the scope that created the group.
struct ThreadGroup {
    std::stop_source stop;
    std::vector<std::jthread> threads;
    ThreadGroup() = default;
    ThreadGroup(const ThreadGroup&) = delete;
    ThreadGroup& operator=(const ThreadGroup&) = delete;
    ~ThreadGroup() { stop.request_stop(); }
};
```

`ThreadGroup` 是本题的 RAII 核心：析构时**先请求停止，再 join 每个线程**（`std::jthread` 的析构函数 join）。成员的声明顺序就是销毁顺序的逆序——`threads` 声明在 `stop` 之后，所以先 join、后销毁 `stop`；它又必须声明在它所引用的队列和 source **之后**，这样线程先结束，被引用的东西后销毁。

### 4.5 合并核心

```cpp
/// Consumer side only; not thread-safe.  The rule: an output is decided only when EVERY live stream has a head.
template <class T, class Less>
class Combiner {
public:
    Combiner(std::vector<Queue<T>*> queues, Less less)
        : queues_(std::move(queues)), heads_(queues_.size()), finished_(queues_.size(), 0), less_(std::move(less)) {}

    /// block = false: never waits (Pending if a head is missing).  block = true: waits for missing heads; returns
    /// std::nullopt if the stop token fired while waiting.
    std::optional<Poll<T>> poll(bool block, std::stop_token st) {
        bool pending = false;
        for (std::size_t i = 0; i < queues_.size(); ++i) {
            if (finished_[i] || heads_[i]) continue;
            std::optional<Msg<T>> m = block ? queues_[i]->pop(st) : queues_[i]->try_pop();
            if (!m) {
                if (block) return std::nullopt;
                pending = true;  // keep looking at the other streams: their failures must surface too
                continue;
            }
            std::visit(overloaded{[&](Item<T>& item) { heads_[i] = std::move(item.value); },
                                  [&](End&) { finished_[i] = 1; },
                                  [&](Failed& f) { throw MergeException(static_cast<int>(i), f.cause); }},
                       *m);
        }
        if (pending) return Poll<T>{Pending{}};
        int best = -1;
        for (std::size_t i = 0; i < heads_.size(); ++i)
            if (heads_[i] && (best < 0 || less_(*heads_[i], *heads_[best]))) best = static_cast<int>(i);  // strict <: ties keep the lower stream
        if (best < 0) return Poll<T>{Done{}};
        Ready<T> out{std::move(*heads_[best]), best};
        heads_[best].reset();
        return Poll<T>{std::move(out)};
    }

private:
    std::vector<Queue<T>*> queues_;
    std::vector<std::optional<T>> heads_;
    std::vector<char> finished_;  // not vector<bool>: that one is a bit-packed proxy container
    Less less_;
};

}  // namespace detail
```

* `poll(block=false)`：缺队首的流不等，记 `pending`，但继续看其余的流——这样别的流的失败也能被发现。
* `poll(block=true)`：在缺队首的流上 `pop(st)`；停止被请求就返回 `nullopt`。
* 选最小时用严格 `<`：相等时保留编号小的，稳定。
* `finished_` 用 `vector<char>` 而不是 `vector<bool>`（后者是位压缩的代理容器，不是真正的 `bool` 数组）。
* 这个类**只在消费者线程里使用**，不需要锁。

### 4.6 `ConcurrentMerge`

```cpp
/// One std::jthread producer per source, each feeding its own bounded queue (capacity >= 1); the consumer merges.
/// Output is independent of thread scheduling.  Destroying the object cancels and joins the producers.
/// A source that ignores its stop token makes close() (and the destructor) wait for it: a thread cannot be killed.
template <class T, class Less = std::less<T>>
class ConcurrentMerge {
public:
    ConcurrentMerge(std::vector<BlockingSource<T>> sources, int capacity, Less less = {})
        : sources_(std::move(sources)), combiner_(make_queues(sources_.size(), capacity), less) {
        for (std::size_t i = 0; i < sources_.size(); ++i) {
            group_.threads.emplace_back([this, i, less, st = group_.stop.get_token()] {
                try {
                    detail::produce<T>(static_cast<int>(i), sources_[i], *queues_[i], st, less);
                } catch (...) {
                    // A thread body must never throw (that is std::terminate): leave the exception as the last message.
                    queues_[i]->push(detail::Failed{std::current_exception()}, st);
                }
            });
        }
    }

    ConcurrentMerge(const ConcurrentMerge&) = delete;
    ConcurrentMerge& operator=(const ConcurrentMerge&) = delete;
    ~ConcurrentMerge() { close(); }

    /// Never blocks.  Throws MergeException (and closes) on a failed stream; std::logic_error once closed.
    Poll<T> try_next() {
        if (closed_.load()) throw std::logic_error("closed");
        try {
            auto p = combiner_.poll(false, {});
            return std::move(*p);  // a non-blocking poll always has a result
        } catch (const MergeException&) {
            close();
            throw;
        }
    }

    /// Blocks until Ready or Done (never Pending).  If close() runs on another thread meanwhile: std::logic_error.
    Poll<T> next() {
        if (closed_.load()) throw std::logic_error("closed");
        try {
            auto p = combiner_.poll(true, group_.stop.get_token());
            if (!p) throw std::logic_error("closed");
            return std::move(*p);
        } catch (const MergeException&) {
            close();
            throw;
        }
    }

    /// Idempotent: cancel every producer and wait for them to finish.
    void close() {
        if (closed_.exchange(true)) return;
        group_.stop.request_stop();
        group_.threads.clear();  // jthread destructors join
    }

private:
    std::vector<detail::Queue<T>*> make_queues(std::size_t n, int capacity) {
        if (capacity < 1) throw std::invalid_argument("capacity must be >= 1: " + std::to_string(capacity));
        for (std::size_t i = 0; i < n; ++i) queues_.push_back(std::make_unique<detail::Queue<T>>(static_cast<std::size_t>(capacity)));
        std::vector<detail::Queue<T>*> raw;
        for (auto& q : queues_) raw.push_back(q.get());
        return raw;
    }

    // Declaration order is destruction order in reverse: group_ (joins the threads) dies BEFORE the queues and sources they use.
    std::vector<BlockingSource<T>> sources_;
    std::vector<std::unique_ptr<detail::Queue<T>>> queues_;
    detail::Combiner<T, Less> combiner_;
    std::atomic<bool> closed_{false};
    detail::ThreadGroup group_;
};
```

* 构造函数里启动线程，**捕获 `this`**：此时 `sources_` 和 `queues_` 已经构造完，线程用得上。
* 成员顺序：`sources_`、`queues_`、`combiner_`、`closed_`、`group_`。`group_` 最后声明，所以析构时**最先**销毁——它的析构函数会请求停止并 join，线程都结束之后，队列和 source 才被销毁。
* `close()` 幂等：`closed_.exchange(true)`。析构函数也调用它，所以忘了 `close()` 不会泄漏线程。
* 失败（`MergeException`）时自动 `close()`，之后调用抛 `std::logic_error`。
* `next()` 把 `group_` 的 token 传给 `poll`：别的线程 `close()` 时，阻塞在 `next()` 里的线程会醒来并抛 `std::logic_error`。
* 限制：source 如果不理会 stop token，`close()` 就要等它——线程不能被杀死，也不能安全地 `detach`（它还引用着队列）。这是 C++ 版的"契约"，Java 版靠 `Thread.interrupt` 和超时 `join` 兜底。

## 5. Part 4：`merge_all`（RAII 作用域）

```cpp
/// Merge everything and return the result.  Producers run in a ThreadGroup that lives inside this function: the first
/// failure is recorded and cancels the others (their stop token fires, blocked sources wake up), and leaving the function
/// by return or by exception always joins every thread.  Throws MergeException with the failing stream's index.
template <class T, class Less = std::less<T>>
std::vector<T> merge_all(std::vector<BlockingSource<T>> sources, int capacity, Less less = {}) {
    if (capacity < 1) throw std::invalid_argument("capacity must be >= 1: " + std::to_string(capacity));
    std::vector<std::unique_ptr<detail::Queue<T>>> queues;
    std::vector<detail::Queue<T>*> raw;
    for (std::size_t i = 0; i < sources.size(); ++i) {
        queues.push_back(std::make_unique<detail::Queue<T>>(static_cast<std::size_t>(capacity)));
        raw.push_back(queues.back().get());
    }
    std::mutex failure_mu;
    std::optional<std::pair<int, std::exception_ptr>> failure;
    detail::ThreadGroup group;  // declared last: destroyed first, so the threads end before the things they reference
    for (std::size_t i = 0; i < sources.size(); ++i) {
        group.threads.emplace_back([&, i, st = group.stop.get_token()] {
            try {
                detail::produce<T>(static_cast<int>(i), sources[i], *queues[i], st, less);
            } catch (...) {
                {
                    std::lock_guard lk(failure_mu);
                    if (!failure) failure.emplace(static_cast<int>(i), std::current_exception());  // the first failure wins
                }
                group.stop.request_stop();
            }
        });
    }
    auto rethrow_failure = [&]() -> void {
        std::lock_guard lk(failure_mu);
        if (!failure) throw std::logic_error("cancelled without a failure");
        throw MergeException(failure->first, failure->second);
    };

    detail::Combiner<T, Less> combiner(raw, less);
    std::vector<T> out;
    for (;;) {
        if (group.stop.stop_requested()) rethrow_failure();
        auto p = combiner.poll(true, group.stop.get_token());
        if (!p) rethrow_failure();
        if (auto* r = std::get_if<Ready<T>>(&*p)) out.push_back(std::move(r->value));
        else if (std::holds_alternative<Done>(*p)) return out;
        else throw std::logic_error("a blocking poll never returns Pending");
    }
}
```

* 所有生产者放在函数里的 `ThreadGroup` 中。**无论正常返回还是抛异常，离开函数时线程一定已经结束**——这就是 C++ 里的"结构化并发"。
* 失败时：记录**第一个**失败（互斥锁保护的 `optional`），调用 `group.stop.request_stop()`；其余生产者阻塞在 source 里（通过 token 醒来）或阻塞在 `push` 上（队列的等待也带 token），都会退出。
* 消费者就是调用线程，不另开任务：每轮先看 `stop_requested()`，阻塞等待时 token 被触发就返回 `nullopt`，然后 `rethrow_failure()` 抛 `MergeException`（带失败流的编号）。
* 声明顺序：`queues`、`failure` 在 `group` 之前，`group` 最后声明、最先销毁。

## 6. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| 比较 | `compareTo`，`null` 要检查 | 只用 `<`（`Less` 模板参数），没有 null；`a - b` 是 UB |
| 堆 | `PriorityQueue<Head<T>>`，每个元素一个对象 | `priority_queue<int>` 存下标，元素留在原处；`top()` 是 `const&` |
| 惰性迭代器 | `Iterator`（`hasNext`/`next`） | 手写 pull 函数 + input range（`iterator` + `sentinel`），可接 `views::take` |
| 线程 | 虚拟线程 | `std::jthread`（OS 线程，数量要自己控制） |
| 取消 | `Thread.interrupt`，阻塞调用会抛 `InterruptedException` | `std::stop_token`：**协作式**，source 和每次等待都要认它 |
| 队列 | `ArrayBlockingQueue` | 自己写：`mutex` + `condition_variable_any` + `deque` |
| 结构化并发 | `StructuredTaskScope`，失败自动取消兄弟任务 | 没有现成的：`ThreadGroup`（析构 = 请求停止 + join）+ 记录第一个失败 |
| 线程里的异常 | 被线程的未捕获处理器接住 | 漏出线程体 = `std::terminate`，必须 `catch (...)` 带出来 |
| 内存 | GC | 谁拥有谁、谁先销毁：成员声明顺序决定一切 |

## 7. 陷阱

1. 相等元素的顺序依赖堆内部实现：比较器里没有序列编号。
2. `a - b` 比较：`LLONG_MIN` / `LLONG_MAX` 上有符号溢出（UB）。
3. `std::priority_queue` 的比较器方向写反：它是大顶堆。
4. `const Head& h = heap.top(); heap.pop(); use(h)`：悬空引用。
5. `Merger` 被拷贝或移动：比较器里的 `this` 指向旧对象。
6. 倒着数的无符号循环：`i >= 0` 永远为真。
7. 线程函数里没 `catch (...)`：一个坏 source 让整个进程 `terminate`。
8. 普通 `condition_variable` 等待、没有 stop token：`close()` 永远 join 不了阻塞的线程。
9. 成员声明顺序：线程组声明得太早，线程还在用的队列已经被销毁。
10. `vector<bool>` 当标志数组用。
11. 构造时就预读所有 source；输出元素后立刻补位。

## 8. 面试官会追问什么（senior）

**Q1. 为什么是堆而不是两两合并 / 排序？** 复杂度 O(N log k) vs O(N k) vs O(N log N)；k 很小时（比如 2）直接线性扫描更快，而且更简单。

**Q2. 堆里放元素还是放下标？** 放下标：元素大时避免拷贝，缓存友好，而且稳定性只需要把下标放进比较器。代价是比较时多一次间接寻址。

**Q3. 线程安全的队列怎么写？** `mutex` + 两个条件变量（not_full / not_empty）+ `deque`；条件变量一定要配谓词（虚假唤醒）；通知可以在释放锁之后。要无锁就是单生产者单消费者的环形缓冲区（`atomic` 的读写下标）。

**Q4. 为什么用 `condition_variable_any` 而不是 `condition_variable`？** 只有它的 `wait` 有 `stop_token` 重载。`std::condition_variable` 要配 `stop_callback`，手动加锁再通知，容易写错。

**Q5. 取消怎么做？** 协作式：停止请求 + 每个阻塞点都能被唤醒。不能强杀线程。`jthread` 的析构函数自动 `request_stop` + `join`。

**Q6. 一个 source 永远不返回会怎样？** `close()` / 析构会一直等它。要有界就必须让 source 自己支持超时或取消；真实系统里还会在 source 外面套一层超时，超时算作 `Failed`。

**Q7. 每个 source 一个线程，source 有一万个怎么办？** OS 线程太贵：改成线程池 + 非阻塞 I/O（`epoll`/`kqueue`），或者限制"同时在读的 source 数 m"（有界并发）；本题的 `capacity` 是每条流的预读深度，不是并发数。

**Q8. 怎么测试并发代码？** 多次重复 + 随机让出（`yield`）打乱交错 + 与顺序实现对拍；用 ThreadSanitizer（`-fsanitize=thread`）找数据竞争；用看门狗线程把死锁变成失败。

**Q9. `try_next()` 能不能"忙等"？** 能，但会烧 CPU；合并器里更好的做法是 `next()` 在缺队首的流上阻塞。需要和别的事件一起等时，给每条队列加回调或用 `eventfd`/管道通知。

**Q10. `Merger` 能不能支持只可移动的元素？** 现在不能：`prev_` 要保留上一个元素做顺序检查，所以要拷贝。想支持，就让比较器只看一个可拷贝的「键」（`prev_` 里只存键），或者把顺序检查交给 source 自己。

## 9. 自测

1. 为什么 `priority_queue` 的比较器里要写 `a.stream > b.stream`，而不是 `<`？
2. `const Head& h = heap.top(); heap.pop();` 之后读 `h.pos` 会怎样？
3. `Merger` 的拷贝构造函数为什么要删掉？
4. 消费 n 个元素后 source 被取元素的总次数为什么是 ≤ k + n − 1？
5. 线程函数里抛出的异常没有被 `catch`，会发生什么？
6. `ConcurrentMerge` 里 `group_` 为什么要最后声明？
7. `try_next()` 返回 `Pending` 的时候，队列里可能已经有数据吗？

<details><summary>答案</summary>

1. `priority_queue` 弹出的是比较器意义下"最大"的元素。比较器说"a 排在 b 后面"，最先出来的才是最靠前的：值小的先出，值相等时编号小的先出，所以编号大的才是"后面"的那个。
2. 悬空引用，读到已经销毁的元素（UB）。先把 16 字节的 `Head` 按值拷出来再 `pop()`。
3. 堆的比较器里存着 `this`；拷贝后的堆比较的是旧对象的 `head_`，旧对象一销毁就悬空。
4. 初始每个 source 取一个队首（k 次）；输出第 j 个元素之后，补位推迟到下一次调用，所以输出 n 个时最多只补位 n − 1 次（最后一个输出的补位还没发生）。
5. `std::terminate()`，整个进程退出。必须在线程体里 `catch (...)`，用 `std::exception_ptr` 把异常交给别的线程。
6. 成员按声明逆序销毁：`group_` 最后声明就最先销毁，它的析构函数请求停止并 join 所有线程，这之后线程用过的 `queues_`、`sources_` 才被销毁。
7. 可能。`Pending` 的含义是"还有一条活流没有队首"；别的流的队列里可能已经有很多元素，但在那条流给出队首之前不能安全输出。

</details>
