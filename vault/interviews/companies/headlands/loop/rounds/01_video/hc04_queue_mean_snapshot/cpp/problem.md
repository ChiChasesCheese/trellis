# hc04 · Queue Mean + 修正快照（C++20 版）

面试官让你实现一个先进先出（FIFO）队列，支持 `push`、`pop` 和 `get_mean`（所有元素的平均数）。第一版几分钟能写完，追问才是重点：均值要 O(1)、不能用 `double` 累加、`long long` 的和会溢出、空队列怎么办、「快照」到底是拷贝还是共享、读者线程怎么不加锁。C++ 版把这些追问落到几件具体的事上：有符号溢出和 `-LLONG_MIN` 是未定义行为（UB）、编译器生成的移动构造函数不会清空源对象、`vector::push_back` 会让旧引用悬空、普通变量被并发读写是数据竞争。题目分 4 个 Part，签名都在 `starter.hpp`（命名空间 `qmean`）。

## 读题前你需要知道

- **环形缓冲区**（ring buffer）：一块定长数组加一个 `head` 下标，队尾写在 `(head + size) % 容量`，满了就扩容。这样 push 和 pop 都是 O(1)，元素在内存里连续。
- **`__int128`**：clang / gcc 提供的 128 位整数。`n` 个 `long long` 之和的绝对值不超过 `n · 2^63`，所以放得进 128 位；它在这套题里充当 Java 的 `BigInteger`。
- **持久化数据结构**（persistent data structure）：每次修改都产生一个新版本，旧版本永远不变，而且不整份复制数据。
- **数据竞争**（data race）：一个线程写、另一个线程同时读同一个普通变量，是 UB，不只是「读到旧值」。

## 公共类型（starter 已给出）

```cpp
using i128 = __int128;
using u128 = unsigned __int128;
std::string i128_to_string(i128 v);   // libc++ 没有 128 位的 operator<<

struct Push    { long long value; };
struct Pop     {};
struct Query   {};
struct Correct { std::vector<long long> contents; };   // 修正快照：丢掉之前的历史，队列变成 contents（队头在前）
using Event = std::variant<Push, Pop, Query, Correct>;

struct Value { Mean mean; };
struct Empty {};
using Answer = std::variant<Value, Empty>;
```

这些类型都带 `operator==`（`= default`），测试直接比较它们。

## Part 1 · 队列 + 均值

| 签名 | 要求 |
|---|---|
| `Mean(i128 n, long long d)` | 精确均值，约分后的分数；分母恒正，符号只放分子；`d <= 0` 抛 `std::invalid_argument`；零是 `0/1` |
| `double Mean::to_double() const` | 最接近精确值的 `double`，整个过程只舍入一次 |
| `void QueueMean::push(long long)` · `long long pop()` | O(1) 均摊；空队列 `pop` 抛 `std::out_of_range` |
| `Mean mean() const` | 精确均值；空队列抛 `std::out_of_range` |
| `double get_mean() const` | 等于 `mean().to_double()`；空队列抛 `std::out_of_range` |
| `size() · empty() · sum()` | 辅助；`sum()` 返回 `i128` |

- 样例：依次 `push 1, 2, 3`，`get_mean() = 2.0`；`push 4` 后 `2.5`；`pop()` 返回 `1`，`get_mean() = 3.0`，`size() = 3`。
- 约分：`Mean(6, 4) == Mean(3, 2)`；`push -1, -2` 后 `mean() == Mean(-3, 2)`；`push -3, 3` 后均值是 `0/1`。
- 不能用 `double` 累加：先 push `10'000'000'000'000'000`（1e16）、`1`、`1`，再 pop 一次，均值必须是 `1/1`。
- 和会溢出 `long long`：push 两个 `LLONG_MAX`，和是 2^64 − 2，均值是 `LLONG_MAX/1`；再 push 一个 `LLONG_MAX`、弹光三个、push `5`，均值必须回到 `5/1`，累加器不能「卡」在大数上。
- 两个 `LLONG_MIN` 加一个 `LLONG_MAX`，和是 −2^63 − 1，均值是 `Mean(LLONG_MIN − 1, 3)`。
- 最近的 `double`：`push LLONG_MAX, LLONG_MAX − 1`，精确均值 `LLONG_MAX − 0.5` 不是 `double`，最近的是 `2^63`。`push 2^53` 后 `get_mean() == 2^53`；再 push `1`，和 `2^53 + 1` 已经不是 `double`，结果必须和「一次舍入」一致。
- 环形缓冲：push 1000 个再全部 pop，顺序必须是 FIFO；`head` 停在缓冲区中间时再扩容（先 push 12 个、pop 10 个、再 push 40 个），弹出顺序仍是 `10, 11, 100`。
- 随机操作（2 万步，含 `LLONG_MAX` / `LLONG_MIN` 附近的值）和「每次从头求和」的参照实现逐项对比，`get_mean()` 对照一个独立的正确舍入实现。
- 性能：100 万次随机 push / pop，每 8 次一个 `get_mean`，要在 2 秒内跑完（无 sanitizer 的 `-O2` 版本）。
- C++ 专属测试：
  - 被移动的队列：`QueueMean b = std::move(a)` 之后 `a` 必须是合法的空队列（`empty()`、`sum() == 0`、`pop()` 抛异常），还能继续 `push`；移动赋值同理；自己移动给自己后对象仍然可用。
  - 拷贝是深拷贝：`head` 在缓冲区中间时拷贝，拷贝出来的队列和原队列互不影响（拷贝构造和拷贝赋值各测一次）。
  - `LLONG_MIN` 不能被取负：`-x`、`std::abs(x)` 都是 UB，UBSan 一触发就终止。三个 `LLONG_MIN` 的均值是 `LLONG_MIN/1`，`get_mean() == -2^63`；`Mean(LLONG_MIN, 2) == Mean(LLONG_MIN / 2, 1)`。
  - 2^53 边界：`push 2^53 + 1`，`get_mean()` 是 `2^53`（平局取偶）；`push 2^53 + 3` 得 `2^53 + 4`；负数一侧对称。
  - 和在 2^53 到 2^62 之间时，`get_mean()` 与一次舍入的结果逐位一致（2 万组随机数据）。
  - `to_double` 与参照实现逐位一致：`1/3`、`-1/3`、`0/5`、`2^126/1`、`1/LLONG_MAX`、`(2^100 + 1)/3`，再加 2 万组随机分子（1 到 125 位）和随机分母。
- 提示：starter 里的注释给了分母和 `to_double` 的思路。`std::gcd` 对 `__int128` 不可移植，自己写欧几里得循环（用 `u128`）。

## Part 2 · 修正快照事件流

事件分四种：`Push`、`Pop`、`Query`（要一个均值）、`Correct`（丢掉之前整段逻辑历史，队列内容变成快照给出的列表）。文本格式：

```
push 1
push 2
mean            → 3/2
pop
mean            → 2
snapshot 10 20 30
mean            → 20
pop
mean            → 25
pop
pop
mean            → empty
```

| 签名 | 要求 |
|---|---|
| `std::vector<Answer> run(const std::vector<Event>&)` | 依次执行事件，每个 `Query` 产生一个 `Answer`（`Value{mean}` 或 `Empty{}`）；空队列上 `Pop` 抛 `std::out_of_range` |
| `std::vector<Event> parse(const std::vector<std::string>&)` | `push N` · `pop` · `mean` · `snapshot [N ...]`；空行忽略；错误抛 `std::invalid_argument`，消息以 `"line k:"` 开头（k 从 1 起，空行也算行号） |
| `std::string render(const Answer&)` | 整数 `7`、分数 `-7/2`、空 `empty`；`0/5` 渲染成 `0` |
| `solve(lines)` | **已给出**：`run(parse(lines))` 再逐个 `render` |

- 上面的会话，`solve` 的输出是 `{"3/2", "2", "20", "25", "empty"}`。
- `Correct` 之后旧历史全部失效；`snapshot` 后面不带数字就是清空；连续两个 `snapshot` 以后一个为准。例：`Push 1, Correct{}, Query, Correct{4, 6}, Correct{8}, Query, Push 2, Query` 的答案是 `Empty、8、5`。
- `snapshot` 里三个 `LLONG_MAX` 的均值是 `LLONG_MAX`。
- 没有 `Query` 时返回空向量。
- 以下输入都必须以 `line 2:` 开头的 `invalid_argument` 拒绝（第 1 行是 `push 1`）：`push`、`push x`、`push 1 2`、`push 99999999999999999999`、`pop 3`、`mean 1`、`snapshot a`、`PUSH 1`、`peek`。
- 性能：100 万个事件（含约 1% 的 `Correct`，每个至多 4 个元素），2 秒内跑完。
- C++ 专属测试：
  - `Correct` 自己持有 `std::vector`，构造时就是拷贝：之后改原向量，事件不受影响；移动后目标仍然相等。
  - 解析要严格：`push +5`、`push 0x10`、`push 1.5`、`push -`、`push 9223372036854775808`、`push -9223372036854775809`、`snapshot 1,2`、`push 1x`、非 ASCII 字节、行内的 `\0` 都要拒绝。`std::stoll("12abc")` 会返回 12，`strtoll` 接受 `+` 和十六进制，所以要用 `std::from_chars` 并检查整个 token 都被消费。
  - 空白只有空格、制表符、`\r`、`\n`、`\v`、`\f`：`"\tpush\t7  "`、`"mean\r"`、`"snapshot\t1  2\r"` 都合法，`"   "` 当空行；`push -9223372036854775808` 合法。
  - 空行也占行号：`{"push 1", "", "   ", "bad"}` 的错误是 `line 4:`。

## Part 3 · 持久化（版本化）队列

换个角度问「快照」：保留每个历史版本，随时查任意版本的均值，还能从旧版本继续分叉。

| 签名 | 要求 |
|---|---|
| `static constexpr int EMPTY = 0` | 空队列的版本号 |
| `int push(int version, long long x)` | 在 `version` 之后入队，返回**新**版本号；`version` 本身永不改变 |
| `int pop(int version)` | 出队，返回新版本号；空版本抛 `std::out_of_range` |
| `int correct(const std::vector<long long>&)` | 新开一条独立历史，内容恰好是参数 |
| `std::size_t size(int) const` · `Mean mean(int) const` · `std::vector<long long> contents(int) const` | 查询；`mean` 在空版本抛 `std::out_of_range`；未知版本号（含负数）抛 `std::invalid_argument` |

- 版本号按创建顺序从 1 递增，没有空洞（测试逐个检查）。
- `push`、`pop`、`mean` 要 O(log n) 或更好，不能每个版本复制一份内容。
- 例：`v1 = push(EMPTY, 1)`，`v2 = push(v1, 2)`，`v3 = pop(v2)`：`contents(v3) = {2}`，而 `mean(v2) = 3/2`、`size(v2) = 2` 不受影响；从 `v2` 分叉 `push 10` 和 `push 20`，内容分别是 `{1, 2, 10}` 和 `{1, 2, 20}`，前者均值 `13/3`。
- `correct({1, 2, 3})` 的均值是 `2/1`，弹一次得 `{2, 3}`；`correct({})` 的 `size` 是 0。
- 溢出：三个 `LLONG_MAX` 的版本均值是 `LLONG_MAX`；弹两次剩一个仍是 `LLONG_MAX`；再 push `LLONG_MIN` 得 `-1/2`。
- 随机分叉（6000 步，从任意旧版本出发 push / pop / correct）与「每个版本存一份拷贝」的参照模型逐版本对比 `contents`、`size`、`mean`。
- 性能：沿一条链 push 30 万次再 pop 30 万次（每次 pop 都要找队头），再随机从 20 万个版本里分叉，总共 2 秒内。
- C++ 专属测试：
  - 节点数组增长不能留下悬空引用：连续 push 7 万次，再回头查旧版本，ASan 下不能报错。`push_back` 会重新分配，持有 `const Node& p = nodes_[i]` 再 push 就读到已释放的内存。
  - 10 万个元素的 `correct`，然后 pop 99990 次，剩下的 10 个元素必须是原数组的最后 10 个。
- 提示：starter 里写了结构：所有 push 的值组成一棵树，一个版本是（尾节点，已弹出个数，和）三个数；`pop` 需要「队头的值」，这是一次祖先查询（level ancestor）。

## Part 4 · 单写者、多读者

后台线程不断 `push` / `pop`，监控线程随时读当前均值：读者不加锁、不阻塞写者、永远读到一致的值（不能是「新的和 + 旧的个数」）。

| 签名 | 要求 |
|---|---|
| `void SharedMean::push(long long)` · `long long pop()` | 第一个调用的线程成为唯一的写者；别的线程写抛 `SingleWriterViolation`；空队列 `pop` 抛 `std::out_of_range` |
| `Stat read() const` | 任意线程调用；无锁；返回某一时刻的一致快照 `Stat{seq, size, sum}` |
| `std::optional<Mean> mean() const` · `Stat::mean() const` | 空队列返回 `std::nullopt` |

- `seq` 从 0 开始，每次成功修改加 1；同一个读者看到的 `seq` 单调不减。
- 单线程行为：初始 `seq = 0`、`mean()` 为空；`push 1, push 2` 后均值 `3/2`；再 `pop` 一次，此时 `seq = 3`、`size = 1`。
- 并发测试：4 个读者线程一直读，1 个写者做 3000 次操作，队列里永远只有 7，所以任何一致的快照都满足 `sum == 7 · size`，均值是 `7/1` 或者空。重复 25 轮。最后 `seq` 必须恰好等于 3000，`size` 等于写者记的数。
- C++ 专属测试：
  - `Stat` 必须是 trivially copyable（编译期 `static_assert`），`std::atomic<std::uint64_t>` 必须是无锁的：读者不能悄悄拿到一把锁。
  - 失败的 `pop`（空队列）不能发布任何东西：`read()` 前后相等，`seq` 不增加。
  - 超过 64 位的和要整体发布：三个 `LLONG_MAX` 之后 `read().sum` 等于 `3 · LLONG_MAX`，弹光后是 0。
- 提示：starter 里写了两条路：seqlock（奇偶版本计数器、relaxed 原子字段、acquire / release 栅栏），或者原子发布的不可变快照。普通字段在写者写的同时被读，是数据竞争。

## 边界清单

- 空队列的 `pop` / `mean` / `get_mean`；弹空之后再 push。
- 和超过 `LLONG_MAX` 再弹回小数；`LLONG_MIN`（不能取负、不能 `std::abs`）；`Mean(x, 0)`、`Mean(x, -2)`。
- 缓冲区扩容时 `head` 不在 0；移动后的队列；拷贝出来的队列。
- 和在 2^53 附近：`get_mean` 要一次舍入；`0/5`、`6/4` 这种需要约分的分数。
- `snapshot` 不带数字；解析的行号要算上空行；`+5`、`0x10`、`1.5`、行内 `\0`。
- 版本分叉：同一个旧版本后面接两个不同的 push；未知版本号；`correct({})`；7 万个节点之后的旧引用。
- 失败的操作不能改变可观察的状态（`seq`、`size`）；第二个写者线程。

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc04_queue_mean_snapshot          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc04_queue_mean_snapshot --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc04_queue_mean_snapshot --tag cpp      # 只跑 C++ 专属边界
python3 tools/cpptest.py run   loop/rounds/01_video/hc04_queue_mean_snapshot                # 全部
```

编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 元素换成 `double` 的滑动窗口均值：running sum 会累积误差，要补偿求和（Kahan）或定期重算；NaN / Inf 进入窗口之后 running sum 回不到有限值，要单独计数。
- 多个写者：串行化，或者用 CAS 循环更新不可变快照；此时 push / pop 不再是单线程可推理的 FIFO。
- 读多写少且读者可以等：`std::shared_mutex` 比 seqlock 简单。
