# hc04 · 思路与追问

## 概要

面试里常见「流式数据结构」一族（队列均值 + 快照、合并多路数据流）。这道题第一问几分钟就能写完，
面试官其实是在看你**接下来 50 分钟**会不会主动想到：O(1) 均值、浮点漂移、溢出、空队列、快照是拷贝还是共享、多线程读。
本题集把这条追问链练成四个 Part。

## 逐 Part 思路

1. **QueueMean**：`long[]` 环形缓冲（容量恒为 2 的幂，用 `& (len-1)` 代替 `%`）+ 两个 `long` 拼成的 128 位累加器。push/pop 各自 O(1) 更新累加器，
   `getMean` 只做一次除法。快路径：和仍在 ±2^53 内时 `(double) sum / size` 的两个操作数都能精确表示，一次 IEEE 除法就是正确舍入；超出再走 `BigDecimal`。
2. **QueueEvents**：`sealed Event`（Push/Pop/Query/Correct）+ 模式匹配 `switch` 解释执行；`Correct` 直接换一个新的 `QueueMean`。解析时给每个错误带行号。
3. **VersionedQueue**：所有 push 过的元素组成一棵「后继树」（节点 = 一次 push，父 = push 之前版本的队尾）。一个版本 = `(尾节点, 已弹出个数, 窗口和)`，三个数。
   push 新建一个节点；pop 需要「队头的值」= 路径上深度 `headDepth+1` 的祖先，用 **skew-binary jump pointer** 在 O(log n) 内找到；均值直接从版本里的窗口和算，O(1)。
   没有任何版本复制数据。
4. **SharedMean**：写者每次改完生成不可变的 `Stat(seq, size, sum)`，用 `VarHandle.setRelease` 发布；读者 `getAcquire` 读引用。
   因为 Stat 不可变且一次发布，读者要么看到旧的完整状态要么看到新的完整状态。写者身份用 `compareAndSet` 抢占，违规线程抛 `IllegalStateException`。

## 隐藏测试会打的坑

* 用 `double` 做 running sum（`1e16 + 1 + 1 − 1e16 = 0`，不是 2）。
* 用 `long` 累加：`Long.MAX_VALUE` 两个就溢出；有人会用 `Math.addExact` 抛异常——题目要的是「正确」，不是「报错」。
* `pop` 后和不「退回」：累加器一旦转成 `BigInteger` 就不再转回的实现，性能会塌；这里 128 位没有这个问题。
* 空队列的 `getMean`：除以 0 得到 `NaN`，被当成合法答案。
* 环形缓冲扩容时直接 `Arrays.copyOf`：`head` 在中间时顺序全乱（测试里专门让 head 停在 10）。
* `Mean` 没约分/负分母：`6/-4` 与 `-3/2` 不相等。
* `Correct(List)` 不拷贝：调用者之后修改列表，历史被偷偷改写。
* 版本化：每个版本复制一份数组（`m = 20,000` 个版本就要 168 ms，按 O(n²) 增长，30 万版本直接超时）。
* 并发：读者分两次读 `sum` 和 `size`；或者用 `volatile` 两个字段——都会读到撕裂值。

## 复杂度

| 操作 | 时间 | 备注 |
|---|---|---|
| `QueueMean.push/pop/getMean` | O(1) 均摊 | 扩容翻倍 |
| `QueueEvents.run` | O(事件数 + 快照总长度) | |
| `VersionedQueue.push/mean/size` | O(1)，`pop` O(log n) | 每节点 4 个原始数组槽 + 每版本 4 个 |
| `SharedMean.read` | O(1)，无锁 | 写者每次分配一个 `Stat`（32 字节左右） |

量级参考：

* 100 万次随机 push/pop + 每 8 次一个 `getMean`：远低于 2 s。
* 20 万次 push（队列长度保持在 2 万以内）、每两次 push 求一次均值：朴素「每次遍历求和」2604 ms，`QueueMean` 3 ms。
* 2 万个版本：每版本复制数组 168 ms，`VersionedQueue` 1 ms。

## Java 21 特性

| 特性 | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| record | `Mean`（紧凑构造器里约分）、`I128`、`Push/Pop/Query/Correct`、`Stat` | 值对象 + `equals` 自带，测试直接比较 `Mean`；约分写在构造器，保证全程只有规范形式 |
| sealed | `Event`、`Answer` | 事件种类封闭；加一种事件，所有 `switch` 编译报错，不会漏处理 |
| switch 模式匹配 | `QueueEvents.run` | 不用 `instanceof` 链 + 强转，也不用 visitor |
| record 模式 | `render`：`case Value(QueueMean.Mean(var n, var d)) when d == 1` | 一行拆开两层嵌套 + `when` 守卫 |
| switch 表达式 + `yield` | `parse` | 每个命令有自己的块，没有 fallthrough |
| 未命名模式 `_`（预览） | `case Pop _`、`catch (InterruptedException _)` | 明说「这个绑定不用」 |
| `VarHandle` | `SharedMean` 的 `setRelease/getAcquire/compareAndSet` | 比 `volatile` 更精确：只要「发布」语义，不要 `volatile` 写的全序开销；也比 `synchronized` 不 pin 虚拟线程 |
| 虚拟线程 | 测试里 `Executors.newVirtualThreadPerTaskExecutor()`、`Thread.ofVirtual()` | 起 5 个读/写线程几乎免费；注意：纯自旋的虚拟线程会饿死别人，所以读者循环里有 `Thread.yield()` |

## 面试官可能的追问

1. **为什么不用 `ArrayDeque<Long>` / `LinkedList<Long>`？** 装箱：每个元素一个 `Long` 对象，指针追逐，GC 压力；`long[]` 环形缓冲是连续内存，100 万元素 8 MB 且预取友好。`ArrayDeque` 本身也是环形数组，只是存引用。
   *答案要点*：先说「O(1) 都一样」，再说常数因子和缓存局部性；承认 `ArrayDeque` 在没有性能要求时是更好的选择（少写代码）。
2. **均值返回 `double` 不够精确怎么办？** 返回分数 `numerator/denominator`（约分）；需要十进制时让调用者选舍入。我的 `getMean` 保证返回「最接近精确值的 double」：和在 ±2^53 内时一次除法就是正确舍入。
3. **128 位够吗？** n 个 `long` 之和的绝对值 ≤ n·2^63；n < 2^63 时 < 2^126，128 位有符号数一定放得下，而队列元素个数最多 2^31，所以绝对安全。若要「任意多」就用 `BigInteger`，代价是分配。
4. **快照要存 O(n) 吗？持久化怎么做？** 说出三档：整份复制 O(n)/版本；路径复制（persistent）；我的做法——元素放进一棵树，版本只是三个数，push O(1)，pop O(log n)。内存只增不减，要回收就需要引用计数或「只保留最近 K 个版本」。
5. **多个读者怎么保证读到一致？** 不可变快照 + 一次发布；对比：`synchronized`/`ReentrantReadWriteLock`（读写互斥）、`StampedLock.tryOptimisticRead`（读完校验 stamp，失败重读，适合写少读多）、两个 `volatile` 字段（撕裂）。
   *关键词*：happens-before、release/acquire、不可变对象的安全发布。
6. **写者也想多个怎么办？** 要么串行化（队列 + 单线程执行器），要么换成 CAS 循环更新不可变 `Stat`（`AtomicReference`），冲突时重试；pop/push 不再是单线程可推理的 FIFO，需要先问清楚语义。
7. **C++ 版本怎么写？** `std::vector<int64_t>` 环形缓冲 + `__int128` 累加器；发布用 `std::atomic<std::shared_ptr<const Stat>>`（C++20）或 `atomic<Stat*>` + hazard pointer/epoch 回收。
