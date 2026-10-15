# hc04 · Queue Mean + 修正快照（Headlands 一小时技术电面）

> 阶段：电面（FastPrep 标 Phone Screen；1p3a 技术电面，C++）· 置信度：**高**（2 个独立来源，最近一次 2026-03-23/24）
> 公开证据只有两个标题和每题的第一句话，以及 1p3a 帖子的一句预览（正文在登录墙后）。
> **题面里凡是标了 (reconstructed) 的部分都是我根据标题补出来的，不是原题**——Part 1 的接口大体可信，Part 2 的「修正快照」语义是猜的，Part 3 / Part 4 是按「面试官会怎么往下追」加的练习。

## 读题前你需要知道

这道题表面是「队列求平均数」，但面试官真正在看的是：你知道不知道**每次重新求和是 O(n)**，知道**浮点数加了又减会丢精度**，知道 **long 加法会溢出**，
以及「保存历史版本」到底要复制多少数据。这些你不必先会——讲义 [[hc04_queue_mean_snapshot]]
（`study/30-articles/hc04_queue_mean_snapshot.md`，从零讲环形缓冲区、128 位整数、持久化数据结构、Java 内存模型）会按顺序教。
建议做法：先读讲义第 1–3 节，再自己写 Part 1，卡住再读第 4 节。

## 背景

* 证据：「实现一个 queue 和三个函数 push、pop 和 get_mean；get_mean 就是所有里面数据的 mean。第二问是实现一个带有 snapshot 的……」（1p3a 1169914，预览被截断）。
* FastPrep 两道题：「Process a sequence of operations on an initially empty first-in, first-out queue of in…」和「A FIFO queue starts empty. Ordinary events belong to one logical his…」（都在第一句话处被截断）。

## Part 1 · 队列 + 均值（高置信）

先进先出（FIFO）队列，元素是 `long`。

| 方法（`QueueMean`） | 含义 |
|---|---|
| `void push(long x)` | 入队（放到队尾） |
| `long pop()` | 出队并返回队头（最早 push 的）；空队列抛 `NoSuchElementException` |
| `double getMean()` | 当前所有元素的平均数；空队列抛 `NoSuchElementException` |
| `Mean mean()` | **精确**均值，约分后的分数 `numerator/denominator`（分母恒正） **(reconstructed)** |
| `int size()` · `boolean isEmpty()` · `I128 sum()` | 辅助 |

要求（原题大概只要求 `get_mean` 是 O(1)；下面这些是追问方向 **(reconstructed)**）：

* 每个操作 **O(1)**（均摊）。不能每次 `getMean` 都遍历。
* **精确**：不能用 `double` 维护 running sum（`1e16 + 1 + 1 − 1e16` 在 double 里等于 0，不是 2）。
* **不溢出**：元素可以是 `Long.MAX_VALUE`，和会超过 `long`。`I128`（128 位有符号整数）已经在 starter 里作为 record 给出，方法要你补。
* `getMean()` 返回**最接近**精确均值的 `double`。

### 样例

```
push 1, push 2, push 3  → getMean() = 2.0
push 4                  → getMean() = 2.5
pop()                   → 返回 1；getMean() = 3.0
```

## Part 2 · 修正快照（snapshot）事件流 (reconstructed)

原题第二问的原文看不到。我的理解：事件分四种——`Push`、`Pop`、`Query`（要一个均值）、`Correct`（**修正快照**：丢掉此前整段逻辑历史，队列内容变成快照给出的列表）。
文本格式（`QueueEvents.parse`）：

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

| 方法（`QueueEvents`） | 含义 |
|---|---|
| `List<Answer> run(List<? extends Event>)` | 应用事件，每个 `Query` 一个 `Answer`（`Value(Mean)` 或 `Empty`）；空队列上 `Pop` 抛 `NoSuchElementException` |
| `List<Event> parse(List<String>)` | `push N` · `pop` · `mean` · `snapshot [N ...]`；空行忽略；错误抛 `IllegalArgumentException("line k: …")`（k 从 1 起） |
| `String render(Answer)` | 整数 `7`、分数 `-7/2`、空 `empty` |
| `List<String> solve(List<String>)` | 整题 |

`Correct` 事件必须**拷贝**传入的列表（调用者之后改原列表不应影响事件），列表里有 `null` 立刻抛 NPE。

> 另一种可能的读法：snapshot 是「某时刻整个队列的真实内容」，用来纠正之前积累的误差。本质上和这里的 `Correct` 是同一个操作：用快照内容替换当前状态。如果真题的语义是别的（比如按时间戳回放），请把差异记到这里。

## Part 3 · 版本化 / 持久化队列 (reconstructed)

「快照」换一个角度问：**我想保留每个历史版本，随时能查任意版本的均值，还能从旧版本继续分叉**。

| 方法（`VersionedQueue`） | 含义 |
|---|---|
| `static final int EMPTY = 0` | 空队列的版本号 |
| `int push(int version, long x)` | 在 `version` 之后入队，返回**新**版本号；`version` 本身永不改变 |
| `int pop(int version)` | 出队，返回新版本号；空版本抛 `NoSuchElementException` |
| `int correct(List<Long> contents)` | 新开一条独立历史，内容恰好是 `contents` |
| `int size(int)` · `Mean mean(int)` · `List<Long> contents(int)` | 查询（`mean` 在空版本抛 `NoSuchElementException`；未知版本号抛 `IllegalArgumentException`） |

要求：`push`、`pop`、`mean` 都是 **O(log n)** 或更好，**不能**每个版本复制一份内容（20 万个版本会 O(n²)）。版本号按创建顺序从 1 递增。

## Part 4 · 单写者、多读者 (reconstructed)

后台线程不断 `push/pop`，监控线程随时想读当前均值，要求：读者**不加锁**、不阻塞写者、**永远读到一致的值**（不能读到「新的和 + 旧的个数」这种撕裂值）。

| 方法（`SharedMean`） | 含义 |
|---|---|
| `void push(long)` · `long pop()` | 只允许一个写者线程（第一个写的线程）；别的线程写抛 `IllegalStateException` |
| `Stat read()` | 任意线程；返回不可变快照 `Stat(seq, size, sum)`，`seq` 从 0 起，每次修改 +1，单个读者看到的 `seq` 单调不减 |
| `Optional<Mean> mean()` | `read().mean()`；空队列 `Optional.empty()` |

## 边界清单

* 空队列的 `pop` / `getMean`；弹空之后再 push。
* 和超过 `Long.MAX_VALUE`，再弹回小数（累加器不能「卡」在大数上）。
* 负数、0、`Long.MIN_VALUE`（`-x` 对它会溢出；`Math.abs` 同理）。
* 环形缓冲扩容时 `head` 不在 0 的情况。
* 均值不是整数：`3/2` 要约分，符号只放分子。
* `snapshot` 后面不带数字（清空）；`snapshot` 里含 `Long.MAX_VALUE` 的溢出。
* 版本分叉：同一个旧版本后面接两个不同的 push。

## 野外变体

* 同一家 FastPrep 页面上「Sliding-Window Means with IEEE Special Values」是同一思路：滚动统计 + 数值稳定性（NaN / Inf 怎么办）。
* C++ 面试官爱追问：`std::deque` 还是环形数组？`get_mean` 返回 `double` 还是分数？线程安全怎么做？

## 来源与置信度

`catalog/raw/forums.md` A1（1p3a 1169914，2026-03-23）；`catalog/raw/github_repos.md`（FastPrep "Queue Mean Queries" / "Queue Mean from Corrective Snapshots"，2026-03-23）；
QuantVault X1 同源不计。**Part 1 的 push/pop/get_mean 来自证据；其余全部 (reconstructed)。**

## 考什么

「O(1) 均值」是门槛；真正拉开差距的是你**主动**说出：浮点累积误差、`long` 溢出、空队列行为、以及「快照到底是拷贝还是共享」。
Part 3/4 是把同一个小题目拉到「持久化数据结构」和「无锁读」两个常见的深度追问上。
