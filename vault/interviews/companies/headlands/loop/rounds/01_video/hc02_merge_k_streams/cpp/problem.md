# hc02 · 合并 K 个有序序列 → 合并多路数据流（C++20 版）

给你 k 个各自升序（允许相等）的序列，合并成一个升序序列。这是最小堆的经典题，几分钟写完 Part 1；后面三个 Part 一路追问：数据是流、可能无限，所以要惰性；每个 source 会阻塞，所以要生产者线程加有界队列；任何一个 source 出错，要取消其余线程并把错误带回来。C++ 版的看点是：只依赖 `operator<`、`std::priority_queue` 是大顶堆且不稳定、线程里的异常漏出去就是 `std::terminate`、取消是协作式的（`std::stop_token`）。签名都在 `starter.hpp`（命名空间 `mergek`）。

## 读题前你需要知道

- **稳定**（stable）：值相等的元素，序列编号小的先输出。比较键是 `(值, 序列编号)`。
- **只用 `<`**：元素类型可能只有 `operator<`（或一个自定义的 `Less`），所以不能用 `==`、`>`、`<=`，更不能写 `a - b`（`long long` 的 `LLONG_MAX - LLONG_MIN` 有符号溢出，是 UB）。
- **惰性**（lazy）：构造时不读任何 source；source 可以是无限的；一个序列刚输出一个元素，它的下一个元素等到下一次调用才去读。
- **有界队列与背压**（bounded queue / backpressure）：队列满了，生产者线程阻塞在 push 上，消费者不动就不会无限读下去。
- **`std::stop_token`**：C++20 的协作式取消。线程不能被强杀，被阻塞的等待和 source 本身都要认这个 token。
- **`Pending` 的含义**：还有一条活着的流没给出队首，所以**无法安全决定**下一个输出（那条流的下一个元素可能比其他流的队首都小）。它不是「没有数据」。

## 公共类型（starter 已给出）

```cpp
class UnsortedInputException : public std::runtime_error {   // stream() 是序列编号，position() 是违规元素在该序列的下标
    UnsortedInputException(int stream, std::size_t position);
};

template <class T> using Source = std::function<std::optional<T>()>;   // 每次调用给下一个元素，结束返回 std::nullopt
template <std::ranges::viewable_range R> auto from_range(R&&);         // 已给出：左值 range 是借用，右值 range 被移入并拥有

template <class T> struct Ready { T value; int stream; };
struct Pending {};
struct Done {};
template <class T> using Poll = std::variant<Ready<T>, Pending, Done>;

class MergeException : public std::runtime_error {           // 某个 source 失败（抛了异常，或者乱序）
    MergeException(int stream, std::exception_ptr cause);    // cause() 是原始异常
};

template <class T> using BlockingSource = std::function<std::optional<T>(std::stop_token)>;
// 会阻塞的 source：一旦 stop 被请求，必须尽快返回 std::nullopt
```

`Merger::iterator` 和 `sentinel` 也已给出，所以 `Merger` 一旦写好就是一个 input range，可以直接 `for (int x : m)`。

## Part 1 · 合并 k 个有序 `vector`

| 签名 | 要求 |
|---|---|
| `template <class T, class Less = std::less<T>> std::vector<T> merge(const std::vector<std::vector<T>>&, Less = {})` | 稳定合并；任一序列不升序抛 `UnsortedInputException(stream, position)`；不修改输入 |
| `std::vector<long long> merge_longs(const std::vector<std::vector<long long>>&)` | 性能版：堆里不放元素的拷贝。语义同上 |

- `[[1,4,7],[2,5,8],[3,6,9]]` 得 `[1,2,3,4,5,6,7,8,9]`；`[[1,4,5],[1,3,4],[2,6]]` 得 `[1,1,2,3,4,4,5,6]`。
- 退化形状：`k = 0`、所有序列都空、空序列夹在中间、`k = 1`。
- `{{LLONG_MIN, LLONG_MAX}, {-1, LLONG_MAX}}` 得 `{LLONG_MIN, -1, LLONG_MAX, LLONG_MAX}`；`merge_longs({{LLONG_MIN, LLONG_MAX}, {0}})` 得 `{LLONG_MIN, 0, LLONG_MAX}`。
- 稳定性用只比较 `key` 的比较器检查：序列 `{1a1, 2a2, 2a3}`、`{1b1, 2b2}`、`{2c1}` 合并出 `a1, b1, a2, a3, b2, c1`；把三个序列倒过来输入，则得 `b1, a1, c1, b2, a2, a3`。
- 乱序：`{{1,2,3},{5,9,4,10}}` 抛 stream = 1、position = 2；`merge_longs({{1,2},{3,2}})` 抛 stream = 1、position = 1。
- 随机 300 轮，结果和「拼接后稳定排序」一致。
- C++ 专属测试：
  - 只有 `operator<` 的类型能用。
  - 自定义比较器：`std::greater<int>` 把降序序列合并成降序；`{9,5,7}` 在这个比较器下是乱序，要抛异常。
  - 每个元素恰好拷贝一次（拷到结果里）、移动 0 次：堆里放下标，结果提前 `reserve`。
  - 比较次数：k = 2、每条最长 4 万个元素（合计超过 1 万）时，总比较次数 ≤ 8n，而「拼接再排序」要约 log2(n) ≥ 16 次每元素。
- 性能：1000 个序列、每条 1000 个元素，`merge` 和 `merge_longs` 各自 2 秒内完成，结果有序。

## Part 2 · 惰性合并器 `Merger`

| 签名 | 要求 |
|---|---|
| `explicit Merger(std::vector<Source<T>>, Less = {})` | 构造时一个 source 都不调用 |
| `bool has_next()` | 幂等；结束后一直是 `false` |
| `T next()` | 没有下一个时抛 `std::out_of_range` |
| `begin()` / `end()` | 已给出，用 `has_next()` + `next()` 取值 |
| 拷贝构造 / 拷贝赋值 | 已 `delete`；测试要求 `Merger` **也不能移动**（`static_assert`） |

- 第一次调用 `has_next()` / `next()` 才对每个 source 各取一个队首；输出一个元素后，它所在 source 的补位推迟到下一次调用。
  `{1,4,7}`、`{2,5,8}`、空：第一次 `next()` 得 1，a 和 b 各被取了 1 次；第二次 `next()` 得 2，a 被取了第 2 次（补位），b 还是 1 次；再调 `has_next()` 之后 b 才被取第 2 次。
- 消费 n 个元素后，所有 source 被调用的总次数 ≤ k + n − 1（测试对 k = 7、n 到 50 逐步检查）。
- 两个无限序列（0, 2, 4, … 和 0, 3, 6, …）前 10 个是 `0 0 2 3 4 6 6 8 9 10`。
- 相等元素序列编号小的先出。
- 乱序在**读到那个元素时**才发现：`{1,5,3}` 和 `{2,4}` 依次得 1, 2, 4, 5，再调 `has_next()` 抛 stream = 0、position = 2。抛出之后是**粘性的**（sticky）：之后每次调用 `has_next()` / `next()` 都重新抛同一个异常，不能悄悄跳过坏元素。
- C++ 专属测试：
  - source 自己抛出的 `std::runtime_error("boom")` 原样传出，之后也粘住。
  - `Merger` 满足 `std::ranges::input_range`，`for (int x : m)` 可用，`m | std::views::take(8)` 能对无限流取前缀。
  - `from_range(std::vector<int>{5, 6})` 拥有临时 vector；`from_range(mine)` 借用左值，调用方必须保证它活着。
  - 每个元素最多被拷贝一次。
- 性能：100 个序列、每条 1 万个元素，共 100 万个，2 秒内读完。

## Part 3 · 生产者线程 + 有界队列 `ConcurrentMerge`

| 签名 | 要求 |
|---|---|
| `ConcurrentMerge(std::vector<BlockingSource<T>>, int capacity, Less = {})` | 每个 source 一个 `std::jthread` 生产者，各有一个容量为 `capacity` 的队列；`capacity < 1` 抛 `std::invalid_argument` |
| `Poll<T> try_next()` | 永不阻塞：`Ready` / `Pending` / `Done` |
| `Poll<T> next()` | 阻塞到 `Ready` 或 `Done`，永不返回 `Pending` |
| `void close()` | 幂等：取消所有生产者（stop token）并 join；析构函数做同样的事 |

- 输出和线程调度无关，永远等于顺序版的稳定合并；`Ready.stream` 是元素来自哪个序列（值相等时 `{5}`、`{5}` 先出 stream 0）。
- 两个 source：fast 先给了 1、3 并结束，slow 什么都没给。此时 `try_next()` 必须一直返回 `Pending`（测试连续调 2000 次），因为 slow 随时可能给出 0。slow 给出 2 并结束后，依次得 1, 2, 3，然后 `Done`。
- 背压：容量 4、source 可以产出 1000 个元素、没人消费，source 被调用的次数停在 5（队列满 + 生产者手里那一个），即 `capacity + 1`。
- 失败：一个 source 在第 3 次调用时抛异常，另一个 source 永远阻塞。消费者先拿到失败前已经产出的 10、20，再得到 `MergeException`（stream = 0，`cause()` 是原来的 `std::runtime_error`）。那个永远阻塞的生产者要被取消，之后 `try_next()` 抛 `std::logic_error`（合并器已自行关闭）。
- 乱序的 source：`{1, 3, 2}` 的失败原因是 `UnsortedInputException`（position = 2）。
- `close()` 之后 `next()` 抛 `std::logic_error`；`close()` 返回时生产者已经结束。
- 空输入：`k = 0`、全是空 source 都直接得到 `Done`。
- C++ 专属测试：
  - source 抛 `int`（不是 `std::exception`）也不能 `terminate`，`cause()` 里取回的就是 `42`。
  - 不调用 `close()`，离开作用域也不能卡住，也不能泄漏线程。
  - 另一个线程调用 `close()`，必须唤醒一个正阻塞在 `next()` 里的调用，使它抛 `std::logic_error`。
- 随机交错：25 个种子，2 到 9 个 source，每个最多 400 个元素，值域很小（大量相等元素），生产者随机 `yield`；结果必须等于 oracle，值相等的元素 stream 不能倒退。
- 性能：8 个 source、每个 5 万个元素、容量 1024，2 秒内读完 40 万个。
- 并发测试带有看门狗线程：死锁会让测试直接失败，不会卡住。

## Part 4 · 一次性合并 `merge_all`

| 签名 | 要求 |
|---|---|
| `std::vector<T> merge_all(std::vector<BlockingSource<T>>, int capacity, Less = {})` | 合并并返回全部结果；`capacity < 1` 抛 `std::invalid_argument` |

- 第一个失败的 source 取消其余的（被阻塞的 source 通过 stop token 醒来），然后 `merge_all` 抛 `MergeException`，带失败 source 的编号。
- 无论正常返回还是抛异常，**离开函数时所有线程都已经结束**。测试在 `merge_all` 抛出后立刻检查：另外两个永远阻塞的 source 都已经被打断。
- 三个 source `{stuck, boom, stuck2}`，中间那个抛 `std::invalid_argument("bad record")`：得到 `MergeException`，stream = 1，`cause()` 是原异常。
- 乱序输入 `{{1,2},{5,4}}` 得 stream = 1 的 `MergeException`，`cause()` 是 `UnsortedInputException`。
- `{{1,4,7},{},{2,5,8},{3,6,9}}`、容量 2，得 `1..9`；空输入得空 vector；降序比较器 `std::greater<int>` 也能用。
- 随机交错 25 个种子，结果等于 oracle。
- 性能：8 × 5 万个元素、容量 1024，2 秒内完成。

## 边界清单

- `k = 0`、全空、单个序列、空序列夹在中间
- 大量相等元素（稳定性要看得出）；比较器只比部分字段的类型
- `LLONG_MIN` / `LLONG_MAX`
- 乱序出现在序列中间，Part 2 里要读到才发现
- 一个 source 永远不给数据（`try_next()` 一直是 `Pending`）
- 一个 source 抛异常，包括抛的不是 `std::exception`
- 消费者不动时，生产者被背压挡住
- `close()` 时生产者阻塞在 source 里；析构时没调用过 `close()`
- `capacity` 为 0 或负数

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/cpptest.py start loop/rounds/01_video/hc02_merge_k_streams          # starter.hpp → work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc02_merge_k_streams --tag part1
python3 tools/cpptest.py run   loop/rounds/01_video/hc02_merge_k_streams --tag conc   # 并发测试
python3 tools/cpptest.py run   loop/rounds/01_video/hc02_merge_k_streams              # 全部
```

标签：`part1` 到 `part4`、`edge`、`cpp`（C++ 专属）、`conc`（并发）、`perf`。编译带 `-fsanitize=address,undefined`，一触发 UB 就终止；带 `perf` 标签的测试另编一个不带 sanitizer 的 `-O2` 版本来跑。

## 相关变体

- 给你一个会抛异常、可能很慢的阻塞 client，要求同时最多读 m 个（有界并发）。这里的 `capacity` 是每条流的预读深度，不是并发数。
- 线程安全的队列怎么写？`mutex` + 条件变量；要无锁，每条流一个生产者一个消费者，正好是 SPSC 环形队列。
- k 很大（上万个 source）时，一个 source 一个 OS 线程太贵。
