# hc14 · Trade Log → VWAP（成交日志、滑动窗口 VWAP 与 top-k）

交易系统每天写出一个成交日志，一行一笔：时间戳、代码、价格、数量。这个任务要你把日志读进来，按代码算成交量加权平均价（VWAP）和最低 / 最高价，坏行要跳过并计数；
然后把同样的计算改成流式：成交一笔一笔到达，只看最近 W 毫秒，随时回答某个代码的 VWAP 和名义金额最大的前 k 个代码。最后的追问是性能：一百万行日志，不建 String、不用正则、不装箱。
全程价格是整数定点数（fixed-point），不用浮点数。

## 读题前你需要知道

* **VWAP**（volume-weighted average price）是什么：Σ(价格 × 数量) / Σ数量，比简单平均更能代表「大家实际成交在哪」；
* **定点数**（fixed-point）：为什么金额用 `long` 存「最小单位的整数倍」，而不是 `double`；
* **滑动窗口 + 队列**：为什么「每笔成交最多入队一次、出队一次」就能让每次操作摊还 O(1)（amortised）；
* **大小为 k 的堆**（heap）如何取前 k 个；
* **整数溢出**：`long` 乘法与累加什么时候会回绕，`Math.multiplyExact` / `addExact`（C++ 里 `__builtin_mul_overflow`）怎么检测。

## 背景

日志每行四个字段，用逗号分隔，没有表头：

```
ts_ms,symbol,price,qty
1000,AAPL,187.25,100
```

* `ts_ms`：毫秒时间戳；`symbol`：代码；`price`：价格（十进制字符串，最多 4 位小数）；`qty`：数量（正整数）。
* **价格定点化**：内部用 `long`，单位 0.0001。`187.25` 存成 `1_872_500`。
* **名义金额**（notional）= `price × qty`，单位也是 0.0001：`1_872_500 × 100 = 187_250_000`，即 18725.0000。
* **VWAP** = Σ notional / Σ qty，结果仍是定点数（单位 0.0001），**四舍五入，半数向上**（half up）：`5 / 2 = 2.5 → 3`，`1 / 3 → 0`。
  舍入要写成不会溢出的形式：`q = n / v`，`r = n % v`，`r ≥ v − r` 时 `q + 1`（不要算 `2 × r`）。

## Part 一览

| Part | 入口 | 内容 |
|---|---|---|
| 1 | `TradeLog.parseLine / parsePrice / vwap / analyze / formatPrice / render` | 解析一行、坏行计数、按代码汇总：笔数、数量、名义金额、VWAP、最低 / 最高价 |
| 2 | `RollingVwap.onTrade / vwap` | 流式：滑动时间窗口（最近 W 毫秒）上的 VWAP，摊还 O(1) |
| 3 | `RollingVwap.topK` | 窗口内名义金额最大的 k 个代码 |
| 4 | `FastLog.analyze(byte[])` | 性能追问：100 万行 < 1 s，总分配 < 4 MB，结果与 Part 1 逐字段一致 |

`Trade`、`SymbolStats`、`Report`、`RollingVwap.SymbolNotional` 在 starter 里已给出。签名以 starter 为准，这里只写语义。

## Part 1 · 解析与汇总

### 一行合法的条件（其余都是坏行）

一行必须**恰好 4 个字段**（恰好 3 个逗号），逐字符匹配，**不做任何 trim**——空格、制表符、`\r` 出现在任何位置都是坏行。

| 字段 | 规则 |
|---|---|
| `ts_ms` | 1–18 个字符，全是 `0`–`9`（允许前导 0，不允许符号、小数点） |
| `symbol` | 1–10 个字符，每个是 `A`–`Z`、`0`–`9` 或 `.`（小写、`-`、空格、非 ASCII 都不行） |
| `price` | `D{1,9}` 或 `D{1,9}.D{1,4}`（`D` 是 `0`–`9`；`5.`、`.5`、`1e3`、`+1`、`-1` 都不合法），且值 **> 0**（`0`、`0.0000` 是坏行） |
| `qty` | 1–12 个字符，全是 `0`–`9`，且值 **> 0** |
| 乘积 | `price × qty`（定点单位）必须装得进 `long`；装不进就是坏行 |

* **空行**（长度为 0 的串）直接跳过，**不计入**坏行。只含空白的行不是空行，是坏行。
* 只认 ASCII 数字：`Character.isDigit` 会接受阿拉伯-印度数字等 Unicode 数字，不要用。
* 不要用正则、`String.split`、`Double.parseDouble` / `stod` / `from_chars`：浮点会丢精度，库函数对符号、空白、指数的宽容度各不相同，也都会在每行上分配。

### 函数

* `parsePrice(String)` → `OptionalLong`：价格文本 → 定点数；不合法返回 empty，不抛异常。
* `parseLine(String)` → `Optional<Trade>`：不合法返回 empty，不抛异常。`Trade` 的构造器校验所有字段，所以拿到手的 `Trade` 一定合法。
* `vwap(long notional, long volume)`：四舍五入（半数向上）；`volume ≤ 0` 或 `notional < 0` → `IllegalArgumentException`；`Long.MAX_VALUE` 附近也不能溢出。
* `analyze(List<String> lines)` → `Report(symbols, accepted, malformed)`：
  * `symbols` 按代码升序（逐字节比较：`.` < 数字 < 字母），每项 `SymbolStats(symbol, count, volume, notional, vwap, minPrice, maxPrice)`；
  * `accepted + malformed` = 非空行数；日志时间顺序无关；
  * 某个代码的 `volume` 或 `notional` 累加溢出 → `ArithmeticException`（C++ 为 `std::overflow_error`）；
  * `lines` 为 null 或含 null → `NullPointerException`（C++ 无此规则）。
* `formatPrice(long)`：`1872500 → "187.2500"`，总是 4 位小数；负数 → `IllegalArgumentException`。
* `render(Report)`：每个代码一行，最后一行汇总：

```
AAPL count=4 volume=900 notional=168515.0400 vwap=187.2389 min=187.0000 max=187.3000
MSFT count=2 volume=200 notional=82100.0000 vwap=410.5000 min=410.5000 max=410.5000
accepted=6 malformed=3
```

### 样例

输入（中间一行是空行）：

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

* 坏行 3 个：`oops`（字段数不对）、`msft`（小写）、`qty = 0`；空行不计；合法 6 行。
* AAPL 四笔：数量 100 + 300 + 100 + 400 = 900；notional = 187_250_000 + 561_900_000 + 187_000_000 + 749_000_400 = 1_685_150_400；
  VWAP = 1_685_150_400 / 900 = 1_872_389.33… → `1872389`（187.2389）；最低 `187`（1_870_000），最高 `187.3`（1_873_000）。
* MSFT 两笔：`410.5` 与 `410.5000` 是同一个价格 `4_105_000`。

## Part 2 · 流式：滑动窗口 VWAP

面试官问：「如果日志是实时流，随时要知道某个代码最近 W 毫秒的 VWAP，怎么做？」

`RollingVwap(long windowMs)`（`windowMs ≥ 1`，否则 `IllegalArgumentException`）。成交按时间戳**不降**的顺序到达。

* 成交在时刻 `now` 是**活的** ⇔ `now − tsMs < windowMs`。窗口是左开右闭 `(now − W, now]`：`tsMs = now − W` 的成交**刚好过期**。
* `onTrade(Trade t)`：先把时钟推进到 `t.tsMs()`（早于当前时钟 → `IllegalArgumentException`，成交不计入），让过期成交出队，再计入。同一时刻可以有多笔。
  这个代码的数量或名义金额累计溢出 `long` → `ArithmeticException`，**这笔不计入**（时钟已推进、过期的已清掉，其余状态不变）。`null` → NPE。
* `vwap(symbol, nowMs)` → `OptionalLong`：把时钟推进到 `nowMs`（小于当前时钟 → `IllegalArgumentException`），返回该代码在窗口内的 VWAP；窗口里没有它 → empty。**查询也会推进时钟**。
* `volume(symbol)` / `notional(symbol)`：最近一次推进之后的窗口值，没有 → 0，不推进时钟。`liveTrades()` / `liveSymbols()` / `now()`（还没有事件时为 0）。
* 复杂度：`onTrade` 与 `vwap` **摊还 O(1)**。每次都重扫窗口的写法在「窗口里常驻 10 万笔、每笔都查一次」时要 10^11 步，会超时。
* 一个代码的所有成交过期后，它从内部表里消失（`liveSymbols()` 减 1），不留空条目。

样例（价格单位 0.0001，`W = 1000`）：

| 事件 | 结果 |
|---|---|
| `onTrade(0, AAPL, 10.0000, 10)`、`onTrade(400, AAPL, 12.0000, 20)`、`onTrade(900, MSFT, 50.0000, 5)` | |
| `vwap(AAPL, 900)` | (100000×10 + 120000×20) / 30 = 113333.33 → `113333`（11.3333） |
| `onTrade(1000, AAPL, 11.0000, 10)` | `t=0` 那笔此刻刚好过期，窗口里 AAPL 剩 `t=400`、`t=1000` 两笔 |
| `vwap(AAPL, 1000)` | 3_500_000 / 30 = 116666.67 → `116667` |
| `vwap(MSFT, 1900)` | `1900 − 900 = 1000`：过期 → empty |

## Part 3 · 窗口内 top-k

`topK(int k, long nowMs)` → `List<SymbolNotional>`：时刻 `nowMs` 窗口内**名义金额最大的 k 个代码**，金额降序，金额相同按代码升序。会推进时钟。

* `k < 0` → `IllegalArgumentException`（**先于**时钟检查）；`k = 0` → 空（仍推进时钟）；`k` 大于代码数 → 全部。
* 返回的是快照：之后的成交不改变已返回的列表（Java 里不可变）。
* 实现自由：每次查询用大小为 k 的最小堆 O(m log k)（m = 窗口内代码数）；或者维护一个有序结构，更新 O(log m)、查询 O(k)。想想各自什么时候划算。

## Part 4 · 性能追问：`FastLog`

面试官：「日志文件有一亿行。你的 `analyze` 要跑多久？瓶颈在哪？」

`FastLog.analyze(byte[] data)`（C++：`analyze_fast(std::string_view)`）：输入是整块字节，行以 `\n` 分隔（最后一行可以没有换行；空行跳过；其余规则同 Part 1）。

* 结果与 `TradeLog.analyze` 对同一批行的结果**逐字段相同**：同样的语法、同样的坏行、同样的溢出异常。
* 100 万行（约 35 MB）< 1 s；总分配 < 4 MB（Part 1 的 String 版处理 100 万行要分配约 150 MB）。
* 提示：一遍扫字节；symbol 最长 10 个字符、字母表 37 个，每个字符 6 位，正好打包进一个 `long` 当哈希键；每个代码的累计值放在并行的 `long[]` 里，开放寻址（键 0 = 空槽）；
  乘积溢出检测用 `Math.multiplyHigh`（C++ `__builtin_mul_overflow`），不要用抛异常的方式，坏行多的时候异常很慢；
  Java 的 `byte` 有符号，查表要 `b & 0xFF`；C++ 的 `char` 同理要先转 `unsigned char`。

## 边界清单（隐藏测试多半打这些）

字段数多 / 少 / 空字段；尾逗号；小写或非 ASCII 的代码（含 Unicode 数字、全角字母）；价格 `.5`、`5.`、`0`、`0.0000`、5 位小数、10 位整数；数量 `0`、负数、13 位；
18 / 19 位时间戳，10 / 11 个字符的代码；`\r` 结尾；空行与全空白行的区别；乘积刚好溢出（`3037000500²`）与刚好不溢出（`3037000499²`）；
VWAP 舍入的半数边界（`n / v = x.5`）与 `Long.MAX_VALUE`；`2 × r` 写法的溢出；同一代码两笔各 9e18 的累加；
窗口边界差一（`now − ts == W` 过期）；同一时刻多笔；时钟倒退；查询推进时钟；窗口大小 1；代码过期后消失；top-k 并列；`k` 为 0 / 负数 / 超大；
Part 4：最后一行无换行、含 `0xE9` / `0xFF` / NUL 字节、符号表增长（3 万个代码）、与 Part 1 对拍（随机改坏的日志）。

## 相关变体

* 变体可能给 `price` 为整数分（没有小数点），或加 `side`（B/S）字段按买卖分别算 VWAP；也可能不要窗口，只要「到目前为止」的累计 VWAP。
* 面试官常见追问：为什么不用 `double`？窗口里的成交乱序到达怎么办（水位线 watermark、允许迟到、缓冲重排）？top-k 每次查询都很频繁怎么办？一亿行怎么并行（分块各算各的再合并，合并是加法与取 min / max，满足结合律）？
* 把 VWAP 换成「时间加权平均价」（TWAP）或「滑动窗口最高价」（单调队列）是同一类题。

## 考什么

不是算法难度，是**把规则说清楚并一致地实现**：什么算坏行、舍入怎么定、溢出怎么处理、窗口边界开还是闭；其次是流式化时对「摊还 O(1)」的理解（队列 + 增量累计，而不是重扫）；
最后是性能意识——知道热路径上的代价来自 `String` 分配、正则、装箱，而不是算术。
