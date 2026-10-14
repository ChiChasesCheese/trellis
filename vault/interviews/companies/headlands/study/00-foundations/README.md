# 基础概念课本（`study/00-foundations/`）

> 写法说明见 [`../TEXTBOOK.md`](../TEXTBOOK.md) 「基础概念课本」一节：每个概念回答四个问题（是什么 / 为什么需要 / 怎么工作 / Java 里怎么写），配 ASCII 图、手算例子、自测题（答案折叠在 `<details>` 里）。
> 读者设定（Chi）：会写基本 Java，数据结构、复杂度、操作系统、网络都需要从头讲。
> 目标场景：Headlands Technologies，Java Software Engineer。JD 强调 performance、Linux、networking、distributed storage；下一轮是一小时的技术视频面试。

## 阅读顺序

```text
① complexity ──▶ ② heap_priority_queue ──▶ ③ ordered_maps_trees
       │
       └──────▶ ④ cpu_cache_locality ──▶ ⑤ os_processes_threads_ipc ──▶ ⑥ networking_basics
```

| 顺序 | 章节 | 一句话 | 前置 | 建议用时 |
|---|---|---|---|---|
| ① | [complexity.md](complexity.md) | Big-O 从数步数讲起；最好/平均/最坏；摊还（`ArrayList` 扩容有证明）；log n；面试里怎么估算运行时间，以及「10⁸ 次/秒」法则的六个局限 | 无 | 1.5–2 h |
| ② | [heap_priority_queue.md](heap_priority_queue.md) | 二叉堆数组布局、上浮/下沉逐步演示、建堆 O(n) 的证明、`PriorityQueue` 的 API 与八个坑（迭代顺序、平局、改键、比较器溢出……） | ① | 1.5 h |
| ③ | [ordered_maps_trees.md](ordered_maps_trees.md) | BST 为何退化 → 旋转 → 红黑树直觉（含高度证明）→ 跳表 → `TreeMap`/`ConcurrentSkipListMap` 的导航 API 与选择指南，联系 LSM/B+ 树 | ①②（树的数组布局） | 2 h |
| ④ | [cpu_cache_locality.md](cpu_cache_locality.md) | 内存层级与真实延迟数字、缓存行、局部性、`long[]` vs `ArrayList<Long>`、AoS vs SoA、伪共享、分支预测；全部配本机实测 | ① 第 8 节 | 2–2.5 h |
| ⑤ | [os_processes_threads_ipc.md](os_processes_threads_ipc.md) | 进程/线程、虚拟内存、调度与上下文切换、系统调用、IPC 全家桶、`mmap`（`FileChannel.map` 与 FFM）、共享内存上的 SPSC 环形缓冲（完整代码，跨 JVM 进程实测） | ④（缓存一致性、伪共享） | 2.5 h |
| ⑥ | [networking_basics.md](networking_basics.md) | 协议栈与套接字、TCP、UDP、延迟 vs 吞吐、Nagle 与 `TCP_NODELAY`、组播（交易所行情）、内核旁路、NIO `Selector`、虚拟线程 vs NIO | ⑤（系统调用、上下文切换） | 2.5 h |

一小时视频面试的现实建议：**时间不够就按 ① → ④ → ⑤（第 7 节 SPSC）→ ⑥（第 5、6 节）的顺序读**，这是 Headlands JD 最可能追问到的部分；②③在做 hc02/hc05 时读即可。

## 哪些问题讲义依赖哪一章

以下依赖关系都是对 `study/30-articles/*.md` 实际 grep 得到的（章节号是讲义里的小节号）；「计划」表示讲义里写了「更完整的讲解会放在……」而链接尚未补上。

| 章节 | 被这些讲义依赖 | 具体位置 |
|---|---|---|
| ① complexity | `oa01_job_chain` | 2.3「时间复杂度」末尾写明「更完整的讲解会放在 `study/00-foundations/complexity.md`」（链接已存在） |
| | `hc01_stock_trading_dp` | 2.1「复杂度：这题为什么不能暴力」 |
| | `hc04_queue_mean_snapshot` | 2.2「复杂度、O(1) 与均摊」（摊还证明见本章第 6 节） |
| | `hc05_market_order_book` | 2.2「复杂度记号：O(1)、O(log n)、O(n)」 |
| | `hc08_order_sequence_api` | 2.6「摊还分析」；第 5 步压缩的摊还 |
| ② heap | `hc02_merge_k_streams` | 2.2「最小堆」；步骤 1「用堆挑最小的」；步骤 3 `mergeLongs` 的去装箱 |
| | `hc05_market_order_book`（间接） | 讲义没有提到堆；本章第 9 节解释订单簿为什么用 `TreeMap` + 价位队列而不是 `PriorityQueue`（取消订单 `remove(Object)` 是 O(n)） |
| ③ ordered maps | `hc05_market_order_book` | 2.3「二叉搜索树、红黑树与 `TreeMap`」；步骤 2、7（`firstEntry`/`pollFirstEntry`）；自测 Q1（`Comparator.reverseOrder()`） |
| | `hc01_stock_trading_dp` | 5.6 `moves` 是 `TreeMap<Integer, Move>` |
| | `hc08_order_sequence_api` | 追问：order-statistic tree / skip list 能不能替代树状数组 |
| ④ cache | `hc04_queue_mean_snapshot` | 2.1 末尾「指针追逐」；步骤 4「`ArrayDeque<Long>` → `long[]`」；追问 |
| | `hc05_market_order_book` | 2.7「装箱、GC 与为什么性能题盯着分配」；步骤 9 `TickBook`（数组式订单簿） |
| | `hc06_cpu_register_bitwise` | 2.9「CPU 的分支预测与缓存」；步骤 8「解码一次，`int[]`，无分支」 |
| | `hc02_merge_k_streams` | 步骤 3「去掉装箱（`long[]` 版）」 |
| ⑤ os/ipc | `hc02_merge_k_streams` | 2.4–2.6（线程、中断、虚拟线程）、步骤 5–7（生产者-消费者、有界队列） |
| | `hc03_recursive_sum` | 2.9「线程、并行、ForkJoin、虚拟线程」；步骤 7–8 |
| | `hc04_queue_mean_snapshot` | 2.8「线程、可见性与撕裂读」；2.9「虚拟线程（细节见基础课）」——第 251–256 行写明计划放在 `00-foundations/`；Part 4 无锁读 |
| | `hc05_market_order_book` | 追问：单线程撮合引擎 + LMAX Disruptor ring buffer（讲义第 551 行）→ 本章第 7 节 |
| ⑥ networking | （暂无问题讲义直接依赖） | 对应 JD 的 networking；其中第 9 节是 `hc02`/`hc03`/`hc04` 的虚拟线程小节在网络场景下的展开 |

反过来：**做某道题前先读哪几章**

| 题 | 先读 |
|---|---|
| `oa01` Job Chain | ① |
| `hc01` 买卖股票 DP | ① |
| `hc02` 合并 K 个有序流 | ① ② ④(第 5 节) ⑤(第 1、3 节) |
| `hc03` 递归求和 | ①，⑤(第 1 节) |
| `hc04` 队列均值与快照 | ① ④ ⑤(第 7 节：环形缓冲的共享内存版) |
| `hc05` 订单簿 | ① ② ③ ④ |
| `hc06` CPU 寄存器位运算 | ④(第 8 节分支预测) |
| `hc08` Order Sequence | ① ③ |

## 配套可运行代码：`examples/`

| 文件 | 对应章节 | 做什么 |
|---|---|---|
| [`ComplexityDemo.java`](examples/ComplexityDemo.java) | ① | 数比较次数、模拟扩容复制量（验证摊还）、`HashMap`/`TreeMap` 单次操作耗时、O(n²) 实测吞吐 |
| [`HeapDemo.java`](examples/HeapDemo.java) | ② | 手写 int 小根堆并打印每次交换；建堆 vs 逐个插入的交换次数；`PriorityQueue` 各种坑的复现 |
| [`TreeDemo.java`](examples/TreeDemo.java) | ③ | 普通 BST 的高度实验、40 行跳表、`TreeMap`/`ConcurrentSkipListMap` 导航 API |
| [`CacheDemo.java`](examples/CacheDemo.java) | ④ | 6 组微基准：`long[]` vs `ArrayList<Long>`、步长、行/列优先、指针追逐延迟阶梯、分支预测、AoS vs SoA、伪共享 |
| [`IpcDemo.java`](examples/IpcDemo.java) | ⑤ | 系统调用开销、线程交接往返、`mmap` 持久化、共享内存 SPSC 环形缓冲（同进程与跨进程） |
| [`NetDemo.java`](examples/NetDemo.java) | ⑥ | Nagle 实验、`Selector` vs 虚拟线程回显服务器、回环接口上的 UDP 组播与缺口检测 |
| [`check_snippets.py`](examples/check_snippets.py) | 全部 | 把章节里每一个 ```` ```java ```` 代码块抽出来，用 `javac --release 21 --enable-preview` 编译 |

运行（均用 JDK 21）：

```bash
J=/opt/homebrew/opt/openjdk@21/bin
cd study/00-foundations/examples
$J/javac --release 21 --enable-preview *.java
$J/java --enable-preview ComplexityDemo
$J/java --enable-preview HeapDemo
$J/java --enable-preview TreeDemo
$J/java --enable-preview CacheDemo                      # 约 20 秒；需要约 1 GB 堆
$J/java --enable-preview --enable-native-access=ALL-UNNAMED IpcDemo
$J/java --enable-preview NetDemo
python3 check_snippets.py ../*.md                       # 章节里所有 java 代码块是否都能编译
rm -f *.class
```

`IpcDemo` 的跨进程模式：先 `IpcDemo consumer /tmp/ring.bin 50000000 &`，等一秒，再 `IpcDemo producer /tmp/ring.bin 50000000`。

## 关于数字的诚实说明

* 所有「本机实测」都来自 **Apple M6 / 12 核 / 16 GB / macOS / JDK 21.0.12**，是**粗糙的**单 JVM 微基准（预热 + 取最小，没有用 JMH，没有绑核）。请把它们当作**量级与方向**，不是 benchmark 结论。多次运行常有 ±30% 的波动，伪共享和跨核通信的波动可达数倍；章节里凡是波动大的地方都写了范围。
* 本机是 macOS，不是 Linux。系统调用、TCP 栈行为（例如 Nagle + 延迟确认的 40 ms 停顿没有复现）、缓存行大小（本机 128 B，x86 通常 64 B）都会不同。凡是「在 Linux 上通常是……」这类说法，如果我没有在 Linux 上验证，章节里都明确写了。
* 所有外部数字都标了出处（Norvig 的时间表、Drepper 的论文章节、Javadoc 原文）。Brendan Gregg《Systems Performance》的「时间尺度缩放表」我是凭记忆引用的量级，具体行以原书为准。

## 权威来源总清单（各章「延伸阅读」的并集）

* 教科书：CLRS《算法导论》；Sedgewick & Wayne《Algorithms》第 4 版；Hennessy & Patterson《Computer Architecture: A Quantitative Approach》；Arpaci-Dusseau《OSTEP》；Kerrisk《The Linux Programming Interface》；Stevens《TCP/IP Illustrated》《UNIX Network Programming》；Kleppmann《Designing Data-Intensive Applications》；Herlihy & Shavit《The Art of Multiprocessor Programming》。
* 手册与论文：Drepper《What Every Programmer Should Know About Memory》；Intel 64 and IA-32 Architectures Optimization Reference Manual；Agner Fog 的 microarchitecture 手册；Arm Cortex-A TRM；Pugh《Skip Lists》(CACM 1990)；Floyd / Williams 堆排序 (CACM 1964)；Thompson 等《Disruptor》(LMAX 2011)；Axboe《Efficient IO with io_uring》。
* 规范：RFC 9293 / 768 / 896 / 1112 / 1122 / 6928；JEP 444 / 442 / 380；Java SE 21 Javadoc；Nasdaq ITCH / MoldUDP64、CME MDP 3.0 公开文档。
* 性能方法论：Brendan Gregg《Systems Performance》第 2 版；Norvig《Teach Yourself Programming in 10 Years》时间表；Jeff Dean "Numbers Everyone Should Know"。
