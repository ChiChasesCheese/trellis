# oa01 · Job Chain 报表（C++20 版）

调度系统里的 job 首尾相接组成若干条链：一个 job 跑完触发它的 `next_job_id`。stdin 给你一份 CSV 运行日志，你为每条链输出一段统计；输入有任何不对，就只输出一行 `Malformed Input`，并且进程以状态 0 退出。这是在线笔试（OA）的形状：公开用例只有 2 个，隐藏用例几乎全打边界，所以分数在于把模糊题面变成完整的校验清单、精确输出格式、不信任输入。题目分 3 个 Part，类型和签名在 `starter.hpp`（命名空间 `jobchains`）。

## 读题前你需要知道

- **严格解析**：`std::stoi("12abc")` 返回 12，`std::stoi(" 7")` 返回 7，都不报错。`std::from_chars` 会返回「读到哪里」的指针，你必须检查它等于 token 的末尾；它不接受 `+` 号，也不跳过空白。
- **有符号溢出是未定义行为**（undefined behavior，UB）：两个很大的运行时长相加，编译器可以假设它不会发生。
- **`std::variant`**：C++ 里和 Java sealed interface 对应的封闭和类型，用 `std::visit` 处理，漏掉一种情况编译不过。

## 输入输出格式（stdin → stdout）

输入：

```text
#job_id,runtime_in_seconds,next_job_id
1,60,23
23,30,3
3,15,0
5,200,0
```

- 以 `#` 开头的行和空行忽略（表头也是 `#` 行）；逗号两侧可以有空格；换行可以是 `\r\n`；最后一行可以没有换行。
- 其余每行恰好三个十进制整数：`job_id > 0`，`runtime_in_seconds >= 0`，`next_job_id >= 0`，`0` 表示链尾。
- `job_id` 和 `next_job_id` 要放进 `int`，运行时长放进 `long long`。

输出：

```text
-
start_job: 5
last_job: 5
number_of_jobs: 1
job_chain_runtime: 00:03:20
average_job_time: 00:03:20
-
start_job: 1
last_job: 3
number_of_jobs: 3
job_chain_runtime: 00:01:45
average_job_time: 00:00:35
-
```

- 每条链一段，段前段后都有 `-`，每行以 `\n` 结尾。
- 时长格式 `hh:mm:ss`，小时至少两位、不截断（`100:00:00`）。
- `average_job_time` = 总时长 / job 数，整秒**截断**：总时长 35 秒、2 个 job，17.5 → `00:00:17`。
- 链按 `job_chain_runtime` 降序排；相同时按 `start_job` 升序。
- 没有任何 job 的输入（空 stdin、只有表头）输出一行 `-`。

## 公共类型（starter 已给出）

```cpp
struct Job   { int id; long long runtime_seconds; int next_id; /* operator== */ };
struct Chain { int start_job; int last_job; int count; long long total_seconds;
               long long average_seconds() const; /* 截断除法 */ };
struct MalformedInput : std::runtime_error { using std::runtime_error::runtime_error; };

struct Ok { std::vector<Chain> chains; };
struct Malformed { std::string reason; };
using Outcome = std::variant<Ok, Malformed>;
```

`Job` 是聚合体（aggregate），没有构造函数能拦住非法值，手工构造的 `Job{0, 5, 0}` 可以不经过 `parse` 直接进入 `chains`。

## Part 1 · 解析与格式化

| 签名 | 要求 |
|---|---|
| `std::vector<Job> parse(const std::vector<std::string>& lines)` | 跳过 `#` 行和空行；其余每行恰好三个整数；单行规则不满足抛 `MalformedInput` |
| `std::string hhmmss(long long seconds)` | `hh:mm:ss`，小时至少两位、不回绕；负数抛 `std::invalid_argument` |

- 解析接受：`1, 60, 23`、`23 ,30,0`、`007,060,000`（前导零按十进制，得到 `{7, 60, 0}`）、`5,-0,0`（`-0` 就是 0）、带 `\r` 的行、只有空白的行。
- 解析拒绝：`1,2`（少字段）、`1,2,3,4`、`a,2,3`、`1;2;3`、`0,5,0`、`-1,5,0`、`3,-5,0`、`3,5,-1`、自环 `4,1,4`、`99999999999,1,0`。
- 「C++ 专属测试：from_chars 严格性」：`1,2,3abc`、`1,2,3 4`、`+1,2,3`、`0x10,1,0`、`1e3,1,0`、`1,2.5,0`、`1,,3`、`,,`、`1,2,`、`-,1,0`、`1, - 5,0`、`1_000,1,0`、UTF-8 的阿拉伯-印度数字 `\xD9\xA1,2,3` 都要拒绝。
- 「C++ 专属测试：字节」：行里有 NUL（`1,2\0,3`）、大于 127 的字节（`\xC3\xA9,1,0`、`1,\xFF,0`、开头的 `\xA0`）要当格式错，不能触发 UB；垂直制表符 `\v` 算空白。
- 「C++ 专属测试：整数范围」：`2147483647,0,0` 合法，`2147483648,0,0` 和 `1,0,2147483648` 拒绝；运行时长 `9223372036854775807` 合法，`9223372036854775808` 和一个 32 位十进制数字的超大数拒绝。
- `hhmmss`：`0` → `00:00:00`，`59` → `00:00:59`，`3661` → `01:01:01`，`7200` → `02:00:00`，`86400` → `24:00:00`，`360000` → `100:00:00`，`LLONG_MAX` → `2562047788015215:30:07`。
- 「C++ 专属测试：`hhmmss(LLONG_MIN)`」抛 `invalid_argument`；先判断负数，不能先取相反数。

## Part 2 · 拼链与跨行校验

| 签名 | 要求 |
|---|---|
| `std::vector<Chain> chains(const std::vector<Job>& jobs)` | 拼链、检查跨行规则、排序（总时长降序，`start_job` 升序） |
| `long long Chain::average_seconds() const` | 总时长 / 个数，截断 |

跨行规则，违反任何一条抛 `MalformedInput`：

| 类别 | 例子 |
|---|---|
| 重复 `job_id` | `1,10,2` · `2,10,0` · `1,5,0` |
| 悬空 `next_job_id` | `1,10,7`（没有 7） |
| 多前驱 | `1,10,3` · `2,10,3` · `3,10,0` |
| 纯环（没有链头） | `1,10,2` · `2,10,1` |
| 好链 + 独立环 | `1,10,0` · `2,10,3` · `3,10,2` |

- 输入顺序无关：`3,15,0` · `1,60,23` · `23,30,3` 反过来读，仍然得到链 `1 → 23 → 3`。
- 样例：`1,60,23` · `23,30,3` · `3,15,0` · `5,200,0` 得到 `{5, 5, 1, 200}` 和 `{1, 3, 3, 105}`，后者平均 35。
- 并列：两条链总时长都是 10，`start_job` 为 4 的排在 9 前面。
- 两个 20 亿秒的 job 链起来总时长是 `4000000000`，所以累加必须用 `long long`。
- 「C++ 专属测试：手工构造的 Job」：`chains` 要自己重新校验，`Job{0,5,0}`、`Job{-3,5,0}`、`Job{4,1,4}`、`Job{1,-1,0}`、`Job{1,1,-2}` 都抛 `MalformedInput`。
- 「C++ 专属测试：总时长溢出」：运行时长 `LLONG_MAX` 的 job 后面再接一个 1 秒的 job，抛 `MalformedInput`，不能触发 UB；总时长恰好是 `LLONG_MAX`（`9223372036854775806` + 1）合法，此时 `average_seconds()` 是 `LLONG_MAX / 2`。
- 「C++ 专属测试：长链」：100 万个 job 的单链（行序是反的）要正常返回 `{1, 1000000, 1000000, 1000000}`，不能用递归沿链走。
- 「C++ 专属测试：输入不变」：`chains` 接受 `const` 引用，对同一输入连调两次结果相同，输入不被修改。
- `average_seconds()`：`{2, 3, 2, 35}` 得 17，`{1, 1, 1, 0}` 得 0，`{1, 3, 3, 1}` 得 0。

## Part 3 · 整题

| 签名 | 要求 |
|---|---|
| `Outcome analyze(const std::vector<std::string>&)` | `MalformedInput` 异常在这里变成 `Malformed` 值 |
| `std::vector<std::string> render(const Outcome&)` | 成功时是上面的报表行，失败时是 `{"Malformed Input"}` |
| `solve(lines)` | `render(analyze(lines))`，已给出 |
| `int run(std::istream&, std::ostream&)` | stdin → stdout 驱动，已给出；永远返回 0 |

- 官方样例：`1,60,23` · `2,23,3` · `3,12,0` · `23,30,0` 得到两段，第一段 `start_job: 1`、`last_job: 23`、`00:01:30`、平均 `00:00:45`，第二段 `start_job: 2`、`last_job: 3`、`00:00:35`、平均 `00:00:17`。
- 「C++ 专属测试：run」：输入 `garbage` 输出 `Malformed Input\n` 且返回 0；CRLF 换行、最后一行没有换行的输入照常处理；空输入输出 `-\n`。
- 「C++ 专属测试：溢出」：两条 `LLONG_MAX` 的 job 相连，整题输出 `Malformed Input`，不是崩溃。
- 「C++ 专属测试：Outcome」：`Malformed.reason` 不能为空；成功时 `Ok.chains` 是 `{{1, 1, 1, 2}}`（输入 `1,2,0`）。
- 性能测试：100 万行（平均每条链约 100 个 job、行序被打乱）整题 2 秒内。

## 边界清单

- 空输入、只有表头、只有空行
- `\r\n`、行尾空白、最后一行没有换行、行内 NUL、大于 127 的字节
- 前导 `+`、前导零、`-0`、十六进制、科学计数法、小数
- `int` 和 `long long` 的上界与上界加一
- 重复 id、悬空、多前驱、自环、纯环、好链加独立环
- 链头在最后一行；两条链总时长相同；总时长恰好 `LLONG_MAX` 与超过 `LLONG_MAX`
- 100 万个 job 的单链；平均数不能整除

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/00_oa/oa01_job_chain                  # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/00_oa/oa01_job_chain --tag part1
python3 tools/cpptest.py run   loop/rounds/00_oa/oa01_job_chain --tag cpp         # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/00_oa/oa01_job_chain                   # 全部
python3 tools/cpptest.py main  loop/rounds/00_oa/oa01_job_chain --impl work < input.txt   # 像 OA 一样 stdin → stdout
```

`main` 编译 `cpp/main.cpp`（调用 `jobchains::run(std::cin, std::cout)`），读 stdin，写 stdout，退出状态 0。`cpp/cases/` 里有 5 组 `.in` / `.out`：`official`、`crlf_no_trailing_newline`、`empty_stdin`、`garbage`、`good_chain_plus_cycle`，可以逐个用 `< cases/名字.in` 喂进去，和对应的 `.out` 逐字节比较。

测试编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 「输入是 10 GB 的流」：两遍扫描，第一遍只存 `(id, next)`，第二遍再累加时长。
- 「允许多个前驱」：链变成 DAG，问题变成关键路径（拓扑序上的最长路径）。
- 「`Malformed Input` 之外还要说明哪一行错了」：异常里带行号，`analyze` 把 `reason` 打到 stderr。
