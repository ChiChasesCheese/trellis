# hc04 · Queue Mean + 修正快照（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

实现一个先进先出（FIFO）队列，元素是 `long long`，要有 `push`、`pop`、`get_mean`（当前所有元素的平均数）。然后面试官一路追问：

| Part | 内容 |
|---|---|
| 1 | `push` / `pop` / `get_mean` 都是 O(1)；均值要**精确**；元素可以是 `LLONG_MAX`；空队列要有明确行为 |
| 2 | 事件流：`push N`、`pop`、`mean`、`snapshot [N ...]`。`snapshot` 是**修正快照**：丢掉此前的整段逻辑历史，队列内容变成快照给出的列表 |
| 3 | 保留每个历史版本，随时查任意版本的均值，还能从旧版本分叉（持久化队列） |
| 4 | 一个写线程不断 `push/pop`，监控线程随时读均值：读者不加锁、不阻塞写者、永远读到一致的值 |

```
push 1 / push 2 / mean       → 3/2
pop / mean                   → 2
snapshot 10 20 30 / mean     → 20
pop / mean                   → 25
pop / pop / mean             → empty
```

手算：`[1,2,3]` 均值 2；`push 4` 得 `[1,2,3,4]`，均值 2.5；`pop` 弹出 1，剩 `[2,3,4]`，均值 3。

## 2. Part 1：队列 + 均值

### 2.1 为什么"和"必须是整数，而且要 128 位

* **每次 `get_mean` 重新求和** 是 O(n)——面试官要的是 O(1)：维护一个 running sum，`push` 加、`pop` 减。
* **running sum 不能是 `double`**：

```cpp
// Why the running sum is an integer: a double running sum forgets small values next to a big one.
#include <iomanip>
#include <iostream>

int main() {
    double running = 0;
    running += 1e16;
    running += 1;      // 1e16 + 1 is not representable (spacing is 2): rounds back to 1e16
    running += 1;
    running -= 1e16;   // "the big element left the queue"
    std::cout << "double running sum after pop: " << running << "   (exact answer: 2)\n";

    long long exact = 0;
    exact += 10'000'000'000'000'000LL;
    exact += 1;
    exact += 1;
    exact -= 10'000'000'000'000'000LL;
    std::cout << "integer running sum after pop: " << exact << "\n";

    // Converting the final fraction: (2^53 + 1) / 1 is a tie between two doubles; one rounding, half to even.
    long long v = (1LL << 53) + 1;
    std::cout << std::setprecision(17) << "(2^53+1) as double = " << static_cast<double>(v) << "\n";
}
```

  `1e16 + 1` 在 `double` 里表示不了（相邻两个 `double` 相差 2），被舍掉；弹出 `1e16` 之后，和是 0 而不是 2。整数加减没有这个问题。
* **`long long` 会溢出**：两个 `LLONG_MAX` 相加就超了，有符号溢出还是 UB。用 `__int128`（clang/gcc 的 128 位整数）：每个元素的绝对值 ≤ 2^63，只要元素个数 < 2^64，和的绝对值就 < 2^127，永远装得下。
* 均值是**分数**：`和 / 个数`，约分后分母恒正、符号放分子，这样 `==` 可以直接比较。

### 2.2 环形缓冲区（ring buffer）

队列用一个定长数组加两个下标：`head` 指向队头，元素 `i` 在 `(head + i) & mask`。`push` 写在队尾，`pop` 读队头并让 `head` 前进，下标到头就绕回去。容量取 2 的幂，用 `& (capacity - 1)` 代替 `%`。满了就把容量翻倍——**按逻辑顺序**（从 `head` 开始，绕到 0）复制到新数组，新的 `head` 是 0。

```
容量 8，head=5，size=5：   下标: 0 1 2 3 4 5 6 7
                          内容: d e . . . a b c      逻辑顺序 a b c d e
扩容到 16 后：              内容: a b c d e . . . ...    head=0
```

和 `std::deque` 比：环形缓冲区是一块连续内存、一次分配，缓存友好；`deque` 是分块的，每个块单独分配，但扩容不用整体复制。两者都是合理的答案，要说得出取舍。

### 2.3 代码

```cpp
#include <algorithm>
#include <atomic>
#include <charconv>
#include <climits>
#include <limits>
#include <cmath>
#include <cstdint>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <thread>
#include <utility>
#include <variant>
#include <vector>

namespace qmean {

using i128 = __int128;
using u128 = unsigned __int128;

inline std::string i128_to_string(i128 v) {
    const bool neg = v < 0;
    u128 m = neg ? u128{0} - static_cast<u128>(v) : static_cast<u128>(v);  // |v| in unsigned space: also right for INT128_MIN
    std::string s;
    do { s.push_back(static_cast<char>('0' + static_cast<int>(m % 10))); m /= 10; } while (m != 0);
    if (neg) s.push_back('-');
    return {s.rbegin(), s.rend()};
}

namespace detail {
inline u128 gcd(u128 a, u128 b) {
    while (b != 0) { a %= b; std::swap(a, b); }
    return a;
}
inline int bit_length(u128 x) {
    const auto hi = static_cast<std::uint64_t>(x >> 64), lo = static_cast<std::uint64_t>(x);
    if (hi != 0) return 128 - __builtin_clzll(hi);
    return lo != 0 ? 64 - __builtin_clzll(lo) : 0;
}
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
}  // namespace detail
```

`Mean`：约分的分数，加一个"最近的 double"转换。

```cpp
/// Exact mean: a reduced fraction, denominator always positive, sign on the numerator.
struct Mean {
    i128 numerator;
    long long denominator;

    Mean(i128 n, long long d) : numerator(n), denominator(d) {
        if (d <= 0) throw std::invalid_argument("denominator must be positive: " + std::to_string(d));
        const u128 mag = n < 0 ? u128{0} - static_cast<u128>(n) : static_cast<u128>(n);
        const u128 g = detail::gcd(mag, static_cast<u128>(d));  // gcd(0, d) = d, so zero becomes 0/1
        numerator = n / static_cast<i128>(g);
        denominator = d / static_cast<long long>(g);
    }

    /// The double nearest to numerator/denominator (ties to even), with no intermediate rounding: long division builds a
    /// 54-bit quotient plus a sticky bit, then one rounding step.  (Apple arm64 has no wider long double to cheat with.)
    double to_double() const {
        if (numerator == 0) return 0.0;
        const bool neg = numerator < 0;
        const u128 n = neg ? u128{0} - static_cast<u128>(numerator) : static_cast<u128>(numerator);
        const u128 d = static_cast<u128>(denominator);
        u128 q = n / d, r = n % d;
        u128 mant;
        int exp2;
        bool sticky;
        if (const int k = detail::bit_length(q); k >= 54) {
            const int shift = k - 54;
            sticky = r != 0 || (shift > 0 && (q & ((u128{1} << shift) - 1)) != 0);
            mant = q >> shift;
            exp2 = shift;
        } else {
            mant = q;
            exp2 = 0;
            while (detail::bit_length(mant) < 54) {  // next binary digit of the fraction; r < d < 2^63 so r*2 cannot overflow
                r <<= 1;
                mant <<= 1;
                if (r >= d) { r -= d; mant |= 1; }
                --exp2;
            }
            sticky = r != 0;
        }
        // mant now has exactly 54 bits: 53 kept + 1 guard bit; sticky says whether anything non-zero lies beyond.
        const bool guard = (mant & 1) != 0;
        mant >>= 1;
        ++exp2;
        if (guard && (sticky || (mant & 1) != 0)) ++mant;
        const double v = std::ldexp(static_cast<double>(static_cast<std::uint64_t>(mant)), exp2);
        return neg ? -v : v;
    }
    friend bool operator==(const Mean&, const Mean&) = default;
};
```

* `gcd(0, d) = d`，所以 `0/5` 约成 `0/1`；`mag` 是绝对值，先转无符号再取负，对任何有符号值都不会溢出。
* **`to_double` 要点**：`(double)n / d` 在 `n` 超过 2^53 时会**舍入两次**（先把 `n` 变成 `double`，再除）。这里用长除法直接得到 54 位商 + 一个"粘滞位"（后面是否还有非零），最后只舍入一次，规则是"最近，平局取偶"。例：`(2^53 + 1) / 1` 恰好在两个 `double` 正中间，取偶数 → `2^53`；`(2^53 + 3) / 1` → `2^53 + 4`。

`QueueMean` 本体：

```cpp
/// FIFO of long long with O(1) push / pop / exact mean.  Ring buffer (power-of-two capacity, mask instead of %), __int128 sum.
class QueueMean {
public:
    QueueMean() = default;
    QueueMean(const QueueMean&) = default;
    QueueMean& operator=(const QueueMean&) = default;
    // The implicitly generated move would move the vector but COPY head_/size_/sum_: the moved-from object would claim
    // size_ elements in an empty buffer.  Moved-from must be a valid empty queue.
    QueueMean(QueueMean&& o) noexcept
        : buf_(std::move(o.buf_)), head_(std::exchange(o.head_, 0)), size_(std::exchange(o.size_, 0)), sum_(std::exchange(o.sum_, 0)) {
        o.buf_.clear();
    }
    QueueMean& operator=(QueueMean&& o) noexcept {
        if (this != &o) {
            buf_ = std::move(o.buf_);
            head_ = std::exchange(o.head_, 0);
            size_ = std::exchange(o.size_, 0);
            sum_ = std::exchange(o.sum_, 0);
            o.buf_.clear();
        }
        return *this;
    }

    void push(long long x) {
        if (size_ == buf_.size()) grow();  // may throw bad_alloc: nothing has been modified yet (strong guarantee)
        buf_[(head_ + size_) & (buf_.size() - 1)] = x;
        ++size_;
        sum_ += x;
    }

    long long pop() {
        if (size_ == 0) throw std::out_of_range("pop on empty queue");
        const long long x = buf_[head_];
        head_ = (head_ + 1) & (buf_.size() - 1);
        --size_;
        sum_ -= x;
        return x;
    }

    std::size_t size() const { return size_; }
    bool empty() const { return size_ == 0; }
    i128 sum() const { return sum_; }

    Mean mean() const {
        if (size_ == 0) throw std::out_of_range("mean of empty queue");
        return Mean(sum_, static_cast<long long>(size_));
    }

    double get_mean() const {
        if (size_ == 0) throw std::out_of_range("mean of empty queue");
        if (sum_ >= -(i128{1} << 53) && sum_ <= (i128{1} << 53))  // both operands exact in a double: one IEEE division is correctly rounded
            return static_cast<double>(static_cast<long long>(sum_)) / static_cast<double>(size_);
        return mean().to_double();
    }

private:
    void grow() {
        if (buf_.size() > (std::numeric_limits<std::size_t>::max() >> 2)) throw std::length_error("queue too large");
        std::vector<long long> bigger(buf_.empty() ? 16 : buf_.size() * 2);
        // copy in LOGICAL order: [head_, end) then [0, head_)  (a plain copy of the buffer would scramble a wrapped queue)
        const auto first = std::min(size_, buf_.size() - head_);
        std::copy_n(buf_.begin() + static_cast<std::ptrdiff_t>(head_), first, bigger.begin());
        std::copy_n(buf_.begin(), size_ - first, bigger.begin() + static_cast<std::ptrdiff_t>(first));
        buf_ = std::move(bigger);
        head_ = 0;
    }

    std::vector<long long> buf_;  // size() is 0 or a power of two
    std::size_t head_ = 0;
    std::size_t size_ = 0;
    i128 sum_ = 0;
};
```

要点：

1. **移动构造函数必须自己写**：

```cpp
// The implicitly generated move constructor moves each member.  For `int` "move" is just copy,
// so the moved-from object keeps its counters but loses its buffer.
#include <iostream>
#include <utility>
#include <vector>

struct Broken {
    std::vector<long long> buf;
    std::size_t size = 0;
    Broken() = default;
    Broken(Broken&&) = default;            // moves buf, copies size
};

struct Fixed {
    std::vector<long long> buf;
    std::size_t size = 0;
    Fixed() = default;
    Fixed(Fixed&& o) noexcept : buf(std::move(o.buf)), size(std::exchange(o.size, 0)) { o.buf.clear(); }
};

int main() {
    Broken a;
    a.buf = {1, 2, 3};
    a.size = 3;
    Broken b = std::move(a);
    std::cout << "Broken: moved-from claims size " << a.size << " but holds " << a.buf.size() << " elements\n";

    Fixed c;
    c.buf = {1, 2, 3};
    c.size = 3;
    Fixed d = std::move(c);
    std::cout << "Fixed:  moved-from claims size " << c.size << " and holds " << c.buf.size() << " elements\n";
}
```

   编译器生成的移动构造函数对每个成员各"移动"一次：`vector` 被掏空，`size_t` / `__int128` 只是拷贝。被移动的对象谎称有 `size_` 个元素，下一次 `push` 就会写进空缓冲区。规则：**被移动后的对象必须是一个合法的、可用的（这里是空的）对象**。
2. `push` 先 `grow()` 再改状态：`grow` 可能抛 `bad_alloc`，此时什么都没改（强异常保证，strong exception guarantee）。
3. 空队列 `pop` / `mean` 抛 `std::out_of_range`。对比：`std::queue::pop()` 在空队列上是 UB。接口上要明确选择：抛异常、返回 `std::optional`、还是文档里写"前置条件"。
4. `get_mean` 的快路径：和在 ±2^53 内时，和与个数都能精确表示成 `double`，一次 IEEE 除法就是正确舍入；否则走 `to_double`。
5. `mean()` 的约分要做一次 gcd，是 O(log d) 而不是严格 O(1)；`get_mean` 的快路径才是真 O(1)。能主动说出这点就是 senior。

## 3. Part 2：事件流

`Event` 是四种事件的 `std::variant`，`Answer` 是 `Value(mean)` 或 `Empty`：

```cpp
struct Push { long long value; friend bool operator==(const Push&, const Push&) = default; };
struct Pop { friend bool operator==(const Pop&, const Pop&) = default; };
struct Query { friend bool operator==(const Query&, const Query&) = default; };
/// Corrective snapshot: forget the logical history so far; the queue becomes `contents` (front first).
/// The vector is owned by value: no defensive copy needed, and "null elements" cannot exist.
struct Correct { std::vector<long long> contents; friend bool operator==(const Correct&, const Correct&) = default; };
using Event = std::variant<Push, Pop, Query, Correct>;

struct Value { Mean mean; friend bool operator==(const Value&, const Value&) = default; };
struct Empty { friend bool operator==(const Empty&, const Empty&) = default; };
using Answer = std::variant<Value, Empty>;

/// Apply the events in order; every Query yields one Answer.  Pop on an empty queue throws std::out_of_range.
inline std::vector<Answer> run(const std::vector<Event>& events) {
    QueueMean q;
    std::vector<Answer> out;
    for (const Event& e : events) {
        std::visit(detail::overloaded{
            [&](const Push& p) { q.push(p.value); },
            [&](const Pop&) { q.pop(); },
            [&](const Query&) { out.push_back(q.empty() ? Answer{Empty{}} : Answer{Value{q.mean()}}); },
            [&](const Correct& c) {
                q = QueueMean{};
                for (long long v : c.contents) q.push(v);
            }}, e);
    }
    return out;
}
```

* `Correct` 里的 `std::vector` 是**值成员**：构造时拷贝，调用者之后改原 vector 不会影响事件——Java 里需要 `List.copyOf` 防御性拷贝，C++ 的值语义直接给了。
* `std::visit(overloaded{...}, e)`：每种事件一个 lambda，漏一个编译不过。
* `q = QueueMean{}` 用到了上面的移动赋值。

解析要严格，错误信息带行号：

```cpp
namespace detail {
inline long long parse_ll(std::string_view tok) {
    long long v = 0;
    auto [ptr, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), v);
    if (ec != std::errc{} || ptr != tok.data() + tok.size()) throw std::invalid_argument("bad integer '" + std::string(tok) + "'");
    return v;
}
inline std::vector<std::string_view> split_ws(std::string_view s) {
    std::vector<std::string_view> out;
    for (std::size_t i = 0; i < s.size();) {
        while (i < s.size() && is_space(s[i])) ++i;
        std::size_t j = i;
        while (j < s.size() && !is_space(s[j])) ++j;
        if (j > i) out.push_back(s.substr(i, j - i));
        i = j;
    }
    return out;
}
inline Event parse_line(const std::vector<std::string_view>& t) {
    if (t[0] == "push") {
        if (t.size() != 2) throw std::invalid_argument("push takes exactly one integer");
        return Push{parse_ll(t[1])};
    }
    if (t[0] == "pop") {
        if (t.size() != 1) throw std::invalid_argument("pop takes no argument");
        return Pop{};
    }
    if (t[0] == "mean") {
        if (t.size() != 1) throw std::invalid_argument("mean takes no argument");
        return Query{};
    }
    if (t[0] == "snapshot") {
        Correct c;
        for (std::size_t i = 1; i < t.size(); ++i) c.contents.push_back(parse_ll(t[i]));
        return c;
    }
    throw std::invalid_argument("unknown command '" + std::string(t[0]) + "'");
}
}  // namespace detail

/// push N | pop | mean | snapshot [N ...]; blank lines ignored; errors are std::invalid_argument("line k: ...").
inline std::vector<Event> parse(const std::vector<std::string>& lines) {
    std::vector<Event> events;
    for (std::size_t i = 0; i < lines.size(); ++i) {
        const auto tokens = detail::split_ws(lines[i]);
        if (tokens.empty()) continue;
        try {
            events.push_back(detail::parse_line(tokens));
        } catch (const std::invalid_argument& e) {
            throw std::invalid_argument("line " + std::to_string(i + 1) + ": " + e.what());
        }
    }
    return events;
}

inline std::string render(const Answer& a) {
    return std::visit(detail::overloaded{
        [](const Value& v) {
            return v.mean.denominator == 1 ? i128_to_string(v.mean.numerator)
                                           : i128_to_string(v.mean.numerator) + "/" + std::to_string(v.mean.denominator);
        },
        [](const Empty&) { return std::string("empty"); }}, a);
}

inline std::vector<std::string> solve(const std::vector<std::string>& lines) {
    std::vector<std::string> out;
    for (const Answer& a : run(parse(lines))) out.push_back(render(a));
    return out;
}
```

* `from_chars` + 检查整个 token 被消耗：`push 1x`、`push +5`、`push 0x10`、`push 9223372036854775808`（越界）都拒绝。
* 行号从 1 开始，**空行也计数**；错误统一包成 `std::invalid_argument("line k: …")`。
* 自己写 `is_space` 而不用 `std::isspace(char)`（负的 `char` 是 UB）。

## 4. Part 3：持久化（persistent）队列

要求：`push(version, x)` 返回**新**版本号，旧版本永远不变；`pop`、`mean` 都是 O(log n)；不能每个版本复制一份内容（20 万个版本就是 O(n²)）。

**想法**：所有 `push` 过的值构成一棵树（子节点 = 在父版本后 push 的值）。一个版本 = `(尾节点, 已弹出个数, 和)`。队列内容就是"根到尾节点"这条路径上、深度在 `(head_depth, depth(tail)]` 的那一段。

* `push`：在尾节点下新建一个子节点，O(1)。
* `pop`：队头是这条路径上深度 `head_depth + 1` 的祖先——要一个 **level ancestor** 查询。逐个往上爬是 O(n)，太慢。
* **skew-binary jump pointer**：每个节点多存一个 `jump` 指针。规则：设 `p` 是父节点，`j = jump[p]`；如果 `depth[p] - depth[j] == depth[j] - depth[jump[j]]`，新节点的 `jump = jump[j]`，否则 `jump = p`。一条链上各深度的 `jump` 指向（深度 → 它跳到的深度）：

| 深度 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | ... |
|---|---|---|---|---|---|---|---|---|---|
| 跳到深度 | 0 | 1 | 0 | 3 | 4 | 3 | 0 | 7 | ... |

  查深度 `d` 的祖先：从 `v` 出发，若 `jump[v]` 的深度 ≥ `d` 就跳过去，否则走父节点——O(log n) 步，每个节点只多一个 `int`（对比二进制倍增需要 `n log n` 的表）。例：从深度 6 找深度 2：`jump(6)=3 ≥ 2` → 到 3；`jump(3)=0 < 2` → 走父节点到 2。

```cpp
/// Persistent queue.  All pushed values form a tree (child = value pushed after its parent); a version is
/// (tail node, number popped, sum).  Contents = the path root->tail between depth head_depth+1 and depth(tail).
/// pop needs the ancestor of tail at a given depth: skew-binary jump pointers give it in O(log n) with one extra int per node.
class VersionedQueue {
public:
    static constexpr int EMPTY = 0;

    VersionedQueue() : nodes_(1, Node{0, 0, 0, 0}), versions_(1, Version{0, 0, 0}) {}

    int push(int version, long long x) {
        const Version v = at(version);  // copy: new_version() below may reallocate versions_ and invalidate references
        const int node = new_node(v.tail, x);
        return new_version(node, v.head_depth, v.sum + x);
    }

    int pop(int version) {
        const Version v = at(version);
        if (nodes_[static_cast<std::size_t>(v.tail)].depth - v.head_depth == 0) throw std::out_of_range("pop on empty version " + std::to_string(version));
        const int h = v.head_depth + 1;
        const long long front = nodes_[static_cast<std::size_t>(level_ancestor(v.tail, h))].val;
        return new_version(v.tail, h, v.sum - front);
    }

    int correct(const std::vector<long long>& contents) {
        int node = 0;
        i128 sum = 0;
        for (long long x : contents) {
            node = new_node(node, x);
            sum += x;
        }
        return new_version(node, 0, sum);
    }

    std::size_t size(int version) const {
        const Version& v = at(version);
        return static_cast<std::size_t>(nodes_[static_cast<std::size_t>(v.tail)].depth - v.head_depth);
    }

    Mean mean(int version) const {
        const std::size_t n = size(version);
        if (n == 0) throw std::out_of_range("mean of empty version " + std::to_string(version));
        return Mean(at(version).sum, static_cast<long long>(n));
    }

    std::vector<long long> contents(int version) const {
        std::vector<long long> out(size(version));
        int node = at(version).tail;
        for (std::size_t i = out.size(); i-- > 0;) {
            out[i] = nodes_[static_cast<std::size_t>(node)].val;
            node = nodes_[static_cast<std::size_t>(node)].parent;
        }
        return out;
    }

private:
    struct Node { long long val; int parent; int jump; int depth; };
    struct Version { int tail; int head_depth; i128 sum; };

    const Version& at(int version) const {
        if (version < 0 || static_cast<std::size_t>(version) >= versions_.size()) throw std::invalid_argument("unknown version " + std::to_string(version));
        return versions_[static_cast<std::size_t>(version)];
    }

    int new_node(int p, long long x) {
        if (nodes_.size() >= static_cast<std::size_t>(INT_MAX)) throw std::length_error("too many nodes");
        const Node parent = nodes_[static_cast<std::size_t>(p)];  // by value, same reason as above
        const Node& j = nodes_[static_cast<std::size_t>(parent.jump)];
        const int jump = (parent.depth - j.depth == j.depth - nodes_[static_cast<std::size_t>(j.jump)].depth) ? j.jump : p;
        nodes_.push_back(Node{x, p, jump, parent.depth + 1});
        return static_cast<int>(nodes_.size() - 1);
    }

    int new_version(int tail, int head_depth, i128 sum) {
        if (versions_.size() >= static_cast<std::size_t>(INT_MAX)) throw std::length_error("too many versions");
        versions_.push_back(Version{tail, head_depth, sum});
        return static_cast<int>(versions_.size() - 1);
    }

    int level_ancestor(int v, int d) const {
        while (nodes_[static_cast<std::size_t>(v)].depth > d) {
            const Node& n = nodes_[static_cast<std::size_t>(v)];
            v = nodes_[static_cast<std::size_t>(n.jump)].depth >= d ? n.jump : n.parent;
        }
        return v;
    }

    std::vector<Node> nodes_;        // [0] is the root sentinel
    std::vector<Version> versions_;  // [0] is the empty queue
};
```

C++ 的关键陷阱：**`push_back` 会让 vector 里所有的指针、引用、迭代器失效。**

```cpp
// push_back may reallocate: every pointer, reference and iterator into the vector dies.  Index, or copy first.
#include <iostream>
#include <vector>

struct Node { long long val; int parent; int depth; };

int add_child_buggy(std::vector<Node>& nodes, int p, long long x) {
    const Node& parent = nodes[p];                       // reference into the vector
    nodes.push_back(Node{x, p, 0});                      // may reallocate: `parent` now dangles
    nodes.back().depth = parent.depth + 1;               // use after free (ASan: heap-use-after-free)
    return static_cast<int>(nodes.size() - 1);
}

int add_child(std::vector<Node>& nodes, int p, long long x) {
    const Node parent = nodes[p];                        // copy the 16 bytes you need BEFORE growing
    nodes.push_back(Node{x, p, parent.depth + 1});
    return static_cast<int>(nodes.size() - 1);
}

int main() {
    std::vector<Node> nodes{Node{0, 0, 0}};
    int last = 0;
    for (int i = 1; i <= 100000; ++i) last = add_child(nodes, last, i);
    std::cout << "depth of last node: " << nodes[last].depth << "\n";
    if (false) add_child_buggy(nodes, last, 0);   // call it with a full vector and ASan reports heap-use-after-free
}
```

所以 `push` / `pop` 里先把需要的 `Version`、`Node` **按值拷出来**（`const Version v = at(version);`），再调用会 `push_back` 的函数。下标（`int`）是稳定的"句柄"，引用不是。

## 5. Part 4：单写者、多读者的无锁读

读者看到的必须是**某一个时刻**的 `(seq, size, sum)`，不能是"新的和 + 旧的个数"。

### 5.1 撕裂读是真的

```cpp
// Two 64-bit halves written separately are NOT one 128-bit value for a concurrent reader.
// (Relaxed atomics keep this program free of data races; the tearing is a logic bug, not UB.)
#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<unsigned long long> hi{0}, lo{0};
    std::atomic<bool> stop{false};
    std::thread writer([&] {
        for (unsigned long long i = 1; i <= 2'000'000; ++i) {
            hi.store(i, std::memory_order_relaxed);   // the pair (hi, lo) should always be (i, i)
            lo.store(i, std::memory_order_relaxed);
        }
        stop.store(true);
    });
    long long torn = 0, reads = 0;
    while (!stop.load()) {
        auto h = hi.load(std::memory_order_relaxed);
        auto l = lo.load(std::memory_order_relaxed);
        ++reads;
        if (h != l) ++torn;                           // saw hi from one update and lo from another
    }
    writer.join();
    std::cout << "torn reads observed: " << (torn > 0 ? "yes" : "none this run") << " (out of " << (reads > 0 ? "many" : "0") << ")\n";
}
```

写者依次写两个 64 位半边，读者可能读到"一半新一半旧"。128 位的和本来就要两个 64 位字，`std::atomic<__int128>` 在许多平台上不是无锁的（内部可能用锁）。

### 5.2 方案对比

| 方案 | 读者 | 写者 | 备注 |
|---|---|---|---|
| `std::mutex` | 加锁，会阻塞写者 | 加锁 | 最简单，面试里先说它再说为什么不够 |
| 原子发布不可变快照（`std::atomic<std::shared_ptr<Stat>>`） | 一次原子加载 | 每次修改分配一个新对象 | 回收靠引用计数；C++20 的 `atomic<shared_ptr>` 并非所有标准库都实现了 |
| 双缓冲 + 版本号 | 无锁 | 无锁 | 读者可能被旧缓冲区的复用坑到，要加版本号 |
| **seqlock（这里用它）** | 无锁，必要时重试 | 无分配、无等待 | 只适合**单写者**；读者重试，所以是 obstruction-free 而不是 wait-free |

### 5.3 seqlock

写者：把版本号 `version_` 变成**奇数**（"正在写"）→ 改字段 → 变成**偶数**。读者：读到偶数版本号 `v1` → 读字段 → 再读版本号，若仍等于 `v1` 才接受，否则重试。

```cpp
struct SingleWriterViolation : std::logic_error {
    using std::logic_error::logic_error;
};

/// Consistent snapshot of the queue state at one instant.
struct Stat {
    std::uint64_t seq;  // number of modifications so far
    std::size_t size;
    i128 sum;
    std::optional<Mean> mean() const {
        if (size == 0) return std::nullopt;
        return Mean(sum, static_cast<long long>(size));
    }
    friend bool operator==(const Stat&, const Stat&) = default;
};

/// One writer thread, any number of lock-free readers, no allocation per update: a seqlock.
/// The writer makes `version_` odd, rewrites the fields, makes it even again.  A reader copies the fields and accepts
/// the copy only if `version_` was even and unchanged around it.  The fields are relaxed atomics (not plain variables):
/// a reader may read them while the writer writes, and for plain variables that is a data race = undefined behaviour.
class SharedMean {
public:
    void push(long long x) {
        claim_writer();
        queue_.push(x);
        publish();
    }

    long long pop() {
        claim_writer();
        const long long x = queue_.pop();  // throws before publish(): readers never see a half-applied operation
        publish();
        return x;
    }

    Stat read() const {
        for (;;) {
            const std::uint64_t v1 = version_.load(std::memory_order_acquire);
            if ((v1 & 1) == 0) {
                const std::uint64_t seq = seq_.load(std::memory_order_relaxed);
                const std::uint64_t size = size_.load(std::memory_order_relaxed);
                const std::uint64_t hi = hi_.load(std::memory_order_relaxed), lo = lo_.load(std::memory_order_relaxed);
                std::atomic_thread_fence(std::memory_order_acquire);  // the field loads above may not move below the re-check
                if (version_.load(std::memory_order_relaxed) == v1)
                    return Stat{seq, static_cast<std::size_t>(size), static_cast<i128>((static_cast<u128>(hi) << 64) | lo)};
            }
            std::this_thread::yield();  // writer is mid-update (or just finished one): try again
        }
    }

    std::optional<Mean> mean() const { return read().mean(); }

private:
    void publish() {
        const std::uint64_t v = version_.load(std::memory_order_relaxed);
        version_.store(v + 1, std::memory_order_relaxed);
        std::atomic_thread_fence(std::memory_order_release);  // the odd marker is visible before any field write
        const auto s = static_cast<u128>(queue_.sum());
        seq_.store(++writes_, std::memory_order_relaxed);
        size_.store(queue_.size(), std::memory_order_relaxed);
        hi_.store(static_cast<std::uint64_t>(s >> 64), std::memory_order_relaxed);
        lo_.store(static_cast<std::uint64_t>(s), std::memory_order_relaxed);
        version_.store(v + 2, std::memory_order_release);  // the even marker is visible only after all field writes
    }

    void claim_writer() {
        const std::thread::id me = std::this_thread::get_id();
        std::thread::id expected{};  // "no thread"
        if (owner_.load(std::memory_order_acquire) == me) return;
        if (!owner_.compare_exchange_strong(expected, me)) throw SingleWriterViolation("single writer violated");
    }

    QueueMean queue_;            // writer thread only
    std::uint64_t writes_ = 0;   // writer thread only
    std::atomic<std::uint64_t> version_{0};
    std::atomic<std::uint64_t> seq_{0}, size_{0}, hi_{0}, lo_{0};
    std::atomic<std::thread::id> owner_{std::thread::id{}};
};

}  // namespace qmean
```

要点：

1. **字段必须是 `std::atomic`（用 `relaxed`），不能是普通变量。** 读者可能在写者写的同时读它；对普通变量这是**数据竞争（data race），UB**。`relaxed` 的原子保证"没有撕裂的单个字"，不保证顺序；顺序由版本号和栅栏（fence）提供。
2. **顺序**：写者：奇数标记 → `release` 栅栏 → 字段 → `release` 存偶数。读者：`acquire` 读版本 → 字段 → `acquire` 栅栏 → 再读版本。这样"读到偶数且前后相同"就说明读字段的期间写者没有进入。
3. 不能用 `volatile`：它不是原子，也不提供顺序。
4. `pop` 在空队列上抛异常，发生在 `publish()` 之前：读者永远看不到半个操作；`seq` 也不会因失败的 `pop` 增加。
5. **单写者怎么保证**：第一个写的线程用 `compare_exchange_strong` 把 `std::thread::id` 存进 `owner_`；别的线程再写 → `SingleWriterViolation`。（线程 id 可能在线程结束后被复用，真实系统里写者线程的生命周期要由设计保证。）
6. 验证数据竞争：用 `-fsanitize=thread`（TSan）跑并发测试。

## 6. 陷阱

1. **默认的移动构造函数**对 `int`/`size_t`/`__int128` 成员只是拷贝（2.3）。
2. **`push_back` 之后继续用旧引用 / 迭代器**（第 4 节）。
3. **`-x`、`std::abs(x)` 对 `LLONG_MIN` 是 UB。** 这里 `x` 可以是 `LLONG_MIN`；用无符号类型取绝对值。
4. **`(double)sum / n` 对大和舍入两次**（2.3）。
5. **环形缓冲区扩容时直接复制整个数组**：`head` 不在 0 时顺序错乱。
6. **读者读普通变量**：数据竞争，UB（5.3）。
7. **`std::vector<bool>`、`std::map::operator[]`** 这类"看起来像普通容器"的坑，在这题里不会用到，但会问。

## 7. 面试官会追问什么（senior）

**Q1. `std::deque` 还是环形数组？** 见 2.2：连续 vs 分块、一次分配 vs 多次、扩容复制 vs 不复制。接口再包一层 `std::queue` 只是适配器。

**Q2. `get_mean` 返回 `double` 还是分数？** 分数是精确的、可比较的；`double` 方便但有舍入。我给两个：`mean()` 精确，`get_mean()` 是对精确值只舍入一次的近似。

**Q3. 如果元素是 `double`，怎么做滑动窗口均值？** running sum 会累积误差：用补偿求和（Kahan），或者定期重新求和，或者用 Welford 的在线算法；NaN / Inf 进入窗口之后，running sum 再也回不到有限值，需要单独计数处理。

**Q4. 线程安全怎么做？** 先说 `std::mutex`（正确且简单）；读多写少用 `std::shared_mutex`；要求读者不阻塞写者时才上 seqlock / 不可变快照；每一步说清楚代价。

**Q5. `snapshot` 到底该拷贝还是共享？** 拷贝：简单，O(k)；共享：需要持久化结构（Part 3），每个版本 O(log n)。取决于快照频率和大小。

**Q6. `memory_order_seq_cst` 不是更安全吗？** 默认 `seq_cst` 一定正确，但全栅栏有额外开销（ARM 上更明显）；这里只要"字段在版本号之间"的顺序，所以 `release` / `acquire` 就够了。先写 `seq_cst` 版本再优化是合理的。

**Q7. `noexcept` 的移动构造有什么用？** `std::vector<QueueMean>` 扩容时，只有移动构造是 `noexcept` 才会用移动，否则为了强异常保证退回拷贝。

## 8. 自测

1. `QueueMean b = std::move(a);` 之后，如果移动构造函数是编译器生成的，`a.push(1)` 会发生什么？
2. 为什么 running sum 用 `__int128` 而不是 `long double`？
3. 环形缓冲区容量 8、`head = 5`、`size = 5`，扩容到 16 时元素怎么复制？
4. seqlock 里，读者读到的版本号是奇数，该怎么办？为什么字段要用 `relaxed` 原子而不是普通变量？
5. `Version v = at(version);` 为什么按值拷贝而不是 `const Version& v = at(version);`？
6. `to_double` 里为什么要"粘滞位"？

<details><summary>答案</summary>

1. `a` 的 `buf_` 已空但 `size_` 还是旧值：`push` 里 `size_ == buf_.size()` 不成立，直接写 `buf_[...]`，越界写（ASan 会报）。
2. `long double` 在不同平台宽度不同（Apple arm64 上就是 64 位 `double`），尾数最多 64 位，装不下 2^127 范围的精确和；`__int128` 是精确整数。
3. 先复制 `[head, 容量)`（3 个元素）到新数组开头，再复制 `[0, head)`（2 个元素）接在后面，新 `head = 0`。
4. 写者正在更新：`yield` 后重试。普通变量在写者写入的同时被读是数据竞争（UB），`relaxed` 原子保证每个字不撕裂，顺序交给版本号和栅栏。
5. `new_version` 里的 `versions_.push_back` 可能重新分配，旧引用悬空（读到已释放内存）；按值拷贝只有 32 字节。
6. 判断"是否恰好在两个 `double` 正中间"：被丢弃的位全 0 才是平局（取偶），只要有任何非零位就必须向上进位；没有粘滞位就会把"略大于一半"误当平局。

</details>
