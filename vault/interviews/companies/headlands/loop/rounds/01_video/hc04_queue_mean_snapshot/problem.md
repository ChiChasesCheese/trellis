# hc04 · 队列求均值 + 快照修正

实现一个先进先出（FIFO）的队列，元素是 `long`，支持入队、出队和「当前所有元素的平均数」，三个操作都要 O(1)。写法很短，面试官看的是你有没有想到：每次重新求和是 O(n)，用 `double` 累加会丢精度，`long` 的和会溢出。写完之后他会加一个「快照修正」：队列的内容被一份新的列表整个替换。并发读写放在口头追问里。

## 面试官会怎么说

> "Implement a queue with `push`, `pop` and `get_mean`. `get_mean` should be O(1)."
> 接着会问："What if values are large?" "Now add a snapshot event that corrects the queue contents." "What if one thread writes and many threads read the mean?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：空队列上 `pop` / `mean` 怎么办？`mean` 返回什么类型？元素会不会很大？ |
| 3–15 分钟 | **Part 1**：队列 + O(1) 均值 |
| 15–30 分钟 | **Part 2**：快照修正 |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 队列 + O(1) 均值（约 12 分钟）

| 语言 | 签名（类 `QueueMean`） |
|---|---|
| Java | `void push(long x)` · `long pop()` · `double mean()` |
| C++ | `void push(long long)` · `long long pop()` · `double mean() const` |

- `pop` 返回队头，也就是最早 `push` 的那个元素。
- 空队列上 `pop` 和 `mean` 都报错：Java 抛 `NoSuchElementException`，C++ 抛 `std::out_of_range`。
- `mean` 用一个 `long` 型的和（sum）加上队列长度（count）算出来，返回 `double`。
- 例子：`push 1, 2, 3` 后 `mean() = 2.0`；再 `push 4` 得 `2.5`；然后 `pop()` 返回 1，`mean() = 3.0`。
- 弹空之后还能继续 `push`，`mean` 重新从新元素算起。

## Part 2 · 快照修正（约 15 分钟）

| 语言 | 签名 |
|---|---|
| Java | `void snapshot(List<Long> contents)` · `static List<Double> run(List<String> events)` |
| C++ | `void snapshot(const std::vector<long long>&)` · `std::vector<double> run(const std::vector<std::string>&)` |

- `snapshot(contents)`：丢掉队列里现有的全部内容，队列变成 `contents`，第一个元素是队头。`contents` 可以为空。之后调用方改它自己的列表，不能影响队列。
- `run(events)`：从空队列开始，按顺序处理事件，返回每条 `mean` 的结果。事件有四种：`push x`、`pop`、`mean`、`snapshot a b c`（后面可以一个数字都没有）。空队列上的 `pop` / `mean` 报错，规则同 Part 1。
- 例子：`push 1, push 2, mean, pop, mean, snapshot 10 20 30, mean, pop, mean` 返回 `[1.5, 2.0, 20.0, 25.0]`。
- 快照后队列里是 10、20、30，均值 20；`pop` 出 10 后剩 20、30，均值 25。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么和要用 `long` 而不是 `double`？
2. 元素是 `Long.MAX_VALUE` 时，和会溢出，怎么办？`mean` 的返回类型要不要改？
3. 一个线程写、很多线程读均值，怎么做到读者不加锁，又读不到撕裂的值？
4. 如果要保留每一个历史版本，随时查任意版本的均值，快照要复制多少数据？
5. 滑动窗口（固定长度 k）的均值怎么做？`std::deque` 和环形数组选哪个？

## 边界

- 空队列的 `pop` / `mean`；弹空之后再 `push`
- 负数、0
- `snapshot` 后面没有数字（清空队列）
- 快照之后 `pop`，和要跟着减掉那个元素

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/01_video/hc04_queue_mean_snapshot       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/01_video/hc04_queue_mean_snapshot --tag part1
python3 tools/cpptest.py start loop/rounds/01_video/hc04_queue_mean_snapshot       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/01_video/hc04_queue_mean_snapshot --tag part1
```
