# C15 · 面试编程题里的 I/O 与性能基础

> 目标：会快速、正确地读入文本、切分、解析数字、格式化输出；知道 `ios::sync_with_stdio(false)`、`getline`、`from_chars` 各自解决什么，以及为什么慢。

## 1. Java 对照

| Java | C++ |
|---|---|
| `BufferedReader.readLine()` | `std::getline(std::cin, line)` |
| `Scanner.nextInt()`（慢） | `std::cin >> x`（慢）；快：`from_chars` / `fread` |
| `String.split(" ")` | 手写切分（返回 `string_view`）或 `istringstream` |
| `Integer.parseInt` | `std::stoi`（抛异常）、`strtol`、`std::from_chars`（无异常、最快） |
| `System.out.println`（带刷新） | `std::cout << x << '\n'`（不刷新） |
| `String.format("%.2f")` | `std::fixed << std::setprecision(2)` 或 `printf("%.2f")` / `std::format` |

## 2. iostream 的两个性能开关

C++ 的 `cin/cout` 默认和 C 的 `stdin/stdout` **同步**（这样 `printf` 与 `cout` 混用时顺序正确），同步意味着每次操作无法缓冲。`cin` 还默认和 `cout` **绑定**（读之前先刷新 `cout`）。

```cpp
std::ios::sync_with_stdio(false);       // stop synchronising C++ streams with C stdio (do NOT mix printf/cin afterwards)
std::cin.tie(nullptr);                  // don't flush cout before every cin read
```

* `sync_with_stdio(false)`：放弃同步，必须在任何 I/O 之前调用；之后**不能再混用** `printf/scanf` 与 `cin/cout`。
* `cin.tie(nullptr)`：读之前不再刷新 `cout`（交互式程序不要用）。
* `std::endl` = `'\n'` + **强制刷新**；输出很多行时用 `'\n'`。
* 注意：这些开关的效果取决于标准库实现（GNU libstdc++ 上通常能快几倍；有些实现上 `cin >> x` 本身就慢，与开关无关）。最稳妥的快速读入是**一次读全部输入，自己解析**。

## 3. 读一行、切分、解析、聚合

典型任务：每行 `BUY AAPL 100 187.50`，汇总每个代码的净持仓和成交额，跳过注释和坏行。

```cpp
std::vector<std::string_view> split(std::string_view s, char sep = ' ') {
    std::vector<std::string_view> out;
    while (!s.empty()) {
        auto pos = s.find(sep);
        if (pos == std::string_view::npos) { out.push_back(s); break; }
        if (pos > 0) out.push_back(s.substr(0, pos));       // skips empty fields from repeated separators
        s.remove_prefix(pos + 1);
    }
    return out;                                              // views into the caller's string: no copies
}
```

* `string_view` 的切分只产生 (指针, 长度)，**不拷贝、不分配**；返回的视图在原字符串存活期间有效。
* 想要数字就别为了切分去构造 `istringstream`（每次要构造一个带 locale 的流对象）。

```cpp
struct Order { bool buy; std::string sym; long qty; double px; };

template <class T>
std::optional<T> parse_num(std::string_view s) {            // no exceptions, no locale, no allocation
    T v{};
    auto [p, ec] = std::from_chars(s.data(), s.data() + s.size(), v);
    if (ec != std::errc{} || p != s.data() + s.size()) return std::nullopt;   // reject "12abc" and ""
    return v;
}

std::optional<Order> parse_order(std::string_view line) {
    auto f = split(line);
    if (f.size() != 4 || (f[0] != "BUY" && f[0] != "SELL")) return std::nullopt;
    auto q = parse_num<long>(f[2]);
    auto p = parse_num<double>(f[3]);
    if (!q || !p) return std::nullopt;
    return Order{f[0] == "BUY", std::string(f[1]), *q, *p};
}
```

`std::from_chars`（`<charconv>`，C++17）：不抛异常、不看 locale、不分配，返回 (结束指针, 错误码)；检查 `ptr == end` 才能拒绝 `12abc`。整数和浮点数都支持（浮点支持较晚，旧编译器要用 `strtod`）。

```cpp
std::map<std::string, long> net;        // symbol -> net position
std::map<std::string, double> notional;
std::string line;
int bad = 0;
while (std::getline(std::cin, line)) {  // reads a whole line; strips the '\n'
    if (line.empty() || line[0] == '#') continue;
    if (auto o = parse_order(line)) {
        net[o->sym] += o->buy ? o->qty : -o->qty;
        notional[o->sym] += static_cast<double>(o->qty) * o->px;
    } else {
        ++bad;
        std::cerr << "skipped: " << line << "\n";
    }
}
```

* `std::getline(std::cin, line)` 读到换行（不含），EOF 返回假；循环条件直接用它。
* 混用 `cin >> x` 和 `getline`：`>>` 会把换行留在流里，下一个 `getline` 读到空行；`cin >> ws` 或统一用 `getline`。

```cpp
std::cout << std::fixed << std::setprecision(2);
for (const auto& [sym, pos] : net)
    std::cout << std::left << std::setw(6) << sym << std::right << std::setw(6) << pos << std::setw(12) << notional[sym] << '\n';   // '\n', not std::endl
std::cout << "bad lines: " << bad << '\n';
```

输入文件：

```text
BUY AAPL 100 187.50
SELL MSFT 50 410.25
BUY AAPL 25 188.00
# comment lines are skipped
SELL AAPL 60 187.75
BAD LINE

BUY NVDA 10 900.10
```

输出（坏行写到 stderr）：

```text
skipped: BAD LINE
AAPL      65    34715.00
MSFT     -50    20512.50
NVDA      10     9001.00
bad lines: 1
```

浮点输出：`std::fixed << std::setprecision(2)` 控制小数位，对 `cout` 持续生效；`std::setw` 只作用于下一个输出。金额用整数分（`long`）而不是 `double`，避免舍入误差。

## 4. 读一百万行数字，各种方法的耗时

```text
generated 1000000 lines
cin >> (synced)           568.6 ms
sum=500001066785
cin >> (no sync)          541.9 ms
sum=500001066785
scanf                      36.6 ms
sum=500001066785
fread + from_chars          7.4 ms
sum=500001066785
istringstream              40.3 ms
stoi                        9.6 ms
strtol                      5.9 ms
from_chars                  4.9 ms
sum=2000004267140
```

（各模式处理同一个 100 万行文件；最后一组是内存里解析 100 万个字符串。）读法：

* `cin >> x` 在这个实现里很慢（和开关无关）；`scanf` 快一个数量级；**一次 `fread` + `from_chars` 最快**。
* 纯解析：`istringstream` 比 `strtol`/`from_chars` 慢约 8–10 倍；`stoi` 居中（有异常和 `string` 开销）。
* 结论：大输入时 **读全部 → 手工解析**；输入不大就用 `getline` + `from_chars`，不要为了省几行代码拖慢热路径。

## 5. 其他实用点

* 读入全部：`std::istreambuf_iterator<char>` 构造 `string`，或循环 `fread` 到缓冲区。
* `std::to_string` 对整数很快；对 `double` 固定 6 位，要控制精度用 `std::format("{:.2f}", x)`（C++20）或 `snprintf`。
* `reserve` 输出缓冲：拼接大量文本时先 `std::string out; out.reserve(n);` 再最后写一次。
* `cerr` 不缓冲、写 stderr；调试信息放这里，别污染标准输出。
* 复杂度提醒：`string` 的 `+` 在循环里拼接是 O(n²)；`+=` / `append` 摊销 O(1)。

## 6. 坑

1. `while (!cin.eof()) { cin >> x; ... }`：最后一次读失败后仍然处理一次；应该 `while (cin >> x)`。
2. `sync_with_stdio(false)` 之后混用 `printf` 和 `cout` → 输出顺序错乱。
3. `int` 读入大数溢出（读失败后流进入错误状态，后续读取全部失败）；用 `long long`，必要时检查 `cin.fail()`。
4. `stoi` 对 `"12abc"` 返回 12 且不报错；`from_chars` + 检查 `ptr == end` 才严格。
5. `getline` 读到的行可能带 `\r`（Windows 换行）。
6. 对 `unordered_map<string,...>` 用 `string_view` 做 key 时，要保证原字符串活着；不确定就存 `string`。
7. 用 `endl` 输出 10 万行。

## 7. 面试官接着会问

**Q：`ios::sync_with_stdio(false)` 是做什么的？有什么副作用？**
要点：解除 C++ 流与 C stdio 的同步以允许独立缓冲；之后不能混用两套 I/O；单线程下安全；`cin.tie(nullptr)` 去掉自动刷新。

**Q：`endl` 和 `'\n'`？**
要点：endl 额外 flush；flush 是系统调用级别的慢操作。

**Q：怎么最快地解析大文本里的数字？**
要点：一次读入缓冲区，`from_chars` 或手写状态机，避免流、`string` 分配、locale；用 `string_view` 切分。

**Q：`stoi`、`strtol`、`from_chars` 区别？**
要点：异常 vs 错误码；locale；分配；严格性。

**Q：怎么读未知行数的输入？**
要点：`while (getline(...))` / `while (cin >> x)`。

**Q：输出格式化为两位小数？**
要点：`fixed << setprecision(2)`、`printf`、`std::format`。

## 8. 自测

1. 为什么 `while (!cin.eof())` 是 bug？
2. `std::from_chars` 返回什么？如何判断整个字符串都被解析？
3. 下面的区别：`cout << x << endl;` 与 `cout << x << '\n';`？
4. `cin >> n; getline(cin, line);` 读到什么？

<details><summary>答案</summary>

1. EOF 标志只在一次读取**失败**后才设置，最后一次读取失败后循环体还会被执行一遍；用 `while (cin >> x)`。
2. `from_chars_result{ptr, ec}`；`ec == errc{}` 且 `ptr == last`。
3. `endl` 多一次强制刷新。
4. 读到 `n` 之后留下的换行，`line` 是空串；先 `cin >> ws` 或 `cin.ignore()`。

</details>
