# kq 语言深度题 · 评分标准（强 / 一般 / 弱）

> 用途：自测时用手机录 60 秒，对着下面的标准打分。面试官的评价维度来自 `loop/LOOP_GUIDE.md` §1：「性能直觉」「系统细节的好奇心」「strong knowledge of the details of computing all throughout the technical stack」（O-C2）、低自我。
> 这些标准是**本 kit 的判断**（`推断`），没有 Headlands 的官方评分表。题号对应 `questions.md`。

## 通用（每一题都适用）

| | 强 | 一般 | 弱 |
|---|---|---|---|
| **结构** | 先一句话结论，再机制（为什么），再一个具体数字或例子，最后说边界/代价（「什么时候不成立」） | 有结论和机制，但没有例子或边界 | 先讲背景、绕半天才说结论；或只有术语列表 |
| **量化** | 给出数量级（「16 字节头」「亚毫秒」「慢约 10 倍」），并说明是自己测的还是常识 | 只说「更快」「更省」 | 用「很快」「很慢」，或说错数量级 |
| **诚实** | 明确分开「我测过」「我记得但没验证」「我不确定」；不确定时说怎么验证 | 偶尔含糊 | 编造细节、把不确定的当事实；被追问时硬撑 |
| **Java ↔ C++** | 能说清「C++ 里对应的是什么、Java 为什么不同、代价在哪」 | 只讲 Java，不接对方的话题 | 贬低一方或「Java 一样快」式的一刀切 |
| **追问** | 追问时往下一层走（从 GC 到 safepoint 到 OS），不会被一个「为什么」问倒 | 能答第一层追问 | 第二个「为什么」就重复第一层或沉默 |
| **时间** | 60 秒内说完要点，然后问「要我展开 X 还是 Y？」 | 90–120 秒 | 超过 2 分钟仍在铺垫 |

**共同的红线**：说「Java 比 C++ 快/慢」而不限定场景；把预览特性说成正式；说 `volatile` 能保证原子递增；说「GC 慢所以不能用于低延迟」而不知道 ZGC；说「ConcurrentHashMap 用分段锁」（那是 Java 7）；把没跑过的命令输出当真。

---

## [A] 速度与延迟（Q01–Q04）

* **强**：说出「稳态靠 JIT + 运行时 profile（内联、去虚化、逃逸分析），差距在尾部——预热、去优化、GC/safepoint、对象头与指针」；能给一个自己测的数（如逃逸分析开/关的分配量；GC 最大停顿对比）；被问「为什么还用 C++」时承认内存布局与内核旁路的差距，并说出缓解手段（零分配、原始数组、堆外、ZGC、绑核）。能在预热题里说出「用真实多样的流量预热，否则触发去优化」。
* **一般**：知道 JIT 把热点编译成机器码、GC 有暂停、C++ 没有；说不出具体机制或数字；预热只会说「先跑一会」。
* **弱**：「Java 是解释型所以慢」；「JVM 慢是因为 GC」没有后文；或相反「Java 和 C++ 一样快」；不知道 C1/C2。

## [B] 版本差异（Q05–Q06）

* **强**：按 LTS 8/11/17/21 讲，每个版本一个特性 + 一个你会用的理由；能把 record + sealed + 模式 switch 串成一个故事（编译器检查穷尽，对比 visitor）；知道运行时差异（G1 默认、紧凑字符串、偏向锁移除、虚拟线程）；区分正式与预览。
* **一般**：能列 lambda/Stream、var、record、虚拟线程，但没有「为什么」和「什么时候不用」。
* **弱**：把非 LTS 当必考、混淆版本号（如说 record 是 Java 11）、提到已撤回的 String Templates、把预览特性当生产特性。

## [C] 语言对比与所有权（Q07–Q10）

* **强**：Java vs Python：静态/动态、JIT/解释、GIL、整数语义（回绕 vs 大整数、`/` 与 `%` 对负数的差异），并给选型。智能指针：知道 Java 没有所有权，GC 做可达性，`WeakReference` ≈ `weak_ptr`，RAII ≈ try-with-resources，`finalize` 被弃用，Cleaner 无时机保证。泛型：擦除 → 装箱 → 内存与缓存代价，Valhalla 是动机但 21 还没有。
* **一般**：能答对表面（Java 有 GC 所以不用智能指针），但不提非内存资源要显式关闭；泛型只说「编译期检查」。
* **弱**：「Java 的引用就是 C++ 指针」；「Java 对象按引用传递」（应为引用按值传递）；不知道循环引用在 GC 下不是问题。

## [D] 分配与内存（Q11–Q17）

* **强**：`new` = TLAB 指针碰撞 + 清零 + 构造，代价后移到 GC，逃逸分析可消除；对象头 12 字节 + 8 字节对齐，能心算 `Integer`=16、`int[10]`=56，`ArrayList<Integer>` ≈ 5 倍于 `int[]`；`Integer` 缓存与 `==`；`String` 不可变/紧凑/缓存 hash/循环拼接 O(n²)；堆外的收益与风险（生命周期、限制、不可见）；缓存行与伪共享，能说「顺序遍历 vs 追指针」约一个数量级。`System.arraycopy` 是 memmove 语义，稳态下手写循环可能被优化成同样的东西，但仍然优先 arraycopy。
* **一般**：知道 `new` 在堆上、有 GC，知道装箱有开销但不会量化；知道 `StringBuilder`。
* **弱**：把 C++ 的 `malloc`/`new` 机制原样套到 Java；说 `substring` 共享底层数组（那是 Java 6 的行为）；不知道缓存行。

## [E] JIT 与 GC（Q18–Q24）

* **强**：分层编译（解释器 → C1 → C2）、OSR、阈值概念；内联的条件（方法大小）和多态内联缓存（单/双/多态）；逃逸分析的收益与失败条件；去优化的触发例子与对延迟的影响；GC：根、分代、Parallel/G1/ZGC 的权衡，选型与诊断顺序（先量再调，降分配率优先）；safepoint 的两段时间；能说出怎么观测（`-XX:+PrintCompilation`、`-Xlog:gc,safepoint`、`jstat`、JFR）。
* **一般**：知道 JIT/GC 的存在与名称，会说「G1 默认、ZGC 低延迟」，但说不出观测方法或权衡。
* **弱**：把 JIT 说成「第一次运行时编译一次」；「调大堆就能解决 GC 问题」；不知道 `System.gc()` 的危害；不区分 young/full GC。

## [F] 并发与内存模型（Q25–Q33）

* **强**：JMM 的目的与 happens-before 规则（监视器、volatile、start/join、传递性）；`volatile` = 可见性 + 有序性但非原子，能举例并说「`count++` 要用 atomic/`LongAdder`」；`synchronized` vs `ReentrantLock` 及 21 里的 pinning；CAS 的原理、ABA、高竞争下 CAS 重试的问题；HashMap 的 `h ^ (h>>>16)`、2 的幂、扩容、树化阈值（8 与表 ≥ 64）；CHM Java 8 的 CAS + 桶头 `synchronized`，null 禁止的原因；虚拟线程适用/不适用；线程池参数顺序和无界队列陷阱；安全发布与 DCL 的 `volatile`；`final` 字段语义。
* **一般**：能背出 volatile 保证可见性，知道 CHM 比 `synchronizedMap` 好，但说不出机制；对 happens-before 只能给定义，给不出规则或例子。
* **弱**：「volatile 保证线程安全」；「synchronized 很慢所以不用」；「CHM 分段锁」；不知道线程池无界队列的问题；DCL 不加 volatile。

## [G] 操作系统与 Linux 性能工具（Q34–Q37）

* **强**：区分进程/线程/虚拟线程，上下文切换直接与间接成本；虚拟内存、缺页、page cache、RSS vs `-Xmx`（能列出堆外组成并说出 NMT）；排查流程自上而下（`top` → `vmstat` 的每一列含义 → `iostat`/`ss` → `top -H` + `jstack` nid → `perf stat`/`perf record` → `strace -c`），知道 strace 开销大、perf 看 Java 需要符号方案；JVM 侧工具：`jcmd Thread.print`、`jstat`、`GC.class_histogram`、JFR。**并且清楚地说明哪些是亲手跑过的、哪些是知识**。
* **一般**：知道 `top`、`vmstat`、`strace` 的名字和大意，能说出 CPU/内存/磁盘/网络四类资源，但不会读 `vmstat` 列，也不会连到 JVM。
* **弱**：只会「看日志」「重启」；把 `load average` 当 CPU 使用率；不知道 `jstack`/`jcmd`。

## [H] 进程间通信（Q38–Q39）

* **强**：列出管道/套接字/共享内存/消息队列/信号/文件并说出数据路径（拷贝次数）与同步责任；共享内存最快但要自己同步、处理对端崩溃；Java 里用 `MappedByteBuffer` + `VarHandle`（或 FFM），SPSC 环形缓冲、head/tail 分缓存行、release/acquire；有数量级（本机：管道 ~3 µs、loopback TCP ~12 µs、共享内存 ~0.15 µs）。
* **一般**：能列出方法并比较快慢；对 Java 实现没有想法，或只知道 `Socket`。
* **弱**：「IPC 就是 socket」；认为 `ByteBuffer.putLong` 在两个进程间自动可见；认为 JVM 内的 `synchronized` 能锁住别的进程。

## [I] 网络（Q40–Q42）

* **强**：TCP 握手/确认/重传/拥塞控制；Nagle + 延迟 ACK 的相互作用与「一条消息一次 write + `TCP_NODELAY`」；`Selector`/epoll 反应器 vs 线程每连接 vs 虚拟线程；`epoll` 为什么优于 `select`；低延迟网络清单（二进制协议、忙轮询、绑核、UDP 多播、内核旁路），并诚实说出 Java 在内核旁路上弱。**能说「我在 macOS 上没复现 40 ms，那是 Linux 常见现象」这样的限定**。
* **一般**：知道 NODELAY，知道 NIO 比 BIO 并发高，说不出为什么。
* **弱**：把 `TCP_NODELAY` 说成「更快的协议」；认为 NIO「更快」而不是「更能扩展」。

## [J] 存储（Q43–Q45）

* **强**：`write` 只到 page cache，`fsync`/`force` 才耐久；每条 fsync vs 组提交的数量级差（本机约 900 倍 vs 约 4 倍）及原因；WAL、顺序写、预分配；mmap 的收益与坑（缺页尾延迟、unmap、2 GB、错误语义）；B 树 vs LSM 的读写放大权衡；复制/共识的延迟代价；能把存储选型与「研究数据一次写多次读」联系起来。
* **一般**：知道 fsync 慢、知道 LSM 写快，但说不出为什么，或不会谈一致性与复制。
* **弱**：认为 `write` 返回即持久；认为 mmap 总是更快；把 CAP 当口号。

---

## 自测流程

1. `python3 build_bank.py` 后用 `bank.json` 抽题（按 topic / difficulty）。
2. 每题：盖住答案，计时 60 秒口述（英文），录音。
3. 对照上表给自己打「强 / 一般 / 弱」，**弱的立刻回 `questions.md` 读该题的「展开」并重跑对应 demo**（`demos/run_all.sh`）。
4. 周期：电话面前 3 天，每天 10 题，优先 ★★ 与 ★★★；最后一天只过「一句话答案」和红线，不学新东西（`LOOP_GUIDE.md` 的 F-A8 教训）。
