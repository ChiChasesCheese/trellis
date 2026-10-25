# hc09 · 按名义金额取 top-k 成交 / ticker（C++20 版）

一天里交易所产生很多成交事件，每个事件的名义金额（notional）等于价格乘以数量。你要取名义金额最大的 k 个事件，再扩展到按 ticker 汇总、滑动窗口里的 top-k，最后是多线程分块聚合。核心工具是大小为 k 的堆和有序集合；追问集中在 tie-break 写没写全、溢出、窗口怎么更新、多核结果是否一致。C++ 版的额外考点是**生命周期**：输入只是借来的视图，结果必须自己拥有字符串。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `toptrades`）。

## 读题前你需要知道

- **大小为 k 的堆**：取最大的 k 个要用「最差者在顶」的堆。`std::priority_queue` 的 `top()` 是比较器下**最大**的元素，所以比较器的方向要自己想清楚。
- **全序**（strict total order）：任意两个事件都分得出先后。top-k 想要可复现的结果，比较器就必须是全序。
- **有符号溢出是 UB**：`price * volume` 不能直接乘，要用 `__builtin_mul_overflow` 一类的检查（starter 已给出 `mul_exact` / `add_exact`）。
- **`std::string_view`**：只借用别人的字符，不拥有。输入数组的字符串、`std::unordered_map` 的键，都可以被借用，但借用方不能比被借用方活得久。
- **并行聚合**：每块算一张私有的表，最后合并，不需要锁。线程函数里逃出的异常会让进程直接 `std::terminate`。

## 公共类型（starter 已给出）

```cpp
using Strings = std::span<const std::string_view>;   // 三个平行数组：第 i 个事件是 (tickers[i], prices[i], volumes[i])
using Longs   = std::span<const long long>;

struct Trade {                       // 构造函数校验：index、price、volume 非负，price*volume 不溢出
    int index; std::string ticker;   // ticker 是拥有的副本：结果比输入活得久
    long long price, volume;
    long long notional() const;
};
struct TickerTotal { std::string ticker; long long notional; };   // notional < 0 抛 invalid_argument
struct Summary     { long long grand_total; std::optional<Trade> largest; };

struct BestFirst;        // 事件排序：notional 大在前 → ticker 升序（按字节）→ index 升序
struct BestTickerFirst;  // ticker 总额：总额大在前 → ticker 升序

using Totals = std::unordered_map<std::string, long long, StringHash, std::equal_to<>>;  // 支持用 string_view 直接 find
```

校验和异常类型是接口的一部分，测试按类型检查：

| 情况 | 异常 |
|---|---|
| 三个数组长度不等、`k < 0`、价格或数量为负 | `std::invalid_argument` |
| `price * volume` 或累加溢出 | `std::overflow_error` |

C++ 没有 `null` 数组和 `null` ticker，Java 版的那类错误在类型里就不存在了。

## Part 1 · top-k 事件

| 签名 | 要求 |
|---|---|
| `std::vector<Trade> top_events(Strings, Longs, Longs, int k)` | 最好的 k 个事件，最好的在前，O(n log k) 时间、O(k) 额外空间 |
| `top_events_sorted(...)` | 基线：全部排序再取前缀 |
| `top_events_partial_sort(...)` | 对事件下标用 `std::partial_sort` |
| `top_events_nth_element(...)` | 对事件下标用 `std::nth_element`，再只排前缀 |

排序规则：notional **大**的在前；相同则 ticker 字节序**升序**；再相同则下标 `index` **升序**。三条合起来是全序。

- `k` 大于事件数返回全部；`k == 0` 或空输入返回空。
- **每一个事件**都要校验并算 notional，即使它进不了 top-k：`prices = {1, LLONG_MAX}`、`volumes = {1, 2}`、`k = 1`，排在末尾的那个溢出事件也要抛 `overflow_error`。
- 输入数组不能被修改。
- 提示（来自 starter）：堆顶是保留集合里**最差**的事件；堆满之后用一次 `long long` 比较做快速拒绝，不分配内存；不要 `reserve(k)`，因为 `k` 可以是 `INT_MAX`。

### 样例

| i | ticker | price | volume | notional |
|---|---|---|---|---|
| 0 | AAPL | 18000 | 10 | 180000 |
| 1 | MSFT | 40000 | 3 | 120000 |
| 2 | AAPL | 18100 | 5 | 90500 |
| 3 | GOOG | 14000 | 9 | 126000 |
| 4 | MSFT | 40000 | 3 | 120000 |
| 5 | TSLA | 25000 | 8 | 200000 |

- `k = 3` 的下标是 `[5, 0, 3]`。
- `k = 4` 的下标是 `[5, 0, 3, 1]`：第 4 名是 1 而不是 4，二者 notional 和 ticker 都相同，下标小的在前。`k = 6` 是 `[5, 0, 3, 1, 4, 2]`。
- 四个 ticker 都是 10、数量都是 5 时：`{"ZZZ", "AAA", "MMM", "AAA"}` 的顺序是 `[1, 3, 2, 0]`。
- 数量为 0 或价格为 0 的事件合法，排在最后。
- `3037000499` 的平方放得下，`3037000500` 的平方溢出（`floor(sqrt(LLONG_MAX)) = 3037000499`）；notional 恰好等于 `LLONG_MAX` 合法。

C++ 专属测试：

- 「ticker 按字节无符号比较」：`"\xC3\xA9"`（UTF-8 的 é）排在 `"Z"` 之后，按有符号 `char` 比较会排到最前。`{"\xC3\xA9", "Z", "", "A"}` 的顺序是 `[2, 3, 1, 0]`。
- 「ticker 里的 `\0` 是名字的一部分」：`"A\0C"`、`"A\0B"`、`"A"` 是三个不同的 ticker，用 `char*` 和 `strcmp` 会看成同一个。
- 「结果拥有字符串」：输入存储释放之后，返回的 `Trade` 和 `TickerTotal` 里的 ticker 仍然有效（ASan 会抓悬空引用）。
- 「`k = INT_MAX` 不预分配」：`n = 6` 时返回 6 个，不能申请几十 GB。
- 「`nth_element` / `partial_sort` 的边界」：`k` 取 1、5、6、7（`n = 6`）时，四种实现结果一致。
- 「检查过的算术不触发 UB」：`mul_exact(1LL << 32, 1LL << 31)`（恰好 2^63）抛 `overflow_error`；`LLONG_MIN` 价格在到达乘法之前就被当作负数拒绝。
- 「`Trade` 可以廉价移动」：`std::is_nothrow_move_constructible_v<Trade>`。

性能测试（`perf`）：100 万个事件、5000 个 ticker、`k = 100`，2 秒内；严格递增的 100 万个事件（每个都进堆）、`k = 1000`，2 秒内。

## Part 2 · top-k ticker

| 签名 | 要求 |
|---|---|
| `void add_to(Totals&, std::string_view, long long amount)` | `totals[ticker] += amount`，溢出抛 `overflow_error`，**抛出时表保持原样**；命中已有键时不构造临时 `std::string` |
| `std::vector<TickerTotal> top_of(const Totals&, int k)` | 从现成的表里取 top-k，总额降序、同额 ticker 升序；`k < 0` 抛 `invalid_argument` |
| `top_tickers(Strings, Longs, Longs, int k)` | 聚合（每个事件都校验）再 `top_of` |
| `top_tickers_sorted(...)` | 同样的答案，用 `std::partial_sort` 排表里的条目 |
| `Summary summarize(Strings, Longs, Longs)` | 一趟遍历同时算总额（检查过）和最大的单个事件（`BestFirst` 序）；空输入返回 `{0, nullopt}` |

- 样例数据 `k = 2` 得 `[AAPL 270500, MSFT 240000]`（TSLA 200000、GOOG 126000 落选）。**最大的事件（TSLA）不属于最大的 ticker（AAPL）**。
- 出现过但总额为 0 的 ticker 存在，排在最后：`{"A", "B"}`、价格 `{0, 3}`、数量 `{5, 1}` 得 `[B 3, A 0]`。
- 总额相同按 ticker 升序：`{"B", "A", "C", "A"}`、价格 `{10, 4, 10, 6}`、数量全 1，`k = 3` 得 `A, B, C`。
- 每个事件都不溢出、合起来溢出也要报：同一个 ticker 的两个 `LLONG_MAX / 2 + 1`（即 2^62）。两个不同 ticker 各一个则不报。总额恰好等于 `LLONG_MAX` 合法。
- `summarize` 在 notional 和 ticker 都相同时，下标小的是最大事件。
- C++ 专属测试：`add_to` 之后改写原缓冲区，表里的键不受影响（表拥有自己的副本）；`top_of` 的结果在表销毁之后仍然有效。

性能测试（`perf`）：100 万个事件、10 万个 ticker、`k = 50`，2 秒内。

## Part 3 · 流式滑动窗口 top-k

事件按时间顺序一个个到达，只关心最近 `window` 个时间单位内的成交，随时要报出当前的 top-k ticker。

```cpp
struct Fill { long long time; std::string ticker; long long price, volume; };   // 构造函数校验，time/price/volume 非负
struct Tick { long long time; };    // 只推进时钟
struct Ask  { long long time; };    // 推进时钟，并记录一次查询
using Feed = std::variant<Fill, Tick, Ask>;
struct Answer { long long time; std::vector<TickerTotal> top; };
```

| 签名（`class SlidingTopK`） | 要求 |
|---|---|
| `SlidingTopK(long long window, int k)` | `window < 1` 或 `k < 0` 抛 `invalid_argument`。拷贝构造和拷贝赋值已 `= delete` |
| `void add(const Fill&)` | 先把时钟推进到 `f.time`（过期旧成交），再计入。时间倒退抛 `invalid_argument`（相等允许）。总额溢出抛 `overflow_error`，**状态保持原样** |
| `void advance_to(long long t)` | 只推进时钟，`t` 比当前小抛 `invalid_argument` |
| `std::vector<TickerTotal> top() const` | 窗口内 top-k，规则同 Part 2 |
| `total_of(string_view)` · `live_events()` · `distinct_tickers()` · `now()` | 某个 ticker 的窗口总额（没有则 0）、活跃成交数、不同 ticker 数、当前时间 |
| `static std::vector<Answer> replay(long long window, int k, const std::vector<Feed>&)` | 逐项处理，每个 `Ask` 产出一个 `Answer`；用 `std::visit`。`Tick` 的时间等于当前时间时什么也不做 |

- **窗口语义**：`now - time < window` 的成交是活的，`now - time >= window` 过期，**恰好差 `window` 就过期**。
- 提示（来自 starter）：活跃成交放 `std::deque`（只有队头会过期）；`unordered_map` 存每个 ticker 的总额和活跃笔数；`std::set` 按（总额降序、ticker 升序）排名，总额变了就是「删旧键、插新键」；`priority_queue` 改不了中间的元素。如果 `set` 里存的是指向 map 键的 `string_view`，类就不能拷贝，而且条目要先离开 `set` 才能删 map 节点。

### 样例（`window = 10`，`k = 2`）

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

| 查询 | 结果 | 说明 |
|---|---|---|
| `Q 5` | `[AAPL 500, MSFT 500]` | 并列按 ticker 升序 |
| `Q 12` | `[MSFT 500, AAPL 300]` | t=1 的 AAPL 200 已过期（12-1=11>=10） |
| `Q 15` | `[TSLA 100]` | MSFT(t=3)、AAPL(t=5) 过期（15-5=10>=10，边界算过期） |
| `Q 40` | `[]` | 全部过期 |

- `window = 10` 时 t=100 的成交：`advance_to(109)` 还活着，`advance_to(110)` 过期，`distinct_tickers()` 回到 0。
- `window = 1` 只保留当前时刻：同一时间戳的多笔都在，时钟走到下一刻就全部过期。
- 同一个 ticker 的老成交先过期：`total_of` 变小但 ticker 还在，`distinct_tickers()` 不变。
- 总额溢出：`window = 10`，t=0 加 2^62，t=1 再加 2^62 抛 `overflow_error`，之后 `total_of`、`live_events()`、`top()` 都和抛出前一样；到 t=10 第一笔过期，再加 2^62 就放得下。
- `replay` 里 `T 9` 之后跟 `Q 3`（时间倒退）抛 `invalid_argument`；空 feed 返回空。
- C++ 专属测试：
  - `SlidingTopK` 既不能拷贝也不能移动（`static_assert`）。
  - 「零 notional 成交」打到已有 ticker 上，总额不变，排名条目不能丢。`{A: 5*2}` 之后 `A` 再来一笔 `0 * 9`，`top()` 仍是 `[A 10]`；第一笔过期后变成 `[A 0]`，再过期才为空。
  - 几百个 ticker 反复进出一个很短的窗口（`window = 7`、300 个 ticker、4000 步），排名里不能留下指向已释放节点的视图。
  - ticker 排序按字节：`{"", "Z", "\xC3\xA9"}`。
  - 构造 `Fill` 时抛出的异常（`Fill(2, "B", LLONG_MAX, 2)`）根本到不了窗口，状态不变。

性能测试（`perf`）：100 万笔成交加 1 万次查询，`window = 5000`、2000 个 ticker、`k = 10`，2 秒内。

## Part 4 · 并行分块聚合

数据有两千万条，单线程太慢：切成块，每块聚合成自己的一张表，最后合并。

| 签名 | 要求 |
|---|---|
| `std::size_t boundary(std::size_t n, int chunks, int c)` | **已给出**：第 c 块的起点，`n * c / chunks` 在 64 位无符号里算 |
| `Totals totals_sequential(Strings, Longs, Longs)` | 顺序基线 |
| `Totals totals_chunked(Strings, Longs, Longs, int chunks)` | 每块一个 `std::jthread`、一张私有表，最后合并；`chunks < 1` 抛 `invalid_argument` |
| `Totals totals_recursive(Strings, Longs, Longs, int threshold)` | 对半切，左半交给 `std::async`，区间长度 ≤ `threshold` 直接算；`threshold < 1` 抛 `invalid_argument` |
| `Totals totals_sharded(Strings, Longs, Longs, int chunks)` | 对照组：所有线程往同一个共享结构里加。标准库没有并发哈希表，按哈希分片，每片一把 `std::mutex` |
| `std::vector<TickerTotal> top_tickers_parallel(Strings, Longs, Longs, int k, int chunks)` | `totals_chunked` 加 `top_of`；`k < 0` 抛 `invalid_argument` |

- 所有变体的结果和 `totals_sequential` **完全相同**，不论块数、线程调度、事件顺序。
- 校验与异常和顺序版一致：负数和长度不等抛 `invalid_argument`；溢出抛 `overflow_error`，来源有三种，**单个事件、某一块的部分和、合并两块时**，都要报。
- 总额恰好等于 `LLONG_MAX` 必须通过，比它大 1 必须报，不论怎么分块。`{LLONG_MAX - 6, 1, 2, 3}` 同一个 ticker 通过，最后一项换成 4 就报。
- 块数多于事件数、空输入都合法。
- 提示（来自 starter）：异常绝不能逃出线程函数体，要 catch、保存 `std::current_exception()`、请求共享的 `std::stop_source` 停止、join 之后再重抛；每处理 4096 个事件看一次 stop token；合并也会溢出。
- 样例数据的总额是 `AAPL=270500, MSFT=240000, TSLA=200000, GOOG=126000`。
- 并发测试：6 个线程同时调用三种实现，各自拿到顺序版的答案；失败的调用不影响同时进行的成功调用；一块失败后其余块被取消，函数返回前所有线程都已 join（200 次调用，进程不能被 `std::terminate` 带走）。
- C++ 专属测试：两个块同时失败（一个溢出、一个负价格），恰好抛出其中一个；快速反复调用（块数 16、事件 3 个）时，线程不能活过函数返回。

性能测试（`perf`）：200 万个事件、5 万个 ticker、8 块，三种实现各自 2 秒内；400 万个事件的 `totals_chunked` 在第一个事件就溢出时，耗时要小于完整运行的一半加 5 毫秒（取消必须真的生效）。

## 边界清单

- 空输入、`k = 0`、`k > n`、`k = INT_MAX`、单个事件
- tie：notional 相同 ticker 不同；notional 与 ticker 都相同；总额相同
- 零价格或零数量的事件和零总额的 ticker
- 溢出：`LLONG_MAX * 2`；`3037000499` 与 `3037000500` 的平方；同一 ticker 两个 2^62；恰好等于 `LLONG_MAX`
- 非法：长度不等、负价格、负数量、`k < 0`、`window = 0`、时间倒退、`chunks = 0`、`threshold = 0`
- ticker：空串、非 ASCII 字节、内嵌 `\0`
- 窗口：恰好 `window` 的边界、`window = 1`、同一时间戳多笔、总额溢出后状态不变、零 notional 成交
- 并行：块数多于事件数、块边界把同一 ticker 的两笔分开使得合并才溢出、打乱事件顺序

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc09_top_trades_by_notional          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc09_top_trades_by_notional --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc09_top_trades_by_notional --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc09_top_trades_by_notional                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 浮点价格：先转成整数 tick。`double` 累加不满足结合律，并行结果会随分块变化。
- 按 VWAP 排序：VWAP = Σ(price × volume) / Σvolume，要注意整除和分母为 0。
- 每个 ticker 内部的前 k 笔最大成交：每个 ticker 一个堆。
- 数据放不进内存：按 ticker 哈希分片，每片各自 top-k，最后 k 路归并。
