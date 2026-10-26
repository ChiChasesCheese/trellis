# hc14 · 成交日志 → VWAP（C++20 版）

交易系统每天写出一个成交日志，一行一笔：时间戳、代码、价格、数量。你要把日志读进来，按代码算成交量加权平均价（VWAP）和最低 / 最高价，坏行跳过并计数；然后改成流式：成交一笔一笔到达，只看最近 W 毫秒，随时回答某个代码的 VWAP 和名义金额最大的前 k 个代码；最后的追问是性能：一百万行日志，不为每行分配内存、不用正则。全程价格是整数定点数（fixed-point），不用浮点数。C++ 版的重点是：自己扫字符、`string_view` 不以 `\0` 结尾、`char` 有符号、有符号溢出是 UB。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `tradelog`）。

## 读题前你需要知道

- **VWAP**（volume-weighted average price）：Σ(价格 × 数量) / Σ数量，比简单平均更能代表大家实际成交在哪。
- **定点数**（fixed-point）：价格用 `long long` 存「最小单位 0.0001 的整数倍」，`187.25` 存成 `1'872'500`。浮点数存不准十进制小数，累加有误差，也不能当 key。
- **名义金额**（notional）= `price × qty`，单位同样是 0.0001。
- **滑动窗口 + 队列**：每笔成交最多入队一次、出队一次，每次操作摊还 O(1)（amortised）。
- **`std::string_view`**：只借用一段字符，不拥有，也**不保证以 `\0` 结尾**；多读一个字符就是越界读。
- **有符号溢出是 UB**：`price × qty`、累加都要用 `__builtin_mul_overflow` / `__builtin_add_overflow`，不能算完再看结果。

## 日志格式

每行四个字段，逗号分隔，没有表头：

```
ts_ms,symbol,price,qty
1000,AAPL,187.25,100
```

- `ts_ms` 毫秒时间戳；`symbol` 代码；`price` 十进制字符串，最多 4 位小数；`qty` 正整数。
- **VWAP** = Σ notional / Σ qty，结果仍是定点数，**四舍五入，半数向上**：`5 / 2 = 2.5 → 3`，`1 / 3 → 0`。舍入要写成不会溢出的形式：`q = n / v`、`r = n % v`，`r >= v - r` 时 `q + 1`（不要算 `2 * r`）。

## 公共类型（starter 已给出）

```cpp
inline constexpr long long SCALE = 10'000;
inline constexpr int MAX_SYMBOL_LEN = 10;

long long add_exact(long long a, long long b);   // 溢出抛 std::overflow_error
long long mul_exact(long long a, long long b);   // 同上
bool valid_symbol(std::string_view s) noexcept;  // 1–10 个字符，每个 A–Z、0–9 或 '.'

struct Trade {                                   // 构造函数校验，所以拿到手的 Trade 一定合法
    long long ts_ms; std::string symbol; long long price, qty;
    Trade(long long ts_ms, std::string symbol, long long price, long long qty);  // 非法字段抛 std::invalid_argument，price*qty 溢出抛 std::overflow_error
    long long notional() const noexcept;         // price * qty
};
struct SymbolStats { std::string symbol; long long count, volume, notional, vwap, min_price, max_price; };
struct Report { std::vector<SymbolStats> symbols; long long accepted, malformed; };
struct SymbolNotional { std::string symbol; long long notional; };
```

`Trade` 没有默认构造函数，非法的成交构造不出来。`Report.symbols` 按代码升序，逐字节比较：`.` < 数字 < 字母。`accepted + malformed` = 非空行数。

## Part 1 · 解析与汇总

### 一行合法的条件（其余都是坏行）

一行必须**恰好 4 个字段**（恰好 3 个逗号），逐字符匹配，**不做任何 trim**：空格、制表符、`\r` 出现在任何位置都是坏行。

| 字段 | 规则 |
|---|---|
| `ts_ms` | 1–18 个字符，全是 `0`–`9`（允许前导 0，不允许符号、小数点） |
| `symbol` | 1–10 个字符，每个是 `A`–`Z`、`0`–`9` 或 `.` |
| `price` | `D{1,9}` 或 `D{1,9}.D{1,4}`（`5.`、`.5`、`1e3`、`+1`、`-1` 都不合法），且值 > 0 |
| `qty` | 1–12 个字符，全是 `0`–`9`，且值 > 0 |
| 乘积 | `price × qty`（定点单位）必须装得进 `long long`，装不进就是坏行 |

- 长度为 0 的行直接跳过，**不计入**坏行。只含空白的行（`" "`、`"\t"`、`"\r"`）是坏行。
- 只认 ASCII 数字。不要用正则、`std::stod`、`std::stoll`、`std::from_chars`、`std::isdigit(char)`：它们对符号、空白、指数的宽容度各不相同，`isdigit` 传负的 `char` 是 UB。

### 函数

| 签名 | 要求 |
|---|---|
| `std::optional<long long> parse_price(std::string_view)` | 价格文本 → 定点数；不合法返回 `nullopt`，不抛异常 |
| `std::optional<Trade> parse_line(std::string_view)` | 不合法返回 `nullopt`，不抛异常 |
| `long long vwap(long long notional, long long volume)` | 四舍五入（半数向上），`LLONG_MAX` 附近也不能溢出；`volume <= 0` 或 `notional < 0` 抛 `std::invalid_argument` |
| `Report analyze(const std::vector<std::string>&)` | 汇总；时间顺序无关；某个代码的 `volume` 或 `notional` 累加溢出抛 `std::overflow_error` |
| `std::string format_price(long long)` | `1872500 → "187.2500"`，总是 4 位小数；负数抛 `std::invalid_argument` |
| `std::vector<std::string> render(const Report&)` | 每个代码一行，最后一行汇总 |

- `parse_price`：`"187" → 1'870'000`，`"187.25" → 1'872'500`，`"187.2501" → 1'872'501`，`"0.0001" → 1`，`"007.5" → 75'000`，`"999999999.9999" → 9'999'999'999'999`。`""`、`"."`、`".5"`、`"5."`、`"0"`、`"0.0000"`、`"1.23456"`、`"1234567890"`、`" 1"`、`"1 "`、`"1e3"` 都是 `nullopt`。
- `parse_line`：`"1000,AAPL,187.25,100"` 得 `Trade(1000, "AAPL", 1'872'500, 100)`；`"0,BRK.B,400,1"` 合法；`"1,AAPL,1,1,"`（第四个逗号）、`"1,aapl,1,1"`、`"1,AAPL,1,1\r"`、`"1,AAPL,1,0"` 都是坏行。
- 长度边界：18 位时间戳合法，19 位不合法；10 个字符的代码合法，11 个不合法；价格整数部分 9 位合法，10 位不合法；12 位数量合法，13 位不合法。
- 乘积边界：`3037000499 × 3037000499` 装得进 `long long`（`"1,A,303700.0499,3037000499"` 合法），`3037000500²` 装不进（`"1,AAPL,303700.0500,3037000500"` 是坏行）。
- `vwap`：`vwap(5,2) = 3`、`vwap(4,2) = 2`、`vwap(1,3) = 0`、`vwap(2,3) = 1`；`vwap(LLONG_MAX, 2) = 2^62`（`4'611'686'018'427'387'904`）；`vwap(LLONG_MAX, LLONG_MAX) = 1`。
- 汇总的溢出：`"1,BIG,100000000.0000,9000000"`（notional 9e18）单独一行合法；同一代码出现两次，累加溢出，`analyze` 抛 `std::overflow_error`；换成两个不同代码则不抛。单行乘积溢出的行只是坏行，不抛。
- `render` 的输出格式：

```
AAPL count=4 volume=900 notional=168515.0400 vwap=187.2389 min=187.0000 max=187.3000
MSFT count=2 volume=200 notional=82100.0000 vwap=410.5000 min=410.5000 max=410.5000
accepted=6 malformed=3
```

### 样例

```
1000,AAPL,187.25,100
1500,MSFT,410.5,50
2000,AAPL,187.3,300
oops
2500,AAPL,187,100

3000,msft,410.0,10
3500,MSFT,410.5000,150
4000,AAPL,187.25,0
4500,AAPL,187.2501,400
```

坏行 3 个：`oops`（字段数不对）、`msft`（小写）、`qty = 0`；空行不计；合法 6 行。AAPL 四笔：数量 900，notional `1'685'150'400`，VWAP `1'685'150'400 / 900 = 1'872'389.33…` → `1'872'389`，最低 `1'870'000`，最高 `1'873'000`。MSFT 两笔：`410.5` 与 `410.5000` 是同一个价格 `4'105'000`。

C++ 专属测试：

- 「视图恰好结束在缓冲区末尾」：测试把输入放进一块刚好够大的堆内存，后面没有 `\0`，多读一个字符就是 ASan 报错。`"5."`、`"1,A,1"`、`"1,"`、`","`、`",,,"` 这类被截断的输入都要正确处理。
- 高位字节和 `\0`：`"1,A\xE9,1,1"`、`"\xFF" "1,A,1,1"` 是坏行；符号里嵌入 `\0` 的 9 字节串 `"1,A\0B,1,1"`、末尾带 `\0` 的 `"1,A,1,1\0"` 也是坏行，不能当 C 字符串截断。
- `Trade` 不能默认构造，可拷贝，移动构造是 `noexcept`。

## Part 2 · 流式：滑动窗口 VWAP

| 签名 | 要求 |
|---|---|
| `explicit RollingVwap(long long window_ms)` | `window_ms >= 1`，否则抛 `std::invalid_argument` |
| `void on_trade(const Trade&)` | 先把时钟推进到 `t.ts_ms`（早于当前时钟抛 `std::invalid_argument`，这笔不计入），让过期成交出队，再计入 |
| `std::optional<long long> vwap(std::string_view symbol, long long now_ms)` | 推进时钟（`now_ms` 小于当前时钟抛 `std::invalid_argument`）；该代码在窗口内的 VWAP；窗口里没有它返回 `nullopt` |
| `long long volume(sv) const` · `notional(sv) const` | 最近一次推进之后的窗口值；没有则 0；**不**推进时钟 |
| `live_trades()` · `live_symbols()` · `now()` | 窗口内的成交数 · 窗口内的代码数 · 当前时钟（还没有事件时为 0） |

- 成交在时刻 `now` 是**活的** ⇔ `now − ts_ms < window_ms`。窗口是左开右闭 `(now − W, now]`：`now − ts_ms == W` 的成交**刚好过期**。同一时刻可以有多笔。
- 累加溢出（数量或名义金额）抛 `std::overflow_error`，**这笔不计入**：时钟已推进、过期的已清掉，其余状态不变。
- `on_trade` 与 `vwap` 要**摊还 O(1)**。每次重扫窗口的写法，在窗口常驻 10 万笔、每笔都查一次时要 10^11 步。
- 一个代码的所有成交都过期后，它从内部表里消失（`live_symbols()` 减 1），不留空条目。
- 提示（starter 已给）：一个 FIFO 放所有活的成交（最老的在队头）+ 每个代码一个累计值。

样例（`W = 1000`，价格单位 0.0001）：

| 事件 | 结果 |
|---|---|
| `on_trade(0, AAPL, 100'000, 10)`、`on_trade(400, AAPL, 120'000, 20)`、`on_trade(900, MSFT, 500'000, 5)` | |
| `vwap("AAPL", 900)` | `(1'000'000 + 2'400'000) / 30 = 113'333.33` → `113'333` |
| `on_trade(1000, AAPL, 110'000, 10)` | `t=0` 那笔刚好过期，`live_trades() == 3`，`live_symbols() == 2` |
| `vwap("AAPL", 1000)` | `3'500'000 / 30 = 116'666.67` → `116'667` |
| `vwap("MSFT", 1900)` | `1900 − 900 = 1000`：过期 → `nullopt`，`live_symbols() == 1`，`now() == 1900` |

其他要点：

- `W = 10`、`on_trade(5, A, …)`：`vwap("A", 14)` 有值，`vwap("A", 15)` 是 `nullopt`。
- `W = 1`：只有时间戳相同的成交同时存活；同一时刻 50 笔一起过期。
- 时钟倒退：`on_trade(T(49,…))` 在时钟为 50 时抛 `std::invalid_argument`，成交没有计入；同一时刻（50）可以；查询把时钟推到 60 之后，`on_trade(T(55,…))` 也要抛。
- 溢出后状态不坏：先放一笔 notional 9e18 的成交，再放同代码同样的一笔，抛 `std::overflow_error`，`live_trades()` 仍是 1，`notional()` 仍是 9e18；窗口过去之后同样大小的成交又能放进去。数量溢出同理（`qty = LLONG_MAX − 1` 之后再加 2 抛，再加 1 成功）。
- 窗口 VWAP 同样半数向上：价格 1 和 2 各一手，VWAP 是 `1.5 → 2`。

## Part 3 · 窗口内 top-k

| 签名 | 要求 |
|---|---|
| `std::vector<SymbolNotional> top_k(int k, long long now_ms)` | 窗口内名义金额最大的 k 个代码；金额降序，金额相同按代码升序；推进时钟 |

- `k < 0` 抛 `std::invalid_argument`，**先于**时钟检查；`k = 0` 返回空，但仍推进时钟；`k` 大于代码数返回全部；`k = INT_MAX` 不能被当成 `reserve` 的大小。
- 返回值是快照（按值返回的 `std::vector`）：之后的成交不改变已返回的结果。
- 例（上面的 `W = 1000` 样例，AAPL 3'400'000，MSFT 2'500'000）：`top_k(5, 900)` 得 `[AAPL 3'400'000, MSFT 2'500'000]`；`top_k(2, 1000)` 得 `[MSFT 2'500'000, AAPL 2'400'000]`；`top_k(10, 1400)` 只剩 `[MSFT 2'500'000]`；`top_k(10, 1900)` 为空。
- 并列：`ZED`、`ABC`、`MID`、`A.B` 都是 30'000，`TOP` 是 40'000，`top_k(3, 0)` 得 `TOP, A.B, ABC`。
- 实现自由：每次查询用大小为 k 的堆 O(m log k)（m = 窗口内代码数），或维护有序集合，更新 O(log m)、查询 O(k)。
- 性能：5000 个代码、50 万笔成交、每 500 笔查一次 `top_k(10, …)`，3 秒内完成。

## Part 4 · 性能追问：`analyze_fast`

| 签名 | 要求 |
|---|---|
| `Report analyze_fast(std::string_view data)` | 输入是整块字节，行以 `\n` 分隔；最后一行可以没有换行；空行跳过；其余规则同 Part 1 |

- 结果与 `analyze` 对同一批行的结果**逐字段相同**：同样的语法、同样的坏行、同样的溢出异常（`std::overflow_error`）。
- 100 万行（约 35 MB）在 1 秒内；10 万行总共分配次数少于 200（只有哈希表增长和结果，每行一个 `std::string` 就是 10 万次以上）。
- 提示（starter 已给）：symbol 最长 10 个字符，每个字符 6 位，打包进一个 `uint64_t` 当开放寻址哈希表的键。
- 边界：`""`、`"\n\n\n"`、`" \n\t\n\r\n"`（空白行是坏行）；最后一行无换行；含 `0xE9`、`0xFF`、`0x80`、`\0` 的字节，只算坏行，不能崩，视图结束在缓冲区末尾也不能越界；3 万个不同的代码（哈希表要扩容，不能丢符号）；10 个字符的代码（60 位全部用上）；随机改坏的日志（每行删 / 改 / 插一个字符）与 `analyze` 对拍，`Report` 必须相等。

## 边界清单

- 字段数多 / 少、空字段、尾逗号、第四个逗号
- 小写或非 ASCII 的代码（UTF-8 数字、全角字母）、`.` 开头的代码
- 价格 `.5`、`5.`、`0`、`0.0000`、5 位小数、10 位整数、`1e3`
- 数量 `0`、负数、小数、13 位；时间戳 19 位、带符号
- `\r` 结尾、空行与空白行的区别
- 乘积 `3037000500²` 与 `3037000499²`；同一代码两笔各 9e18
- VWAP 半数边界、`LLONG_MAX` 附近
- 窗口：`now − ts == W` 过期、同一时刻多笔、时钟倒退、查询推进时钟、窗口 1、代码过期后消失
- top-k：并列、`k` 为 0 / 负数 / `INT_MAX`
- Part 4：高位字节、`\0`、无换行结尾、符号表增长

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc14_vwap_trade_log          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc14_vwap_trade_log --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc14_vwap_trade_log --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc14_vwap_trade_log                # 全部
```

编译带 `-fsanitize=address,undefined -fno-sanitize-recover=undefined`，一触发 UB 或越界就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 价格改成整数分，或加一个 `side`（B/S）字段按买卖分别算 VWAP。
- 不要窗口，只要到目前为止的累计 VWAP。
- 把 VWAP 换成时间加权平均价（TWAP）或滑动窗口最高价（单调队列）。
- 窗口里的成交乱序到达：水位线（watermark）加允许迟到的时间。
