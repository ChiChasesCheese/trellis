# hc14 · Trade Log → VWAP（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。口头回答用英文，这里的英文术语可以直接拿去说。题目语义和 Java 版完全相同（规则表见下，样例见 `problem.md`）。

## 1. 题目

交易系统每笔成交写一行 `ts_ms,symbol,price,qty`。四个 Part：

| Part | 内容 |
|---|---|
| 1 | 解析一行、坏行计数、按代码汇总：笔数、数量、名义金额（notional）、VWAP、最低 / 最高价 |
| 2 | 流式：滑动时间窗口（最近 W 毫秒）上的 VWAP，摊还 O(1) |
| 3 | 窗口内名义金额最大的 k 个代码 |
| 4 | 百万行：一遍扫字节，不为每行分配内存，结果与 Part 1 逐字段一致 |

### 规则（先写下来再写代码）

| 项 | 约定 |
|---|---|
| 字段数 | 恰好 4 个（3 个逗号），不 trim，空白 / `\r` 都是坏行 |
| `ts_ms` | 1–18 个 `0`–`9` |
| `symbol` | 1–10 个字符，`A`–`Z`、`0`–`9`、`.` |
| `price` | `D{1,9}` 或 `D{1,9}.D{1,4}`，值 > 0；内部是 `long long`，单位 0.0001（`187.25` → `1'872'500`） |
| `qty` | 1–12 个 `0`–`9`，值 > 0 |
| 乘积 | `price × qty` 装不进 `long long` → 坏行 |
| 空行 | 长度 0：跳过，不计数；只含空白：坏行 |
| VWAP | `Σ notional / Σ qty`，四舍五入，半数向上 |
| 汇总溢出 | `std::overflow_error` |

价格为什么用整数：`0.1 + 0.2 != 0.3`，二进制浮点存不准十进制小数；整数精确，可比较，可当哈希键。

## 2. 类型

```cpp
inline constexpr long long SCALE = 10'000;
inline constexpr int MAX_SYMBOL_LEN = 10;

inline long long add_exact(long long a, long long b) {
    long long r;
    if (__builtin_add_overflow(a, b, &r)) throw std::overflow_error("addition overflow");
    return r;
}
inline long long mul_exact(long long a, long long b) { /* 同理，__builtin_mul_overflow */ }

struct Trade {
    long long ts_ms; std::string symbol; long long price; long long qty;
    Trade(long long ts, std::string sym, long long p, long long q)
        : ts_ms(ts), symbol(std::move(sym)), price(p), qty(q) {
        if (ts_ms < 0) throw std::invalid_argument("negative timestamp");
        if (!valid_symbol(symbol)) throw std::invalid_argument("invalid symbol");
        if (price <= 0) throw std::invalid_argument("non-positive price");
        if (qty <= 0) throw std::invalid_argument("non-positive quantity");
        mul_exact(price, qty);                      // 乘积溢出 → overflow_error
    }
    long long notional() const noexcept { return price * qty; }
    friend bool operator==(const Trade&, const Trade&) = default;   // C++20：默认逐成员比较
};
```

要点：

* 溢出检测用 `__builtin_mul_overflow` / `__builtin_add_overflow`（GCC / Clang）。有符号整数溢出在 C++ 里是**未定义行为**（UB），不是回绕；编译器甚至可以假设它不发生而删掉你的检查。测试用 `-fsanitize=undefined`，一溢出就终止。
* `Trade` **没有默认构造函数**：不能有「半合法」的 `Trade`。构造函数是合法性的唯一出口，手里有 `Trade` 就一定合法。
* `friend bool operator==(...) = default;`：C++20 的默认比较，`SymbolStats`、`Report` 也这样写，测试里直接 `CHECK_EQ(report, expected)`。

## 3. Part 1：解析与汇总

### 解析价格

不用 `std::stod`（浮点、受 locale 影响、接受 `1e3`、`inf`），也不用 `std::from_chars` 直接解整串（它会接受 `-`，也表达不了「整数部分最多 9 位、小数最多 4 位」）。逐字符扫：

```cpp
inline std::optional<long long> parse_price(std::string_view s) {
    std::size_t i = 0;
    long long whole = 0, frac = 0;
    int int_digits = 0, frac_digits = 0;
    while (i < s.size() && detail::is_digit(s[i])) {
        whole = whole * 10 + (s[i++] - '0');
        if (++int_digits > 9) return std::nullopt;
    }
    if (int_digits == 0) return std::nullopt;
    if (i < s.size() && s[i] == '.') {
        ++i;
        while (i < s.size() && detail::is_digit(s[i])) {
            frac = frac * 10 + (s[i++] - '0');
            if (++frac_digits > 4) return std::nullopt;
        }
        if (frac_digits == 0) return std::nullopt;
    }
    if (i != s.size()) return std::nullopt;
    for (int d = frac_digits; d < 4; ++d) frac *= 10;      // "187.3" → 3000
    const long long price = whole * SCALE + frac;
    if (price <= 0) return std::nullopt;
    return price;
}
```

参数是 `std::string_view`：不拥有内存，不拷贝。必须**每次访问前先检查 `i < s.size()`**——`string_view` 不保证以 `\0` 结尾，读过末尾一个字节就是越界（测试里把视图放在恰好分配的缓冲区末尾，AddressSanitizer 会抓到）。

`is_digit` 自己写成 `c >= '0' && c <= '9'`；不要用 `std::isdigit`（它的参数是 `int`，传负的 `char` 是 UB，还受 locale 影响）。

### 解析一行

```cpp
const auto c1 = line.find(',');
if (c1 == std::string_view::npos) return std::nullopt;
const auto c2 = line.find(',', c1 + 1);
if (c2 == std::string_view::npos) return std::nullopt;
const auto c3 = line.find(',', c2 + 1);
if (c3 == std::string_view::npos || line.find(',', c3 + 1) != std::string_view::npos) return std::nullopt;   // 第 4 个逗号 = 坏行
```

时间戳和数量用同一个 `detail::digits(sv, max_digits)`（全是数字、长度 1..max，否则 -1）；代码用 `valid_symbol`；乘积用 `__builtin_mul_overflow` 检查，溢出就返回 `nullopt`，最后 `return Trade(ts, std::string(symbol), *price, qty);`。

### VWAP 舍入

```cpp
inline long long vwap(long long notional, long long volume) {
    if (volume <= 0 || notional < 0) throw std::invalid_argument("...");
    const long long q = notional / volume, r = notional % volume;
    return r >= volume - r ? q + 1 : q;      // 半数向上；不写 2*r，那样在 volume 接近 LLONG_MAX 时溢出
}
```

### 汇总

```cpp
std::map<std::string, Acc> by;                       // 有序：天然按代码升序
for (const auto& line : lines) {
    if (line.empty()) continue;
    const auto t = parse_line(line);
    if (!t) { ++malformed; continue; }
    auto [it, fresh] = by.try_emplace(t->symbol);    // 结构化绑定（C++17）
    Acc& a = it->second;
    a.volume = add_exact(a.volume, t->qty);
    a.notional = add_exact(a.notional, t->notional());
    a.min = fresh ? t->price : std::min(a.min, t->price);
    a.max = fresh ? t->price : std::max(a.max, t->price);
    ++a.count; ++accepted;
}
```

`std::map<std::string, ...>` 比较是逐字节的，`.`(46) < `0`(48) < `A`(65)，和 Java 的 `String.compareTo` 一致（代码里只有 ASCII）。

## 4. Part 2：滑动窗口 VWAP

规则：成交在时刻 `now` 是活的 ⇔ `now − ts < W`；时钟只进不退；查询也推进时钟；累加溢出时这笔不计入，其余状态不变。

结构：`std::deque<Trade> live_`（队头最老）+ `std::unordered_map<std::string, Acc> by_symbol_`。

```cpp
void advance(long long t) {
    if (t < now_) throw std::invalid_argument("time went backwards");
    now_ = t;
    while (!live_.empty() && now_ - live_.front().ts_ms >= window_) {
        const Trade& old = live_.front();
        const auto it = by_symbol_.find(std::string_view(old.symbol));
        it->second.volume -= old.qty;
        it->second.notional -= old.notional();
        if (--it->second.count == 0) by_symbol_.erase(it);       // 过期的代码从表里消失
        live_.pop_front();
    }
}

void on_trade(const Trade& t) {
    advance(t.ts_ms);
    auto it = by_symbol_.find(std::string_view(t.symbol));
    const long long volume   = add_exact(it == by_symbol_.end() ? 0 : it->second.volume, t.qty);      // 先算，可能抛
    const long long notional = add_exact(it == by_symbol_.end() ? 0 : it->second.notional, t.notional());
    if (it == by_symbol_.end()) it = by_symbol_.emplace(t.symbol, Acc{}).first;
    ++it->second.count; it->second.volume = volume; it->second.notional = notional;
    live_.push_back(t);
}
```

摊还 O(1)：每笔成交入队一次、出队一次。

**透明哈希（heterogeneous lookup，C++20）**：`by_symbol_.find(std::string_view)` 默认不能编译——`unordered_map<std::string, ...>` 的 `find` 只收 `std::string`，传 `string_view` 要先构造 `std::string`（可能分配）。解决：给容器一个「透明」的哈希器和比较器：

```cpp
struct SvHash {
    using is_transparent = void;
    std::size_t operator()(std::string_view s) const noexcept { return std::hash<std::string_view>{}(s); }
};
std::unordered_map<std::string, Acc, SvHash, std::equal_to<>> by_symbol_;
```

`std::equal_to<>`（即 `equal_to<void>`）本身是透明的。这样 `find(string_view)` 不拷贝。

**引用悬空**：`advance` 里 `const Trade& old = live_.front();` 之后一直用到 `pop_front()` 之前，所以引用有效；如果把 `pop_front()` 放在读 `old` 之前就是悬空引用。

## 5. Part 3：top-k

```cpp
std::vector<SymbolNotional> top_k(int k, long long now_ms) {
    if (k < 0) throw std::invalid_argument("k must be >= 0");   // 先于时钟检查
    advance(now_ms);
    std::vector<SymbolNotional> all;
    for (const auto& [sym, a] : by_symbol_) all.push_back({sym, a.notional});
    const auto best_first = [](const SymbolNotional& x, const SymbolNotional& y) {
        return x.notional != y.notional ? x.notional > y.notional : x.symbol < y.symbol;      // 全序
    };
    const auto keep = std::min<std::size_t>(static_cast<std::size_t>(k), all.size());     // k 是 int：先钳到代码数
    std::partial_sort(all.begin(), all.begin() + static_cast<std::ptrdiff_t>(keep), all.end(), best_first);
    all.resize(keep);
    return all;
}
```

* `std::partial_sort` 做的是堆法：O(m log k)。
* `k` 是 `int`，`size()` 是 `size_t`：直接比较有符号 / 无符号会出错，所以显式 `static_cast` 后用 `std::min`。`k = INT_MAX` 不能拿来 `reserve`。
* 返回值是**拷贝**（`std::vector` 按值返回，NRVO / 移动，不是引用）：之后的成交不会改变已返回的结果。
* 比较器必须是严格弱序且是全序（金额降序，同额按代码升序）。

查询比成交频繁时，改成维护 `std::set<std::pair<…>>`：成交和过期各「删旧键、插新键」O(log m)，查询取前 k 个 O(k)。不能只用 `std::priority_queue`：它不支持改键。

## 6. Part 4：字节级解析

目标：100 万行 < 1 s 且**不为每行分配**。`std::string_view data` 是整个文件；扫到 `'\n'` 切行。

要点：

1. **符号表是 `unsigned char` 下标**：`codes[base[p]]`，其中 `base` 是 `const unsigned char*`（`reinterpret_cast` 自 `data.data()`）。`char` 通常有符号，`0xE9` 当下标是 −23，越界读。
2. **代码打包**：字符映射到 1..37（`A`–`Z`=1..26，`0`–`9`=27..36，`.`=37），每个 6 位，10 个字符 = 60 位，装进 `std::uint64_t` 当键。不同长度的代码键不同。
3. **开放寻址表**：`keys_`（0 = 空槽）+ 并行 `std::vector<long long>`（count / volume / notional / min / max）；槽位 `(key * GOLDEN) >> (64 − log2(cap))`，`std::countr_zero(cap)` 求 `log2`（`<bit>`，C++20）；装填率超过 1/2 就翻倍重哈希。
4. 乘积溢出用 `__builtin_mul_overflow`，不抛异常。
5. 最后才把键解码成 `std::string`、排序，产出 `Report`。

```cpp
while (pos < n) {
    std::size_t end = pos;
    while (end < n && base[end] != '\n') ++end;
    if (end > pos) { if (line(pos, end)) ++accepted; else ++malformed; }   // 空行（end == pos）跳过
    pos = end + 1;                                                          // 最后一行可以没有换行
}
```

`line` 是一个捕获了 `base`、`table` 的 lambda：逐字段推进 `p`，每一步都检查 `p < e`。性能测试 100 万行（约 35 MB）在 `-O2` 下不到 0.1 s。`std::string` 版每行都会分配（`std::string(symbol)`、`Trade`）；测试用全局 `operator new` 计数器验证：10 万行的字节版总共分配不到 200 次（哈希表增长和结果）。

**对拍**：随机改坏日志（每行删 / 改 / 插一个字符），`analyze(lines)` 与 `analyze_fast(text)` 的 `Report` 必须相等。

## 7. 和 Java 版的区别

| 点 | Java | C++ |
|---|---|---|
| 溢出 | `Math.multiplyExact` 抛 `ArithmeticException` | `__builtin_mul_overflow`；有符号溢出是 UB，不是回绕 |
| 异常类型 | `IllegalArgumentException` / `ArithmeticException` / `NoSuchElement…` | `std::invalid_argument` / `std::overflow_error` / `std::out_of_range` |
| 字符串 | `String`（不可变，UTF-16） | `std::string_view` 借用 + `std::string` 拥有；注意生命周期与 `\0` |
| 字节 | `byte` 有符号，`& 0xFF` | `char` 有符号（平台相关），先转 `unsigned char` |
| 值类型 | `record` | `struct` + `operator== = default`；无默认构造以禁止非法值 |
| 哈希 key 查找 | `map.get(String)` | 异构查找需要透明哈希器 |
| 零分配证明 | `ThreadMXBean.getThreadAllocatedBytes` | 替换全局 `operator new` 计数 |

## 8. 陷阱

1. 读 `string_view` 越过末尾（它不以 `\0` 结尾）。
2. `std::isdigit(char)` 传负值是 UB；用自己写的范围比较。
3. 有符号溢出是 UB：`price * qty`、`n + v/2`、`2 * r` 都可能触发。
4. `char` 当数组下标（高位字节为负）。
5. `std::stod` / `std::stoll`：接受前导空白、`+`、`1e3`，不符合语法；还会抛异常。
6. `unordered_map<std::string,…>::find(string_view)` 不能编译；写成 `std::string(sv)` 则每次分配。
7. 引用悬空：持有 `live_.front()` 的引用后 `pop_front()`。
8. `k`（`int`）与 `size()`（`size_t`）比较；`k = INT_MAX` 拿去 `reserve`。
9. 窗口边界差一（`now − ts == W` 必须过期）；先改状态再检查溢出。
10. `top_k` 比较器不是全序，并列顺序不稳定。
11. （Part 4）最后一行没有换行；表满不扩容；快慢版本语法不一致。

## 9. 面试官会追问什么（senior）

1. **为什么价格用整数？** 浮点存不准十进制小数，累加误差、相等比较不可靠；整数精确，可作键。代价是自己管舍入与溢出。
2. **怎么证明快版和慢版一致？** 对拍：随机改坏的日志同时喂两个版本，比较整个 `Report`；加上每类坏行的穷举样例。
3. **一亿行怎么办？** `mmap`；按行边界切块，每个线程一张表，最后合并（加法与 min / max 满足结合律）；解析可用 SIMD 找换行与逗号。
4. **窗口里成交乱序到达？** 水位线 + 允许迟到；窗口用按时间排序的结构代替 deque，出队 O(log n)。
5. **top-k 查询很频繁？** 维护 `std::set` 按 (金额, 代码) 排序，成交 / 过期各删旧键插新键。
6. **为什么用 `deque` 不用 `vector`？** 队头弹出 O(1)；`vector` 的 `erase(begin())` 是 O(n)。也可以用环形缓冲区 / 双指针。
7. **透明哈希是什么？** 让 `find` 接受与键类型不同但可比较的类型，省掉构造临时 `std::string`。

## 10. 自测

**Q1** `parse_price("187.3")`、`"0.0001"`、`"5."`、`".5"`、`"0.0000"` 各返回什么？

<details><summary>答案</summary>`1'873'000`；`1`；后三个都是 `nullopt`（小数点后无数字、整数部分为空、值为 0）。</details>

**Q2** `vwap(5, 2)`、`vwap(1, 3)`、`vwap(LLONG_MAX, 2)`？

<details><summary>答案</summary>3；0；`2^62`（`q = 2^62 − 1`，`r = 1`，`1 ≥ 2 − 1` 加一）。</details>

**Q3** 为什么 `codes[base[p]]` 里 `base` 要是 `unsigned char*`？

<details><summary>答案</summary>`char` 通常有符号，字节 `0xE9` 读成 −23，作下标越界（未定义行为，ASan 会报）；`unsigned char` 的取值是 0..255，正好是 256 项表的下标。</details>

**Q4** 窗口 W = 10，`on_trade(0, A, …)`，然后 `vwap("A", 9)` 与 `vwap("A", 10)`，各返回什么？之后 `on_trade(5, …)` 会怎样？

<details><summary>答案</summary>`vwap("A", 9)` 有值（9 − 0 < 10）；`vwap("A", 10)` 为 `nullopt`（10 − 0 = 10 过期）；`vwap` 已把时钟推到 10，再 `on_trade(5, …)` 抛 `std::invalid_argument`（时间倒退）。</details>

**Q5** `top_k(INT_MAX, 0)` 会发生什么？应该怎么实现？

<details><summary>答案</summary>`k` 要先钳到代码数再用：`std::min<std::size_t>(k, all.size())`；把 `k` 当 `reserve` 的参数会尝试分配几十 GB。返回全部代码。</details>
