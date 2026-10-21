# hc08 · Order Sequence API（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。

## 1. 题目

交易系统里有一串**活跃订单**，按**到达（插入）顺序**排好。实现几个 API：往末尾放订单、删订单，以及问「从序列头数到订单 X，一共有几张订单 / 总共多少数量」。订单数很大、查询很多，所以查询不能是 O(n)。

* 订单 = `id`（任意 `long long`，同时只能有一张同 id 的活跃订单）+ `qty`（正整数）。
* `put(id, qty)`：放到序列**末尾**。`qty ≤ 0` → `std::invalid_argument("invalid quantity")`；id 已活跃 → `invalid_argument("duplicate id")`；全体活跃订单数量之和会超过 `LLONG_MAX` → `std::overflow_error("overflow")`，**状态不变**。
* `remove(id, qty)`：从订单里删掉 `qty` 个单位，返回**剩余数量**；剩余为 0 时订单从序列里移除；订单**位置不变**。`qty ≤ 0` → `invalid_argument`；未知 id → `UnknownId("unknown id")`；`qty >` 剩余 → `invalid_argument("quantity exceeds remaining")`，状态不变。（Java 里叫 `delete`；`delete` 是 C++ 关键字。）
* `count_up_to(id)`：从序列头到该订单（含）的活跃订单数。`qty_up_to(id)`：同范围内剩余数量之和。未知 id → `UnknownId`。
* `id_at(k)`：第 k 张（1 起）活跃订单的 id；越界 → `std::out_of_range("index out of range")`。
* `size()` · `total_qty()` · `entries()`（全部活跃订单，插入顺序）。
* 同一个 id 删光后可以再 `put`，它排到**最后**。

| Part | 内容 |
|---|---|
| 1 | 语义做对，允许朴素实现（线性扫描）。另有文本接口 `parse / apply / render / replay` |
| 2 | **亚线性查询**：`count_up_to` / `qty_up_to` / `id_at` 都是 O(log n)；50 万张订单 + 50 万次操作 < 2 s |
| 3 | **部分删除** + **压缩**（compaction）：下标空间写满时把活跃订单重新编号；200 万次 put/remove 循环、活跃订单 ≤ 1000，容量必须 ≤ 4096 |

文本接口：`PUT id qty` · `DELETE id qty` · `COUNT id` · `QTY id` · `AT k`（大小写不敏感、空白任意；脚本里空行和 `#` 行跳过）。输出：`PUT` → `OK`；`DELETE` → 剩余数量；`COUNT` / `QTY` / `AT` → 数字；业务错误 → `ERR <message>`。

```
PUT 10 5        OK
PUT 20 3        OK
PUT 30 7        OK
COUNT 30        3         序列 [10:5, 20:3, 30:7]，30 排第 3
QTY 20          8         5 + 3
DELETE 20 3     0         20 被删光
QTY 30          12        5 + 7
AT 2            30
DELETE 10 5     0
PUT 20 4        OK        20 重新进来，排到最后：[30:7, 20:4]
QTY 20          11
DELETE 99 1     ERR unknown id
DELETE 30 9     ERR quantity exceeds remaining
PUT 30 1        ERR duplicate id
AT 3            ERR index out of range
AT 2            20
```

部分删除（Part 3）：`PUT 1 10 / PUT 2 10 / PUT 3 10 / DELETE 2 4 / QTY 3 / COUNT 3 / DELETE 2 6 / COUNT 3 / AT 2` → `6 26 3 0 2 3`。`DELETE 2 4` 只是减量（10 → 6），订单还在，所以 `COUNT 3` 仍是 3；再删 6 才真正移除。

## 2. Part 1：朴素版

先把语义做对。一个 `std::vector<std::pair<id, qty>>`，查询线性扫描：

```cpp
// Part 1 in the simplest possible way: a vector scanned linearly.  Correct, but every query is O(n).
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

struct Naive {
    std::vector<std::pair<long long, long long>> orders;  // {id, qty} in insertion order
    std::size_t find(long long id) const {
        for (std::size_t i = 0; i < orders.size(); ++i)
            if (orders[i].first == id) return i;
        throw std::runtime_error("unknown id");
    }
    void put(long long id, long long qty) { orders.emplace_back(id, qty); }
    long long count_up_to(long long id) const { return static_cast<long long>(find(id)) + 1; }
    long long qty_up_to(long long id) const {
        long long s = 0;
        for (std::size_t i = 0, at = find(id); i <= at; ++i) s += orders[i].second;
        return s;
    }
};

int main() {
    Naive s;
    s.put(10, 5); s.put(20, 3); s.put(30, 7);
    std::cout << "COUNT 30 = " << s.count_up_to(30) << ", QTY 20 = " << s.qty_up_to(20) << "\n";
}
```

```text
COUNT 30 = 3, QTY 20 = 8
```

每次 `count_up_to` / `qty_up_to` 都是 O(n)，50 万张订单 × 50 万次查询是 2.5 × 10¹¹ 次操作，超时。面试官要听到你**自己说出来**这一点，然后问：「前缀和 + 在线修改，想到什么？」——树状数组。

## 3. Part 2：树状数组（Fenwick tree / BIT）

### 3.1 前缀和（prefix sum）的问题

数组 `a[1..n]`，要支持：**改一个数**（`a[i] += d`）和**求前缀和**（`a[1] + … + a[i]`）。

* 直接存数组：改是 O(1)，求和 O(n)。
* 存前缀和数组：求和 O(1)，改是 O(n)。
* 线段树：两个都是 O(log n)，但要 2n 个节点、递归。
* **树状数组**：两个都是 O(log n)，一个数组，两个 `for` 循环，常数很小。

### 3.2 `lowbit` 与它管的区间

`i & -i` 取出 `i` 二进制里**最低的那个 1**（`lowbit`）：`12 = 1100₂` → `0100₂ = 4`；`8 = 1000₂` → `8`。（补码里 `-i` 是 `~i + 1`：最低的 1 以下全是 0，所以与 `i` 相与只剩最低的 1。）

树状数组的 `tree[i]` 管的是下标区间 **(i − lowbit(i), i]** 的和：

```
i:        1   2   3   4   5   6   7   8
lowbit:   1   2   1   4   1   2   1   8
tree[i] 管: (0,1] (0,2] (2,3] (0,4] (4,5] (4,6] (6,7] (0,8]
```

* **求前缀和 `prefix(7)`**：`tree[7]`（管 7）+ `tree[6]`（管 5..6）+ `tree[4]`（管 1..4）。每次 `i -= lowbit(i)` 跳到前一块，把 `[1, 7]` 拆成互不相交的块。
* **改 `a[3] += d`**：要更新所有管着 3 的节点：`tree[3]`、`tree[4]`、`tree[8]`。每次 `i += lowbit(i)` 跳到下一个管着它的节点。
* 两个循环都至多走 log₂(n) 步：每步至少消掉（或进位掉）一个 1。

### 3.3 在树上二分：找第 k 个

如果 `a[i]` 是 0/1（这个位置有没有活跃订单），`tree[i]` 就是区间里活跃订单的个数。要找第 k 张活跃订单的位置：从大步长往小步长试，**如果整块里的订单数还 < k，说明第 k 个在这块后面，整块跳过**，k 减去这块的数量；否则留在块里、缩小步长。容量是 2 的幂时，`pos` 的二进制每次补一位，等于在二进制上逐位确定答案。

```cpp
// A Fenwick tree in 20 lines: point update, prefix sum, and "find the k-th" by binary descent.
#include <bit>
#include <iostream>
#include <vector>

struct Fenwick {
    int n;  // power of two
    std::vector<long long> t;
    explicit Fenwick(int size) : n(static_cast<int>(std::bit_ceil(static_cast<unsigned>(size)))), t(static_cast<std::size_t>(n) + 1, 0) {}
    void add(int i, long long d) { for (; i <= n; i += i & -i) t[static_cast<std::size_t>(i)] += d; }      // i & -i = lowest set bit
    long long prefix(int i) const { long long r = 0; for (; i > 0; i -= i & -i) r += t[static_cast<std::size_t>(i)]; return r; }
    int kth(long long k) const {  // smallest index whose prefix sum >= k (all values are 0 or 1 here)
        int pos = 0;
        for (int pw = n; pw > 0; pw >>= 1)
            if (pos + pw <= n && t[static_cast<std::size_t>(pos + pw)] < k) { pos += pw; k -= t[static_cast<std::size_t>(pos)]; }
        return pos + 1;
    }
};

int main() {
    Fenwick f(8);
    for (int i : {1, 2, 3, 5, 8}) f.add(i, 1);   // live slots
    f.add(2, -1);                                  // slot 2 removed: a hole
    std::cout << "live slots up to 5: " << f.prefix(5) << "\n";   // 1, 3, 5 -> 3
    std::cout << "3rd live slot: " << f.kth(3) << "\n";           // slot 5
    std::cout << "4th live slot: " << f.kth(4) << "\n";           // slot 8
    std::cout << "lowbit(12)=" << (12 & -12) << " lowbit(8)=" << (8 & -8) << "\n";
}
```

```text
live slots up to 5: 3
3rd live slot: 5
4th live slot: 8
lowbit(12)=4 lowbit(8)=8
```

### 3.4 怎么把订单放进树里

* 每张订单占一个**只增不减**的「插入下标」（1..capacity），顺序就是插入顺序——订单一律追加在末尾，不需要离散化。
* **删除只留洞**：该下标上的数量清零、订单数 −1；下标不回收（回收会破坏插入顺序）。
* **两棵树**：`cnt_`（每个活跃订单 1）和 `sum_`（剩余数量）。`count_up_to(id)` = `prefix_cnt(index_of[id])`，`qty_up_to(id)` = `prefix_sum(index_of[id])`，`id_at(k)` = 在 `cnt_` 上找第 k 个，再查 `id_by_idx_`。
* **`id → 下标`** 用 `std::unordered_map`。

## 4. 代码

### 4.1 类型、错误、哈希

```cpp
// hc08 · Order sequence API — C++20 reference.  Statement: ../problem.md (Java: reference/OrderSequence.java).
// Parts: 1 semantics + text interface, 2 Fenwick trees (prefix count / quantity / k-th id in O(log n)),
//        3 partial removal + compaction of the index space (memory follows the live orders, not the history).
#pragma once

#include <algorithm>
#include <bit>
#include <charconv>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <string>
#include <string_view>
#include <system_error>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>

namespace oseq {

// ------------------------------------------------------------------------------------------------ messages and errors
inline constexpr std::string_view INVALID_QTY = "invalid quantity";
inline constexpr std::string_view DUPLICATE_ID = "duplicate id";
inline constexpr std::string_view UNKNOWN_ID = "unknown id";
inline constexpr std::string_view QTY_EXCEEDS = "quantity exceeds remaining";
inline constexpr std::string_view INDEX_RANGE = "index out of range";
inline constexpr std::string_view SUM_OVERFLOW = "overflow";  // not OVERFLOW: <math.h> defines that macro on some platforms

/// Java NoSuchElementException.  The other mappings: IllegalArgumentException -> std::invalid_argument,
/// IndexOutOfBoundsException -> std::out_of_range, ArithmeticException -> std::overflow_error.
struct UnknownId : std::runtime_error {
    using std::runtime_error::runtime_error;
};

struct Entry {
    long long id;
    long long qty;
    friend bool operator==(const Entry&, const Entry&) = default;
};

// ------------------------------------------------------------------------------------------------ text commands
struct Put { long long id; long long qty; friend bool operator==(const Put&, const Put&) = default; };
struct Delete { long long id; long long qty; friend bool operator==(const Delete&, const Delete&) = default; };
struct CountUpTo { long long id; friend bool operator==(const CountUpTo&, const CountUpTo&) = default; };
struct QtyUpTo { long long id; friend bool operator==(const QtyUpTo&, const QtyUpTo&) = default; };
struct IdAt { int k; friend bool operator==(const IdAt&, const IdAt&) = default; };
using Op = std::variant<Put, Delete, CountUpTo, QtyUpTo, IdAt>;

struct Ok { friend bool operator==(const Ok&, const Ok&) = default; };
struct Num { long long value; friend bool operator==(const Num&, const Num&) = default; };
struct Err { std::string message; friend bool operator==(const Err&, const Err&) = default; };
using Result = std::variant<Ok, Num, Err>;

namespace detail {
template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }
constexpr char to_upper(char c) { return c >= 'a' && c <= 'z' ? static_cast<char>(c - 'a' + 'A') : c; }
inline std::string_view strip(std::string_view s) {
    while (!s.empty() && is_space(s.front())) s.remove_prefix(1);
    while (!s.empty() && is_space(s.back())) s.remove_suffix(1);
    return s;
}
inline std::vector<std::string_view> split_words(std::string_view s) {
    std::vector<std::string_view> out;
    std::size_t i = 0;
    while (i < s.size()) {
        while (i < s.size() && is_space(s[i])) ++i;
        const std::size_t start = i;
        while (i < s.size() && !is_space(s[i])) ++i;
        if (i > start) out.push_back(s.substr(start, i - start));
    }
    return out;
}
/// std::hash<long long> is the identity function.  libc++ keeps a power-of-two bucket count when it is asked for one (and maps
/// hash & mask), so ids that differ only in the high bits (i << 32) would all share bucket 0 and every lookup becomes a linear scan.
/// splitmix64's finaliser spreads every input bit over all output bits.
struct IdHash {
    std::size_t operator()(long long id) const noexcept {
        auto x = static_cast<std::uint64_t>(id);
        x ^= x >> 30; x *= 0xBF58476D1CE4E5B9ull;
        x ^= x >> 27; x *= 0x94D049BB133111EBull;
        x ^= x >> 31;
        return static_cast<std::size_t>(x);
    }
};
/// std::from_chars succeeds on a valid prefix ("12abc" -> 12): the end pointer must be the end of the token.  It also rejects '+'.
template <class T> T parse_number(std::string_view tok, std::string_view line) {
    T v{};
    const auto [end, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), v);
    if (ec != std::errc{} || end != tok.data() + tok.size()) throw std::invalid_argument("bad number in: " + std::string(line));
    return v;
}
inline void expect_args(const std::vector<std::string_view>& t, std::size_t n) {
    if (t.size() != n) throw std::invalid_argument(std::string(t[0]) + " expects " + std::to_string(n - 1) + " arguments");
}
}  // namespace detail
```

* **异常对应关系**：Java 的 `IllegalArgumentException` → `std::invalid_argument`；`IndexOutOfBoundsException` → `std::out_of_range`；`ArithmeticException` → `std::overflow_error`；`NoSuchElementException` → 自定义的 `UnknownId`（继承 `runtime_error`）。
* **错误信息是常量 `std::string_view`**，`std::string(INVALID_QTY)` 构造异常。常量不叫 `OVERFLOW`：`<math.h>` 在一些平台上把它定义成宏。
* **`IdHash`——`std::hash<long long>` 是恒等函数。** 桶号是 `hash % 桶数`，如果桶数是 2 的幂（libc++ 在你 `rehash` 成 2 的幂时就保持 2 的幂），就变成 `hash & mask`，只用低位。id 是 `i << 32` 这样**只在高位不同**的数时，全部落进同一个桶，每次查找退化成线性扫描：

```cpp
// std::hash<long long> is the identity.  With a power-of-two bucket array (libc++ keeps one when you ask for one) the bucket is
// hash & mask, so keys that differ only in their high bits all land in bucket 0.
#include <cstdint>
#include <functional>
#include <iostream>
#include <unordered_map>

struct Mixed {  // splitmix64 finaliser
    std::size_t operator()(long long id) const noexcept {
        auto x = static_cast<std::uint64_t>(id);
        x ^= x >> 30; x *= 0xBF58476D1CE4E5B9ull;
        x ^= x >> 27; x *= 0x94D049BB133111EBull;
        x ^= x >> 31;
        return static_cast<std::size_t>(x);
    }
};

template <class Map> std::size_t longest_chain(Map& m) {
    std::size_t worst = 0;
    for (std::size_t b = 0; b < m.bucket_count(); ++b) worst = std::max(worst, m.bucket_size(b));
    return worst;
}

int main() {
    std::cout << "std::hash<long long>(42) = " << std::hash<long long>{}(42) << "\n";
    std::unordered_map<long long, int> plain;
    std::unordered_map<long long, int, Mixed> mixed;
    plain.rehash(4096);   // a power of two, as the order sequence asks for min_capacity buckets
    mixed.rehash(4096);
    for (long long i = 0; i < 2000; ++i) { plain[i << 32] = 1; mixed[i << 32] = 1; }
    std::cout << "2000 keys of the form i<<32, longest bucket chain:  identity hash = " << longest_chain(plain)
              << ",  mixed hash = " << longest_chain(mixed) << "\n";
}
```

```text
std::hash<long long>(42) = 42
2000 keys of the form i<<32, longest bucket chain:  identity hash = 2000,  mixed hash = 5
```

  splitmix64 的末尾混合步骤让每一位输入都影响每一位输出。
* `parse_number`：`std::from_chars` 成功解析一个合法前缀就算成功（`12abc` → 12），所以要检查结束指针；它也不认 `+`。

### 4.2 构造、拷贝、移动

```cpp
// ------------------------------------------------------------------------------------------------ the sequence
/// Live orders in insertion order.  Every order owns an ever-increasing "insertion index" 1..capacity; removal only zeroes it
/// (leaves a hole).  Two Fenwick trees over that index space: cnt_ (number of live orders) and sum_ (remaining quantity).
/// When the index space is full, compact(): renumber the live orders 1..m in their original order.
class OrderSequence {
public:
    OrderSequence() : OrderSequence(16) {}

    /// Index space rounded up to a power of two; compaction never goes below it.  <= 0 or > 2^29 -> std::invalid_argument.
    explicit OrderSequence(int initial_capacity) {
        if (initial_capacity < 1 || initial_capacity > (1 << 29)) throw std::invalid_argument("capacity out of range");
        min_capacity_ = static_cast<int>(std::bit_ceil(static_cast<unsigned>(initial_capacity)));  // bit_ceil(x) is UB when the result is not representable: the range check came first
        allocate(min_capacity_);
        index_of_.rehash(static_cast<std::size_t>(min_capacity_));  // enough buckets for a full index space: puts never rehash
    }

    OrderSequence(const OrderSequence&) = default;
    OrderSequence& operator=(const OrderSequence&) = default;
    // The generated move would move the vectors but COPY capacity_, next_index_ and the counters: the moved-from object
    // would claim a full index space and then index into empty vectors.  Moved-from = valid, empty, capacity 0 (the first put
    // finds next_index_ > capacity_ and compacts into a fresh min_capacity_ space).
    OrderSequence(OrderSequence&& o) noexcept
        : min_capacity_(o.min_capacity_),
          capacity_(std::exchange(o.capacity_, 0)),
          cnt_(std::move(o.cnt_)),
          sum_(std::move(o.sum_)),
          id_by_idx_(std::move(o.id_by_idx_)),
          qty_by_idx_(std::move(o.qty_by_idx_)),
          next_index_(std::exchange(o.next_index_, 1)),
          index_of_(std::move(o.index_of_)),
          total_qty_(std::exchange(o.total_qty_, 0)),
          compactions_(std::exchange(o.compactions_, 0)) {
        o.reset_containers();
    }
    OrderSequence& operator=(OrderSequence&& o) noexcept {
        if (this != &o) {
            min_capacity_ = o.min_capacity_;
            capacity_ = std::exchange(o.capacity_, 0);
            cnt_ = std::move(o.cnt_);
            sum_ = std::move(o.sum_);
            id_by_idx_ = std::move(o.id_by_idx_);
            qty_by_idx_ = std::move(o.qty_by_idx_);
            next_index_ = std::exchange(o.next_index_, 1);
            index_of_ = std::move(o.index_of_);
            total_qty_ = std::exchange(o.total_qty_, 0);
            compactions_ = std::exchange(o.compactions_, 0);
            o.reset_containers();
        }
        return *this;
    }
```

* 容量用 `std::bit_ceil` 取 2 的幂。`bit_ceil` 的结果装不下时是 UB，所以**先**检查范围（≤ 2^29），再调用。
* 构造时就 `rehash(min_capacity_)`：活跃订单数永远 ≤ 容量，所以 `put` 永远不会触发 rehash，没有偶发的长停顿。
* **移动构造函数要手写。** 编译器生成的会搬走 `std::vector`，却**拷贝** `capacity_`、`next_index_` 这些 `int`——被搬走的对象声称下标空间是满的，下一次 `put` 就去写空 vector。手写的版本把被搬走的对象变成「合法的空序列」：`capacity_ = 0`、`next_index_ = 1`、容器清空；第一次 `put` 看到 `next_index_ > capacity_`，走压缩流程，重新分配 `min_capacity_`。
* `std::unordered_map` 被移动后只是「合法但未指定」，所以显式 `clear()`。

### 4.3 `put` 与 `remove`

```cpp
    /// Append at the end.  qty <= 0 / id live -> invalid_argument; the total would exceed LLONG_MAX -> overflow_error.
    /// Every check that can throw comes before the first mutation, so a failed put changes nothing (not even the compaction count).
    void put(long long id, long long qty) {
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        if (index_of_.contains(id)) throw std::invalid_argument(std::string(DUPLICATE_ID));
        long long new_total;
        if (__builtin_add_overflow(total_qty_, qty, &new_total)) throw std::overflow_error(std::string(SUM_OVERFLOW));
        if (next_index_ > capacity_) compact();  // behaviour-preserving, so it is fine that it happens before the insert below
        const int i = next_index_;
        index_of_.try_emplace(id, i);  // the only remaining call that can throw (bad_alloc); nothing else has changed yet
        ++next_index_;
        id_by_idx_[idx(i)] = id;
        qty_by_idx_[idx(i)] = qty;
        add_cnt(i, 1);
        add_sum(i, qty);
        total_qty_ = new_total;
    }

    /// Remove qty units from an order; returns what is left (0 = the order is gone).  The position never changes.
    /// (`delete` is a C++ keyword, hence the name.)  qty <= 0 -> invalid_argument; unknown id -> UnknownId; qty > left -> invalid_argument.
    long long remove(long long id, long long qty) {
        if (qty <= 0) throw std::invalid_argument(std::string(INVALID_QTY));
        const int i = index_or_throw(id);
        const long long have = qty_by_idx_[idx(i)];
        if (qty > have) throw std::invalid_argument(std::string(QTY_EXCEEDS));
        const long long left = have - qty;
        qty_by_idx_[idx(i)] = left;
        add_sum(i, -qty);  // qty > 0, so -qty cannot be LLONG_MIN
        total_qty_ -= qty;
        if (left == 0) {
            add_cnt(i, -1);
            index_of_.erase(id);
        }
        return left;
    }
```

* **先检查、后修改，且检查顺序有讲究**：`qty`、重复 id、总量溢出这三个会抛异常的检查，都排在 `compact()` 之前。否则容量满时一个失败的 `put` 会白白触发一次压缩（`compactions()` 加一，对象的内部布局变了）。
* **总量溢出**：`__builtin_add_overflow(total_qty_, qty, &new_total)`。有符号溢出是 UB，不能事后检查。
* **`try_emplace` 是唯一可能抛 `bad_alloc` 的调用**，放在所有别的修改之前；它之后的赋值都不抛异常。这样 `put` 对异常有**强保证**（失败则无变化）。
* `add_sum(i, -qty)`：`qty > 0`，所以 `-qty` 不会是 `LLONG_MIN`。
* Fenwick 树里每个节点存的是一段活跃订单的数量和，不会超过 `total_qty_ ≤ LLONG_MAX`，所以树内部也不会溢出。

### 4.4 查询

```cpp
    /// Live orders from the head up to and including this one.
    long long count_up_to(long long id) const { return prefix_cnt(index_or_throw(id)); }
    /// Remaining quantity over the same range.
    long long qty_up_to(long long id) const { return prefix_sum(index_or_throw(id)); }

    /// Id of the k-th live order (1-based).  O(log n) binary descent on the cnt_ tree: tree[pos + 2^j] covers (pos, pos + 2^j].
    long long id_at(int k) const {
        if (k < 1 || static_cast<std::size_t>(k) > index_of_.size()) throw std::out_of_range(std::string(INDEX_RANGE));  // k < 1 first: a negative k would convert to a huge size_t
        int pos = 0, rem = k;
        for (int pw = capacity_; pw > 0; pw >>= 1) {
            const int nxt = pos + pw;
            if (nxt <= capacity_ && cnt_[idx(nxt)] < rem) {
                pos = nxt;
                rem -= cnt_[idx(nxt)];
            }
        }
        return id_by_idx_[idx(pos + 1)];
    }

    std::size_t size() const { return index_of_.size(); }
    long long total_qty() const { return total_qty_; }
    int capacity() const { return capacity_; }
    int compactions() const { return compactions_; }
    /// Bucket count of the id -> index hash map (unordered_map never gives bucket memory back by itself; compaction rehashes it).
    std::size_t index_buckets() const { return index_of_.bucket_count(); }

    /// All live orders in insertion order.  O(capacity).
    std::vector<Entry> entries() const {
        std::vector<Entry> out;
        out.reserve(index_of_.size());
        for (int i = 1; i < next_index_; ++i)
            if (qty_by_idx_[idx(i)] > 0) out.push_back({id_by_idx_[idx(i)], qty_by_idx_[idx(i)]});
        return out;
    }
```

* `index_or_throw` 里用 **`find`**，绝不用 `operator[]`：对不存在的 key，`operator[]` 会**插入**一个默认元素：

```cpp
// map[key] on a missing key INSERTS a default element.  Lookups must use find / contains / at.
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<long long, int> index_of;
    index_of[7] = 3;
    const int wrong = index_of[99];            // "lookup" of an unknown id
    std::cout << "operator[] of unknown id returned " << wrong << ", size is now " << index_of.size() << "\n";
    std::cout << "contains(99) is now " << std::boolalpha << index_of.contains(99) << "   <- the unknown id became a live one\n";

    std::unordered_map<long long, int> clean{{7, 3}};
    if (const auto it = clean.find(99); it == clean.end()) std::cout << "find(99): not found, size still " << clean.size() << "\n";
}
```

```text
operator[] of unknown id returned 0, size is now 2
contains(99) is now true   <- the unknown id became a live one
find(99): not found, size still 1
```

  如果查询未知 id 时顺手插入了它，`size()` 会变大，之后真正 `put` 这个 id 还会报「重复」。
* `id_at` 里先判 `k < 1`，再把 `k` 转成 `size_t` 和 `size()` 比较：意图明确，不依赖「负数回绕成无符号后碰巧很大」。`INT_MIN` / `INT_MAX` 都要抛 `out_of_range`。
* `i & -i` 用 `int`：容量 ≤ 2^29，`i + lowbit(i) ≤ 2^30`，不会溢出。

### 4.5 文本接口

```cpp
    // -------------------------------------------------------------------------------------------- text interface
    /// PUT id qty | DELETE id qty | COUNT id | QTY id | AT k (case-insensitive, any whitespace).  Bad format -> invalid_argument.
    static Op parse(std::string_view line) {
        const auto t = detail::split_words(line);
        if (t.empty()) throw std::invalid_argument("empty command");
        const std::string_view shown = detail::strip(line);
        std::string cmd(t[0]);
        for (char& c : cmd) c = detail::to_upper(c);
        if (cmd == "PUT" || cmd == "DELETE") {
            detail::expect_args(t, 3);
            const auto id = detail::parse_number<long long>(t[1], shown);
            const auto qty = detail::parse_number<long long>(t[2], shown);
            if (cmd == "PUT") return Put{id, qty};
            return Delete{id, qty};
        }
        if (cmd == "COUNT" || cmd == "QTY") {
            detail::expect_args(t, 2);
            const auto id = detail::parse_number<long long>(t[1], shown);
            if (cmd == "COUNT") return CountUpTo{id};
            return QtyUpTo{id};
        }
        if (cmd == "AT") {
            detail::expect_args(t, 2);
            return IdAt{detail::parse_number<int>(t[1], shown)};
        }
        throw std::invalid_argument("unknown command: " + std::string(t[0]));
    }

    /// Execute one command; business errors become Err, they do not escape.  Only the four expected exception types are caught:
    /// std::bad_alloc and friends must still propagate.
    Result apply(const Op& op) {
        try {
            return std::visit(detail::overloaded{[&](const Put& p) -> Result { put(p.id, p.qty); return Ok{}; },
                                                 [&](const Delete& d) -> Result { return Num{remove(d.id, d.qty)}; },
                                                 [&](const CountUpTo& c) -> Result { return Num{count_up_to(c.id)}; },
                                                 [&](const QtyUpTo& q) -> Result { return Num{qty_up_to(q.id)}; },
                                                 [&](const IdAt& a) -> Result { return Num{id_at(a.k)}; }},
                              op);
        } catch (const std::invalid_argument& e) {
            return Err{e.what()};
        } catch (const UnknownId& e) {
            return Err{e.what()};
        } catch (const std::out_of_range& e) {
            return Err{e.what()};
        } catch (const std::overflow_error& e) {
            return Err{e.what()};
        }
    }

    static std::string render(const Result& r) {
        return std::visit(detail::overloaded{[](const Ok&) { return std::string("OK"); },
                                             [](const Num& n) { return std::to_string(n.value); },
                                             [](const Err& e) { return "ERR " + e.message; }},
                          r);
    }

    /// Run a script (blank lines and '#' lines skipped).  A malformed line throws invalid_argument starting with "line N" (1-based).
    static std::vector<std::string> replay(const std::vector<std::string>& lines) {
        OrderSequence seq;
        std::vector<std::string> out;
        for (std::size_t i = 0; i < lines.size(); ++i) {
            const std::string_view line = detail::strip(lines[i]);
            if (line.empty() || line.front() == '#') continue;
            Op op;
            try {
                op = parse(line);
            } catch (const std::invalid_argument& e) {
                throw std::invalid_argument("line " + std::to_string(i + 1) + ": " + e.what());
            }
            out.push_back(render(seq.apply(op)));
        }
        return out;
    }
```

* `parse` 先看有几个参数、再解析数字。数字解析失败（含 `AT 99999999999`，装不进 `int`）统一是 `invalid_argument("bad number in: ...")`。
* **`apply` 只捕获四种预期的异常**。`catch (const std::exception&)` 会把 `std::bad_alloc` 也变成 `ERR ...`——内存不足应当继续往上抛。
* 返回类型：`std::variant<Ok, Num, Err>`；`render` 用 `std::visit`，同样编译期穷尽。
* `replay` 把 `parse` 的 `invalid_argument` 加上 `line N: ` 前缀再抛。

## 5. Part 3：压缩（compaction）

### 5.1 为什么需要

删除只留洞、下标不回收，所以下标只增不减。哪怕任何时刻只有 1000 张活跃订单，处理 200 万张订单也要 200 万大小的数组。压缩 = 把活跃订单**按原顺序**重新编号为 1..m，同时重建两棵树。**内存应该跟活跃量走，而不是跟历史总量走。**

### 5.2 新容量

新容量 = 2 的幂 ≥ `max(min_capacity, 1.5m + 1)`（m = 活跃订单数）：

* 压缩后至少腾出约 m/2 个空位，所以下次压缩之前至少还有 m/2 次 `put`；一次压缩 O(容量)=O(m)，摊还到每次 `put` 是 O(1)；
* 活跃订单少时容量会**缩回去**（但不会低于初始容量）；全是活跃订单时必须**长**（`1.5m + 1 > m`）。

```cpp
// Amortised cost of compaction: a compaction costs O(capacity) but frees about m/2 slots, so each put pays O(1) on average.
#include <algorithm>
#include <bit>
#include <iostream>

int main() {
    const int live = 1000, min_capacity = 16;
    long long moved = 0, puts = 0;
    int capacity = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity, live + live / 2 + 1))));
    int next = live + 1;                       // 1000 live orders were just compacted into the front
    for (int cycle = 0; cycle < 1000; ++cycle) {
        while (next <= capacity) { ++next; ++puts; }   // each put also removes the oldest: live stays 1000
        moved += live;                                  // compaction moves the live orders
        capacity = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity, live + live / 2 + 1))));
        next = live + 1;
    }
    std::cout << "capacity " << capacity << ", puts per compaction ~" << puts / 1000 << ", moves per put = " << static_cast<double>(moved) / static_cast<double>(puts) << "\n";
}
```

```text
capacity 2048, puts per compaction ~1048, moves per put = 0.954198
```

### 5.3 实现

线性建树：先把每个活跃订单放进新数组的 `cnt[j] = 1`、`sum[j] = qty`，再从 1 到 n 让每个节点把自己加到父节点（`p = i + lowbit(i)`），O(容量) 而不是逐个 `add` 的 O(m log n)。

```cpp
private:
    static std::size_t idx(int i) { return static_cast<std::size_t>(i); }

    void allocate(int cap) {
        capacity_ = cap;
        cnt_.assign(idx(cap) + 1, 0);
        sum_.assign(idx(cap) + 1, 0);
        id_by_idx_.assign(idx(cap) + 1, 0);
        qty_by_idx_.assign(idx(cap) + 1, 0);
    }

    void reset_containers() noexcept {
        cnt_.clear();
        sum_.clear();
        id_by_idx_.clear();
        qty_by_idx_.clear();
        index_of_.clear();  // a moved-from unordered_map is "valid but unspecified"
    }

    int index_or_throw(long long id) const {
        const auto it = index_of_.find(id);  // find, never operator[]: operator[] would INSERT the missing id
        if (it == index_of_.end()) throw UnknownId(std::string(UNKNOWN_ID));
        return it->second;
    }

    // i & -i is the lowest set bit of i.  tree[i] covers (i - lowbit(i), i]; update climbs with i += lowbit, query descends with i -= lowbit.
    // int is enough: capacity <= 2^29, so i + lowbit(i) <= 2^30 never overflows.
    void add_cnt(int i, int delta) {
        for (; i <= capacity_; i += i & -i) cnt_[idx(i)] += delta;
    }
    void add_sum(int i, long long delta) {
        for (; i <= capacity_; i += i & -i) sum_[idx(i)] += delta;
    }
    long long prefix_cnt(int i) const {
        long long r = 0;
        for (; i > 0; i -= i & -i) r += cnt_[idx(i)];
        return r;
    }
    long long prefix_sum(int i) const {
        long long r = 0;
        for (; i > 0; i -= i & -i) r += sum_[idx(i)];
        return r;
    }
```

```cpp
    /// Renumber the live orders 1..m in order; new capacity = power of two >= max(min_capacity, 1.5m + 1), so at least ~m/2 slots are
    /// free afterwards (amortised O(1) per put) and the space shrinks back when few orders are live.
    /// Strong guarantee: all allocation happens first; the commit at the end cannot throw.
    void compact() {
        const int m = static_cast<int>(index_of_.size());
        const int new_cap = static_cast<int>(std::bit_ceil(static_cast<unsigned>(std::max(min_capacity_, m + (m >> 1) + 1))));
        std::vector<int> n_cnt(idx(new_cap) + 1, 0);
        std::vector<long long> n_sum(idx(new_cap) + 1, 0), n_id(idx(new_cap) + 1, 0), n_qty(idx(new_cap) + 1, 0);
        index_of_.rehash(static_cast<std::size_t>(new_cap));  // grows or SHRINKS the bucket array to follow the index space

        int j = 0;
        for (int i = 1; i < next_index_; ++i) {
            if (qty_by_idx_[idx(i)] == 0) continue;
            ++j;
            n_id[idx(j)] = id_by_idx_[idx(i)];
            n_qty[idx(j)] = qty_by_idx_[idx(i)];
            n_cnt[idx(j)] = 1;
            n_sum[idx(j)] = qty_by_idx_[idx(i)];
        }
        for (int i = 1; i <= new_cap; ++i) {  // linear Fenwick build: every node adds itself to its parent
            const int p = i + (i & -i);
            if (p <= new_cap) {
                n_cnt[idx(p)] += n_cnt[idx(i)];
                n_sum[idx(p)] += n_sum[idx(i)];
            }
        }
        for (int k = 1; k <= j; ++k) index_of_.find(n_id[idx(k)])->second = k;  // existing keys only: no allocation
        cnt_ = std::move(n_cnt);
        sum_ = std::move(n_sum);
        id_by_idx_ = std::move(n_id);
        qty_by_idx_ = std::move(n_qty);
        capacity_ = new_cap;
        next_index_ = j + 1;
        ++compactions_;
    }

    int min_capacity_ = 16;
    int capacity_ = 0;  // power of two (0 only in a moved-from object)
    std::vector<int> cnt_;       // Fenwick: live orders
    std::vector<long long> sum_;  // Fenwick: remaining quantity
    std::vector<long long> id_by_idx_;
    std::vector<long long> qty_by_idx_;  // 0 = hole
    int next_index_ = 1;                 // next free index; never reused until compaction
    std::unordered_map<long long, int, detail::IdHash> index_of_;
    long long total_qty_ = 0;
    int compactions_ = 0;
};

}  // namespace oseq
```

* **异常安全**：所有分配（四个新 vector、`rehash`）都在最前面；之后的提交（改 `index_of_` 里已有 key 的值、搬走 vector、改计数）不再分配、不会抛异常。要么什么都没变，要么完整完成。
* **`unordered_map` 不会自己归还桶数组**：删光元素以后 `bucket_count()` 保持不变，只有 `rehash` 才会缩小。所以压缩里 `index_of_.rehash(new_cap)` 让桶数组跟着下标空间一起缩放：

```cpp
// unordered_map keeps its bucket array after erase; only rehash gives it back.
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<long long, int> m;
    m.reserve(100'000);
    for (long long i = 0; i < 100'000; ++i) m.emplace(i, 0);
    for (long long i = 10; i < 100'000; ++i) m.erase(i);
    std::cout << "after erasing down to " << m.size() << " keys: bucket_count = " << m.bucket_count() << "\n";
    m.rehash(64);
    std::cout << "after rehash(64):               bucket_count = " << m.bucket_count() << "\n";
}
```

```text
after erasing down to 10 keys: bucket_count = 100003
after rehash(64):               bucket_count = 64
```

* `index_of_.find(id)->second = k`：只修改已有 key 的值，不插入，所以不分配。

## 6. 复杂度

| 操作 | 时间 |
|---|---|
| `put` | O(log n)，压缩摊还 O(1) |
| `remove` | O(log n) |
| `count_up_to` / `qty_up_to` / `id_at` | O(log n) |
| `entries` | O(容量) |
| 压缩 | O(容量) |

空间 O(容量)；压缩之后容量 ≤ max(初始容量, 约 3 × 活跃订单数)。

## 7. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| `delete` | 方法名 | 关键字：改名 `remove` |
| 异常 | `NoSuchElementException` 等 | `UnknownId`（自定义）、`out_of_range`、`overflow_error`、`invalid_argument` |
| 总量溢出 | `Math.addExact` | `__builtin_add_overflow`（有符号溢出是 UB） |
| 取 2 的幂 | `Integer.highestOneBit(x - 1) << 1` | `std::bit_ceil`（结果装不下是 UB：先检查范围） |
| 查找 | `HashMap.get` 返回 `null` | `find`；`operator[]` 会插入 |
| 哈希 | `HashMap` 会把高位混进低位 | `std::hash<long long>` 恒等；桶数为 2 的幂时只用低位：自己混 |
| 内存回收 | GC | `unordered_map` 的桶数组不会自动缩小：`rehash` |
| 移动 | 引用，无此问题 | 编译器生成的移动构造函数拷贝标量成员：手写，让被搬走的对象是合法的空对象 |
| `int` 参数 | `AT 99999999999` → `NumberFormatException` | `from_chars` 返回 `result_out_of_range`；`+1` 被拒绝 |
| 解析 | `Long.parseLong`（接受 `+5`） | `from_chars`（拒绝 `+5`，必须检查结束指针） |
| 命令类型 | `sealed interface` + `record` | `std::variant` + 小结构体，`std::visit` |
| 异常处理范围 | `catch (A \| B \| C \| D)` | 四个 `catch`；不要 `catch (const std::exception&)` |
| 字符分类 | Unicode | 自己写 ASCII；`std::toupper(char)` 传负数是 UB |

## 8. 陷阱

1. `index_of_[id]` 查询：缺 key 时插入一个默认值。
2. `std::hash<long long>` 恒等 + 2 的幂桶：`i << 32` 的 id 全部冲突。
3. 溢出检查放在 `compact()` 之后：失败的 `put` 也会触发压缩。
4. 编译器生成的移动构造函数：被搬走的对象 `capacity_` 非零但 vector 为空。
5. `std::bit_ceil` 的参数太大（结果超过 `unsigned` 范围）：UB。先检查范围。
6. Fenwick 下标从 0 开始：`0 & -0` 是 0，`i += i & -i` 不前进，死循环。下标必须从 1 开始。
7. 删除后下标被回收：破坏插入顺序。
8. 压缩时直接复制数组：洞没有被消掉，顺序也没重排。
9. 压缩后 `next_index_` 没更新：新订单写进旧位置。
10. `unordered_map` 删光后不 `rehash`：桶数组跟着历史峰值，内存没有回到活跃量。
11. `k < 1` 的判断放在转 `size_t` 之后：负数变成巨大的无符号数，只是碰巧也被拒绝。
12. `catch (const std::exception&)` 把 `bad_alloc` 变成 `ERR`。

## 9. 面试官会追问什么（senior）

**Q1. 为什么不是线段树？** 前缀和 + 单点修改，两者都是 O(log n)；Fenwick 一个数组、循环里只有加法和位运算，常数小、代码短。需要区间最值、区间修改时才上线段树。

**Q2. 为什么不用 `std::map` / 平衡树按序存？** 查询是「按插入顺序的前缀」，key 是顺序而不是 id；平衡树要 order-statistic（子树大小），自己写；Fenwick 是现成的数组。

**Q3. 压缩什么时候触发？为什么摊还 O(1)？** 下标写满时。压缩后至少腾出约 m/2 个空位，下一次压缩前至少 m/2 次 `put`；一次压缩 O(m)。

**Q4. 并发怎么办？** 一把 `std::mutex` 最简单（正确）；读多写少用 `std::shared_mutex`；要读者不阻塞写者，写者每次产生新的不可变快照（但 Fenwick 的更新是原地的，需要持久化结构）；或者单线程 + 命令队列（所有操作排成一个序列，这题本来就是 event-sourcing 的形态）。

**Q5. 压缩期间会卡住吗？怎么避免长停顿？** 一次压缩是 O(容量) 的停顿；可以增量压缩（分批迁移）、或者两个结构交替（新写入进新结构，旧结构后台迁移）。取舍：复杂度 vs 尾延迟。

**Q6. 如果需要「按价格区间」的前缀怎么办？** 把下标换成价格的离散化排名（Fenwick 要求下标有序且稠密），或者用 order-statistic tree。

**Q7. 哈希表怎么选？** `std::unordered_map` 是节点式（每个元素一次分配，引用稳定），id 数量大时缓存不友好；扁平开放寻址表更快但要自己处理删除（墓碑 / 回移）。无论哪种，哈希函数要混合高位。

**Q8. 如果要撤销（undo）呢？** 记录反向操作（`put` ↔ `remove`），或者给每个版本存一份快照（持久化），或者重放日志。

**Q9. 总量溢出时为什么要保证状态不变？** 调用者可以捕获异常继续用对象；半修改的状态（树改了、map 没改）会让后续查询给出错误答案，这是比抛异常更难发现的错误。

## 10. 自测

1. `12 & -12` 是多少？`tree[12]` 管哪个区间？
2. 更新 `a[3]` 要改哪几个节点（n = 8）？
3. 为什么 `std::unordered_map<long long, ...>` 配 `i << 32` 的 id 会很慢？怎么修？
4. `OrderSequence b = std::move(a);` 之后 `a.put(1, 1)` 会怎样？为什么要手写移动构造函数？
5. 为什么失败的 `put` 不能引起一次压缩？代码里是怎么保证的？
6. 压缩的新容量为什么是 `1.5m + 1` 而不是 `m`？
7. 删除订单之后 `unordered_map` 的内存会自动回收吗？

<details><summary>答案</summary>

1. `4`。`tree[12]` 管 `(12 − 4, 12] = (8, 12]`，即下标 9..12。
2. `tree[3]`、`tree[4]`、`tree[8]`：`3 → 3 + 1 = 4 → 4 + 4 = 8 → 8 + 8 = 16 > 8` 结束。
3. `std::hash<long long>` 恒等，桶号只用低位（2 的幂桶数时）；`i << 32` 的低 32 位全是 0，全部落进同一个桶，查找退化成线性扫描。自己提供混合哈希（splitmix64）。
4. 编译器生成的移动构造函数搬走 vector 但拷贝 `capacity_` / `next_index_`：`a` 声称下标空间是满的却没有存储，`put` 会越界写。手写后 `a` 是合法的空序列，`capacity_ = 0`，第一次 `put` 触发压缩，重新分配。
5. 失败的操作不应当有任何可见的副作用（包括 `compactions()` 和容量）。所有会抛异常的检查（`qty`、重复、溢出）都排在 `compact()` 之前；压缩本身是行为保持的，之后唯一可能失败的 `try_emplace` 在任何其他修改之前。
6. 只有 `m` 时压缩后立刻又满，下一次 `put` 又压缩，每次 `put` 都是 O(m)；`1.5m + 1` 保证至少腾出约 m/2 个空位，压缩的 O(m) 成本摊到至少 m/2 次 `put` 上，每次 O(1)。
7. 不会。`erase` 不改桶数；只有 `rehash`（或销毁容器）才会缩小桶数组。所以压缩里要 `rehash(new_cap)`。

</details>
