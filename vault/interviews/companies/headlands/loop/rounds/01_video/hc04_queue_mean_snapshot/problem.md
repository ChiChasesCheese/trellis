# hc04 · Queue Mean + 修正快照（Headlands 一小时技术电面）

## 读题前你需要知道

这个任务表面是「队列求平均数」，但面试官真正在看的是：你知道不知道**每次重新求和是 O(n)**，知道**浮点数加了又减会丢精度**，知道 **long 加法会溢出**，
以及「保存历史版本」到底要复制多少数据。涉及的基础：环形缓冲区、128 位整数、持久化数据结构、Java 内存模型。

## 背景

实现一个 queue 和三个函数 `push`、`pop`、`get_mean`（`get_mean` 返回队列里所有数据的平均数）；第二问是实现一个带 snapshot 的版本：队列在一个空队列上处理一串操作，普通事件属于同一段逻辑历史，快照事件用来修正这段历史。

## Part 1 · 队列 + 均值

先进先出（FIFO）队列，元素是 `long`。

| 方法（`QueueMean`） | 含义 |
|---|---|
| `void push(long x)` | 入队（放到队尾） |
| `long pop()` | 出队并返回队头（最早 push 的）；空队列抛 `NoSuchElementException` |
| `double getMean()` | 当前所有元素的平均数；空队列抛 `NoSuchElementException` |
| `Mean mean()` | **精确**均值，约分后的分数 `numerator/denominator`（分母恒正） |
| `int size()` · `boolean isEmpty()` · `I128 sum()` | 辅助 |

基本要求是 `get_mean` 为 O(1)；追问方向：

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

## Part 2 · 修正快照（snapshot）事件流

事件分四种——`Push`、`Pop`、`Query`（要一个均值）、`Correct`（**修正快照**：丢掉此前整段逻辑历史，队列内容变成快照给出的列表）。
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

> 另一种可能的读法：snapshot 是「某时刻整个队列的真实内容」，用来纠正之前积累的误差。本质上和这里的 `Correct` 是同一个操作：用快照内容替换当前状态。

## Part 3 · 版本化 / 持久化队列

「快照」换一个角度问：**我想保留每个历史版本，随时能查任意版本的均值，还能从旧版本继续分叉**。

| 方法（`VersionedQueue`） | 含义 |
|---|---|
| `static final int EMPTY = 0` | 空队列的版本号 |
| `int push(int version, long x)` | 在 `version` 之后入队，返回**新**版本号；`version` 本身永不改变 |
| `int pop(int version)` | 出队，返回新版本号；空版本抛 `NoSuchElementException` |
| `int correct(List<Long> contents)` | 新开一条独立历史，内容恰好是 `contents` |
| `int size(int)` · `Mean mean(int)` · `List<Long> contents(int)` | 查询（`mean` 在空版本抛 `NoSuchElementException`；未知版本号抛 `IllegalArgumentException`） |

要求：`push`、`pop`、`mean` 都是 **O(log n)** 或更好，**不能**每个版本复制一份内容（20 万个版本会 O(n²)）。版本号按创建顺序从 1 递增。

## Part 4 · 单写者、多读者

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

## 相关变体

* 滑动窗口均值带 IEEE 特殊值：同一思路，滚动统计 + 数值稳定性（NaN / Inf 怎么办）。
* C++ 面试官爱追问：`std::deque` 还是环形数组？`get_mean` 返回 `double` 还是分数？线程安全怎么做？

## 考什么

「O(1) 均值」是门槛；真正拉开差距的是你**主动**说出：浮点累积误差、`long` 溢出、空队列行为、以及「快照到底是拷贝还是共享」。
Part 3/4 是把同一个小题目拉到「持久化数据结构」和「无锁读」两个常见的深度追问上。
