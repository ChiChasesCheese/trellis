# hc02 · 合并 K 个有序序列 → 合并多路数据流（Headlands 一小时技术电面）

> 阶段：电面（FastPrep Phone Screen + FastPrep LLD；1p3a 两个技术电面，C++）· 置信度：**高**（3 个独立来源，2024-06 ~ 2024-10）
> 证据只有标题和每题第一句话：「Given sequences, an array of integer sequences, merge all their entries into one…」；LLD 版「incremental sorted merging through a supplied unsafe blocking client, with bounded overlapping background reads…」；
> 1p3a 1089956：「coding in C++ to merge multiple data streams, including a multithreaded non-blocking follow-up」；1p3a 1071034：「merge k sorted list and streaming problems」。
> **所以：Part 1 的"合并 k 个有序序列"高置信；"流式/增量"和"多线程 + 非阻塞 + 有界并发"方向有证据；具体接口、异常行为、测试语义全部 (reconstructed)。**

## 读题前你需要知道

这题的核心是**最小堆**（heap）：k 个序列各自的"队首"里最小的那个就是下一个输出。如果你不知道堆、`Iterator`、有界阻塞队列（bounded blocking queue）、
虚拟线程、`StructuredTaskScope`，没关系——讲义 [[hc02_merge_k_streams]]（`study/30-articles/hc02_merge_k_streams.md`）从零讲，
并且从最笨的"全部拼起来再排序"和"两两合并"开始推导。建议：先读讲义第 1–3 节，自己写 Part 1，再读第 4 节。

## Part 1 · 合并 k 个有序序列（高置信）

输入：`k` 个各自**升序**（允许相等）的序列。输出：把所有元素合并后的一个升序序列。

| 方法（`MergeK`） | 含义 |
|---|---|
| `static <T extends Comparable<? super T>> List<T> merge(List<? extends List<? extends T>>)` | 合并 k 个 `List`。相等元素按**序列编号小的在前**（稳定）。 |
| `static long[] mergeLongs(long[][] arrays)` | 性能版：不装箱。 |
| `UnsortedInputException(stream, position)` | 某个序列不是升序时抛出：序列编号 + 违规元素在该序列的下标 **(reconstructed)** |

* 序列可以为空，`k` 可以为 0，所有序列可以都为空。
* 元素是 `null` → `NullPointerException`。输入列表不得被修改。
* 比较必须用 `compareTo`，不能用 `a - b`（`Long.MIN_VALUE` 与 `Long.MAX_VALUE` 会溢出）。

### 样例

```
[[1,4,7],[2,5,8],[3,6,9]]  →  [1,2,3,4,5,6,7,8,9]
[[1,4,5],[1,3,4],[2,6]]    →  [1,1,2,3,4,4,5,6]
```

## Part 2 · 惰性 / 流式 (reconstructed)

数据不一定一次性在内存里（"streams"），也可能是无限的。

| 方法（`MergeK`） | 含义 |
|---|---|
| `static <T …> Iterator<T> mergeIterators(List<? extends Iterator<? extends T>>)` | 惰性合并：**构造时不碰任何 source**；第一次 `hasNext/next` 才各取一个队首；输出一个元素后，它所在 source 的**下一个元素推迟到下一次调用**才取。 |
| `static <T …> Stream<T> mergeStreams(List<? extends Stream<? extends T>>)` | `Stream` 版，同样惰性；关闭返回的 `Stream` 要关闭所有输入。 |

* 相等元素：序列编号小的在前（稳定），与 Part 1 一致。
* 乱序检查发生在**读到那个元素的时候**（惰性）：`UnsortedInputException` 从 `hasNext()`/`next()` 抛出。
* 总取数约束（测试）：消费 n 个元素后，source 被 `next()` 的总次数 ≤ k + n − 1。
* 要能对两个无限序列取前 10 个。

## Part 3 · 多线程、非阻塞、有界并发 (reconstructed；方向有证据)

现实里每个 source 是一个**会阻塞的 client**（读网络、读文件），慢且不可信。要求：

| 方法（`ConcurrentMerge<T>`） | 含义 |
|---|---|
| `static ConcurrentMerge<T> start(List<? extends Iterator<? extends T>> sources, int capacity)` | 每个 source 起一个**虚拟线程**生产者，把元素放进自己的**有界队列**（容量 `capacity ≥ 1`，否则 `IllegalArgumentException`）。 |
| `Poll<T> tryNext()` | **立刻返回**，不阻塞。`Ready(value, stream)` / `Pending` / `Done`。 |
| `Poll<T> next() throws InterruptedException` | 阻塞到 `Ready` 或 `Done`（不返回 `Pending`）。 |
| `void close()` | 幂等；中断所有生产者并等它们退出（有上限，不会永远卡）。 |
| `MergeException(stream, cause)` | 某个 source 出错（抛异常、乱序、null）。 |

语义：

* **`Pending` 的含义**：还有活着的流没给出队首，所以**无法安全决定**下一个输出（那条流的下一个元素可能比其他流的队首都小）。不是"没有数据"。
* 生产者 backpressure：队列满了生产者阻塞在 `put` 上；消费者不动，每个 source 最多被 `next()` 取走 `capacity + 1` 个元素。
* 终止标记：每个生产者结束时一定留下 `End` 或 `Failed` 消息（sealed 类型），所以合并器不会永远等一个已经死掉的生产者。
* 失败：合并器在读到 `Failed` 时抛 `MergeException`（先输出该流失败前已入队的元素），并自动 `close()`；之后调用 `tryNext/next` 抛 `IllegalStateException`。
* 输出与线程调度**无关**：永远等于顺序版的稳定合并。

## Part 4 · 结构化并发 (reconstructed)

| 方法 | 含义 |
|---|---|
| `static List<T> mergeAll(List<? extends Iterator<? extends T>> sources, int capacity) throws InterruptedException` | 一次性合并并返回全部结果。所有生产者和合并任务放在同一个 `StructuredTaskScope.ShutdownOnFailure` 里：任何一个失败 → 其余被**中断** → 抛 `MergeException`（带失败的流编号）。 |

要求：走出方法时所有线程都已结束（不泄漏）；其他生产者阻塞在慢 source 上也要被中断，不能等它们。

## 边界清单

* `k = 0`、全空、单个序列、空序列夹在中间。
* 大量相等元素（稳定性）；元素类型的 `compareTo` 只比较部分字段时，稳定性才看得出。
* `Long.MIN_VALUE` / `Long.MAX_VALUE`。
* 乱序输入在序列**中间**才出现。
* 一个 source 永远不给数据（`Pending` 永不变成 `Ready`）。
* 一个 source 抛异常；消费者不消费时生产者被背压挡住。
* `close()` 时生产者阻塞在 source 里。

## 野外变体

* LLD 版（FastPrep "Concurrent Sorted-Stream Merger"）：给你一个 **unsafe 阻塞 client** 接口（可能抛异常、可能很慢），要求"有界地重叠"读取（同时最多读 m 个）。本题的 `capacity` 是 per-stream 的预读深度，作用相近；真题的并发界定方式未知。
* QuantVault 的标题 "Merge K Sorted Streams with Bounded Concurrency" 指向同一方向。
* C++ 面试官爱追问：线程安全的队列怎么写？`condition_variable`？无锁？

## 来源与置信度

`catalog/raw/forums.md` A6（1p3a 1089956）、A7（1p3a 1071034）；`catalog/raw/github_repos.md`（FastPrep "Merge K Sorted Sequences"、LLD "Concurrent Sorted-Stream Merger"）。
Part 1 来自证据；Part 2–4 的接口细节全部 **(reconstructed)**。

## 考什么

Part 1 是 LeetCode 23 的变体，门槛是"想到堆，说出 O(N log k)"。拉开差距的是 Part 2/3：**惰性**（不要预读）、**稳定**（tie 规则）、
**为什么不能"先到先出"**（Pending 的含义）、**有界**（背压）、**不会永远阻塞**（终止标记 + 超时/关闭）、**失败传播**。
