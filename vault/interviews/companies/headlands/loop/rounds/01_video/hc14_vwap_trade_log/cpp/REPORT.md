# hc14 · 思路与追问（C++20 版）

成交日志加工是「小而真实」的题：解析、汇总、流式化、提速。十分钟能写完，分数在追问里：规则有没有先说清楚（什么算坏行、怎么舍入、溢出怎么办、窗口边界开还是闭），流式化时有没有想到「队列 + 增量累计」，追问到性能时知不知道代价在哪。C++ 版再加一层：自己扫字符、`string_view` 的生命周期和越界、`char` 的符号、有符号溢出。下面按 Part 写清怎么写、面试官在探什么、该说出口的那句话。详细推导和可运行的示例在讲义 [[hc14_vwap_trade_log_cpp]]。

## 30 秒版本

- **先写规则再写代码**：恰好 3 个逗号、不 trim、只认 `'0'..'9'`、价格 `D{1,9}(.D{1,4})?` 且 > 0、`price × qty` 必须装得进 `long long`。
- **定点数**：价格是 `long long`，单位 0.0001；乘积用 `__builtin_mul_overflow`，累加用 `add_exact`。
- **舍入**：`q = n / v`、`r = n % v`，`r >= v - r` 才加一；不写 `2 * r`。
- **窗口**：一个 `deque` + 每个代码一个累计值，每笔成交入队出队各一次；`now − ts >= W` 过期；时钟只进不退，查询也推进时钟。
- **top-k**：全序比较器（金额降序、代码升序），`k` 先钳到代码数；`partial_sort` 是 O(m log k)。
- **字节版**：一遍扫 `unsigned char`，代码打包成 `uint64_t` 键，开放寻址表；全程不为每行分配；用随机改坏的日志与慢版对拍。

## Part 1 · 解析与汇总

**写法**

```cpp
const auto c1 = line.find(',');                       // 找三个逗号，第四个逗号 = 坏行
...
if (c3 == npos || line.find(',', c3 + 1) != npos) return std::nullopt;
const long long ts  = detail::digits(line.substr(0, c1), 18);   // 逐字符，只认 '0'..'9'
const long long qty = detail::digits(line.substr(c3 + 1), 12);
if (__builtin_mul_overflow(*price, qty, &unused)) return std::nullopt;  // 乘积溢出 = 坏行
```

`parse_price`：整数部分最多 9 位，`.` 之后 1–4 位，小数补零到 4 位后 `whole * SCALE + frac`，值必须 > 0。汇总用 `std::map<std::string, Acc>`（天然按代码升序），累加用 `add_exact`。

**面试官在探什么**

1. **为什么不用 `std::stod` / `from_chars` / 正则**：浮点会丢精度；库函数接受前导空白、`+`、`1e3`，语法比题目宽；正则每行都分配。自己扫一遍，规则一目了然。
2. **`std::isdigit(char)`**：参数是 `int`，传负的 `char` 是 UB；自己写 `c >= '0' && c <= '9'`。
3. **溢出在哪里查**：`Trade` 的构造函数里查一次 `price × qty`，所以手里有 `Trade` 就说明乘积没溢出；汇总再用 `add_exact` 查累加。有符号溢出是 UB，所以必须用 builtin，不能算完再看符号。边界是 `3037000499²`（合法）与 `3037000500²`（坏行）。
4. **舍入为什么不写 `2 * r >= v`**：`v` 接近 `LLONG_MAX` 时 `2 * r` 溢出。`vwap(LLONG_MAX, 2)` 要得到 `2^62`。
5. **空行与空白行**：长度 0 才跳过，不计数；`" "`、`"\r"` 是坏行，`\r` 结尾也是坏行。
6. **`string_view` 不以 `\0` 结尾**：扫描时每一步都要先判断 `i < size()`；多读一个字符，测试里视图恰好结束在缓冲区末尾，ASan 会直接报。
7. **高位字节与 `\0`**：`0xE9` 不是合法字符，直接拒绝；`"A\0B"` 是 3 个字符，不能当 C 字符串截断。
8. **两种错误的区别**：坏行是数据问题，计数后跳过；累加溢出是汇总本身出错，抛 `std::overflow_error`，不能静默回绕。

**该说出口的话**：「先把规则写下来：恰好三个逗号、不 trim、只认 ASCII 数字、乘积不能溢出。价格用定点整数，溢出用 builtin 检查，舍入写成不会溢出的形式。」

## Part 2 · 滑动窗口 VWAP

**写法**

```cpp
void advance(long long t) {
    if (t < now_) throw std::invalid_argument("time went backwards");
    now_ = t;
    while (!live_.empty() && now_ - live_.front().ts_ms >= window_) {
        const Trade& old = live_.front();
        auto it = by_symbol_.find(std::string_view(old.symbol));
        it->second.volume -= old.qty;
        it->second.notional -= old.notional();
        if (--it->second.count == 0) by_symbol_.erase(it);   // 过期的代码从表里消失
        live_.pop_front();                                    // 引用 old 在这之后不能再用
    }
}
```

`on_trade`：先 `advance`，再算好新的累计（`add_exact`，可能抛），最后才改状态、入队，所以溢出时这笔不计入。

**面试官在探什么**

1. **摊还 O(1)**：每笔成交入队一次、出队一次，一次 `advance` 可能弹很多，但总数不超过入队数。每次重扫窗口，窗口常驻 10 万笔时是 10^11 步。
2. **边界差一**：`now − ts == W` 必须过期，写成 `>` 会多留一笔。窗口是 `(now − W, now]`。
3. **同一时刻的多笔**：循环弹到不满足为止，不是只弹一笔。
4. **查询也推进时钟**：`vwap(sym, now)` 先 `advance`；所以查询之后再 `on_trade` 一个更早的时间要抛。
5. **失败原子性**：先算后写。溢出抛出去之后，`live_trades()` 和累计值都不能变。
6. **`deque` 与 `vector`**：队头弹出 `deque` 是 O(1)，`vector::erase(begin())` 是 O(n)。
7. **悬空引用**：持有 `live_.front()` 的引用，`pop_front()` 之后不能再读。
8. **按 `string_view` 查 `unordered_map<std::string, …>`**：默认的 `find` 只收 `std::string`，转换会分配。用透明哈希（`is_transparent` 的哈希和 `std::equal_to<>`）可以直接查。
9. **乱序到达怎么办**：约定时间不降，倒退直接拒绝。真实系统用水位线加允许迟到的时间；窗口改用按时间排序的结构，出队从 O(1) 变成 O(log n)。

**该说出口的话**：「一个队列装所有活的成交，再给每个代码一个累计值；每笔成交入队一次、出队一次，所以摊还 O(1)。`now − ts >= W` 过期，查询也推进时钟。」

## Part 3 · 窗口内 top-k

**写法**

```cpp
if (k < 0) throw std::invalid_argument("k must be >= 0");      // 先于时钟检查
advance(now_ms);
...
const auto keep = std::min<std::size_t>(static_cast<std::size_t>(k), all.size());
std::partial_sort(all.begin(), all.begin() + static_cast<std::ptrdiff_t>(keep), all.end(), best_first);
all.resize(keep);
```

比较器：金额降序，金额相同按代码升序。

**面试官在探什么**

1. **复杂度**：`partial_sort` 是 O(m log k)。要说出什么时候该换成别的：查询比成交频繁时，维护 `std::set` 按（金额，代码）排序，成交和过期各「删旧键、插新键」O(log m)，查询取前 k 个 O(k)。
2. **为什么不能只用 `priority_queue`**：金额会变小（成交过期），需要改任意元素的键，堆不支持。
3. **比较器必须是全序**：只按金额比，并列的顺序不确定；`partial_sort` 对不是严格弱序的比较器是 UB。
4. **`int` 与 `size_t`**：`k` 是 `int`，`size()` 是 `size_t`，直接比较是有符号对无符号；先显式转换再 `std::min`。`k = INT_MAX` 拿去 `reserve` 会尝试分配几十 GB。
5. **快照**：按值返回 `std::vector`，之后的成交改变不了已返回的结果；返回内部容器的引用就做不到。
6. **`k = 0` 仍然推进时钟**，`k < 0` 先于时钟检查。

**该说出口的话**：「比较器是全序：金额降序、代码升序。`k` 先钳到代码数再用，用 `partial_sort` 取前 k 个，O(m log k)；查询特别频繁时换成有序集合。」

## Part 4 · `analyze_fast`

**写法**：整块 `string_view` 转成 `const unsigned char*`，扫到 `'\n'` 切行，`line(p, e)` 逐字段推进 `p`，每一步都检查 `p < e`。

```cpp
const auto& codes = detail::symbol_codes();        // 256 项表：A–Z=1..26，0–9=27..36，'.'=37，其余 0
const unsigned code = codes[base[p]];              // base 是 const unsigned char*
if (code == 0 || ++len > MAX_SYMBOL_LEN) return false;
key = (key << 6) | code;                           // 10 个字符 = 60 位
```

开放寻址表：键 0 = 空槽，并行数组存 count / volume / notional / min / max；槽位 `(key * GOLDEN) >> (64 − log2(cap))`；装填率超过 1/2 就翻倍重哈希。整行校验通过之后才 `table.add`，所以坏行不会留下半个更新。结果最后才把键解码成字符串并排序。

**面试官在探什么**

1. **瓶颈在哪**：每行的 `std::string` 分配、正则、拷贝，不是算术。字节版没有逐行分配，测试用替换全局 `operator new` 的计数器验证：10 万行的总分配次数少于 200。
2. **`char` 有符号**：`0xE9` 当下标是负数，越界读。先转成 `unsigned char`，表正好 256 项。
3. **键为什么不会冲突**：每个字符的编码从 1 开始、没有 0，所以 `"A"` 和 `"AA"` 的键不同，键 0 只能表示空槽。
4. **溢出不用异常**：`__builtin_mul_overflow` 返回 bool，坏行多的时候抛异常很慢；汇总阶段的累加溢出才抛 `std::overflow_error`，与慢版一致。
5. **怎么证明快版和慢版一致**：对拍。随机改坏的日志（每行删 / 改 / 插一个字符）同时喂两个版本，比较整个 `Report`；再加每类坏行的穷举样例。任何一条语法规则漏掉都会暴露。
6. **最后一行没有换行**、**空行**、**表满不扩容**、**含 `\0` 的字节**：都是测试专门打的。
7. **一亿行怎么办**：先量；`mmap`；按行边界切块并行，每块自己一张表，最后合并（加法与 min / max 满足结合律，合并顺序不影响结果）；解析可以用 SIMD 找换行和逗号。

**该说出口的话**：「瓶颈是每行的分配，不是算术。我一遍扫字节，代码打包成 64 位整数当键，开放寻址表放累计值，乘积溢出用 builtin 判断；再用随机改坏的日志和慢版对拍。」

## C++ 专属陷阱

- 读 `string_view` 越过末尾：它不以 `\0` 结尾。
- `char` 当数组下标；`std::isdigit(char)` 传负值。
- `price * qty`、`n + v / 2`、`2 * r` 都可能触发有符号溢出（UB）。
- `unordered_map<std::string, …>::find(string_view)` 不能编译，写成 `std::string(sv)` 又每次分配；用透明哈希。
- 持有 `live_.front()` 的引用后 `pop_front()`。
- `int` 的 `k` 与 `size_t` 比较；`k = INT_MAX` 拿去 `reserve`。
- `Trade` 的构造函数抛异常，所以 `parse_line` 里先查乘积再构造，保证「不抛异常」的承诺。

## 和 Java 版的区别

| 话题 | Java | C++ |
|---|---|---|
| 溢出 | `Math.multiplyExact` 抛 `ArithmeticException` | `__builtin_mul_overflow`；有符号溢出是 UB，不会回绕 |
| 异常类型 | `IllegalArgumentException` / `ArithmeticException` | `std::invalid_argument` / `std::overflow_error` |
| 字符串 | `String`（不可变，UTF-16） | `std::string_view` 借用、`std::string` 拥有；注意生命周期和 `\0` |
| 字节 | `byte` 有符号，`& 0xFF` | `char` 有符号，先转 `unsigned char` |
| 值类型 | `record`，紧凑构造器校验 | `struct` + `operator== = default`；构造函数校验，无默认构造 |
| 汇总容器 | `TreeMap` | `std::map`，或 `unordered_map` 加最后排序 |
| 按视图查找 | `map.get(String)` | 需要透明哈希，否则要构造临时 `std::string` |
| 零分配的证明 | `ThreadMXBean.getThreadAllocatedBytes` | 替换全局 `operator new` 计数 |
| 数字解析 | `Character.isDigit` 会接受 Unicode 数字 | 自己写范围比较；`isdigit(char)` 传负值是 UB |
