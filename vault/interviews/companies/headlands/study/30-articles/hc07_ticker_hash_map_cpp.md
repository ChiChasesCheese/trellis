# hc07 · 股票代码哈希表（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。下面所有代码块按顺序拼起来就是一份能编译、能通过全部测试的完整实现。

## 1. 题目

行情系统里到处是「按股票代码（ticker）累加 / 查找」：每个 ticker 的累计成交量、最新价、持仓……每秒几百万次。面试官的问题是：**用 `std::unordered_map<std::string, long long>` 能做，如果 key 是股票代码，你还能做得更好吗？** 股票代码的结构很特别：**至多 8 个大写 ASCII 字母**（`AAPL`、`MSFT`）。这个结构就是突破口。

| Part | 内容 |
|---|---|
| 1 | 自己写一个开放寻址 + 线性探测的哈希表（key 是字符串，value 是 `long long`）：`put`/`get`/`add`/`remove`，墓碑，扩容；1024 个哈希值**完全相同**的 key 也必须正确 |
| 2 | 把代码**打包进一个 `uint64_t`**（每个字母 5 比特），key 变成整数，不分配、不比较字符串；报文里 8 字节的代码字段直接解析；`LongTickerMap` 稳态下 `add`/`get` 零分配 |
| 3 | 开盘前就知道全部代码 → **最小完美哈希**：零冲突，value 放进长度恰好 n 的数组；订阅时缓存下标，之后每条消息直接 `add_at(下标)` |
| 4 | 一块 64 字节对齐、定长、一次分配的表（`FixedTickerMap`）；以及：**你怎么知道它更快** |

## 2. Part 1：手写开放寻址哈希表

### 2.1 从零理解哈希表

* **哈希函数**把 key 变成一个整数；表是一个数组，key 的「家」（home slot）是 `hash(key)` 对容量取模（或移位）的结果。
* **冲突**（collision）：两个 key 的家相同。两种处理：
  * **链地址法**（chaining）：每个格子挂一条链表。`std::unordered_map` 就是这样——**每个条目一个单独分配的节点**，查找要追指针（pointer chasing），每个条目几十字节，缓存不友好。
  * **开放寻址**（open addressing）：所有条目直接放在数组里；家被占了就看下一格（**线性探测**，linear probing），直到找到它自己或碰到空格。数组连续，缓存友好，没有逐条目分配。
* **装载因子**（load factor）= 已用格子 / 容量。越高探测越长。本题要求（占用 + 墓碑）/ 容量 ≤ 3/4，实现里在 ≤ 1/2 时扩容；容量取 2 的幂，翻倍扩容，均摊 O(1)。
* **删除为什么要留墓碑**（tombstone）。设 A、B 的家都是第 5 格，A 在 5，B 被挤到 6：

```
格子:   4   5   6   7
内容:       A   B
删除 A，如果直接置空:   4   5   6
                           .   B      ← 查 B：从 5 出发，碰到空格，结论「B 不存在」。错！
删除 A，放墓碑:           x   B      ← 墓碑「过去有人」：探测继续，找到 B。
```

  墓碑也占用探测链，所以装载因子要把墓碑算进去；扩容（rehash）时只搬活条目，墓碑自动消失。反复「插入新 key、删旧 key」时，表不会被墓碑撑大，也不会满到没有空格而死循环。

### 2.2 `std::hash` 的陷阱，和 Fibonacci hashing

`std::hash<std::string_view>` 对字符串是个正常的哈希函数；但 `std::hash<整数>` 在 libc++ 和 libstdc++ 里是**恒等函数**。下标写成 `hash & mask` 时只用了 key 的低位——打包后的股票代码低位全是补的 0：

```cpp
// std::hash<integer> is (in libc++ and libstdc++) the identity, so `hash & mask` keeps only the low bits of the key.
// A packed ticker has zeros there.  Simulate linear probing for the 17576 three-letter codes.
#include <cstdint>
#include <functional>
#include <iostream>
#include <vector>

using Key = std::uint64_t;

Key pack3(char a, char b, char c) {  // 5 bits per letter, first letter in bits 35..39: the low 25 bits stay 0
    auto code = [](char ch) { return static_cast<Key>(ch - 'A' + 1); };
    return (code(a) << 35) | (code(b) << 30) | (code(c) << 25);
}

template <class Index>
std::size_t longest_probe(const std::vector<Key>& keys, std::size_t capacity, Index index) {
    std::vector<std::uint8_t> used(capacity, 0);
    std::size_t worst = 0;
    for (Key k : keys) {
        const std::size_t home = index(k);
        std::size_t i = home;
        while (used[i]) i = (i + 1) & (capacity - 1);
        used[i] = 1;
        worst = std::max(worst, (i - home) & (capacity - 1));
    }
    return worst;
}

int main() {
    std::vector<Key> keys;
    for (char a = 'A'; a <= 'Z'; ++a)
        for (char b = 'A'; b <= 'Z'; ++b)
            for (char c = 'A'; c <= 'Z'; ++c) keys.push_back(pack3(a, b, c));

    constexpr std::size_t capacity = 1 << 16;
    constexpr int shift = 64 - 16;
    std::cout << "std::hash<uint64_t>(42) = " << std::hash<std::uint64_t>{}(42) << "   (the identity)\n";
    std::cout << "17576 codes, capacity " << capacity << ", longest probe:\n";
    std::cout << "  std::hash & mask     : " << longest_probe(keys, capacity, [](Key k) { return std::hash<Key>{}(k) & (capacity - 1); }) << "\n";
    std::cout << "  (key * golden) >> 48 : " << longest_probe(keys, capacity, [](Key k) { return static_cast<std::size_t>((k * 0x9E3779B97F4A7C15ull) >> shift); }) << "\n";
}
```

所以表自己再混一次：**Fibonacci hashing**，`(h * 2^64/φ) >> (64 - log2(容量))`。乘一个奇数常数，让输入的**每一位**都影响高位，再取**高位**。这样即使 `Hash` 很差（本题的测试会塞一个对所有 key 返回同一个值的哈希），表也只是变慢，不会出错。

### 2.3 代码

```cpp
#include <algorithm>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <functional>
#include <memory>
#include <new>
#include <optional>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <variant>
#include <vector>
namespace tickers {
```

```cpp
/// Open addressing + linear probing over one std::vector<Slot>.  A slot is Empty (never used: a probe stops here),
/// Full, or Tomb (deleted: a probe must go on).  (full + tombs) / capacity <= 1/2 after every insert.
/// `Hash` hashes the key text; the table mixes it again (Fibonacci hashing), so even a poor Hash stays correct.
template <class Hash = std::hash<std::string_view>>
class BasicTickerMap {
public:
    explicit BasicTickerMap(std::size_t expected_size = 0, Hash hash = {}) : hash_(std::move(hash)) {
        allocate(capacity_for(expected_size, 2, std::size_t{1} << 30));
    }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return slots_.size(); }
    std::size_t tombstones() const noexcept { return tombs_; }

    bool contains(std::string_view key) const { return locate(key).found; }

    std::optional<long long> get(std::string_view key) const {
        const Probe p = locate(key);
        if (!p.found) return std::nullopt;
        return slots_[p.index].value;
    }

    /// Returns the previous value, if any.
    std::optional<long long> put(std::string_view key, long long value) {
        const Probe p = locate(key);
        if (p.found) return std::exchange(slots_[p.index].value, value);
        insert_new(p.index, key, value);
        return std::nullopt;
    }

    /// value += delta (a missing key counts as 0); returns the new value.  Overflow: std::overflow_error, table unchanged.
    long long add(std::string_view key, long long delta) {
        const Probe p = locate(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);  // computed first, stored after
        insert_new(p.index, key, delta);
        return delta;
    }

    std::optional<long long> remove(std::string_view key) {
        const Probe p = locate(key);
        if (!p.found) return std::nullopt;
        Slot& s = slots_[p.index];
        const long long old = s.value;
        s.state = State::Tomb;  // NOT Empty: a key that was pushed past this slot would become unreachable
        s.key.clear();
        s.value = 0;
        --size_;
        ++tombs_;
        return old;
    }

    template <class F>
    void for_each(F&& f) const {
        for (const Slot& s : slots_)
            if (s.state == State::Full) f(std::string_view(s.key), s.value);
    }

    /// Distance of the farthest live key from its home slot (0 = every key sits at home).
    std::size_t max_probe_length() const {
        std::size_t worst = 0;
        for (std::size_t i = 0; i < slots_.size(); ++i)
            if (slots_[i].state == State::Full) worst = std::max(worst, (i - home(slots_[i].key)) & mask_);
        return worst;
    }
```

要点：

* `add_checked`：`__builtin_add_overflow` 检查溢出。**有符号溢出在 C++ 里是 UB**，不能写 `a + b < a` 之类事后检查；先算（并检查），后写，溢出时表保持原样。
* `Slot` 里的 key 是 `std::string`。**短字符串优化**（SSO）：不超过 15 个字符的 `std::string` 把字符存在对象内部，不分配堆内存——股票代码（≤ 8 个字符）插入时零分配；参数用 `std::string_view`，查找时也不会为了比较而构造临时 `std::string`：

```cpp
// Short std::strings live inside the string object (small-string optimisation): no heap allocation.
// A std::string_view parameter avoids the temporary std::string a `const std::string&` parameter would need.
#include <cstdlib>
#include <iostream>
#include <new>
#include <string>
#include <string_view>

static std::size_t g_news = 0;
void* operator new(std::size_t n) {
    ++g_news;
    if (void* p = std::malloc(n ? n : 1)) return p;
    throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

std::size_t length_by_ref(const std::string& s) { return s.size(); }
std::size_t length_by_view(std::string_view s) { return s.size(); }

int main() {
    std::size_t before = g_news;
    { std::string ticker("AAPL"); (void)ticker; }
    std::cout << "std::string(\"AAPL\"):             " << g_news - before << " allocations\n";

    before = g_news;
    { std::string long_key(40, 'X'); (void)long_key; }
    std::cout << "std::string of 40 characters:    " << g_news - before << " allocation\n";

    const char* literal = "this literal is longer than the small buffer of a std::string";
    before = g_news;
    (void)length_by_ref(literal);  // builds a temporary std::string from the literal
    std::cout << "const std::string& parameter:    " << g_news - before << " allocation\n";
    before = g_news;
    (void)length_by_view(literal);
    std::cout << "std::string_view parameter:      " << g_news - before << " allocations\n";
}
```

* `Probe locate(key)`：一次探测同时回答「找到了吗」和「没找到的话该插在哪」（探测路上的第一个墓碑，否则终点的空格），查找、插入、`add` 共用。
* `capacity_for` 在 `entries * load_inverse` 乘法之前先除法检查上限，所以参数是 `size_t(-1)` 时抛 `std::length_error`，而不是溢出后分配一个很小的表。

```cpp
private:
    enum class State : std::uint8_t { Empty, Full, Tomb };
    struct Slot {
        std::string key;  // <= 15 chars live inside the string object (small-string optimisation): no allocation
        long long value = 0;
        State state = State::Empty;
    };
    struct Probe {
        std::size_t index;  // found: the key's slot.  Otherwise: where to insert (first tombstone on the way, else the empty slot)
        bool found;
    };

    std::size_t home(std::string_view key) const { return static_cast<std::size_t>((std::uint64_t{hash_(key)} * GOLDEN) >> shift_); }

    Probe locate(std::string_view key) const {
        std::size_t i = home(key);
        std::optional<std::size_t> first_tomb;
        for (;;) {  // terminates: the load factor keeps empty slots around
            const Slot& s = slots_[i];
            if (s.state == State::Empty) return {first_tomb.value_or(i), false};
            if (s.state == State::Tomb) {
                if (!first_tomb) first_tomb = i;
            } else if (s.key == key) {
                return {i, true};
            }
            i = (i + 1) & mask_;
        }
    }

    void insert_new(std::size_t i, std::string_view key, long long value) {
        if (slots_[i].state == State::Tomb) {
            slots_[i].key.assign(key);  // may allocate for long keys: do it before touching the counters
            --tombs_;
        } else {
            if ((size_ + tombs_ + 1) * 2 > slots_.size()) {  // taking an empty slot would use more than half of the table
                rehash();
                i = home(key);
                while (slots_[i].state != State::Empty) i = (i + 1) & mask_;
            }
            slots_[i].key.assign(key);
        }
        slots_[i].value = value;
        slots_[i].state = State::Full;
        ++size_;
    }

    /// Rebuild with capacity >= 4 * live entries.  Tombstones disappear, so insert/delete churn cannot bloat the table.
    void rehash() {
        std::vector<Slot> old = std::move(slots_);
        allocate(capacity_for(size_, 4, std::size_t{1} << 30));
        for (Slot& s : old) {
            if (s.state != State::Full) continue;
            std::size_t i = home(s.key);
            while (slots_[i].state != State::Empty) i = (i + 1) & mask_;
            slots_[i] = std::move(s);
        }
        // allocate() reset the counters; the live entries were re-inserted
    }

    void allocate(std::size_t cap) {
        const std::size_t live = size_;
        slots_ = std::vector<Slot>(cap);
        mask_ = cap - 1;
        shift_ = 64 - std::countr_zero(cap);
        tombs_ = 0;
        size_ = live;
    }

    Hash hash_;
    std::vector<Slot> slots_;
    std::size_t size_ = 0, tombs_ = 0, mask_ = 0;
    int shift_ = 0;
};

using TickerMap = BasicTickerMap<>;
```

* 插入前检查 `(size + tombs + 1) * 2 > capacity`：占用一个空格会让「已用格子」超过一半，就先 `rehash()`。重用墓碑不增加已用格子，不需要检查。
* `rehash()` 新容量按**活条目数**的 4 倍算：纯插入场景恰好翻倍；墓碑很多时容量甚至会缩小。
* `slots_[i].key.assign(key)` 可能分配（长 key），所以放在改计数器之前。

## 3. Part 2：打包进一个 `uint64_t`

### 3.1 编码

26 个字母只需要 5 比特（2⁵ = 32），8 个字母 = 40 比特，一个 `uint64_t` 绰绰有余。`'A'..'Z'` → `1..26`（0 留给「没有字符」），第 i 个字符放在第 `[35−5i, 39−5i]` 比特，不足 8 个的尾部补 0：

```
"AAPL" -> 00001 00001 10000 01100 00000 00000 00000 00000      (从高位到低位)
       =  (1<<35) | (1<<30) | (16<<25) | (12<<20)
```

性质：不同代码 → 不同的数（单射）；合法代码恒 > 0 且 < 2⁴⁰，所以 **0 可以当哈希表的「空格」，`~0`（全 1）可以当「墓碑」**；比较两个代码 = 比较两个整数。

### 3.2 `codec`

```cpp
/// 1..8 uppercase ASCII letters packed into the low 40 bits of a uint64_t: A..Z = 1..26, 5 bits per letter, the first
/// letter in the highest field, unused trailing fields 0.  "AAPL" = (1<<35) | (1<<30) | (16<<25) | (12<<20).
namespace codec {

inline constexpr int MAX_LEN = 8;
inline constexpr int BITS = 5;
inline constexpr Key FIELD_MASK = 0x1F;

enum class Error { Empty, TooLong, BadChar };
constexpr const char* what(Error e) {
    switch (e) {
        case Error::Empty: return "empty ticker";
        case Error::TooLong: return "ticker longer than 8 characters";
        case Error::BadChar: return "not an uppercase ASCII letter";
    }
    return "?";
}
struct Ticker {
    Key key;
    friend bool operator==(const Ticker&, const Ticker&) = default;
};
struct Invalid {
    Error error;
    std::size_t position;  // index of the offending character
    friend bool operator==(const Invalid&, const Invalid&) = default;
};
/// Bad input is routine on a market-data feed, so parse() reports it as a value; pack() throws.
using Parsed = std::variant<Ticker, Invalid>;

constexpr Parsed parse(std::string_view s) noexcept {
    if (s.empty()) return Invalid{Error::Empty, 0};
    if (s.size() > static_cast<std::size_t>(MAX_LEN)) return Invalid{Error::TooLong, MAX_LEN};
    Key key = 0;
    for (std::size_t i = 0; i < s.size(); ++i) {
        const auto c = static_cast<unsigned char>(s[i]);  // plain `char` may be signed: bytes >= 0x80 would compare as negative
        if (c < 'A' || c > 'Z') return Invalid{Error::BadChar, i};
        key |= static_cast<Key>(c - 'A' + 1) << (BITS * (MAX_LEN - 1 - static_cast<int>(i)));  // widen BEFORE shifting
    }
    return Ticker{key};
}

constexpr Key pack(std::string_view s) {
    const Parsed p = parse(s);
    if (const auto* t = std::get_if<Ticker>(&p)) return t->key;
    throw std::invalid_argument(what(std::get<Invalid>(p).error));
}

constexpr bool is_valid_key(Key key) noexcept {
    if (key == 0 || (key >> (BITS * MAX_LEN)) != 0) return false;
    bool ended = false;
    for (int i = 0; i < MAX_LEN; ++i) {
        const Key f = (key >> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
        if (f > 26) return false;
        if (f == 0) ended = true;
        else if (ended) return false;  // no letter after a 0 field
    }
    return true;
}

inline std::string unpack(Key key) {
    if (!is_valid_key(key)) throw std::invalid_argument("not a packed ticker: " + std::to_string(key));
    std::string s;
    for (int i = 0; i < MAX_LEN; ++i) {
        const Key f = (key >> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
        if (f == 0) break;
        s.push_back(static_cast<char>('A' + f - 1));
    }
    return s;
}
```

* **`char` 可能是有符号的。** UTF-8 的字节 `0xC3` 作为 `char` 是负数，`c < 'A'` 为真。所以先转 `unsigned char` 再比较。
* **先转宽再移位**：`static_cast<Key>(c - 'A' + 1) << 35`。`(c - 'A' + 1) << 35` 是 `int` 移位，移位量超过 31 是 UB。
* **`std::string_view` 里可以有 `'\0'`**：`std::string_view("AB\0CD", 5)` 是 5 个字节，其中一个是 NUL → 非法；而 `std::string_view("AB\0CD")` 从字符串字面量构造，长度是 2，得到 `"AB"`。
* `parse` 把「非法」当成返回值（`std::variant<Ticker, Invalid>`）：行情流里非法输入是常态，不该靠异常；`pack` 才抛。`parse`、`pack` 都是 `constexpr`，可以在编译期求值：

```cpp
// pack() and parse() are constexpr: a ticker literal is packed at compile time, and a bad literal is a compile error.
#include <iostream>

#include "../../../../loop/rounds/01_video/hc07_ticker_hash_map/cpp/reference.hpp"

using namespace tickers;

constexpr Key AAPL = codec::pack("AAPL");  // evaluated by the compiler
static_assert(AAPL == ((1ull << 35) | (1ull << 30) | (16ull << 25) | (12ull << 20)));
static_assert(codec::is_valid_key(AAPL));
static_assert(std::holds_alternative<codec::Invalid>(codec::parse("BRK.B")));  // invalid input is just a value
// constexpr Key bad = codec::pack("BRK.B");   // does not compile: the throw is reached during constant evaluation

int main() {
    LongTickerMap volume;
    volume.add(AAPL, 100);
    volume.add(AAPL, 50);
    std::cout << codec::unpack(AAPL) << " -> " << volume.get(AAPL, 0) << "\n";
}
```

```cpp
/// Ticker field of a wire message: 8 bytes, uppercase letters, right-padded with spaces ("AAPL    ").
/// Invalid (blank, leading/inner space, lowercase, NUL, non-letter) -> std::invalid_argument.
/// Does not fit in the buffer -> std::out_of_range.  The low 5 bits of a letter are exactly its code (0x41 -> 1 ... 0x5A -> 26)
/// and the low 5 bits of a space are 0, so the packed value is just the low 5 bits of every byte laid side by side.
inline Key pack_wire(std::span<const std::byte> buf, std::size_t off) {
    if (buf.size() < 8 || off > buf.size() - 8)  // `off + 8 > size` would wrap around for a huge off
        throw std::out_of_range("ticker field does not fit in the buffer");
    std::uint64_t word;
    std::memcpy(&word, buf.data() + off, 8);  // no aliasing or alignment problem, and the compiler emits one load
    if constexpr (std::endian::native == std::endian::little) word = __builtin_bswap64(word);  // byte 0 -> most significant
    if ((word >> 56) == ' ') throw std::invalid_argument("empty ticker field");
    bool seen_space = false;
    Key key = 0;
    for (int i = 0; i < MAX_LEN; ++i) {
        const auto b = static_cast<unsigned>((word >> (8 * (MAX_LEN - 1 - i))) & 0xFF);
        if (b == ' ') seen_space = true;
        else if (seen_space || b < 'A' || b > 'Z') throw std::invalid_argument("bad ticker field at byte " + std::to_string(i));
        key |= static_cast<Key>(b & FIELD_MASK) << (BITS * (MAX_LEN - 1 - i));
    }
    return key;
}

}  // namespace codec
```

行情报文里的代码字段是 8 个字节、右侧补空格（`"AAPL    "`）。字母 `0x41..0x5A` 的低 5 位恰好是 1..26，空格 `0x20` 的低 5 位恰好是 0——和编码天然吻合，所以每个字节取低 5 位并排放好就是结果（x86 的 BMI2 有一条 `pext` 指令可以一次完成这件事）。三个陷阱：

```cpp
// Three traps when reading a fixed-width field from a byte buffer.
#include <bit>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <iostream>

int main() {
    // 1. plain `char` is signed here: a UTF-8 byte compares as a NEGATIVE number and slips through a range check
    const char e_acute = static_cast<char>(0xC3);
    std::cout << "(char)0xC3 < 'A'            : " << std::boolalpha << (e_acute < 'A') << "   (true: negative)\n";
    std::cout << "(unsigned char)0xC3 > 'Z'   : " << (static_cast<unsigned char>(e_acute) > 'Z') << "\n";

    // 2. `off + 8 > size` wraps around for a huge offset; `off > size - 8` (after size >= 8) does not
    const std::size_t size = 8, off = static_cast<std::size_t>(-1) - 3;
    std::cout << "off + 8 = " << (off + 8) << ", so `off + 8 > size` is " << (off + 8 > size) << "   (the huge offset passes!)\n";
    std::cout << "size >= 8 && off > size - 8 : " << (size >= 8 && off > size - 8) << "   (rejected)\n";

    // 3. load 8 bytes with memcpy (no aliasing / alignment problem), then fix the byte order: the first byte of the
    //    field must become the most significant byte
    const unsigned char field[8] = {'A', 'A', 'P', 'L', ' ', ' ', ' ', ' '};
    std::uint64_t word;
    std::memcpy(&word, field, 8);
    if constexpr (std::endian::native == std::endian::little) word = __builtin_bswap64(word);
    std::cout << "first byte after the swap   : " << static_cast<char>(word >> 56) << "\n";
}
```

* 读 8 字节用 `memcpy`（没有别名和对齐问题，编译器会优化成一次 load），再把字节序转成「第一个字节是最高位」。
* 边界检查写成 `off > size - 8`（先保证 `size >= 8`）：`off + 8 > size` 在 `off` 很大时会回绕。

### 3.3 `LongTickerMap`

```cpp
/// Key = packed ticker (anything but 0 and ~0), value = long long.  Open addressing, linear probing, tombstones, one
/// std::vector<Slot> of 16-byte {key, value} pairs: a probe that finds the key has the value in the same cache line.
/// In steady state add()/get() allocate nothing.
class LongTickerMap {
public:
    explicit LongTickerMap(std::size_t expected_size = 0) { allocate(capacity_for(expected_size, 2, std::size_t{1} << 29)); }

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return slots_.size(); }
    std::size_t tombstones() const noexcept { return tombs_; }

    bool contains(Key key) const {
        check(key);
        return locate(key).found;
    }

    long long get(Key key, long long if_absent) const {
        check(key);
        const Probe p = locate(key);
        return p.found ? slots_[p.index].value : if_absent;
    }

    /// true = new key, false = overwrote.
    bool put(Key key, long long value) {
        check(key);
        const Probe p = locate(key);
        if (p.found) {
            slots_[p.index].value = value;
            return false;
        }
        insert_new(p.index, key, value);
        return true;
    }

    /// value += delta (a missing key counts as 0).  Overflow: std::overflow_error, value unchanged.
    long long add(Key key, long long delta) {
        check(key);
        const Probe p = locate(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);
        insert_new(p.index, key, delta);
        return delta;
    }

    bool remove(Key key) {
        check(key);
        const Probe p = locate(key);
        if (!p.found) return false;
        slots_[p.index] = {TOMB, 0};
        --size_;
        ++tombs_;
        return true;
    }

    template <class F>
    void for_each(F&& f) const {
        for (const Slot& s : slots_)
            if (s.key != EMPTY && s.key != TOMB) f(s.key, s.value);
    }

    std::size_t max_probe_length() const {
        std::size_t worst = 0;
        for (std::size_t i = 0; i < slots_.size(); ++i)
            if (slots_[i].key != EMPTY && slots_[i].key != TOMB) worst = std::max(worst, (i - home(slots_[i].key)) & mask_);
        return worst;
    }
```

和 `TickerMap` 同一个思路，区别：

* 比较就是 `==`，没有字符串；**稳态下 `add`/`get` 零分配**（测试用重载 `operator new` 数分配次数）。
* 槽位是 16 字节 `{key, value}`：一次探测读到 key 的同时 value 已经在同一条缓存行里（64 字节 = 4 个槽位）。
* 合法 key 是 `1 .. 2⁶⁴−2`；`0` 是空格、`~0` 是墓碑。**`-1` 隐式转成 `uint64_t` 就是 `~0`**：`put(-1, ...)` 能编译，但会被当成非法 key 拒绝（测试里钉住了这件事）。
* **哈希不能写成 `key & mask`。** `home()` 乘 `GOLDEN` 取高位。

```cpp
private:
    struct Slot {
        Key key;
        long long value;
    };
    struct Probe {
        std::size_t index;
        bool found;
    };

    static void check(Key key) {
        if (key == EMPTY || key == TOMB) throw std::invalid_argument("key must not be 0 or ~0 (empty / tombstone marker)");
    }

    // Never `key & mask`: a packed short ticker has zeros in its low bits.  And std::hash<uint64_t> is the identity.
    std::size_t home(Key key) const noexcept { return static_cast<std::size_t>((key * GOLDEN) >> shift_); }

    Probe locate(Key key) const noexcept {
        std::size_t i = home(key);
        std::optional<std::size_t> first_tomb;
        for (;;) {
            const Key k = slots_[i].key;
            if (k == key) return {i, true};
            if (k == EMPTY) return {first_tomb.value_or(i), false};
            if (k == TOMB && !first_tomb) first_tomb = i;
            i = (i + 1) & mask_;
        }
    }

    void insert_new(std::size_t i, Key key, long long value) {
        if (slots_[i].key == TOMB) {
            --tombs_;
        } else if ((size_ + tombs_ + 1) * 2 > slots_.size()) {
            rehash();
            i = home(key);
            while (slots_[i].key != EMPTY) i = (i + 1) & mask_;
        }
        slots_[i] = {key, value};
        ++size_;
    }

    void rehash() {
        std::vector<Slot> old = std::move(slots_);
        allocate(capacity_for(size_, 4, std::size_t{1} << 29));
        for (const Slot& s : old) {
            if (s.key == EMPTY || s.key == TOMB) continue;
            std::size_t i = home(s.key);
            while (slots_[i].key != EMPTY) i = (i + 1) & mask_;
            slots_[i] = s;
        }
    }

    void allocate(std::size_t cap) {
        slots_.assign(cap, Slot{EMPTY, 0});
        mask_ = cap - 1;
        shift_ = 64 - std::countr_zero(cap);
        tombs_ = 0;
    }

    std::vector<Slot> slots_;
    std::size_t size_ = 0, tombs_ = 0, mask_ = 0;
    int shift_ = 0;
};
```

## 4. Part 3：完美哈希

### 4.1 想法

开盘前就知道今天会出现的全部代码（比如 8000 个），盘中只会查这些代码。既然 key 集合固定，可以花一点启动时间「找一个对这批 key 完全没有冲突的哈希函数」：

* **完美**（perfect）：任意两个 key 的结果不同，查询是确定的 O(1)，没有探测循环；
* **最小**（minimal）：n 个 key 恰好映射到 `0..n−1`，value 放进一个长度正好 n 的紧凑数组。

算法：**hash-and-displace**（CHD 的简化）。

1. 把 key 按 `bucket(h)` 分到 r ≈ n/4 个桶里（每桶平均 4 个 key）；
2. **从大桶到小桶**处理：对一个桶，找一个位移 `d`，使得桶里每个 key 的 `slot(h, d)` 都落在**没被占用、且互不相同**的格子里（试 d = 0, 1, 2, …）；
3. 只有 1 个 key 的桶最后处理：直接给它下一个空格子，位移里存 `~slot`（负数表示「直接指定」）。

查询：`h = hash(key)`；`d = disp[bucket(h)]`；`slot = d < 0 ? ~d : slot(h, d)`；然后**必须校验 `keys[slot] == key`**——完美哈希只保证「集合内的 key」不冲突，集合外的 key 也会被映射到某个格子。

### 4.2 `SymbolIndex`

```cpp
/// Minimal perfect hash (hash-and-displace, a simplified CHD): the n keys of a fixed universe map one-to-one onto 0..n-1.
/// 1. split the keys into ~n/4 buckets by hash; 2. largest bucket first, find a displacement d that sends every key of the
/// bucket to a free slot; 3. single-key buckets last: take the next free slot (stored as ~slot, a negative number).
/// index_of() must compare the stored key: a key outside the universe still hashes to SOME slot.
class SymbolIndex {
public:
    static constexpr int NPOS = -1;

    /// Keys must be unique and not 0 / ~0, else std::invalid_argument.  The universe may be empty.
    static SymbolIndex build(std::span<const Key> universe) {
        for (Key k : universe)
            if (k == EMPTY || k == TOMB) throw std::invalid_argument("key must not be 0 or ~0");
        std::vector<Key> sorted(universe.begin(), universe.end());
        std::sort(sorted.begin(), sorted.end());
        if (std::adjacent_find(sorted.begin(), sorted.end()) != sorted.end()) throw std::invalid_argument("duplicate key");
        if (universe.empty()) return SymbolIndex({}, {}, 0);
        for (int seed = 0; seed < MAX_SEEDS; ++seed)
            if (auto built = try_build(universe, seed)) return std::move(*built);
        throw std::runtime_error("no perfect hash found");
    }

    std::size_t size() const noexcept { return keys_.size(); }

    /// Index of `key` in 0..size()-1, or NPOS if it is not in the universe.
    int index_of(Key key) const noexcept {
        if (keys_.empty()) return NPOS;
        const std::uint64_t h = hash(key, seed_);
        const std::int32_t d = disp_[bucket(h, disp_.size())];
        const std::size_t s = d < 0 ? static_cast<std::size_t>(~d) : slot(h, d, keys_.size());
        return keys_[s] == key ? static_cast<int>(s) : NPOS;
    }

    Key key_at(std::size_t index) const { return keys_.at(index); }

private:
    static constexpr int MAX_SEEDS = 64;
    static constexpr int MAX_DISPLACEMENT = 1 << 22;

    SymbolIndex(std::vector<Key> keys, std::vector<std::int32_t> disp, int seed)
        : keys_(std::move(keys)), disp_(std::move(disp)), seed_(seed) {}

    // splitmix64 finalizer: a bijection with good avalanche, so keys differing in one letter get unrelated hashes
    static std::uint64_t mix(std::uint64_t z) noexcept {
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBull;
        return z ^ (z >> 31);
    }
    static std::uint64_t hash(Key key, int seed) noexcept { return mix(key ^ (static_cast<std::uint64_t>(seed) * GOLDEN)); }
    /// Map a 32-bit value into [0, range) with a multiply and a shift instead of a division (Lemire's fastrange).
    static std::size_t bucket(std::uint64_t h, std::size_t r) noexcept { return static_cast<std::size_t>(((h >> 32) * r) >> 32); }
    /// Candidate slot number d.  Mixing d in (instead of adding d * c) makes the candidates behave independently.
    static std::size_t slot(std::uint64_t h, std::int32_t d, std::size_t m) noexcept {
        const std::uint64_t x = (h ^ (static_cast<std::uint64_t>(d) * GOLDEN)) * 0xD6E8FEB86659FD93ull;
        return static_cast<std::size_t>(((x >> 32) * m) >> 32);
    }
```

* `mix` 是 splitmix64 的终结函数：双射、雪崩性好，只差一个字母的 key 输出完全不同。
* `bucket` 用乘法加移位把 32 位数缩到 `[0, r)`（Lemire 的 fastrange），不用除法。
* `slot(h, d, m)`：把 `d` **搅进** `h` 再乘一个大奇数，而不是 `h + d * c`。后者让桶里两个 key 的格子差永远固定，小表上可能永远放不进去。
* 失败的种子不会死循环：位移上限 `2²²`，种子上限 64，超了就换种子 / 抛异常。

```cpp
    static std::optional<SymbolIndex> try_build(std::span<const Key> universe, int seed) {
        const std::size_t n = universe.size();
        const std::size_t r = std::max<std::size_t>(1, (n + 3) / 4);
        std::vector<std::uint64_t> h(n);
        std::vector<std::size_t> start(r + 1, 0);
        for (std::size_t i = 0; i < n; ++i) {
            h[i] = hash(universe[i], seed);
            ++start[bucket(h[i], r) + 1];
        }
        for (std::size_t b = 0; b < r; ++b) start[b + 1] += start[b];  // counting sort: bucket b = members[start[b] .. start[b+1])
        std::vector<std::size_t> fill(start.begin(), start.end() - 1), members(n);
        for (std::size_t i = 0; i < n; ++i) members[fill[bucket(h[i], r)]++] = i;
        std::vector<std::uint64_t> order(r);  // (size << 32 | bucket): sorting puts the biggest buckets last
        for (std::size_t b = 0; b < r; ++b) order[b] = ((start[b + 1] - start[b]) << 32) | b;
        std::sort(order.begin(), order.end());

        std::vector<Key> slot_keys(n, EMPTY);
        std::vector<std::uint8_t> used(n, 0);  // not vector<bool>
        std::vector<std::int32_t> disp(r, 0);
        std::vector<std::size_t> tmp(n);
        std::size_t cursor = 0;
        for (std::size_t idx = r; idx-- > 0;) {
            const std::size_t b = order[idx] & 0xFFFFFFFFull;
            const std::size_t from = start[b], to = start[b + 1], size = to - from;
            if (size == 0) continue;
            if (size == 1) {
                while (used[cursor]) ++cursor;
                used[cursor] = 1;
                slot_keys[cursor] = universe[members[from]];
                disp[b] = ~static_cast<std::int32_t>(cursor);
                continue;
            }
            bool placed = false;
            for (std::int32_t d = 0; d < MAX_DISPLACEMENT && !placed; ++d) {
                std::size_t ok = 0;
                for (std::size_t p = from; p < to; ++p) {
                    const std::size_t s = slot(h[members[p]], d, n);
                    if (used[s]) break;
                    used[s] = 1;  // claim at once, so two keys of the same bucket landing on one slot are noticed
                    tmp[ok++] = s;
                }
                if (ok == size) {
                    for (std::size_t p = 0; p < size; ++p) slot_keys[tmp[p]] = universe[members[from + p]];
                    disp[b] = d;
                    placed = true;
                } else {
                    for (std::size_t p = 0; p < ok; ++p) used[tmp[p]] = 0;  // roll back, try the next d
                }
            }
            if (!placed) return std::nullopt;  // this seed failed: the caller tries the next one
        }
        return SymbolIndex(std::move(slot_keys), std::move(disp), seed);
    }

    std::vector<Key> keys_;           // keys_[slot] = the key assigned to that slot
    std::vector<std::int32_t> disp_;  // per bucket: displacement d, or ~slot for single-key buckets
    int seed_ = 0;
};
```

* `used` 是 `vector<uint8_t>`，不是 `vector<bool>`（位压缩的代理容器：不能取引用、不能取地址，相邻的位共用一个字节，多线程写会冲突）：

```cpp
// std::vector<bool> is a bit-packed container of proxies, not a vector of bool.
#include <cstdint>
#include <iostream>
#include <type_traits>
#include <vector>

int main() {
    std::vector<bool> bits(8);
    std::vector<std::uint8_t> bytes(8);
    static_assert(!std::is_same_v<decltype(bits[0]), bool&>);     // a proxy object, returned by value
    static_assert(std::is_same_v<decltype(bytes[0]), std::uint8_t&>);
    // auto& first = bits[0];     // does not compile: cannot bind a reference to a temporary proxy
    // bool* p = &bits[0];        // does not compile: no address
    std::cout << "sizeof(bits[0]) = " << sizeof(bits[0]) << " bytes (the proxy), sizeof(bytes[0]) = " << sizeof(bytes[0]) << "\n";
    bits[3] = true;               // works through the proxy
    std::cout << "bits[3] = " << bits[3] << "\n";
    // Neighbouring bits share a byte: two threads writing bits[0] and bits[1] race.  Use std::vector<std::uint8_t>.
}
```

* 「先占着再检查」：桶里两个 key 落到同一格时也能发现；失败就按 `tmp` 回滚。

### 4.3 `FrozenTickerMap`

```cpp
/// The key set is fixed at construction; only the values change.  A key of the universe that was never written has value 0.
/// get/put/add take a packed key; index_of + add_at/get_at let a caller cache the index and skip hashing altogether.
class FrozenTickerMap {
public:
    explicit FrozenTickerMap(const std::vector<std::string>& universe)
        : index_(SymbolIndex::build(pack_all(universe))), values_(index_.size(), 0) {}  // duplicates -> invalid_argument

    std::size_t size() const noexcept { return values_.size(); }
    int index_of(Key key) const noexcept { return index_.index_of(key); }
    bool contains(Key key) const noexcept { return index_of(key) >= 0; }

    long long get(Key key, long long if_absent) const noexcept {
        const int i = index_of(key);
        return i < 0 ? if_absent : values_[static_cast<std::size_t>(i)];
    }

    /// false if the key is not in the universe.
    bool put(Key key, long long value) noexcept {
        const int i = index_of(key);
        if (i < 0) return false;
        values_[static_cast<std::size_t>(i)] = value;
        return true;
    }

    /// Unknown key: std::invalid_argument.  Overflow: std::overflow_error, value unchanged.
    long long add(Key key, long long delta) {
        const int i = index_of(key);
        if (i < 0) throw std::invalid_argument("unknown ticker key: " + std::to_string(key));
        return add_at(i, delta);
    }

    long long add_at(int index, long long delta) {
        long long& v = values_.at(checked(index));
        return v = add_checked(v, delta);  // the sum is computed before the store: overflow leaves the value alone
    }
    long long get_at(int index) const { return values_.at(checked(index)); }
    Key key_at(int index) const { return index_.key_at(checked(index)); }

private:
    static std::size_t checked(int index) {
        if (index < 0) throw std::out_of_range("negative index");
        return static_cast<std::size_t>(index);
    }
    static std::vector<Key> pack_all(const std::vector<std::string>& universe) {
        std::vector<Key> keys;
        keys.reserve(universe.size());
        for (const std::string& t : universe) keys.push_back(codec::pack(t));  // invalid -> invalid_argument
        return keys;
    }
    SymbolIndex index_;
    std::vector<long long> values_;
};
```

* 「在 universe 里但还没写过」的值是 0，不是 absent。
* `index_of` + `add_at`：订阅行情时把代码解析成下标缓存起来，之后每条消息直接用下标——连哈希都省了。
* **下标要检查边界**：`values_.at()` 越界抛 `std::out_of_range`；若用 `operator[]`，传错下标是 UB（悄悄读写别人的内存）。检查是一个几乎总被预测正确的分支，代价很小；追求极限时另提供不检查的版本，并把前置条件写进文档。
* 成员 `SymbolIndex index_` 在初始化列表里构造：`index_(SymbolIndex::build(pack_all(universe)))`，`values_` 的大小用 `index_.size()`。

## 5. Part 4：一块对齐的定长内存

Java 里「堆外表」是为了躲开 GC。**C++ 没有 GC，所有内存本来就是「堆外」的**；这一部分真正剩下的东西是：

* **布局可控**：一次分配一整块，**按 64 字节（一条缓存行）对齐**，每个槽位 16 字节 `{key, value}`，4 个槽位正好一行；
* **定长**：槽位数 = `bit_ceil(2·maxEntries)`，装载因子 ≤ 1/2；放满 `maxEntries` 个 key 之后新 key 抛 `std::length_error`，已有 key 仍可更新；没有 `remove`，没有 `resize`——**地址永远不变**，方便迁移到共享内存或 `mmap`，别的线程可以一直拿着指针；
* **对象的生命周期**：只能移动，不能拷贝；被移走或 `close()` 之后是空对象，访问抛 `std::logic_error`。

```cpp
/// Fixed capacity, one allocation, never grows or moves: 64-byte aligned storage of 16-byte slots {key, value}
/// (four slots per cache line), slots = bit_ceil(2 * max_entries).  A new key beyond max_entries -> std::length_error,
/// existing keys can still be updated.  No remove.  Move-only; a moved-from or closed map throws std::logic_error.
class FixedTickerMap {
public:
    explicit FixedTickerMap(std::size_t max_entries) {
        if (max_entries < 1 || max_entries > (std::size_t{1} << 28)) throw std::invalid_argument("max_entries out of range");
        max_entries_ = max_entries;
        capacity_ = std::bit_ceil(std::max<std::size_t>(8, 2 * max_entries));
        mask_ = capacity_ - 1;
        shift_ = 64 - std::countr_zero(capacity_);
        const std::size_t bytes = capacity_ * sizeof(Slot);
        void* raw = ::operator new(bytes, std::align_val_t{64});
        std::memset(raw, 0, bytes);  // key == 0 means empty
        slots_.reset(static_cast<Slot*>(raw));
    }

    FixedTickerMap(FixedTickerMap&& o) noexcept
        : slots_(std::move(o.slots_)), capacity_(std::exchange(o.capacity_, 0)), max_entries_(std::exchange(o.max_entries_, 0)),
          size_(std::exchange(o.size_, 0)), mask_(std::exchange(o.mask_, 0)), shift_(std::exchange(o.shift_, 0)) {}
    FixedTickerMap& operator=(FixedTickerMap&& o) noexcept {
        if (this != &o) {
            slots_ = std::move(o.slots_);
            capacity_ = std::exchange(o.capacity_, 0);
            max_entries_ = std::exchange(o.max_entries_, 0);
            size_ = std::exchange(o.size_, 0);
            mask_ = std::exchange(o.mask_, 0);
            shift_ = std::exchange(o.shift_, 0);
        }
        return *this;
    }
    FixedTickerMap(const FixedTickerMap&) = delete;
    FixedTickerMap& operator=(const FixedTickerMap&) = delete;

    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return capacity_; }
    std::size_t max_entries() const noexcept { return max_entries_; }
    const void* data() const noexcept { return slots_.get(); }

    bool contains(Key key) const { return probe(key).found; }

    long long get(Key key, long long if_absent) const {
        const Probe p = probe(key);
        return p.found ? slots_[p.index].value : if_absent;
    }

    bool put(Key key, long long value) {
        const Probe p = probe(key);
        if (!p.found) {
            claim(p.index, key);
            slots_[p.index].value = value;
            return true;
        }
        slots_[p.index].value = value;
        return false;
    }

    long long add(Key key, long long delta) {
        const Probe p = probe(key);
        if (p.found) return slots_[p.index].value = add_checked(slots_[p.index].value, delta);
        claim(p.index, key);
        return slots_[p.index].value = delta;
    }

    /// Idempotent: release the storage.  Every later access throws std::logic_error.
    void close() noexcept {
        slots_.reset();
        capacity_ = max_entries_ = size_ = mask_ = 0;
    }

private:
    struct Slot {
        Key key;
        long long value;
    };
    struct AlignedDelete {
        void operator()(Slot* p) const noexcept { ::operator delete(p, std::align_val_t{64}); }
    };
    struct Probe {
        std::size_t index;
        bool found;
    };

    Probe probe(Key key) const {
        if (!slots_) throw std::logic_error("closed or moved-from");
        if (key == EMPTY || key == TOMB) throw std::invalid_argument("key must not be 0 or ~0");
        std::size_t i = static_cast<std::size_t>((key * GOLDEN) >> shift_);
        for (;;) {
            const Key k = slots_[i].key;
            if (k == key) return {i, true};
            if (k == EMPTY) return {i, false};
            i = (i + 1) & mask_;
        }
    }

    void claim(std::size_t i, Key key) {
        if (size_ == max_entries_) throw std::length_error("full: " + std::to_string(max_entries_) + " entries");
        slots_[i].key = key;
        ++size_;
    }

    std::unique_ptr<Slot[], AlignedDelete> slots_;
    std::size_t capacity_ = 0, max_entries_ = 0, size_ = 0, mask_ = 0;
    int shift_ = 0;
};
```

* `::operator new(bytes, std::align_val_t{64})` 返回对齐的内存，必须用配套的 `::operator delete(p, std::align_val_t{64})` 释放（`AlignedDelete`）；`memset` 清零，`key == 0` 就是空槽。
* **编译器生成的移动构造函数对 `size_t` 成员只是拷贝**：被移走的对象的 `slots_` 是空指针，但 `size_`、`capacity_` 还是旧值，下一次访问就会解引用空指针。这里手写移动，用 `std::exchange` 把源对象清成「空」状态，并让所有访问先检查 `slots_`。
* 线程：没有线程亲和性（不像 Java 的 `Arena.ofConfined`）。`join` 之后另一个线程读写是安全的；**同时**写不是——需要并发就每个线程一张表再合并，或者按 key 分片。

## 6. 你怎么知道更快：测量

被问「你怎么知道更快」时，要能说出怎么测、测到了什么、**哪些结论没有测**。做法：同一串更新喂给每种实现；预热；多轮取最好的；访问模式（`picks`）预先生成，不放进计时循环；用 `-O2`，不开 sanitizer；输出 ns/op。

```cpp
// How to answer "how do you know it is faster": same update stream into each table, warm up, best of five, print ns/op.
// `reference.hpp` is the code of the lecture.  Build with -O2 and no sanitizers.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <random>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../../../../loop/rounds/01_video/hc07_ticker_hash_map/cpp/reference.hpp"

using namespace tickers;
using Clock = std::chrono::steady_clock;

template <class F>
double best_ns_per_op(std::size_t ops, F run) {
    run();  // warm-up: caches, branch predictors, page faults
    double best = 1e18;
    for (int round = 0; round < 5; ++round) {
        const auto t0 = Clock::now();
        run();
        const auto t1 = Clock::now();
        best = std::min(best, std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(ops));
    }
    return best;
}

int main() {
    constexpr std::size_t kOps = 20'000'000;
    std::mt19937_64 rng(1);
    for (std::size_t universe_size : {8000u, 2'000'000u}) {
        std::unordered_set<std::string> seen;
        std::vector<std::string> names;
        while (names.size() < universe_size) {
            std::string s;
            const int len = 3 + static_cast<int>(rng() % 6);
            for (int i = 0; i < len; ++i) s.push_back(static_cast<char>('A' + rng() % 26));
            if (seen.insert(s).second) names.push_back(s);
        }
        std::vector<Key> keys;
        for (const auto& n : names) keys.push_back(codec::pack(n));
        std::vector<std::uint32_t> picks(1 << 20);  // the access pattern is generated once, outside the timed loops
        for (auto& p : picks) p = static_cast<std::uint32_t>(rng() % universe_size);
        const std::size_t mask = picks.size() - 1;

        std::unordered_map<std::string, long long> stl;
        TickerMap strmap(universe_size);
        LongTickerMap longmap(universe_size);
        FrozenTickerMap frozen(names);
        std::vector<int> index;
        for (Key k : keys) index.push_back(frozen.index_of(k));
        for (std::size_t i = 0; i < universe_size; ++i) { stl[names[i]] = 0; strmap.put(names[i], 0); longmap.put(keys[i], 0); }

        std::cout << universe_size << " tickers, " << kOps << " updates per round\n";
        auto report = [](const char* what, double ns) { std::cout << "  " << what << ns << " ns/op\n"; };
        report("std::unordered_map<string>  ", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) stl.find(names[picks[i & mask]])->second += 1; }));
        report("TickerMap (string_view)     ", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) strmap.add(names[picks[i & mask]], 1); }));
        report("LongTickerMap (packed key)  ", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) longmap.add(keys[picks[i & mask]], 1); }));
        report("FrozenTickerMap::add(key)   ", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) frozen.add(keys[picks[i & mask]], 1); }));
        report("FrozenTickerMap::add_at(idx)", best_ns_per_op(kOps, [&] { for (std::size_t i = 0; i < kOps; ++i) frozen.add_at(index[picks[i & mask]], 1); }));
    }
}
```

{{BENCH}}

## 7. 和 Java 版的区别

| 点 | Java | C++20 |
|---|---|---|
| key 类型 | `String` / `long`（有符号，`> 0` 才合法） | `std::string_view` / `uint64_t`（`0` 空、`~0` 墓碑；`-1` 的隐式转换是陷阱） |
| 链地址的代价 | `HashMap` 每条目一个对象 + 装箱 | `unordered_map` 每条目一个节点；`std::string` ≤ 15 字符有 SSO，**不分配**，所以「装箱」不是主要问题，指针追逐才是 |
| 溢出 | `Math.addExact` | `__builtin_add_overflow`（有符号溢出是 UB，不能事后检查） |
| 位运算 | `Long.compress`、`Integer.numberOfTrailingZeros` | `std::countr_zero`、`std::bit_ceil`（`<bit>`），x86 上 `pext`；字节序用 `std::endian` |
| 字节缓冲 | `VarHandle` 读 `byte[]` | `memcpy` 进 `uint64_t` + `bswap` |
| 越界 | 一律抛 `IndexOutOfBounds` | `operator[]` 是 UB，`at()` 才检查；偏移量计算要防回绕 |
| 分配统计 | `ThreadMXBean.getThreadAllocatedBytes` | 重载全局 `operator new` 计数 |
| 堆外 | `Arena` / `MemorySegment`，为了躲 GC | 没有 GC；剩下的是对齐、定长、地址不变、对象生命周期 |
| 失败 | 异常 | 异常（本题）；热路径也可以返回 `optional` / 错误码 |

## 8. 陷阱

1. 下标用 `hash & mask`（`std::hash<整数>` 是恒等函数；打包 key 的低位全是 0）。
2. 删除时把格子置空，断掉探测链；遇到墓碑就插入，造成重复 key；装载因子不算墓碑，导致没有空格而死循环。
3. 用 `(c - 'A' + 1) << 35`：`int` 移位。
4. `char` 有符号：`c < 'A' || c > 'Z'` 对 `0xC3` 判断错。
5. `std::string_view` 里有 `'\0'`，或者用 `const char*` 构造导致截断。
6. `off + 8 > size` 回绕。
7. `put(-1, v)`：`-1` 变成 `0xFFFF…`，正好是墓碑标记。
8. `SymbolIndex::index_of` 不比较原始 key：集合外的 key 被误认成集合内的。
9. 用 `h + d * c` 做哈希族。
10. `vector<bool>` 当标志数组。
11. 编译器生成的移动构造函数不会清空源对象的标量成员。
12. `operator new[]` / `aligned new` 和普通 `delete` 混用。
13. `add` 溢出后表被改了一半。

## 9. 面试官会追问什么（senior）

**Q1. 链地址 vs 开放寻址怎么选？** 开放寻址：连续内存、缓存友好、无逐条目分配，但装载因子要低、删除要墓碑（或回移）、对哈希质量敏感；链地址：实现简单、能容忍高装载因子、删除容易、引用/迭代器稳定（`unordered_map` 保证元素的引用不失效），但指针追逐。读多写少、key 小、要低延迟选开放寻址。

**Q2. 删除怎么做？** 墓碑 + 装载因子算上墓碑 + rehash 时清理；另一种是**回移删除**（backward-shift，不留墓碑，探测链不会越来越长，实现更复杂）。

**Q3. 为什么容量是 2 的幂、每次翻倍？** `&` 或移位代替 `%`（除法很贵）；翻倍使总搬运量 < 2n，均摊 O(1)。

**Q4. 怎么证明你的哈希函数好？** 测最长 / 平均探测距离，用真实代码集合和结构化输入（连续的三字母代码、低位全 0 的 key），不要只用随机串。

**Q5. `unordered_map` 为什么慢，怎么调？** 每个条目一个节点、桶数组里存指针、两次间接寻址；`reserve()` 避免 rehash；换成扁平的开放寻址表（`absl::flat_hash_map`、`boost::unordered_flat_map`、自己写的）。

**Q6. 完美哈希一定更快吗？** 不一定：单次 `add` 并不一定比调好的开放寻址快；收益是**最坏情况确定、内存紧凑、可缓存下标**（`add_at` 不做任何哈希）。

**Q7. 多线程更新怎么办？** 每线程一张表，最后合并；完美哈希下 value 数组固定、不 resize，可以用 `std::atomic_ref<long long>`（C++20）对元素原子累加；热点冲突时分片、避免 false sharing（把计数器按 64 字节对齐）。

**Q8. key 不止 8 个字符 / 含 `.` 和数字？** 扩字符集（6 比特 × 10 个字母 = 60 比特）、128 位 key（两个 `uint64_t`）、或字符串哈希（FNV-1a / xxHash）+ 字节比较；热路径避免 `std::string` 的构造。

**Q9. `std::string` 的 SSO 对你有什么影响？** ≤ 15 字符不分配，所以股票代码作 key 时 `unordered_map<string, …>` 的节点是一次分配而不是两次；但 `string` 对象本身 32 字节，比较要先比长度再 `memcmp`。

**Q10. 对齐有什么用？** 一个 16 字节的槽位不会跨缓存行，一次探测只触碰一条缓存行；64 字节对齐 + 4 槽/行时尤其明显。多线程时，把**不同线程写的数据**放到不同的缓存行，避免 false sharing。

## 10. 自测

1. 为什么 `hash & mask` 对打包后的股票代码是灾难？
2. 删除 A 时把格子置空，会让哪些 key 丢失？
3. 为什么 `static_cast<Key>(c - 'A' + 1) << 35` 要先转宽？
4. `std::string_view("AB\0CD", 5)` 和 `std::string_view("AB\0CD")` 有什么区别？
5. 为什么 `SymbolIndex::index_of` 最后必须比较 `keys_[s] == key`？
6. `FixedTickerMap` 的移动构造函数为什么不能 `= default`？
7. `off + 8 > size` 为什么不安全？

<details><summary>答案</summary>

1. `std::hash` 对整数是恒等函数，`& mask` 只留低位；打包后短代码的低 20 多位全是补的 0，几乎所有 key 落到同一格，查找退化成线性扫描。
2. 所有「家在 A 的家、但因为冲突被挤到 A 后面」的 key：查它们时从家出发会先碰到空格，误判不存在。所以要放墓碑。
3. `c - 'A' + 1` 是 `int`，把 `int` 左移 35 位是未定义行为（移位量 ≥ 32）；先转成 `uint64_t` 再移位。
4. 前者是 5 个字节（含一个 NUL），后者从 C 字符串字面量构造，在第一个 NUL 处截断，长度是 2。
5. 完美哈希只保证集合内的 key 互不冲突；集合外的 key 也会被映射到某个格子，不比较就会把它误认成那个格子里的 key。
6. 默认的移动对 `size_`、`capacity_` 这类标量只是拷贝，被移走的对象指针为空而计数还是旧值，之后访问会解引用空指针。要手写并把源对象清成空状态。
7. `off` 接近 `SIZE_MAX` 时 `off + 8` 回绕成一个很小的数，检查通过，后面的读就越界了。先保证 `size >= 8`，再写 `off > size - 8`。

</details>
