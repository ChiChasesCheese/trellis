# hc07 · 股票代码哈希表（C++20 版）

股票代码（ticker）是至多 8 个大写字母的短字符串，交易系统要拿它反复查表。这个任务从最普通的 `std::unordered_map<std::string, long long>` 出发，一步步把它优化成更小更快的表：自己写开放寻址哈希表、把代码打包进一个 `uint64_t`、用完美哈希消灭冲突，最后做一块对齐的定长内存，并说清楚你怎么测量。key 的结构特殊（至多 8 个大写字母），这个特点就是优化的突破口。签名都在 `starter.hpp`（命名空间 `tickers`）。

## 读题前你需要知道

- **链地址法**（chaining）和**开放寻址**（open addressing）：前者每个桶挂一条链、每个条目一次分配，后者所有条目放在一块连续数组里，冲突时往后找空格。`std::unordered_map` 是前者。
- **线性探测**（linear probing）：哈希落到第 h 格，被占就看 h+1、h+2……直到找到目标或碰到空格。**装载因子**（load factor）= 已占格子 / 总格子，越高探测越长。
- **墓碑**（tombstone）：删除不能把格子置空，否则落在它后面的 key 会因为探测链被截断而「消失」。删除只做标记，插入时可以复用，重建表（rehash）时才清掉。
- **缓存行**（cache line）：CPU 一次读 64 字节。把 key 和 value 放在同一个 16 字节的槽位里，找到 key 时 value 已经在缓存里。
- **完美哈希**（perfect hashing）：key 集合固定时，让 n 个 key 一一落到 `0..n-1`，零冲突。集合外的 key 也会落到某个格子，所以最后必须比较原始 key。
- **SSO**（small string optimization）：`std::string` 的短字符串（常见实现里约 15 个字符以内）直接存在对象内部，不分配堆内存。股票代码都不超过 8 个字符，不触发分配。
- **未定义行为**（UB）：有符号溢出、`int` 左移 35 位、`size_t` 回绕后的越界读，这套题里到处都是。测试带 sanitizer，一触发就终止。

## 公共类型（starter 已给出）

```cpp
using Key = std::uint64_t;
inline constexpr Key EMPTY = 0;       // 从没用过的格子
inline constexpr Key TOMB  = ~Key{0}; // 删除过的格子；所有合法 key 都严格落在 EMPTY 和 TOMB 之间
inline constexpr std::uint64_t GOLDEN = 0x9E3779B97F4A7C15ull;

long long add_checked(long long a, long long b);  // 溢出抛 std::overflow_error
```

## Part 1 · 手写哈希表 `BasicTickerMap<Hash>` / `TickerMap`

不许用 `std::unordered_map` / `std::map` 做存储。`Hash` 是对 key 文本的哈希；换成「所有 key 哈希值都相同」的 `Hash`，表也必须保持正确，只是变慢。`TickerMap = BasicTickerMap<>`，默认用 `std::hash<std::string_view>`。

| 签名 | 要求 |
|---|---|
| `explicit BasicTickerMap(std::size_t expected_size = 0, Hash = {})` | 放 `expected_size` 条不需要 rehash；大得离谱抛 `std::length_error`（`static_cast<std::size_t>(-1)` 就是这种） |
| `size()` · `capacity()` · `tombstones()` | 活条目数 · 格子总数 · 墓碑数（诊断用） |
| `bool contains(std::string_view)` | 存在与否 |
| `std::optional<long long> get(std::string_view)` | 不存在得 `std::nullopt`；value 为 0 或负数也是存在 |
| `std::optional<long long> put(std::string_view, long long)` | 返回旧值，没有则 `nullopt` |
| `long long add(std::string_view, long long delta)` | `value += delta`，不存在当作 0，返回新值；溢出抛 `std::overflow_error`，表不变（用 `add_checked`） |
| `std::optional<long long> remove(std::string_view)` | 返回被删的值 |
| `template<class F> void for_each(F&&) const` | 对每个活条目调用 `f(std::string_view key, long long value)` 恰好一次 |
| `std::size_t max_probe_length() const` | 所有活 key 里离自己「家」最远的距离（0 = 都在家） |

- 空字符串 `""` 是普通 key。
- 要求：开放寻址 + 线性探测、存在 `std::vector` 里；**（占用 + 墓碑）/ 容量 ≤ 3/4** 在每次操作之后都成立；删除留墓碑，rehash 清掉墓碑；反复「插入新 key、删旧 key」时容量不能无限增长，也不能死循环（表里必须始终留有空格）。
- 查找参数是 `std::string_view`，查找不分配。
- 测试检查的行为：
  - 基本：`put("AAPL", 100)` 得 `nullopt`；再 `put("AAPL", 150)` 得 `100`；`remove` 得 `150`，再 `remove` 得 `nullopt`。
  - `add("MSFT", 5)`、`add("MSFT", 3)`、`add("MSFT", -10)` 依次得 5、8、−2。
  - 溢出：`LLONG_MAX` 上 `add(…, 1)`、`LLONG_MIN` 上 `add(…, -1)` 都抛 `std::overflow_error`，值不变；新 key `add("NEWKEY", LLONG_MAX)` 得 `LLONG_MAX`。
  - 插入 10 万个 key，每一步装载因子都 ≤ 3/4，之后全部查得到。`TickerMap m(10000)` 插入 10000 个 key，容量不变。
  - 1024 个哈希值完全相同的 key（`BasicTickerMap` 配一个永远返回 42 的 `Hash`）：全部 put、get；删掉偶数下标的一半，剩下的仍然查得到，`size() == 512`。
  - 删除探测链的头和中间之后，后面的 key 仍然查得到；重新插入被删的 key，不重复、不丢失，`for_each` 每个 key 恰好一次。
  - 对同一个 key 反复 `remove` + `put` 10 万次，容量不变，`tombstones() == 0`（复用墓碑要把它从计数里扣掉）。
  - 同时最多 10 个活 key、30 万个不同 key 的 churn：`capacity() <= 1024`，每一步查一个从没插入过的 key 都能返回（不会死循环），`tombstones() + size() <= capacity * 3/4`。
  - 与 `std::unordered_map` 对拍：20 万步随机 put / add / remove / get。
  - 全部 17576 个三字母代码（`AAA`…`ZZZ`）：`max_probe_length() <= 64`。相邻的 key 不能变成表里相邻的格子。
  - 20 万个代码上 100 万次 `add` 加查询，2 秒内。
- C++ 专属测试：
  - 先 `put` 一个 `"AAPL"` 和一个 40 字符的 key，之后 1000 轮 `get` / `contains` / `add`（含 `std::string_view` 参数）**零次 `operator new`**。
  - 5000 个 ≤ 8 字符的 key，表预留 5000，插入过程**零次** `operator new`（短 key 活在 SSO 里）。
  - `std::string_view("AB\0CD", 5)` 和 `"AB"` 是两个不同的 key：带长度的 view 不会在 NUL 处截断。

## Part 2 · 打包进 `uint64_t`：`codec` + `LongTickerMap`

### 编码（测试会检查具体的值）

`'A'..'Z'` 对应 `1..26`，每个字符 **5 比特**；第 i 个字符（i 从 0 起）放在第 `[35−5i, 39−5i]` 比特；不足 8 个字符的尾部补 0。结果恒 `> 0` 且 `< 2^40`。

`"AAPL"`：

| i | 字符 | 值 | 5 比特 | 比特位置 |
|---|---|---|---|---|
| 0 | A | 1 | `00001` | 35–39 |
| 1 | A | 1 | `00001` | 30–34 |
| 2 | P | 16 | `10000` | 25–29 |
| 3 | L | 12 | `01100` | 20–24 |
| 4–7 | 补 0 | 0 | `00000` | 0–19 |

整个值 = `(1<<35) | (1<<30) | (16<<25) | (12<<20)`。`"A"` = `1ull << 35`；`"ZZZZZZZZ"` 是 8 个字段全是 26。

| 签名（命名空间 `tickers::codec`） | 要求 |
|---|---|
| `Parsed parse(std::string_view)` | `Parsed = std::variant<Ticker{Key key}, Invalid{Error error; std::size_t position}>`。空 → `Invalid{Empty, 0}`；超过 8 个 → `Invalid{TooLong, 8}`；第一个不在 `A..Z` 的字节 → `Invalid{BadChar, 下标}`（`>= 0x80` 的字节、NUL 都算）。starter 提示：让它能 `constexpr` |
| `Key pack(std::string_view)` | 同 `parse`，非法抛 `std::invalid_argument` |
| `bool is_valid_key(Key)` | `1 <= key < 2^40`，每个字段 ≤ 26，0 字段之后不能再有字母 |
| `std::string unpack(Key)` | `pack` 的反函数；非法 key 抛 `std::invalid_argument` |
| `Key pack_wire(std::span<const std::byte>, std::size_t off)` | 行情报文里的代码字段：从 `off` 起 **8 个字节，大写字母 + 右侧补空格**，如 `"AAPL    "`。非法（全空格、前导空格、中间空格、小写、NUL、非字母）抛 `std::invalid_argument`；放不进缓冲区抛 `std::out_of_range`。starter 提示：字母的低 5 位就是它的编码，空格的低 5 位是 0 |

- 合法例子：`"A"`、`"AB"`、`"IBM"`、`"AAPL"`、`"GOOGL"`、`"BRKBXX"`、`"ABCDEFG"`、`"ABCDEFGH"` 往返 `unpack(pack(t)) == t`；2 万个随机代码往返成立。
- 17576 个三字母代码的 key 互不相同，都在 `(0, 2^40)` 内；`"A"`、`"AA"`、`"AAA"` 是三个不同的 key。
- 非法：`""`、`"ABCDEFGHI"`（9 个）、`"aapl"`、`"AaPL"`、`"BRK.B"`、`"BRK-B"`、`"A1"`、`"A B"`、`" AAPL"`、`"AAPL "`、UTF-8 的 `É`、全角 `ＡＢ`。`parse("AB.C")` 得 `Invalid{BadChar, 2}`。
- 非法 key（`unpack` / `is_valid_key`）：`0`、`~0ull`、`1ull << 40`、`0x7FFFFFFFFFFFFFFFull`、`A·空·A`（`(1<<35) | (1<<25)`）、`27ull << 35`、`31ull << 35`、`1ull`。
- `pack_wire`：`"AAPL    "` 得 `pack("AAPL")`；`"xx12AAPL    yy"` 从 `off = 4` 开始也得 `pack("AAPL")`。`"AAPL"`（4 字节）、从 `off = 1` 读 8 字节的缓冲、空缓冲，都抛 `std::out_of_range`。
- C++ 专属测试：
  - `std::string_view("AB\0CD", 5)` 是非法的（含 NUL），不能被截成 `"AB"`；而 `std::string_view("AB\0CD")` 从字面量构造，长度是 2，得 `pack("AB")`。
  - 对 128..255 的每个字节，`"A" + 该字节` 都是 `Invalid`：`char` 可能是有符号的，只检查上界会放过 `0xC3`。
  - `off = SIZE_MAX - 3` 和 `off = SIZE_MAX` 必须抛 `std::out_of_range`，不能因为 `off + 8` 回绕而越界读。

### `LongTickerMap`

key 是打包好的 `Key`，**任意 `uint64_t` 都可以，除了 `0` 和 `~0`**（抛 `std::invalid_argument`），value 是 `long long`。开放寻址 + 线性探测 + 墓碑，装载因子 ≤ 3/4。

| 签名 | 要求 |
|---|---|
| `explicit LongTickerMap(std::size_t expected_size = 0)` | 同 Part 1 的预留语义，大得离谱抛 `std::length_error` |
| `size()` · `capacity()` · `tombstones()` | 诊断用 |
| `bool contains(Key)` | |
| `long long get(Key, long long if_absent)` | 不存在返回 `if_absent` |
| `bool put(Key, long long)` | `true` = 新 key，`false` = 覆盖 |
| `long long add(Key, long long delta)` | 不存在当作 0；溢出抛 `std::overflow_error`，值不变 |
| `bool remove(Key)` | 是否删到 |
| `for_each(F&&)` | `f(Key, long long)` 每个活条目一次 |
| `max_probe_length()` | 同 Part 1 |

- **稳态下 `add` / `get` 零次 `operator new`**。8000 个 key 预留好之后，160 万次 `add` 不分配。
- 一个扁平表 8000 个 key 一共只分配 **1 次**（槽位数组），同样的数据放进 `std::unordered_map` 至少是每个条目一次。
- **哈希不能写成 `key & mask`**：打包后短代码的低位全是补的 0，几乎所有 key 落到同一格。全部 17576 个三字母代码和 8000 个随机代码，`max_probe_length() <= 64`。starter 提醒：`std::hash<uint64_t>` 是恒等函数。
- `put(0, …)` / `get(0, …)` / `add` / `remove` / `contains` 对 `0` 和 `TOMB` 都抛 `std::invalid_argument`；`TOMB - 1` 和 `1ull << 63` 是合法 key。
- C++ 专属测试：`static_cast<Key>(-1)`（`int` 的 −1 转成 `uint64_t`）就是 `TOMB`，也要抛 `std::invalid_argument`。
- 其他：value 为 0 和 `LLONG_MIN` 是真实的值；`m(4)` 之后插入 3000 个 key 再删一半，剩下的仍查得到；`for (Key i = 1; i <= 400000; ++i) put(i)` + 删 `i − 10`，容量 ≤ 1024；删除再插入同一个 key 复用墓碑，`tombstones()` 回到 0；30 万步随机操作与 `std::unordered_map` 对拍；与 Part 1 的 `TickerMap` 在同一串行情上结果一致。
- 性能：8000 个代码上 500 万次 `add` + 查询，2 秒内。

## Part 3 · 完美哈希：`SymbolIndex` + `FrozenTickerMap`

场景：开盘前就知道今天会出现的全部代码（比如 8000 个）。

### `SymbolIndex`

| 签名 | 要求 |
|---|---|
| `static SymbolIndex build(std::span<const Key>)` | key 互不相同且不是 `0` / `~0`，否则抛 `std::invalid_argument`；空集合合法；10 万个 key 要在 2 秒内建好。starter 提示：hash-and-displace；标志数组用 `std::vector<std::uint8_t>`，不要用 `std::vector<bool>`（它是按位压缩的代理容器） |
| `std::size_t size() const noexcept` | |
| `int index_of(Key) const noexcept` | 集合内的 key **一一映射到 `0..n−1`**，集合外的 key（包括 `0`、`TOMB`、`1`、`1ull << 63`）返回 `SymbolIndex::NPOS`（`-1`） |
| `Key key_at(std::size_t) const` | `index_of` 的反函数 |

- `index_of` 里**必须比较存下来的 key**：完美哈希只保证集合内的 key 不冲突，集合外的 key 也会被映射到某个格子。6 万个集合外的随机代码都要返回 `-1`。
- 退化集合：0 个、1 个、2 个 key，以及 1 到 40 个随机 key；`AAA..ZZZ` 共 17576 个（每个 key 低 25 位全是 0，结构化输入）；构建顺序（打乱）不影响结果。
- 8000 个 key 上 2000 万次 `index_of`，2 秒内。

### `FrozenTickerMap`

| 签名 | 要求 |
|---|---|
| `explicit FrozenTickerMap(const std::vector<std::string>&)` | 代码按 `codec` 格式；非法（含 `""`、小写）或重复抛 `std::invalid_argument`；所有 value 初始为 0（**在集合里但还没写过 = 0，不是不存在**） |
| `size()` · `index_of(Key)` · `contains(Key)` | `0` 和 `TOMB` 视为不存在 |
| `long long get(Key, long long if_absent) const noexcept` | |
| `bool put(Key, long long) noexcept` | 不在集合里返回 `false` |
| `long long add(Key, long long)` | 不在集合里抛 `std::invalid_argument`；溢出抛 `std::overflow_error`，值不变 |
| `long long add_at(int, long long)` · `long long get_at(int) const` · `Key key_at(int) const` | 行情订阅时把代码解析成下标缓存起来，之后每条消息直接用下标。下标在 `0..size()-1` 之外抛 `std::out_of_range`，不能是 UB |

- `FrozenTickerMap(Strings{"AAPL","MSFT","GOOG"})`：`get(AAPL, -1) == 0`，`get(IBM, -1) == -1`，`add(AAPL, 100)`、`add(AAPL, 30)` 得 100、130，`put(MSFT, 5)` 为 `true`，`put(IBM, 5)` 为 `false`，`add(IBM, 1)` 抛 `std::invalid_argument`。
- `add_at(-1, 1)`、`add_at(2, 1)`（`size() == 2`）抛 `std::out_of_range`，`get_at(2)`、`key_at(-1)`、`key_at(2)` 同理。
- 与 `LongTickerMap` 在同一串 30 万次更新上结果一致。
- 热路径零分配：对 8000 个 key 各做 100 轮 `add(key, 1)` 和 `add_at(cached_index, 1)`，零次 `operator new`。
- 性能：2000 万次 `add(key, 1)`，2 秒内。

## Part 4 · 定长对齐内存：`FixedTickerMap`

| 签名 | 要求 |
|---|---|
| `explicit FixedTickerMap(std::size_t max_entries)` | `max_entries` 不在 `1..2^28` 抛 `std::invalid_argument`（包括 0、`2^28 + 1`、`SIZE_MAX`）。槽位数 = `bit_ceil(2 * max_entries)`，至少 8 |
| 移动构造 / 移动赋值（`noexcept`），拷贝 `= delete` | 被移走或 `close()` 之后，对象是空的：`size() == 0`、`capacity() == 0`，任何访问抛 `std::logic_error` |
| `size()` · `capacity()` · `max_entries()` | |
| `const void* data() const noexcept` | 槽位数组的起始地址，测试用它检查 64 字节对齐 |
| `bool contains(Key)` · `long long get(Key, long long)` · `bool put(Key, long long)` · `long long add(Key, long long)` | 语义同 `LongTickerMap`；`0` 和 `TOMB` 抛 `std::invalid_argument` |
| `void close() noexcept` | 幂等 |

- 一次分配、不增长：槽位是 16 字节的 `{key, value}`，数组 **64 字节对齐**，`key == 0` 表示空格。starter 提示：`::operator new(bytes, std::align_val_t{64})` 和与之匹配的对齐版 `delete`。没有 `remove`，没有 rehash。
- `max_entries` 个 key 放满之后，再 `put` 或 `add` **新** key 抛 `std::length_error`；已有 key 仍可更新。
- 槽位数：`max_entries = 1, 2, 3` → 8；`7, 8` → 16；`100` → 256；`1000` → 2048；`4096` → 8192；`5000` → 16384。
- `add` 溢出抛 `std::overflow_error`，值不变。
- 随机对拍：1000 个 key、30 万步 put / add，与 `std::unordered_map` 一致。
- C++ 专属测试：
  - `data()` 对 `max_entries = 1, 100, 5000` 都是 64 的倍数。
  - 类型是 move-only，移动构造是 `nothrow`：`a` 移给 `b` 之后 `a.size() == 0`、`a.capacity() == 0`，`a.get(…)` 抛 `std::logic_error`。移动赋值之后，目标原来的内容消失。
  - 从另一个线程（`std::jthread`）访问，`join` 之后主线程能读到结果。
- 性能：8000 个 key，500 万次 `add`，2 秒内且**零次 `operator new`**。

## 你怎么知道更快：测量

题目最后会问：「你怎么知道这个版本更快？」你要能说出怎么测、测到了什么、哪些结论没有测。测试里没有基准代码，这部分只考口头回答：同一串更新喂给每种实现；先预热；多轮取最好；访问序列预先生成、放在计时循环外；用 `-O2`，不开 sanitizer；输出每次操作的纳秒数。

## 边界清单

- 空表、`""` 作 key、value 为 0 / 负数 / `LLONG_MIN`、`LLONG_MAX`
- 哈希值完全相同的一大批 key；删除探测链的头和中间；删除后重新插入同一个 key
- 一直插入新 key 并删除旧 key（墓碑清理、永远留有空格）
- `std::string_view` 里含 NUL；`char` 是有符号的，`>= 0x80` 的字节
- 打包：1 个、8 个、9 个字符；小写、数字、`.`、全角字母；报文里的前导空格、中间空格、全空格、NUL
- `Key` 的 `0` 和 `~0`，以及 `static_cast<Key>(-1)`
- `off + 8` 回绕；下标为负或越界
- 完美哈希：0、1、2 个 key；集合外的 key；重复 key；`AAA..ZZZ`
- 定长表：放满后新 key、已有 key；移动后与 `close()` 后的访问
- 溢出：`add` 之后表和值都不变

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc07_ticker_hash_map          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc07_ticker_hash_map --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc07_ticker_hash_map --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc07_ticker_hash_map                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 「`std::unordered_map` 为什么慢」：每个条目一个节点、桶里存指针、两次间接寻址 → 换成开放寻址（和 Part 1、2 同构）。
- 「key 不止 8 个字符」：128 位 key（两个 `uint64_t`），或 FNV / xxHash 之类的字符串哈希加字节比较。
- 「多线程更新同一张表」：每个线程一张表最后合并；完美哈希下 value 数组固定，可以对元素做原子累加；热点冲突时分片，计数器按 64 字节对齐避免 false sharing。
- 「怎么证明哈希函数好」：看最长探测距离和平均探测次数，用真实或结构化数据（连续的三字母代码），不要只用随机串。
