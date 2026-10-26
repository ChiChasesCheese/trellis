# hc14 · 解法与原理

这个题没有难算法。Part 1 是切字符串加两个累加器，Part 2 是「队列加运行和」。面试官在看三件事：坏行有没有处理干净，取整规则有没有先说清楚，窗口边界差一个毫秒时你会不会写错。

## 开场 3 分钟：先把问题问清楚

你可以这样说：

> "I'll keep, per symbol, the sum of price times quantity and the sum of quantity, and divide at the end. Is the price an integer number of ticks or a decimal string? Should I round the division down, or to nearest? And what counts as a malformed line — wrong field count, non-numeric fields, zero quantity?"

面试官通常会说：价格是整数 tick，先向下取整，字段数不对、解析失败、价格或数量不是正数都算坏行。

## Part 1 · 解析与按代码 VWAP

**思路**：每行按逗号切成 4 段；4 段都合法才处理，否则 `malformed++`。每个代码存两个数：`Σ(price × qty)` 和 `Σqty`；最后一除。

**原理：为什么存两个和而不是存每笔成交**

VWAP 是比值，只依赖这两个和，所以不用把成交留着。多一笔成交只是两个加法。

**坑**：Java 的 `split(",")` 默认会丢掉末尾的空字符串，`1,AAPL,100,` 会被切成 3 段，字段数检查恰好抓到；但 `1,AAPL,,` 会被切成 2 段。写 `split(",", -1)` 保留所有空字段，行为才一致。C++ 里 `std::from_chars` 读完一个字段后要检查指针是不是到了末尾，否则 `12abc` 会被当成 12。

**Java**

```java
public class TradeLog {
    private final Map<String, long[]> sums = new HashMap<>();  // symbol -> {Σ price*qty, Σ qty}
    private int malformed;

    public void add(String line) {
        String[] f = line.split(",", -1);
        try {
            if (f.length != 4 || f[1].isEmpty()) throw new NumberFormatException();
            Long.parseLong(f[0]);
            long price = Long.parseLong(f[2]), qty = Long.parseLong(f[3]);
            if (price <= 0 || qty <= 0) throw new NumberFormatException();
            long[] s = sums.computeIfAbsent(f[1], k -> new long[2]);
            s[0] += price * qty;
            s[1] += qty;
        } catch (NumberFormatException e) {
            malformed++;
        }
    }

    public int malformed() { return malformed; }

    public Map<String, Long> vwap() {
        Map<String, Long> out = new HashMap<>();
        sums.forEach((sym, s) -> out.put(sym, s[0] / s[1]));
        return out;
    }
}
```

**C++**

```cpp
inline bool to_num(const std::string& s, long long& v) {
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    return ec == std::errc() && p == s.data() + s.size();  // 整个字段都被读完才算数字
}

class TradeLog {
    std::map<std::string, std::pair<long long, long long>> sums_;  // symbol -> {sum price*qty, sum qty}
    int malformed_ = 0;

public:
    void add(const std::string& line) {
        std::vector<std::string> f;
        size_t start = 0, pos;
        while ((pos = line.find(',', start)) != std::string::npos) {
            f.push_back(line.substr(start, pos - start));
            start = pos + 1;
        }
        f.push_back(line.substr(start));
        long long ts, price, qty;
        if (f.size() != 4 || f[1].empty() || !to_num(f[0], ts) || !to_num(f[2], price) ||
            !to_num(f[3], qty) || price <= 0 || qty <= 0) {
            ++malformed_;
            return;
        }
        auto& s = sums_[f[1]];
        s.first += price * qty;
        s.second += qty;
    }

    int malformed() const { return malformed_; }

    std::map<std::string, long long> vwap() const {
        std::map<std::string, long long> out;
        for (const auto& [sym, s] : sums_) out[sym] = s.first / s.second;
        return out;
    }
};
```

复杂度：每行 O(L)（L 是行长），`vwap()` 是 O(S)（S 是代码数）。

## Part 2 · 滑动窗口 VWAP

**思路**：每个代码一个窗口对象：一个队列（队头最老）加 `notional`、`volume` 两个运行和。`onTrade` 把成交放进队尾并加到两个和里；`vwap` 先从队头弹出所有 `now - ts >= windowMs` 的成交，从和里减掉，再用 `notional / volume`。

**原理：为什么是均摊 O(1)**

每笔成交只会入队一次、出队一次，弹出的总次数不会超过压入的总次数。所以 n 次操作总共最多 n 次弹出，平均到每次操作是常数。如果每次查询都重扫窗口，窗口里常驻 m 笔、查 q 次就是 O(m·q)。

**原理：边界为什么是 `>=`**

窗口是 `(now - W, now]`，左开右闭。`ts = now - W` 的成交已经不在窗口里，所以过期条件是 `now - ts >= W`。写成 `>` 会多算一个毫秒的成交。

**Java**

```java
private static class Window {
    final Deque<long[]> trades = new ArrayDeque<>();  // {ts, price, qty}，队头最老
    long notional, volume;
}
private final long windowMs;
private final Map<String, Window> windows = new HashMap<>();

public void onTrade(long ts, String symbol, long price, long qty) {
    Window w = windows.computeIfAbsent(symbol, k -> new Window());
    w.trades.addLast(new long[] {ts, price, qty});
    w.notional += price * qty;
    w.volume += qty;
}

public OptionalLong vwap(String symbol, long nowMs) {
    Window w = windows.get(symbol);
    if (w == null) return OptionalLong.empty();
    while (!w.trades.isEmpty() && nowMs - w.trades.peekFirst()[0] >= windowMs) {
        long[] t = w.trades.pollFirst();
        w.notional -= t[1] * t[2];
        w.volume -= t[2];
    }
    return w.volume == 0 ? OptionalLong.empty() : OptionalLong.of(w.notional / w.volume);
}
```

构造函数里检查 `windowMs < 1` 并抛 `IllegalArgumentException`。

**C++**

```cpp
struct Trade { long long ts, price, qty; };
struct Window {
    std::deque<Trade> trades;  // 队头最老
    long long notional = 0, volume = 0;
};
long long window_;
std::unordered_map<std::string, Window> windows_;

void on_trade(long long ts, const std::string& symbol, long long price, long long qty) {
    Window& w = windows_[symbol];
    w.trades.push_back({ts, price, qty});
    w.notional += price * qty;
    w.volume += qty;
}

std::optional<long long> vwap(const std::string& symbol, long long now_ms) {
    auto it = windows_.find(symbol);
    if (it == windows_.end()) return std::nullopt;
    Window& w = it->second;
    while (!w.trades.empty() && now_ms - w.trades.front().ts >= window_) {
        w.notional -= w.trades.front().price * w.trades.front().qty;
        w.volume -= w.trades.front().qty;
        w.trades.pop_front();
    }
    if (w.volume == 0) return std::nullopt;
    return w.notional / w.volume;
}
```

构造函数里检查 `window_ms < 1` 并抛 `std::invalid_argument`。

复杂度：`onTrade` O(1)；`vwap` 均摊 O(1)；空间 O(窗口内成交数)。

## Part 3 · 口头追问和回答

**1. 价格里的小数怎么处理？为什么不用 `double`？**

把价格乘以最小价位的倒数，变成整数 tick。例如最小价位 0.0001，`187.25` 存成 `1_872_500`。解析时按字符手动处理小数点，不经过浮点数。`double` 的问题是 0.1 这类十进制小数无法精确表示，累加几百万次后误差会积累；整数加法是精确的，也满足结合律，求和顺序不影响结果。

**2. 除法怎么做四舍五入而不是向下取整？**

先说规则：半数向上（half up）。写成 `q = n / v`，`r = n % v`，如果 `r >= v - r` 就 `q + 1`。不要写 `(2 * n + v) / (2 * v)`，也不要算 `2 * r`，因为 `n` 或 `r` 大的时候乘 2 会溢出；`v - r` 不会。

**3. `price × qty` 和累加会溢出吗？怎么检测？**

会。`long` 最大约 9.2 × 10^18，价格和数量都很大、或者累加了很多笔，乘积和累加和都可能超出。Java 用 `Math.multiplyExact` / `Math.addExact`，溢出时抛 `ArithmeticException`；C++ 有符号溢出是未定义行为（UB），要用 `__builtin_mul_overflow` / `__builtin_add_overflow`，不能「算完再看是不是负数」。遇到溢出可以把这一行当坏行跳过，也可以让整个计算失败，要和面试官约定。如果业务上确实会超，把累加改成 128 位整数（C++ `__int128`，Java `BigInteger`）。

**4. 窗口内名义金额最大的前 k 个代码怎么取？**

每个代码的窗口里已经有 `notional` 这个运行和。遍历所有代码（先各自弹掉过期成交），用一个大小为 k 的最小堆：堆没满就放入，满了就和堆顶比，大于堆顶才替换。时间 O(S log k)，S 是代码数，空间 O(k)。S 不大时直接全排序 O(S log S) 也行，先写简单的。

**5. 一百万行日志怎么读得又快又省？**

瓶颈是每行建 `String`、`split` 建数组、`parseLong` 再切子串。改成：一次把文件读成字节数组（或用缓冲读），自己按字节扫描，遇到逗号和换行就切，手写数字解析（`v = v * 10 + (c - '0')`）；代码名用一个 `HashMap` 映射到整数编号，之后所有累加用数组下标。这样每行没有分配。先写对再优化，面试里说出这几步就够。

**6. 为什么不是每次查询都重扫窗口？**

重扫一次是 O(窗口内成交数)。窗口里常驻 m 笔、每笔到达后都查一次，总共 O(m·n)；n = 10^5、m = 10^5 就是 10^10 级别，会超时。运行和加队列让每笔成交只被加一次、减一次。

## 常见错误

1. `split(",")` 不带 `-1`：末尾空字段被吞掉，字段数检查失效。
2. 过期条件写成 `now - ts > windowMs`：边界上的那一笔多算了。
3. 查询时不弹过期成交，只在 `onTrade` 里弹：长时间没有新成交时，旧成交一直留在窗口里。
4. 只在 `volume` 里减、忘了在 `notional` 里减（或反过来）：VWAP 悄悄漂移。
5. 窗口清空后还做 `notional / volume`：除以 0，该返回空。
6. 价格用 `double` 累加：结果和整数版本差几个 tick，测试对不上。
