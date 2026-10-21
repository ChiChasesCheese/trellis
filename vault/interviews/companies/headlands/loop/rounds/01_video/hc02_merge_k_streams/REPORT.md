# hc02 · 思路与追问

## 概要

"合并 k 个有序序列"通常带"流式"和"多线程 non-blocking"的追问。
Part 1 是 LeetCode 23 的变体（几分钟）；面试官真正想看的是你能不能把它推到 **惰性迭代器**、**生产者-消费者 + 有界队列**、**永不无限阻塞**、**失败传播/取消**。

## 逐 Part 思路

1. **merge / mergeLongs**：最小堆里放"每个序列当前队首"，比较键 `(值, 序列编号)`，所以相等时序列号小的先出（稳定）。弹出堆顶，把它所在序列的下一个补进堆：每个元素 `O(log k)`，总共 `O(N log k)`。
   `mergeLongs` 的堆是手写的 `int[]`（只放序列号），数据留在原 `long[][]` 里，无装箱；建堆用自底向上 `O(k)`。
2. **mergeIterators**：同样的堆，但 (a) 构造时不取任何元素，(b) 输出元素 x 后不立刻取 x 所在序列的下一个，而是记成 `lastEmitted`，下一次 `hasNext/next` 时才补位——
   这样慢 source 的下一个元素不会拖慢当前已经能返回的结果。乱序在"读到那个元素"时检查。`mergeStreams` 把迭代器包成 `Stream`，`onClose` 关闭所有输入。
3. **ConcurrentMerge**：每个 source 一个虚拟线程生产者 → 各自一个 `ArrayBlockingQueue`（有界）→ 合并核心 `Combiner`。
   核心规则：**只有每条还活着的流都有队首，才能决定谁最小**。有流没队首 → `Pending`（非阻塞）或 `take()` 等（阻塞）。消息是 sealed 的 `Item/End/Failed`，生产者无论怎么结束都会留下 `End` 或 `Failed`。
   `close()` 中断生产者并 `join(Duration)` 有上限。
4. **mergeAll**：同一套生产者逻辑放进 `StructuredTaskScope.ShutdownOnFailure`；生产者失败抛 `MergeException(流编号, cause)`，scope 关闭并中断所有兄弟任务（包括阻塞在 `take()` 的合并任务）。`try` 块结束时所有子线程一定结束。

## 隐藏测试会打的坑

* 用 `a - b` 比较（`Long.MIN_VALUE`/`MAX_VALUE` 溢出）。
* 稳定性：没把序列号放进比较键，相等元素的顺序依赖堆的内部细节。
* k = 0 / 全空 / 空序列夹在中间：堆为空时 `poll()` 返回 `null`。
* 构造时就预读所有 source（惰性测试会数 `next()` 调用次数）。
* 刚输出 x 就阻塞去取 x 后面的元素（延迟补位测试）。
* "先到先出"：有一条流没数据时直接输出别的流的元素 → 顺序错（`tryNextIsPendingUntilEveryLiveStreamHasAHead`）。
* 无界队列：消费者慢时内存无限涨（`backpressureBoundsReadAhead` 精确断言 `capacity + 1`）。
* 生产者出错时没留标记 → 消费者永远 `take()`；或 `close()` 没中断生产者 → 线程泄漏。
* 吞掉 `InterruptedException`（`catch` 后不 `return` / 不恢复中断标志）→ 取消失效。
* `mergeAll` 里用普通线程池 + `Future.get()`：一个失败不会取消其他，测试里的"永远阻塞的 source"会让方法挂住。

## 复杂度

| 方案 | 时间 | 额外空间 |
|---|---|---|
| 全部拼起来再排序 | `O(N log N)`（但 TimSort 会利用已有的有序段） | `O(N)` |
| 依次两两合并（`acc = merge(acc, list_i)`） | `O(N·k)` | `O(N)` |
| 堆合并 | `O(N log k)` | 输出 + `O(k)` |
| 堆合并（惰性迭代器） | 同上，但可以只取前 m 个：`O(k + m log k)` | `O(k)` |

量级参考（k = 1000，每条 1000 个 `int`，N = 10^6）：

* 拼接 + `Collections.sort`：约 **50 ms**（意外地最快——`Collections.sort` 用的 TimSort 会识别已有序的"段"并归并它们）。
* 两两顺序合并：约 **1230 ms**。
* 堆合并 `MergeK.merge`（装箱 `Integer`）：约 **110 ms**。
* `MergeK.mergeLongs`（`long[]`，无装箱）：约 **65 ms**。

结论（面试里要诚实说）：**内存里的 List 用拼接 + 排序在 Java 里很难被打败**；堆合并的价值是 (1) 流式/惰性——输入放不进内存或是无限的，(2) 只要前 m 个，(3) 额外空间 `O(k)`，(4) 可以并发地边产生边合并。

## Java 21 特性

| 特性 | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| record | `Ready/Pending/Done`、`Item/End/Failed`、测试里的 `Rec` | 消息类型一行一个，`equals/toString` 免费 |
| sealed | `Poll`、`Msg` | 合并器的结果和队列消息是封闭集合；漏处理任何一种编译就报错 |
| 模式匹配 switch + record 模式 | `Combiner.poll`：`case Failed<T>(var cause) -> …`；`mergeAll`：`case Ready<T>(var v, _)` | 不用 `instanceof` 链和强转；穷尽检查保证终止标记不会被漏掉 |
| `instanceof` 模式 | `mergeAll`：`e instanceof MergeException me ? me : new MergeException(-1, e)` | 判断 + 绑定一步完成 |
| 虚拟线程 | 每个 source 一个 `Thread.ofVirtual()` 生产者 | source 阻塞在 I/O 时不占 OS 线程；开 k 个很便宜。对比平台线程池要为"最坏阻塞数"定池大小 |
| `StructuredTaskScope`（预览） | `mergeAll` | 子线程生命周期绑定在 `try` 块；一个失败自动取消其余；不会泄漏线程 |
| 未命名变量 `_`（预览） | `catch (InterruptedException _)`、`case End<T> _` | 明说"不用" |
| Stream API | `mergeStreams`（`StreamSupport` + `onClose`）；测试里 `Stream.iterate`、`toList()` | 惰性管道，`Stream.iterate` 造无限序列 |
| `Comparator` 组合子 | 堆的比较器 `comparing(h -> h.value).thenComparingInt(h -> h.stream)` | tie-break 写成链，一眼看出"先值后序列号" |

## 面试官可能的追问

1. **复杂度？为什么是 `log k` 不是 `log N`？** 堆里永远只有 ≤ k 个元素（每条序列的队首），每次堆操作 `O(log k)`，共 N 次。*要点*：和"全部排序 O(N log N)"比，k 小时有优势；k ≈ N 时退化成一样。
2. **有没有更好的办法？** 分治：把 k 个序列两两合并，再两两合并，共 `log k` 轮，每轮处理 N 个元素，也是 `O(N log k)`，不需要堆，对缓存友好，且易并行（同一轮的合并互相独立）。*反面*：不能流式输出（要先合并完一整轮）。
3. **输入是流、放不进内存怎么办？** 惰性迭代器：堆里只放 k 个队首；每个 source 带一个小缓冲（预读 `capacity` 个）。重点说"只比需要的多读 k 个"。
4. **其中一个 source 很慢或卡死了怎么办？** 先说清楚语义——有序合并**必须**等每个活着的流的队首，否则可能输出错误顺序。所以：(a) `tryNext` 返回 `Pending`，让调用方决定去做别的；(b) 给 `next` 加超时；(c) 对"可以接受乱序"的场景改成"尽力有序"的窗口合并（水位线 watermark，流处理里的做法）。
5. **怎么保证消费者不会永远阻塞？** 终止标记：每个生产者无论成功、失败还是被取消都要留下 `End`/`Failed`（`finally`/`catch Throwable`），队列是有界的所以 `put` 也可能阻塞——取消用线程中断唤醒。对**不响应中断**的 source，`close()` 只能带上限地 `join`，之后放弃它（说清楚这是权衡）。
6. **为什么用虚拟线程而不是线程池？** source 的 `hasNext` 可能阻塞在 I/O；虚拟线程阻塞时让出载体线程，数量不受池大小限制，代码仍是普通阻塞风格。注意：**不要池化**虚拟线程；`synchronized` 里阻塞在 JDK 21 会钉住载体线程，所以队列用 `ArrayBlockingQueue`（`ReentrantLock`）。
7. **为什么用 `StructuredTaskScope`？** 对比手写：`ExecutorService` + `Future.get()`，一个失败不会取消其他，容易泄漏线程；StructuredTaskScope 保证"离开 try 块时所有子任务已结束"，并且 `ShutdownOnFailure` 自动取消兄弟。它在 JDK 21 是**预览**特性（需要 `--enable-preview`）。
8. **C++ 怎么做？** `std::priority_queue` + 比较器 `(value, index)`；线程用 `std::thread` + 有界队列（`std::mutex` + 两个 `condition_variable`：not_full / not_empty）；取消用 `std::stop_token`（C++20 `std::jthread`）；无锁则是 SPSC 环形队列 + `atomic` acquire/release（每条流一个生产者一个消费者，正好是 SPSC）。
