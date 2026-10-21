# oa01 · Job Chain 报表（C++20 版）

> 读者：会写 C++ 基础语法，其余从零讲。面试里任何口头回答都用英文，这里的英文术语可以直接拿去说。

## 1. 题目

调度系统的日志是一份 CSV，每行一个 job：`job_id, runtime_in_seconds, next_job_id`。`next_job_id = 0` 表示链尾。job 首尾相接成 **chain**，要求为每条链输出一段统计，链按总时长**降序**排列。输入有任何不对就只输出 `Malformed Input`，并且**进程退出码为 0**。

```
#job_id,runtime_in_seconds,next_job_id        -
1,60,23                                       start_job: 1
2,23,3                  ──────────►           last_job: 23
3,12,0                                        number_of_jobs: 2
23,30,0                                       job_chain_runtime: 00:01:30
                                              average_job_time: 00:00:45
                                              -
                                              start_job: 2
                                              last_job: 3
                                              number_of_jobs: 2
                                              job_chain_runtime: 00:00:35
                                              average_job_time: 00:00:17      ← 35/2 = 17.5，截断
                                              -
```

细节：第一行表头以 `#` 开头，空行忽略，逗号两边可以有空格；时长格式 `hh:mm:ss`，小时至少两位、不回绕（`100:00:00`）；平均值**截断**取整；总时长相同时按 `start_job` 升序（题面没说，自己定并说出来）。

这题不考算法（哈希表 + 一遍扫描，O(n)），考的是：**把模糊题面变成完整的校验清单**、精确的输出格式、不信任输入。

## 2. 思路：五步流水线

```
lines ──parse──► vector<Job> ──chains──► vector<Chain> ──render──► lines
         ▲ 单行规则              ▲ 跨行规则 + 排序
         └──────── 任何一步发现问题 → throw MalformedInput → analyze() 捕获 → "Malformed Input"
```

校验清单（面试时先口头列出来，面试官会很满意）：

| 类别 | 规则 | 在哪一步查 |
|---|---|---|
| 单行 | 恰好 3 个字段；都是十进制整数且不越界；`id > 0`；`runtime ≥ 0`；`next ≥ 0`；`next ≠ id`（自环） | `parse`（`validate`） |
| 跨行 | `id` 不重复；`next` 指向存在的 job（无悬空）；每个 job 至多一个前驱；无环 | `chains` |

**怎么查环**：每个节点入度 ≤ 1 之后，从每个"没有前驱的头"沿 `next` 走到尾，一路计数；走完后如果被访问的节点数 < 总数，剩下的节点必然在环上（环上每个节点都有前驱，所以没有任何头能走到它们）。整个过程 O(n)，不需要并查集、不需要 DFS。

## 3. 代码

### 3.1 类型

```cpp
#include <algorithm>
#include <charconv>
#include <cstdio>
#include <istream>
#include <ostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <variant>
#include <vector>

namespace jobchains {

struct Job {
    int id;
    long long runtime_seconds;
    int next_id;
    friend bool operator==(const Job&, const Job&) = default;
};

struct Chain {
    int start_job;
    int last_job;
    int count;
    long long total_seconds;
    long long average_seconds() const { return total_seconds / count; }  // integer division truncates toward zero; total >= 0 and count >= 1
    friend bool operator==(const Chain&, const Chain&) = default;
};

struct MalformedInput : std::runtime_error {
    using std::runtime_error::runtime_error;
};

/// Result of analyze(): a closed sum type.  std::variant is the C++ spelling of Java's sealed interface + records.
struct Ok { std::vector<Chain> chains; };
struct Malformed { std::string reason; };
using Outcome = std::variant<Ok, Malformed>;
```

* `Job`、`Chain` 是**聚合体**（aggregate）：没有构造函数、没有访问器，编译器自动给出拷贝、移动，`= default` 的 `operator==`（C++20）逐成员比较。
* `Outcome` 是 `std::variant<Ok, Malformed>`：C++ 对"封闭的几种结果"的写法，等价于 Java 的 sealed interface。取值用 `std::visit` / `std::get_if` / `std::holds_alternative`。
* `MalformedInput` 继承 `std::runtime_error`，`using std::runtime_error::runtime_error;` 继承构造函数。

### 3.2 解析：`from_chars` 而不是 `stoi`

```cpp
namespace detail {

template <class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

// Not std::isspace(char): passing a negative char (any byte >= 0x80 where char is signed) is undefined behaviour.
constexpr bool is_space(char c) { return c == ' ' || c == '\t' || c == '\r' || c == '\n' || c == '\v' || c == '\f'; }

constexpr std::string_view trim(std::string_view s) {
    while (!s.empty() && is_space(s.front())) s.remove_prefix(1);
    while (!s.empty() && is_space(s.back())) s.remove_suffix(1);
    return s;
}

// The WHOLE token must be a base-10 integer that fits Int.  std::from_chars never skips whitespace and never accepts a
// leading '+'; unlike std::stoi / strtol it also reports "stopped early" through the returned pointer, which we check.
template <class Int> Int parse_int(std::string_view tok, std::string_view line) {
    Int v{};
    const char* first = tok.data();
    const char* last = tok.data() + tok.size();
    auto [ptr, ec] = std::from_chars(first, last, v);
    if (ec == std::errc::result_out_of_range) throw MalformedInput("number out of range: " + std::string(line));
    if (ec != std::errc{} || ptr != last) throw MalformedInput("bad number '" + std::string(tok) + "' in line: " + std::string(line));
    return v;
}

}  // namespace detail
```

`parse_int` 要求**整个 token** 是一个能装进 `Int` 的十进制整数。`std::from_chars` 不跳空格、不接受 `+`、溢出时返回 `result_out_of_range`，并且通过返回的指针告诉你停在哪——我们检查它走到了末尾。对比见第 5 节第 1 条。

```cpp
/// Single-row rules.  Cross-row rules (duplicates, dangling, two predecessors, cycles) live in chains().
inline void validate(const Job& j) {
    if (j.id <= 0) throw MalformedInput("job_id must be positive: " + std::to_string(j.id));
    if (j.runtime_seconds < 0) throw MalformedInput("negative runtime: " + std::to_string(j.runtime_seconds));
    if (j.next_id < 0) throw MalformedInput("negative next_job_id: " + std::to_string(j.next_id));
    if (j.next_id == j.id) throw MalformedInput("self loop: " + std::to_string(j.id));
}

/// Part 1: skip blank lines and '#' lines; every other line is exactly three comma-separated integers.
inline std::vector<Job> parse(const std::vector<std::string>& lines) {
    std::vector<Job> jobs;
    jobs.reserve(lines.size());
    for (const std::string& raw : lines) {
        std::string_view line = detail::trim(raw);
        if (line.empty() || line.front() == '#') continue;
        std::string_view field[3];
        std::size_t begin = 0;
        for (int i = 0; i < 3; ++i) {
            std::size_t comma = line.find(',', begin);
            if (i < 2 ? comma == std::string_view::npos : comma != std::string_view::npos)
                throw MalformedInput("expected exactly 3 fields: " + raw);
            field[i] = detail::trim(line.substr(begin, comma == std::string_view::npos ? comma : comma - begin));
            begin = comma + 1;
        }
        Job j{detail::parse_int<int>(field[0], raw), detail::parse_int<long long>(field[1], raw), detail::parse_int<int>(field[2], raw)};
        validate(j);
        jobs.push_back(j);
    }
    return jobs;
}
```

* `string_view` 只是"指针 + 长度"的借用，`trim` / `substr` 都不拷贝；它指向 `raw`（调用者的 `vector<string>` 里的字符串），在这个函数里一直有效。
* 字段切分：前两个字段后面必须有逗号，第三个字段后面**不能**再有逗号——这样 `1,2` 和 `1,2,3,4` 都被拒绝。

### 3.3 格式化与拼链

```cpp
/// Part 1: seconds -> hh:mm:ss.  Hours are at least two digits and never wrapped (100:00:00 is fine).
inline std::string hhmmss(long long seconds) {
    if (seconds < 0) throw std::invalid_argument("negative duration: " + std::to_string(seconds));
    char buf[48];
    std::snprintf(buf, sizeof buf, "%02lld:%02lld:%02lld", seconds / 3600, seconds / 60 % 60, seconds % 60);
    return buf;
}
```

小时不 `% 24`，分钟、秒要 `% 60`（经典 bug：`7200` 秒打印成 `02:120:00`）。`long long` 的最大值也不会让 `buf[48]` 溢出（16 位小时 + `:mm:ss`）。

```cpp
/// Part 2: stitch rows into chains and enforce every cross-row rule.  O(n) expected, no recursion (a million-job chain
/// would overflow the call stack of a recursive walk).
inline std::vector<Chain> chains(const std::vector<Job>& jobs) {
    constexpr std::size_t none = static_cast<std::size_t>(-1);
    const std::size_t n = jobs.size();
    std::unordered_map<int, std::size_t> index_of;
    index_of.reserve(n * 2);
    for (std::size_t i = 0; i < n; ++i) {
        validate(jobs[i]);  // an aggregate can be built invalid by hand
        if (!index_of.emplace(jobs[i].id, i).second) throw MalformedInput("duplicate job_id " + std::to_string(jobs[i].id));
    }
    std::vector<std::size_t> next(n, none);
    std::vector<char> has_predecessor(n, 0);  // vector<bool> is a bit-packed proxy container; char is simpler and faster
    for (std::size_t i = 0; i < n; ++i) {
        if (jobs[i].next_id == 0) continue;
        auto it = index_of.find(jobs[i].next_id);
        if (it == index_of.end()) throw MalformedInput("dangling next_job_id " + std::to_string(jobs[i].next_id));
        if (has_predecessor[it->second]) throw MalformedInput("two jobs point at " + std::to_string(jobs[i].next_id));
        has_predecessor[it->second] = 1;
        next[i] = it->second;
    }
    std::vector<Chain> out;
    std::size_t visited = 0;
    for (std::size_t head = 0; head < n; ++head) {
        if (has_predecessor[head]) continue;
        int count = 0;
        long long total = 0;
        std::size_t cur = head;
        for (;;) {
            ++visited;
            ++count;
            // Signed overflow is undefined behaviour in C++ (Java would wrap, or throw with addExact): detect it.
            if (__builtin_add_overflow(total, jobs[cur].runtime_seconds, &total)) throw MalformedInput("chain runtime overflows 64 bits");
            if (next[cur] == none) break;
            cur = next[cur];
        }
        out.push_back(Chain{jobs[head].id, jobs[cur].id, count, total});
    }
    // Every node has in-degree <= 1 and was walked from a head; a node nobody walked sits on a cycle.
    if (visited != n) throw MalformedInput("cycle among jobs not reachable from a head");
    std::ranges::sort(out, [](const Chain& a, const Chain& b) {
        return a.total_seconds != b.total_seconds ? a.total_seconds > b.total_seconds : a.start_job < b.start_job;
    });
    return out;
}
```

读这段的要点：

1. `index_of` 把 `id` 映射到 `jobs` 里的**下标**，之后全用下标（`next` 数组、`has_predecessor` 数组）——比存指针安全（vector 不动就不悬空），也更省内存。
2. `reserve(n * 2)` 避免 rehash。
3. `validate(jobs[i])` 在 `chains` 里再调一次：`Job` 是聚合体，调用者可以不经过 `parse` 手工造出 `Job{0, 5, 0}`。
4. `__builtin_add_overflow` 检测累加溢出（有符号溢出是未定义行为，见第 5 节）。这里把"总时长超出 64 位"判为 Malformed——题面没给范围，这是一个必须说出口的假设。
5. 排序比较器必须是**严格弱序**：先比总时长（降序），相等再比 `start_job`（升序）。

### 3.4 分析、渲染、驱动

```cpp
/// Part 3: the whole analysis; a MalformedInput exception becomes a Malformed value.
inline Outcome analyze(const std::vector<std::string>& lines) {
    try {
        return Ok{chains(parse(lines))};
    } catch (const MalformedInput& e) {
        return Malformed{e.what()};
    }
}

/// Part 3: render.  std::visit needs a branch for every alternative, so adding a third Outcome breaks the build here.
inline std::vector<std::string> render(const Outcome& outcome) {
    return std::visit(detail::overloaded{
        [](const Malformed&) { return std::vector<std::string>{"Malformed Input"}; },
        [](const Ok& ok) {
            std::vector<std::string> lines{"-"};
            for (const Chain& c : ok.chains) {
                lines.push_back("start_job: " + std::to_string(c.start_job));
                lines.push_back("last_job: " + std::to_string(c.last_job));
                lines.push_back("number_of_jobs: " + std::to_string(c.count));
                lines.push_back("job_chain_runtime: " + hhmmss(c.total_seconds));
                lines.push_back("average_job_time: " + hhmmss(c.average_seconds()));
                lines.push_back("-");
            }
            return lines;
        }}, outcome);
}

inline std::vector<std::string> solve(const std::vector<std::string>& lines) { return render(analyze(lines)); }

/// stdin -> stdout driver.  The statement demands exit status 0 even for Malformed Input, so this always returns 0.
inline int run(std::istream& in, std::ostream& out) {
    std::vector<std::string> lines;
    for (std::string line; std::getline(in, line);) lines.push_back(std::move(line));
    for (const std::string& l : solve(lines)) out << l << '\n';
    return 0;
}

}  // namespace jobchains
```

* `std::visit(overloaded{...}, outcome)`：每个 alternative 一个 lambda。**少写一个分支编译不过**——和 sealed + switch 一样的穷尽性保证。
* `run` 总是返回 0：题面要求非法输入也 exit zero。

`main.cpp`：

```cpp
// HackerRank shape: stdin -> stdout.  The statement requires exit status 0 even when the input is malformed.
#include <iostream>

#include IMPL_HEADER

int main() {
    std::ios::sync_with_stdio(false);
    return jobchains::run(std::cin, std::cout);
}
```

`sync_with_stdio(false)` 关掉 C 流同步，大输入读得更快；输出用 `'\n'` 而不是 `std::endl`（后者每次都 flush）。

## 4. 和 Java 版相比变了什么

| Java | C++ | 为什么 |
|---|---|---|
| `record Job` + 紧凑构造器校验 | `struct Job` + 独立的 `validate()` | 聚合体能被手工造出非法值，所以每个入口都要验 |
| `sealed interface Outcome` + 模式匹配 `switch` | `std::variant` + `std::visit(overloaded{…})` | 同样是封闭类型、同样编译期穷尽 |
| `Integer.parseInt` + 正则 | `std::from_chars` + 检查结束指针 | 标准库里没有"整串必须是整数"的现成函数，`stoi` 会放过尾巴 |
| `Math.addExact` 抛异常 | `__builtin_add_overflow` | 有符号溢出在 C++ 里是 UB，不是回绕也不是异常 |
| `HashMap<Integer, Job>` | `unordered_map<int, size_t>`（下标） | 值语义，没有 GC：不要保存会悬空的指针 |
| `String` 切片会拷贝 | `string_view` 零拷贝借用 | 代价：你要自己保证被借用的字符串活得比 view 久 |
| GC 兜底 | RAII（`vector` / `string` 析构自动释放） | 没有手写 `new` / `delete` |

## 5. 陷阱

1. **`stoi` / `atoi` / `strtol` 太宽松。** 下面的程序输出什么？

```cpp
#include <cctype>
#include <charconv>
#include <iostream>
#include <string>
#include <string_view>

// Returns true only if the WHOLE token is a base-10 int that fits.
bool strict_int(std::string_view tok, int& out) {
    auto [ptr, ec] = std::from_chars(tok.data(), tok.data() + tok.size(), out);
    return ec == std::errc{} && ptr == tok.data() + tok.size();
}

int main() {
    // std::stoi stops at the first bad character and does not tell you.
    std::cout << "stoi(\"12abc\") = " << std::stoi("12abc") << "\n";
    std::cout << "stoi(\" 7\")    = " << std::stoi(" 7") << "\n";
    std::cout << "stoi(\"+5\")    = " << std::stoi("+5") << "\n";
    try { (void)std::stoi("99999999999"); } catch (const std::out_of_range&) { std::cout << "stoi(\"99999999999\") throws out_of_range\n"; }

    int v = 0;
    for (std::string_view s : {"12", "12abc", " 7", "+5", "-5", "99999999999", ""})
        std::cout << "strict_int(\"" << s << "\") = " << std::boolalpha << strict_int(s, v) << "\n";

    // std::isspace takes an int that must be unsigned-char range or EOF: a plain char >= 0x80 is negative = UB.
    char c = static_cast<char>(0xE9);
    std::cout << "safe: " << (std::isspace(static_cast<unsigned char>(c)) != 0) << "\n";
}
```

输出：`stoi("12abc")` 是 `12`，`stoi(" 7")` 是 `7`，`stoi("+5")` 是 `5`；而 `strict_int` 对 `"12abc"`、`" 7"`、`"+5"`、越界数、空串都返回 `false`。`atoi` 连错误都不报告；`strtol` 要手工看 `endptr` 和 `errno`。

2. **`std::isspace(char)` 是未定义行为。** 参数必须在 `unsigned char` 范围内或为 `EOF`；`char` 在 ARM / x86 上通常有符号，字节 `0xE9`（UTF-8 的一部分）会变成负数。要么先转 `unsigned char`（如上面的 `safe:` 一行），要么像这里这样自己写 `is_space`（只认 ASCII 空白）。

3. **有符号整数溢出是未定义行为。** `total += runtime` 在两个 `LLONG_MAX` 相加时，编译器可以假设它不会发生——可能回绕，也可能把后面的判断整个优化掉。用 UBSan（`-fsanitize=undefined`）能抓到。无符号溢出是定义良好的回绕，所以"想要回绕"时用无符号类型。检查加法的三种正确写法：

```cpp
// Signed overflow is undefined behaviour in C++.  Three correct ways to add with a check.
#include <climits>
#include <iostream>
#include <optional>

// 1. The compiler builtin (clang, gcc): the best answer.
std::optional<long long> add_builtin(long long a, long long b) {
    long long s;
    if (__builtin_add_overflow(a, b, &s)) return std::nullopt;
    return s;
}

// 2. Test BEFORE adding, using only operations that cannot overflow.
std::optional<long long> add_precheck(long long a, long long b) {
    if (b > 0 && a > LLONG_MAX - b) return std::nullopt;
    if (b < 0 && a < LLONG_MIN - b) return std::nullopt;
    return a + b;
}

// 3. Widen: the exact sum of two long longs always fits __int128.
std::optional<long long> add_wide(long long a, long long b) {
    __int128 s = static_cast<__int128>(a) + b;
    if (s < LLONG_MIN || s > LLONG_MAX) return std::nullopt;
    return static_cast<long long>(s);
}

int main() {
    for (auto f : {add_builtin, add_precheck, add_wide}) {
        auto r1 = f(LLONG_MAX, 1), r2 = f(LLONG_MIN, -1), r3 = f(LLONG_MAX, LLONG_MIN);
        std::cout << r1.has_value() << r2.has_value() << (r3 ? *r3 : 0) << "\n";   // 0 0 -1
    }
}
```

4. **`vector<bool>` 不是 `vector` of `bool`。** 它是按位压缩的特化，`operator[]` 返回代理对象，不能取地址。需要一排标志位时用 `vector<char>`（这里的 `has_predecessor`）。

5. **比较器必须是严格弱序。** `a.total >= b.total` 这种带 `=` 的比较器会让 `std::sort` 越界读（UB）。正确写法：

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

struct Chain { int start; long long total; };

int main() {
    std::vector<Chain> v{{9, 10}, {4, 10}, {1, 105}, {5, 200}};
    // Strict weak ordering: total descending, ties by start ascending.  `<=` here would be undefined behaviour.
    std::ranges::sort(v, [](const Chain& a, const Chain& b) {
        return a.total != b.total ? a.total > b.total : a.start < b.start;
    });
    for (auto& c : v) std::cout << c.start << ":" << c.total << " ";
    std::cout << "\n";
}
```

6. **不要递归地沿链走。** 一条链可以有一百万个 job，递归每层一个栈帧，默认 8 MiB 的栈撑不住。循环版 O(1) 栈。

7. **`unordered_map::operator[]` 会插入。** 只想查就用 `find`；想"没有才插入"用 `emplace(...).second`（这里用来查重复 id）。

8. **输入的边角。** Windows 换行 `\r\n`（所以 `trim` 要吃掉 `\r`）；最后一行没有换行；完全空的输入（输出一个 `-`，因为没有任何链）；行内含 `\0`。

## 6. 面试官会追问什么（senior）

**Q1. 为什么用异常，而不是返回错误码 / `std::optional`？**
非法输入是少数情况，异常让正常路径不带错误检查，一个 `catch` 就能把所有校验失败统一成 `Malformed`。如果非法行是常态（每秒百万行里很多坏行），异常很慢（每次几微秒），改用返回值：`std::optional`、`std::variant<Job, Error>`，或 C++23 的 `std::expected<Job, Error>`。能说出取舍就够了。

**Q2. 一百万行输入，内存和时间怎么算？**
`vector<string>` 每个 `string` 在 libc++ 里 24 字节，且 ≤ 22 个字符的串内联存放（SSO），不额外分配；`unordered_map` 每个节点一次堆分配，是最大的开销。更快的做法：id 先排序去重得到稠密下标，用 `vector` + 二分，或开放寻址哈希表。时间是 O(n) 期望，加最后的 O(c log c) 排序（c = 链数）。

**Q3. 能不能边读边处理，不存所有行？**
解析可以流式做（逐行 `getline`），但拼链要知道全部 job 才能判断悬空、多前驱、环，所以 job 本身要存；省掉的只是原始字符串。

**Q4. `string_view` 什么时候会悬空？**
`std::string_view v = make_string();`（指向临时对象）；把 view 存进长寿命容器而底层字符串先析构；`string` 被修改后重新分配。这里的 view 都只在 `parse` 内部使用，底层是调用者持有的 `lines`。

**Q5. `unordered_map` 的最坏情况？**
所有 key 落进同一个桶时退化为 O(n)。对 `int` 的标准库哈希是恒等映射，对抗性输入可以构造冲突；比赛里常用自定义哈希（splitmix64）。面试里说出"期望 O(1)、最坏 O(n)、可以换排序 + 二分得到确定的 O(n log n)"即可。

**Q6. 怎么测试？**
单行规则、跨行规则、格式、边界（空、单条、`INT_MAX`、`LLONG_MAX`）、CRLF、随机大输入对照暴力解；全部在 `-fsanitize=address,undefined` 下跑。

## 7. 自测

1. `std::stoi("12abc")` 返回什么？为什么这里不能用它？
2. `chains()` 已经被 `parse()` 校验过的数据喂过，为什么还要在里面再调一次 `validate`？
3. 两个 `runtime = LLONG_MAX` 的 job 在一条链上，`total += runtime` 会发生什么？应该怎么写？
4. 比较器写成 `return a.total >= b.total;` 有什么问题？
5. 空输入（0 行）应该输出什么？
6. 为什么 `has_predecessor` 用 `vector<char>` 而不是 `vector<bool>`？

<details><summary>答案</summary>

1. `12`。它在第一个非法字符处静默停止；这里要求整行必须合法，`"12abc"` 应该被拒绝。用 `from_chars` 并检查结束指针。
2. `Job` 是聚合体，别的调用者可以直接构造 `Job{0, 5, 0}` 传给 `chains()`；不能假设数据一定经过了 `parse`。
3. 有符号溢出是 UB：UBSan 报错，优化后的代码可能回绕成负数。用 `__builtin_add_overflow` 检测，然后按需求处理（这里判为 Malformed）。
4. 不满足严格弱序（相等的元素 `comp(a,a)` 返回 true），`std::sort` 可能越界访问，是 UB。要写 `>`。
5. 只有一行 `-`（没有任何链，报告仍然格式良好）。
6. `vector<bool>` 是位压缩的代理容器：访问慢、不能取元素地址、不是线程安全的"相邻元素独立"；用一个字节存一个标志更简单。

</details>
