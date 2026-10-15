# kq 语言深度题库（Java 版）· 45 题

> **这是什么**：Headlands 电话面里「语言深度」类问题（CATALOG Table D，kq01–kq06）的 Java 版。所有一手报告都是 **C++** 候选人写的，**没有任何 Java 知识题的一手报告**
> （`catalog/CATALOG.md` Table D 开头原话：「没有任何来源是 Java 知识题的一手报告」）。所以每道由 C++ 问法翻译来的题，来源行都标 `推断：Java 对应`，并引用 C++ 原话；
> Java 原生经典题标 `推断：Java 低延迟岗经典`；与 Java JD（`catalog/raw/official_and_process.md` §C2）对应的题标 `推断：JD`。**这些「会被问到」的判断全部是推断，不是证据。**
> 面试节奏证据：「面试官反应很快，喜欢讨论 C++ 相关的技术知识」（F-A1）、「c++/Python 的区别，会问得比较详细」（F-A8）、「招 c++ linguist」（F-A2）；见 `loop/LOOP_GUIDE.md` §1「常见挂法」。

## C++ 原题 → 本题库的 Java 题（对照表）

| 报告里的 C++ 问法（来源） | CATALOG | 本库的 Java 翻译 |
|---|---|---|
| 「为什么C++比别的语言快？」+ follow up「为什么比别的需要compile的语言也快？」（1p3a 1011799，F-A13） | kq04 | Q01、Q02；延伸 Q03（什么时候不够快）、Q04（预热）、Q18–Q24（JIT/GC 机理） |
| 「Differences between C++ 11, 14, 17, and 20」（WSO，F-W2）；「C++ versions」（1p3a 974931，F-A16） | kq02 | Q05（Java 8/11/17/21）、Q06（运行时差异） |
| 「c++/Python的区别，会问得比较详细。在哪种情…」（1p3a 1068621，F-A8） | kq05 | Q07（Java vs Python）、Q09（Java vs C++ 的保证）、Q10（泛型 vs 模板） |
| 「smart pointers」（F-A8） | kq05 | Q08（引用/GC/try-with-resources） |
| 「`malloc` vs `new`」（Blind 2023-03，OP §D2，低置信） | kq06 | Q11（`new` 与分配）、Q13（对象布局）、Q14–Q16（装箱/字符串/堆外） |
| 「`std::copy` vs `memcpy`」（同上） | kq06 | Q12（`System.arraycopy`） |
| 「IPC methods」（974931，F-A16）、「interprocess communication」（938472，F-A18）、「shared memory」（1011799，F-A13） | kq03 | Q38、Q39 |
| 「OS concepts, concurrency, open-ended systems」（Glassdoor RVW89062704，F-G2） | kq01 | Q25–Q33（并发/JMM）、Q34–Q37（OS 与 Linux 工具）、Q40–Q45（网络与存储） |
| 公司博客 #3「OutOfLine – A Memory-Locality Pattern」（OP §B2） | — | Q13、Q17（对象布局与缓存行） |
| Java JD（OP §C2）：Linux/性能瓶颈/监控/网络/存储 | — | Q35–Q37、Q40–Q45 |

## 怎么用

* 每题结构（教科书模式，`study/TEXTBOOK.md`）：**难度 → 来源 → 一句话答案 → 展开（前因后果，从零讲） → 能说出口的 60 秒版本（英文，面试时直接说） → 面试官可能的下一问**。
* 难度：★ 基础（必须秒答）· ★★ 中等（电话面主力）· ★★★ 深（追问到这里算加分）。
* **Demo**：凡是几行代码能演示的 Java 说法，都有在本机编译并运行的 demo（`demos/Kxx*.java`，原始输出全文在 `demos/OUTPUTS.txt`，一键复现 `demos/run_all.sh`）。
  环境：JDK 21.0.12.1，Apple Silicon（arm64，12 核，16 GB），macOS。**数字只看量级和趋势**，不是严格基准（没用 JMH）；Linux/x86 上数字会不同。
* 链接约定：`S10/Jxx_*.md` 是已有的 Java 21 课文；`S00/*.md` 是 `study/00-foundations/` 的六章（`complexity`、`heap_priority_queue`、`ordered_maps_trees`、`cpu_cache_locality`、`os_processes_threads_ipc`、`networking_basics`，文件名核对自 `study/00-foundations/README.md`）。
  基础课里**没有** JMM / JIT / GC / 哈希表专章：JMM 与 CAS 看 `S10/J16_concurrency_primitives.md`，JIT / GC 看 `S10/J19_runtime_zgc_jit.md`，虚拟线程看 `S10/J10_virtual_threads.md`，哈希表看 `S30/hc07_ticker_hash_map.md`。
* 练习：先盖住答案，计时 60 秒口述，再对照「一句话答案」和「展开」补漏。评分标准见 `rubric.md`；机器可读题库 `bank.json`（由 `build_bank.py` 从本文件生成，不要手改）。

路径前缀（本文件位于 `loop/rounds/01_video/kq_language_depth/`）：`S10 = ../../../../study/10-java21/`，`S00 = ../../../../study/00-foundations/`，`S30 = ../../../../study/30-articles/`。

---

## [A] 速度与延迟：为什么快、什么时候不够快（kq04）

### Q01 · Why can Java be fast even though it is garbage-collected and runs on a VM? What does the JVM do at run time that a C++ compiler does ahead of time?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（1p3a 1011799，F-A13，2023-08，CATALOG kq04）：「为什么C++比别的语言快？」→ https://www.1point3acres.com/interview/thread/1011799
- **一句话答案**：Java 源码先编成字节码，运行时热点方法被 JIT（C1/C2）编成机器码，并且可以利用**运行时才知道的信息**（真实的类型分布、分支概率、哪些类已加载）做内联、逃逸分析、去虚化；代价是预热、GC 和比 C++ 更大的内存占用。

**展开**

先弄清「快」是什么意思。一段程序慢，原因几乎总是下面几类之一：

```
 1. 执行指令太多        -> 解释执行 vs 编译成机器码；有没有内联、有没有多余的检查
 2. 等内存              -> 缓存未命中；对象散落在堆里要追指针
 3. 做了不必要的工作    -> 分配对象、装箱、虚调用、锁
 4. 被打断              -> GC 暂停、线程切换、系统调用
```

C++ 的答案是：**把 1、3 全部交给编译器在编译期（AOT, ahead-of-time）解决，把 2、4 交给程序员手工控制**。
具体地：模板在编译期按类型展开并内联（"零开销抽象"）；对象可以放在栈上、成员内联在父对象里，所以数据是连续的；
没有 GC，析构是确定的；数组下标默认不检查；有未定义行为（UB）这个"承诺"，编译器可以放心做激进优化。

Java 的路线完全不同：

```
 Foo.java --javac--> Foo.class(字节码) --JVM--> 解释器(tier0) --热了--> C1(tier1-3, 快速编译, 带 profiling)
                                                          --更热--> C2(tier4, 激进优化)
                                                                         ^
                       运行时 profile: 这个调用点实际只见过 1 种类型 / 这个分支 99.9% 不走
```

* **JIT 的优势是信息**：C++ 编译器在编译期不知道某个接口调用点运行时到底是哪个实现类；HotSpot 看到"这个调用点只见过 `Sq`"，就直接把 `Sq.area` 内联进去（并留一个陷阱防止以后猜错，见 Q21）。这就是 profile-guided optimization，只是自动且在线。
* **逃逸分析**（Q20）：证明对象不会跑出方法，就根本不分配，字段拆成寄存器。本机 demo `K04EscapeAnalysis`：同一段代码，开着逃逸分析 steady state 分配 **0 字节**、约 48 ms；用 `-XX:-DoEscapeAnalysis` 关掉，分配 **4,800,000,000 字节**、约 386 ms（8 倍慢）。
* **内联 + 去掉边界/空指针检查**：循环里数组访问的边界检查常被提到循环外（range check elimination），空指针检查用"出了信号再处理"的隐式检查实现，热路径上几乎没有开销。
* **代价**（所以"什么时候不够快"见 Q03）：预热期慢（Q04）、GC（Q22–24）、对象头 + 指针追逐（Q13、Q17）、内存占用大。

**怎么回答"和 C++ 比"才不翻车**：不要说"Java 一样快"（面试官是做低延迟的，会不信），也不要说"Java 慢"。要说"稳态吞吐可以接近；尾延迟和内存布局是差距所在；我知道差距在哪里、怎么缩小"。

**能说出口的 60 秒版本**

> "Java isn't interpreted in steady state. The JVM starts in an interpreter, profiles the code, and compiles hot methods to machine code - first with C1, then with C2, which does aggressive optimization: inlining, escape analysis, loop optimizations, bounds-check elimination. The interesting part is that it optimizes with *runtime* information, like which classes a call site has actually seen, so it can devirtualize and inline calls a static compiler has to leave virtual. In a quick experiment, the same loop allocated zero bytes with escape analysis on and 4.8 GB with it off, about eight times slower. The price is warm-up time, GC, and a heavier memory layout - object headers and pointers - which is where C++ still wins on tail latency."

**面试官可能的下一问**

* "So if it's that good, why do HFT firms still write C++?"（→ Q03）
* "What's the difference between C1 and C2? What is tiered compilation?"（→ Q18）
* "Show me how you would check that a method was inlined."（`-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining`，Q19）

**Demo / 课文**：`demos/K04EscapeAnalysis.java`；`demos/K10Jit.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q02 · You said Java is also compiled. Then what makes C++ faster than other compiled languages — and where does Java sit relative to C++, Go and Rust?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（F-A13 follow-up，CATALOG kq04 p2）：「follow up：为什么C++比别的需要compile的语言也快？」→ https://www.1point3acres.com/interview/thread/1011799
- **一句话答案**：速度差异不来自"是否编译"，而来自**运行时系统的厚度和内存布局的控制权**：GC、边界检查、虚调用、对象头、能否把数据内联进父对象；C++/Rust 把这些成本设计成"用才付费"，Java/Go 把一部分成本变成默认。

**展开**

"编译"只是把源码变成机器码。真正决定速度的是编译之后**还剩多少运行时工作**：

| 维度 | C++ | Rust | Go | Java (HotSpot) |
|---|---|---|---|---|
| 编译时机 | AOT | AOT | AOT | JIT（运行时） |
| 内存回收 | 手动/RAII | 所有权（编译期） | GC | GC |
| 值类型/内联布局 | 有（struct 成员内联） | 有 | 有 | **没有**（21；Valhalla 未发布）：除原始类型外都是堆对象 + 引用 |
| 数组边界检查 | 默认无 | 默认有（可被优化掉） | 有 | 有（JIT 常消除） |
| 泛型实现 | 模板按类型展开 | 单态化 | 字典/展开混合 | 擦除，容器里装引用（装箱） |
| 未定义行为 | 有（优化器可利用） | 无（unsafe 除外） | 无 | 无（数据竞争也有定义的弱语义） |
| 多态调用 | 非虚默认；虚调用需手动 | trait 静态分发默认 | 接口间接调用 | 虚调用默认，JIT 去虚化 |

所以 C++ 对 Go 和 Java 的优势是**结构性**的：

* **内存布局**：`std::vector<Order>` 是一块连续内存，遍历是顺序读；`ArrayList<Order>` 是一块"指针数组"，每个 `Order` 散落在堆上，遍历是追指针（Q17 的 demo：同样 1200 万个 long，`long[]` 约 2 ms，打乱顺序的 `Long[]` 约 29 ms）。
* **没有隐式暂停**：C++ 你不分配就没有 malloc，没有 GC 线程抢核、没有 safepoint（Q24）。
* **ABI 稳定的小对象**：`struct {int; long;}` 24 字节没有头；Java 同样的 record 每个实例有 12 字节头（Q13 实测 `P2(int,int)` = 24 字节）。

Java 的反向优势：profile 引导的去虚化（Q01）、没有 UB 造成的"优化器惊喜"、内存安全、生产力。Go 在启动速度和尾延迟上通常好于 Java 的 G1，但稳态峰值通常不如 C2。（这条是一般认识，未在本机测。）

**能说出口的 60 秒版本**

> "Compilation by itself doesn't decide speed - what matters is how much runtime work is left and how much control you have over memory. C++ and Rust let you lay data out contiguously, put structs inline in arrays, avoid allocation entirely, and there's no collector. Java and Go have a GC, and in Java almost everything except primitives is a heap object behind a reference, so a list of orders is a list of pointers. That's a cache-locality cost, not an instruction-count cost - in a quick test, summing a shuffled `Long[]` was roughly ten times slower than summing a `long[]`. Java gets some of it back with JIT optimizations that a static compiler can't do, but the memory model is the structural gap until value types arrive."

**面试官可能的下一问**

* "What is Project Valhalla trying to fix?"（值类型，消除头与指针；21 尚未发布，只需知道动机。）
* "Rust has no GC either - why isn't it just 'C++ with safety'?"（所有权在编译期证明安全，边界检查可被消除；不要在这里展开太多，转回 Java。）
* "How do you get contiguous layout in Java today?"（原始类型数组 + 并行数组/结构化数组；`ByteBuffer`/`MemorySegment` 打包记录，Q16。）

**Demo / 课文**：`demos/K21Locality.java`、`demos/K03ObjectSize.java`；`S00/cpu_cache_locality.md`；`S00/examples/CacheDemo.java`。

---

### Q03 · Where can Java approach C++ latency, and where can't it? How would you build a low-latency Java system?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`；与 JD 对应：「Address performance limitations within our own software … Linux」「Improve networking communication … to achieve optimal latency and throughput」（O-C2）。公司博客 #3 讲热/冷数据与缓存行（O-B2，C++），同一思想。
- **一句话答案**：**稳态热路径可以接近 C++（几百纳秒到微秒级），差距在尾部**：GC/safepoint 暂停、JIT 预热与去优化、对象头与指针追逐、没有内联值类型；做法是"热路径零分配 + 预热 + 选低暂停 GC + 绑核 + 必要时堆外"。

**展开**

可以接近的部分（有证据）：

* 热点循环、数值计算、小对象被逃逸分析消除后——和 C++ 同一数量级。本机 demo：`K04` steady state 每次迭代约 1 ns。
* 尾延迟的 GC 部分可以压到亚毫秒：同一负载（`K19Pauses`，8 秒、约 100 MB 活跃数据、持续分配垃圾，堆 1 GB，探测线程记录相邻迭代的最大间隔）：

```
 Parallel GC          max gap 22.4 ms   gaps>1ms: 230   gaps>10ms: 10
 G1                   max gap  8.2 ms   gaps>1ms: 116   gaps>10ms:  0
 Generational ZGC     max gap  0.14 ms  gaps>1ms:   0   gaps>10ms:  0
 (对照: 不分配垃圾)   max gap  0.02 ms 与 2.26 ms（两次独立实跑）= 操作系统自身的抖动，别把它算到 GC 头上
```

  （一次实跑，`demos/OUTPUTS.txt`；ZGC 用 `-XX:+UseZGC -XX:+ZGenerational`，21 里分代 ZGC 需要显式打开。）

不能（或很难）接近的部分：

| 差距 | 为什么 | 缓解 |
|---|---|---|
| 预热 | 方法要先解释执行、被 C1/C2 编译；第一批请求慢（Q04） | 启动时回放典型流量；固定热路径；考虑 CDS/AOT 缓存（JDK 新版本在推进，21 不要依赖） |
| 去优化 | 推测失败时回到解释器（Q21） | 避免热路径上类型分布突变；上线前用真实多样的输入预热 |
| 内存布局 | 无值类型；每个对象 12 字节头 + 对齐；容器装引用 | 原始类型数组、并行数组、`ByteBuffer`/`MemorySegment` 打包 |
| GC | 即便 ZGC 也有读/写屏障开销和并发线程抢核；分配速率过高仍会拖垮 | 热路径零分配（对象池/复用、避免装箱、避免 lambda 捕获） |
| 系统调用/网络 | JNI/FFM 有调用开销；没有一流的内核旁路支持 | 第三方库、固定线程绑核；这类场景 C++ 仍占优 |
| 尾部的其他来源 | safepoint、页错误、操作系统调度 | `-Xlog:safepoint`、`-XX:+AlwaysPreTouch`、绑核（Q34） |

**一个低延迟 Java 热路径的 checklist**：单线程事件循环（避免锁）→ 预分配的环形缓冲/对象复用 → 原始类型 + 避免装箱 → 不用 `String` 拼接和日志格式化 → 无锁队列在线程间传递（SPSC）→ 预热 → ZGC 或足够大的堆 + 调好 G1 → 线程绑核 → 用 JFR / 分配 profiler 验证"热路径真的不分配"（`ThreadMXBean.getThreadAllocatedBytes`，见 `K02`/`K03`）。

**能说出口的 60 秒版本**

> "In steady state, hot loops can get close to C++. The gap is in the tail. First, warm-up and deoptimization - the first requests run in the interpreter, and a changed type profile can throw compiled code away. Second, GC and safepoints - I measured the same allocation-heavy workload with a jitter probe: Parallel GC had a max stall around 22 ms, G1 about 8 ms, generational ZGC about 0.14 ms. Third, memory layout: no value types, so objects carry headers and sit behind pointers. The way I'd build a latency-critical Java path is: keep the hot path allocation-free, use primitive arrays or off-heap buffers, pre-warm, use ZGC, pin threads, and verify with JFR and allocation counters rather than trust intuition. For things like kernel-bypass networking, I would honestly still expect C++."

**面试官可能的下一问**

* "How do you prove the hot path doesn't allocate?"（`getThreadAllocatedBytes` 前后差；JFR allocation events；`-Xlog:gc` 里没有 young GC。）
* "Why not just give the heap a huge size and disable GC?"（Epsilon GC：`-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC`，只适合短命进程/基准；本机未跑。）
* "What about the pause from `System.gc()` or class loading?"（Q24）

**Demo / 课文**：`demos/K19Pauses.java`、`demos/K04EscapeAnalysis.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q04 · Your Java service is slow for the first few seconds after start-up, then fine. Why, and what would you do about it?

- **难度**：★★
- **来源**：`推断：Java 低延迟岗经典`（预热是 Java vs C++ 的标准差距；与 Q01 的 follow-up 同源）。
- **一句话答案**：因为代码一开始在**解释器**里跑，热点要累计到阈值才被编译，而且 JIT 编译线程、类加载、CDS 都要时间；做法是预热（回放真实流量）、减少启动期类加载、必要时提前编译（AOT/CDS 类共享），并不要把预热前的数据计入延迟 SLO。

**展开**

看 `K10Jit` 的前 12 批（每批 2 万次调用同一方法，本机实测）：

```
 cold batch  0:  23.6 ns/call     <- 解释器
 cold batch  1:  20.1 ns/call
 cold batch  2:  19.9 ns/call
 cold batch  3:   8.5 ns/call     <- C1 版本上线（这一批是混合）
 cold batch  4:   2.2 ns/call     <- C2 版本上线
 ...
 cold batch 11:   2.2 ns/call     <- 稳态：约 10 倍快
```

原因链：

1. 字节码被**解释执行**（慢约一个数量级）。每个方法/循环有计数器。
2. 计数器过阈值（本机默认 `Tier3InvocationThreshold` 之类，见 `-XX:+PrintFlagsFinal`：`Tier4InvocationThreshold=5000`）→ 入编译队列，**后台编译线程**编译；编译完成才切换。
3. C1 版本带 profiling，稍慢；够热再让 C2 做激进编译（可能几十到几百毫秒）。
4. 方法被调用多次但在一个长循环里？用 **OSR**（on-stack replacement）在循环中途切换。`-XX:+PrintCompilation` 里带 `%` 的行就是 OSR。

对策：

* **预热**：上线前用与生产同分布的流量/回放跑一遍（注意：只用单一类型预热会让 C2 做过于乐观的推测，真实流量一来触发去优化，Q21）。
* **减少类加载/初始化**：CDS（类数据共享，JDK 默认有 JDK 类的归档；应用类可用 AppCDS）。
* **服务注册晚于预热**：负载均衡把预热完成的实例才加入。
* AOT / native image（GraalVM）：启动快，但峰值通常低于 C2，且反射/动态特性受限；Leyden 项目在推进 AOT 缓存（21 里没有，不要说已有）。

**能说出口的 60 秒版本**

> "A JVM starts every method in the interpreter, which is about ten times slower than compiled code in my test - 24 ns per call versus 2 ns. Counters trigger C1 compilation, then C2 for the really hot code, in background compiler threads, so there is a window where you're slow. In production I handle it by warming up before taking traffic - replaying realistic requests, not a single synthetic one, so the profile isn't skewed - keeping the instance out of the load balancer until it's warm, and using class-data sharing to cut start-up work. If start-up matters more than peak throughput, native image is an option, with trade-offs."

**面试官可能的下一问**

* "Why can't the JVM just compile everything immediately?"（编译贵，且没有 profile 就没有优化信息；分层编译就是为了折中。）
* "How would you see which methods are compiled?"（`-XX:+PrintCompilation`）

**Demo / 课文**：`demos/K10Jit.java`；`S10/J19_runtime_zgc_jit.md`。

---

## [B] 版本差异（kq02）

### Q05 · What are the main differences between Java 8, 11, 17 and 21? Which features would you actually use?

- **难度**：★
- **来源**：`推断：Java 对应`。C++ 原题（WSO 2020-11，F-W2，kq02）：「Differences between C++ 11, 14, 17, and 20」→ https://www.wallstreetoasis.com/company/headlands-technologies-llc/interview ；1p3a 974931（F-A16）「C++ versions」→ https://www.1point3acres.com/interview/thread/974931
- **一句话答案**：8 = lambda/Stream/Optional/`java.time`；11 = `var`、HttpClient、字符串/集合小工具（第一个 8 之后的 LTS）；17 = record、sealed、文本块、`switch` 表达式、`instanceof` 模式；21 = `switch` 模式匹配 + record 模式、虚拟线程、Sequenced Collections、分代 ZGC。LTS 是 8/11/17/21。

**展开**

C++ 的 11/14/17/20 是"语言标准版本"。Java 的对应物是 **LTS（长期支持）发布**：8 → 11 → 17 → 21（每 6 个月发一个版本，但生产上多数人只用 LTS）。回答要有结构：**每个版本一句话 + 一个你真会用的例子**。

```
 Java 8  (2014)  lambda、方法引用、Stream、Optional、java.time、接口 default 方法、CompletableFuture
 Java 9  (2017)  模块系统(JPMS)、List.of/Set.of/Map.of、G1 成为默认 GC、紧凑字符串(JEP 254)、字符串拼接走 invokedynamic(JEP 280)
 Java 10 (2018)  var（局部变量类型推断）
 Java 11 (2018, LTS)  String.isBlank/lines/strip/repeat、HttpClient、单文件运行 `java Foo.java`、JFR 开源
 Java 14-16     switch 表达式(14)、文本块(15)、record(16)、instanceof 模式(16)
 Java 17 (2021, LTS)  sealed 类(17)、强封装 JDK 内部、Stream.toList(16)
 Java 21 (2023, LTS)  虚拟线程(JEP 444)、switch 模式匹配(441)、record 模式(440)、Sequenced Collections(431)、分代 ZGC(439)
                      预览: 结构化并发、ScopedValue、未命名变量、FFM API
```

本机验证（`demos/K14Versions.java`，`--release 21 --enable-preview` 编译运行）一个文件里用到了：`List.of`（9）、`stream().toList()`（16）、文本块（15）、`instanceof` 模式（16）、`sealed` + record 模式 + `when` 守卫的 `switch`（17/21）、`reversed()/getFirst()`（21）、`Collectors.teeing`（12）、虚拟线程执行器（21），输出：

```
[1, 2, 3]
{"k": 1}
instanceof pattern: hi
6.0 4.0
[c, b, a] first=a
teeing count/sum: 4/10
virtual: true
```

面试里最容易讲出"设计理由"的主线是 **数据导向编程**：`record`（数据）→ `sealed`（封闭种类）→ `switch` 模式（按种类分派，编译器检查穷尽）→ record 模式（拆开）。
对比 Java 8 的 visitor / `instanceof` 链：新增一种事件时，老写法编译器不会提醒你漏改，sealed + switch 会编译失败。见 `S10/J01_record.md`、`J02_sealed.md`、`J03_pattern_switch.md`、`J04_record_patterns.md`。

**不要说的**：String Templates（21 预览，后来被撤回）；预览特性（结构化并发、ScopedValue）要说清是预览、需 `--enable-preview`。

**能说出口的 60 秒版本**

> "The LTS line is 8, 11, 17, 21. Java 8 brought lambdas, streams and `java.time`. Between 9 and 11 we got `var`, the module system, the HTTP client, and G1 as the default collector. Java 17 is where the data-modelling features land: records, sealed types, text blocks, switch expressions, pattern matching for `instanceof`. Java 21 completes it - pattern matching for `switch` and record patterns, so with a sealed hierarchy the compiler checks exhaustiveness - and adds virtual threads, sequenced collections, and generational ZGC. The ones I'd use daily are records and sealed types with pattern switches for modelling events, and virtual threads for I/O-heavy code."

**面试官可能的下一问**

* "Why sealed + pattern switch instead of the visitor pattern?"（编译器穷尽检查；不用 accept 样板；加新类型时漏处理会编译失败。）
* "What is a record exactly? Is it just Lombok `@Value`?"（语言级：规范构造器、紧凑构造器校验、`equals/hashCode/toString` 由 `ObjectMethods` 引导方法生成；不能继承、字段 final。）

**Demo / 课文**：`demos/K14Versions.java`；`S10/J01…J09`；`S10/README.md`。

---

### Q06 · Beyond language features: what changed in the JVM and runtime between Java 8 and 21 that matters for performance?

- **难度**：★★
- **来源**：`推断：Java 对应`（kq02 的"运行时"侧；C++ 版本题里常见的追问是"编译器/标准库改了什么"）。
- **一句话答案**：G1 成为默认（9）、分代 ZGC（21）、紧凑字符串与 indy 字符串拼接（9）、容器感知（10）、统一日志与 JFR 免费可用（9/11）、偏向锁移除、字符串/Stream 实现持续优化、虚拟线程（21）。

**展开**

按"你会遇到的现象"组织，而不是背清单：

| 现象 | 8 | 21 |
|---|---|---|
| 默认 GC | Parallel GC（吞吐优先，停顿长） | G1（9 起默认）；可选 ZGC（15 起正式；21 起可 `-XX:+ZGenerational`） |
| 字符串内存 | `char[]`，每字符 2 字节 | **紧凑字符串**（9）：Latin-1 用 1 字节，本机实测 `"a".repeat(1000)` = 1040 字节，`"中".repeat(1000)` = 2040 字节（`K03`） |
| 字符串拼接 | `StringBuilder` 链（编译期生成） | `invokedynamic makeConcatWithConstants`（9），运行时选最优策略；本机 `javap` 可见（`K05Concat`） |
| 锁 | 默认有偏向锁（竞争少时快，撤销时要停世界） | 偏向锁在 15 默认关闭、后续移除；本机：`java -XX:+UseBiasedLocking -version` 在 21.0.12 报 `Unrecognized VM option 'UseBiasedLocking'` |
| 容器 | 不认 cgroup 限制，容易拿宿主机核数/内存 | 10 起识别容器限制 |
| 日志/诊断 | 各种 `-XX:+PrintGC*` | 统一日志 `-Xlog:gc,safepoint…`；JFR 11 起开源可用（`jcmd JFR.start`） |
| 线程模型 | 平台线程 | 虚拟线程（Q31） |
| 反射/内部 API | 随便 `setAccessible` | 17 起强封装：本机 K06 需要 `--add-opens java.base/java.util=ALL-UNNAMED` 才能反射读 `HashMap.table` |
| NPE 信息 | `NullPointerException`（没消息） | 有帮助的 NPE 消息（14 引入，15 默认开） |

重点不是背全，而是知道**升级 8 → 21 通常白捡的东西**（G1 改进、字符串、锁、JIT 优化）和**需要动手的东西**（强封装导致的 `--add-opens`、移除的 API）。

**能说出口的 60 秒版本**

> "Several things changed under the hood. G1 became the default collector, and ZGC went production, with a generational mode in 21 that gets pauses well under a millisecond in my test. Strings got compact - one byte per Latin-1 character - and concatenation goes through invokedynamic so the runtime can pick a strategy. Biased locking was removed - on 21 the flag isn't even recognised. The JVM understands container limits, there's unified logging and JFR is free, and in 21 we have virtual threads. When upgrading from 8, the main friction is strong encapsulation of JDK internals, which needs `--add-opens` for reflective code."

**面试官可能的下一问**

* "Why was biased locking removed?"（维护成本高、现代并发场景收益小、撤销要进 safepoint；这条是一般认识，非本机验证。）
* "Would you move from G1 to ZGC?"（Q23）

**Demo / 课文**：`demos/K03ObjectSize.java`、`demos/K05Concat.java`、`demos/OUTPUTS.txt`（`UseBiasedLocking` 一节）；`S10/J19_runtime_zgc_jit.md`。

---

## [C] 语言对比与所有权（kq05）

### Q07 · Compare Java and Python in detail. When would you use each?

- **难度**：★
- **来源**：`推断：Java 对应`。C++ 原题（1p3a 1068621，F-A8，2024-05，kq05）：「c++/Python的区别，会问得比较详细。在哪种情…」→ https://www.1point3acres.com/interview/thread/1068621
- **一句话答案**：Java 是静态类型、JIT 编译、真正多线程、低延迟可预测；Python 是动态类型、解释执行、GIL 限制 CPU 并行、开发快生态强。选择：延迟敏感/长期服务/大型团队 → Java；研究、胶水、数据分析、原型 → Python（热点交给 NumPy 等 C 扩展）。

**展开**

| 维度 | Java | Python (CPython) |
|---|---|---|
| 类型 | 静态、编译期检查；泛型被擦除 | 动态；类型注解不强制 |
| 执行 | 字节码 + JIT（C1/C2），稳态接近本地代码 | 字节码解释（3.13 有实验 JIT）；纯 Python 循环通常比 Java 慢一到两个数量级 |
| 内存管理 | 追踪式 GC（可达性），循环引用无问题（`K13`：互相引用的两个对象被回收） | 引用计数 + 循环垃圾收集器；`__del__` 时机较确定 |
| 并发 | 真线程（OS 线程），共享内存 + JMM；虚拟线程 | GIL：同一时刻只有一个线程执行字节码，CPU 密集要多进程；3.13 有 free-threaded 实验构建 |
| 整数 | `int` 32 位、`long` 64 位，溢出回绕（`K15`：`MAX+1 = -2147483648`）；`BigInteger` 另算 | 任意精度整数 |
| 除法/取模 | `-7 / 2 = -3`，`-7 % 2 = -1`（向零截断）；`Math.floorMod(-7,2)=1` | `-7 // 2 = -4`，`-7 % 2 = 1` |
| 启动/内存 | JVM 启动百毫秒级，内存占用大 | 启动快，内存占用小 |
| 参数传递 | 引用的值传递：对象引用被复制，可改对象内容，不能让调用者的变量指向别处 | 相同（"call by sharing"） |

选型：Headlands 这类公司——研究员用 Python/其他做原型和分析，系统/基础设施用 Java/C++（JD 就是 Java 研究平台 + 基础设施，O-C2）；热路径的延迟和吞吐需要静态类型、可预测性能和真线程。

**能说出口的 60 秒版本**

> "Java is statically typed and JIT-compiled, so steady-state performance is close to native; Python is dynamically typed and interpreted, so pure-Python loops are one to two orders of magnitude slower, and the GIL stops threads from running Python bytecode in parallel - so you use processes or native extensions. Java has real threads and a defined memory model, which matters for services; Python's strength is productivity and the ecosystem - NumPy, pandas - so I'd use it for research and glue, and Java for long-running, latency-sensitive services. One practical difference: Java ints are 32-bit and wrap around on overflow, Python has big integers - and integer division rounds toward zero in Java, floors in Python."

**面试官可能的下一问**

* "What exactly does the GIL protect?"（解释器内部状态/引用计数；不是你的数据，所以仍要加锁。）
* "How does Java pass objects to methods?"（引用按值传递。）

**Demo / 课文**：`demos/K15Overflow.java`、`demos/K13SmartPtr.java`。

---

### Q08 · C++ has `unique_ptr`, `shared_ptr` and `weak_ptr`. What is the Java equivalent — how does Java handle ownership and resource cleanup?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（1p3a 1068621，F-A8）：「smart pointers」→ https://www.1point3acres.com/interview/thread/1068621
- **一句话答案**：Java 没有所有权概念：**每个引用都像 `shared_ptr` 但由 GC 追踪可达性，不用引用计数，所以没有循环引用泄漏**；`WeakReference` ≈ `weak_ptr`；RAII 对应 **try-with-resources**（`AutoCloseable`）；`Cleaner` 是兜底，不是析构函数。

**展开**

C++ 需要智能指针，是因为**内存和资源的生命周期要由程序员/类型系统精确管理**：

```
 unique_ptr<T>  唯一所有者，离开作用域就 delete
 shared_ptr<T>  引用计数，最后一个释放时 delete；循环引用 -> 计数永不为 0 -> 泄漏
 weak_ptr<T>    不增加计数，打破循环，用时 lock() 升级
 RAII           资源 = 对象生命周期：构造时获取，析构时释放（文件、锁、socket）
```

Java 把"内存"和"其它资源"拆开：

* **内存**：GC 从根（线程栈、静态变量…）出发做可达性分析，不可达就回收。所以不需要 `delete`，也没有 `shared_ptr` 的循环泄漏。本机 `K13`：两个互相引用的 1 MB 对象，丢掉外部引用后 `WeakReference` 被清空 —— `shared_ptr` 在同样结构下会泄漏。
* **引用强度**：强引用（普通）、`SoftReference`（内存紧张时回收，缓存）、`WeakReference`（下次 GC 就回收，≈ `weak_ptr`；`WeakHashMap`）、`PhantomReference`/`Cleaner`（回收后的清理回调）。本机 `K13`：`b = null; System.gc()` 后 `weak.get() == null`。
* **其它资源（文件、socket、锁）**：GC 不管它们什么时候释放，所以**必须显式关闭**：`try (var r = open()) { … }`，退出块时按**相反顺序**调用 `close()`，包括异常路径。`K13` 输出：

```
open  A
open  B
body
close B      <- 反序
close A
caught boom  <- 先关资源，再进 catch
```

* **`finalize()` 已弃用且在被移除**（JEP 421，18）；`Cleaner` 只能当安全网：没有时机保证（`K13` 里 `System.gc()` 后才见到清理动作），不要依赖它释放稀缺资源。

对比所有权：Java 没有"这个对象归谁"的类型表达；靠约定和 `try-with-resources`。**`unique_ptr` 最接近的是"把资源包在一个 `AutoCloseable` 里，在作用域内使用"**。

**能说出口的 60 秒版本**

> "Java doesn't need smart pointers for memory, because the garbage collector traces reachability from roots - so there's no reference counting and no leak from cycles that you get with `shared_ptr`. `WeakReference` is the analogue of `weak_ptr`. The place where RAII matters in Java is non-memory resources like files, sockets and locks, and there we use try-with-resources: `AutoCloseable.close()` runs deterministically at the end of the block, in reverse order, even on exceptions. `Cleaner` exists as a safety net, but it has no timing guarantee, and `finalize` is deprecated for removal. What Java lacks is ownership in the type system - nothing says 'this object belongs to that one'."

**面试官可能的下一问**

* "What happens if you forget to close a stream?"（文件描述符泄漏，直到 GC 回收对象并跑 Cleaner 才可能关；长时间运行会 `Too many open files`。）
* "Why not reference counting?"（循环、每次赋值有开销、多线程下计数要原子操作；GC 批量处理更适合吞吐。）

**Demo / 课文**：`demos/K13SmartPtr.java`。

---

### Q09 · What does Java guarantee that C++ does not (and vice versa)? Think undefined behaviour, integer semantics, memory safety.

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题族（A8「c++/Python 差异，问得比较详细」F-A8；A13「language features」F-A13）的 Java 视角。
- **一句话答案**：Java 的每个程序行为都有定义（整数溢出回绕、数组越界抛异常、空指针抛 NPE、数据竞争也有受限的弱语义，不会"凭空"产生值）；C++ 的 UB 让优化器更激进但程序员背风险。

**展开**

```
 C++:   int x = INT_MAX; x + 1   -> 有符号溢出 = UB: 编译器可以假设它不会发生, 删掉你的检查
        a[10] (a 只有 5 个)      -> UB: 可能读到别的数据、崩溃、被利用
        两个线程无同步读写同一变量 -> UB (data race)
 Java:  Integer.MAX_VALUE + 1    -> -2147483648 (JLS 规定二进制补码回绕)
        a[10]                    -> ArrayIndexOutOfBoundsException
        null.method()            -> NullPointerException
        数据竞争                 -> 有定义但弱: 可能读到旧值/乱序, 但每个读到的值都是某次写入的值
```

本机 `K15Overflow`：

```
MAX+1 = -2147483648  (wraps, defined by JLS)
Math.addExact -> integer overflow          <- 想要检查就用 *Exact 方法
(int) 3_000_000_000L = -1294967296, (byte) 200 = -56
1 << 33 = 2 (shift count masked to 5 bits), 1L << 33 = 8589934592
```

要点：

* **安全 ≠ 免费**：边界检查、空检查有成本，但 JIT 大量消除（循环里的 range check elimination）。
* **Java 里"确定"但会坑人**：`int` 回绕（金额/时间戳溢出）、`0.1+0.2 != 0.3`、`-7 % 2 == -1`、移位次数取模（`1 << 33 == 2`）、`Integer` 装箱缓存（Q14）、`char` 是无符号 16 位。
* **Java 没有**：指针运算、`const` 正确性、析构函数、多重继承、运算符重载、内联值类型、模板元编程、头文件/ODR 问题。**有**：反射、动态加载、可预测的崩溃（栈追踪）。
* 对金融代码：金额用 `long`（最小单位）或 `BigDecimal` + 明确舍入；累加用 `Math.addExact`/`multiplyExact` 防止悄悄回绕（`S10/J15_math_string_utils.md`）。

**能说出口的 60 秒版本**

> "Java defines every behaviour: signed overflow wraps by two's complement, out-of-range array access throws, null dereference throws, and even a data race has a restricted meaning - you may see stale values, but never out-of-thin-air ones. C++ leaves overflow, out-of-bounds access and data races undefined, which lets the optimizer assume they never happen - faster, but the bugs are silent. In Java the traps are different: ints wrap silently, so for money or sizes I use `Math.addExact` or `long`, and I know that shifts are masked and `%` keeps the sign of the dividend."

**面试官可能的下一问**

* "Does Java's bounds checking slow down hot loops?"（JIT 常消除；剩下的分支预测良好，通常成本很小；不要给具体百分比。）
* "How would you detect overflow in an order-quantity accumulation?"（`Math.addExact` 抛异常，或 `long` + 校验。）

**Demo / 课文**：`demos/K15Overflow.java`；`S10/J15_math_string_utils.md`。

---

### Q10 · How do Java generics differ from C++ templates? What is type erasure and what does it cost?

- **难度**：★★
- **来源**：`推断：Java 低延迟岗经典`（C++/Java 对比的标准追问；源于 A8 的"差异问得详细"）。
- **一句话答案**：C++ 模板为每个类型实例化一份代码；Java 泛型在编译期检查、运行时**擦除**成 `Object`，所以泛型容器不能装原始类型（要装箱）、运行时没有 `T`，这就是 `List<Integer>` 比 `int[]` 慢且占内存的原因。

**展开**

```
 C++:  vector<int>  --编译-->  专门为 int 生成的代码, 元素就是 4 字节连续排列
 Java: List<Integer> --javac--> List (元素类型 Object)
                                  [ref][ref][ref]...  每个 ref -> 一个 Integer 对象 (16 字节, 在堆上)
```

后果：

1. **装箱成本**：`ArrayList<Integer>` 100 万元素：本机 `K02` 测得 `int[1M]` = 4,000,016 字节，`ArrayList<Integer>`（含 100 万个 Integer 对象）= **20,000,208 字节**（5 倍）。
2. **没有运行时类型信息**：不能 `new T()`、`T[]`、`instanceof List<String>`；用 `Class<T>` token 或 `Supplier<T>` 绕。
3. **不能用原始类型做类型参数**：所以有 `IntStream`、`Int2IntMap`（fastutil）等专门版本。
4. **好处**：二进制兼容、没有代码膨胀、字节码大小稳定。
5. Valhalla（值类对象 + 泛型特化）的动机正是这里；21 里还没有，不要说已有。

在热路径上：优先 `int[]`/`long[]`，或第三方原始类型集合；自己写 `class LongIntMap` 开放寻址表（Q29 追问常见）。

**能说出口的 60 秒版本**

> "Java generics are erased: the compiler checks types and then everything becomes `Object` at run time, so a `List<Integer>` is an array of references to boxed Integers. C++ templates instantiate separate code per type, so a `vector<int>` is a contiguous array of ints. The cost in Java is boxing: in my measurement a million-element `ArrayList<Integer>` took about five times the memory of an `int[]`, and iteration chases pointers. So on hot paths I use primitive arrays or primitive-specialised collections; the language-level fix, value classes, is the Valhalla work and isn't in 21."

**面试官可能的下一问**

* "Why was erasure chosen?"（兼容旧代码/字节码，迁移兼容性。）
* "Can you write a generic method that works on `int` without boxing?"（不能；写重载或用 `IntBinaryOperator` 这类原始类型特化函数接口。）

**Demo / 课文**：`demos/K02Boxing.java`；`S30/hc07_ticker_hash_map.md`。

---

## [D] 分配与内存（kq06）

### Q11 · What happens on `new Foo()` in Java? Compare with `malloc` / `new` in C++. How fast is Java allocation, and what does it cost later?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（Blind 2023-03，OP §D2，kq06，**置信度低**，发帖人断言）：「`malloc` vs `new`」→ OP §D2 Blind 2023-03 行（帖链接见 `official_and_process.md` 缺口 §4 的 teamblind 链接）。
- **一句话答案**：Java 的 `new` 在线程私有的 **TLAB** 里做**指针碰撞**（几条指令），内存已清零，再跑构造器；快的原因是 GC 统一回收、不做 free-list 搜索。代价后移到 GC：分配速率越高，GC 越频繁。C++ 的 `malloc` 要找空闲块，`new` = `malloc` + 构造。

**展开**

先回答原题（C++ 侧要点，因为面试官可能顺口问）：`malloc` 只分配未初始化的字节，返回 `void*`，失败返回 `NULL`，用 `free` 释放；`new` 分配并**调用构造函数**，失败抛 `bad_alloc`，类型安全，用 `delete`（调析构）。

Java 的 `new Foo()` 做三件事：

```
  线程 A 的 TLAB (Thread-Local Allocation Buffer, Eden 里一块线程私有区域)
  [ 已用 ......... ][top]-----------free-----------[end]
                      |
  new Foo(): 检查 top + size <= end ? 是 -> obj = top; top += size   (一次加法 + 比较, 无锁)
                                       否 -> 申请新 TLAB 或慢路径(可能触发 GC)
  然后: 内存已被清零 -> 写对象头(mark word + 类指针) -> 调构造器
```

* 分配便宜是因为 **GC 是复制/整理式的**：回收时把存活对象搬走，剩下的整块空间一次性当作空闲；所以分配永远是"顶指针前移"，没有碎片，不搜索空闲表。
* **本机实测每个对象多大**（`K03`，`ThreadMXBean.getThreadAllocatedBytes`）：`new Object()` = 16 字节；`record P2(int x,int y)` = 24；`P3(long×3)` = 40；`Integer` = 16；`new int[10]` = 56。
* **便宜 ≠ 免费**：没逃逸的对象会被 JIT 直接消除（Q20：steady state 分配 0 字节），逃逸的则增加 GC 压力。`K04`：关掉逃逸分析，每次迭代分配 96 字节，50M 次迭代 4.8 GB，耗时 8 倍。
* 大对象（超过 region 大小一半，G1 的 humongous）和超大数组走慢路径，别在热路径上分配。

**与 C++ 的差别总结**：

| | C++ `malloc/new` | Java `new` |
|---|---|---|
| 分配 | 分配器找空闲块（ptmalloc/jemalloc…），可能加锁/系统调用 | TLAB 指针碰撞，通常无锁 |
| 初始化 | `malloc` 不初始化；`new` 调构造 | 一律清零 + 构造 |
| 释放 | 手动 `free/delete`，或 RAII | GC，不能手动 |
| 失败 | `NULL` / `bad_alloc` | `OutOfMemoryError` |
| 碎片 | 会产生 | 复制/整理式 GC 无碎片（代价是搬迁） |
| 栈上对象 | 默认 | 只能靠逃逸分析"优化出来"，不是语义保证 |

**能说出口的 60 秒版本**

> "In C++, `malloc` just gives you raw uninitialised bytes from the allocator, and `new` is `malloc` plus running the constructor, and you must free it yourself. In Java, `new` is much cheaper at the allocation step: each thread has a TLAB in the young generation, so allocation is bumping a pointer - a handful of instructions, no lock - and the memory is already zeroed. That's possible because the collector copies live objects out and reclaims the whole region, so there's no free list or fragmentation. The cost moves to GC frequency - allocation rate is what drives young collections - and the JIT can eliminate allocations that don't escape. I measured a plain object at 16 bytes and a two-int record at 24 bytes."

**面试官可能的下一问**

* "What's a TLAB and what if it's full?"（线程私有分配缓冲；满了申请新的，Eden 满了触发 young GC。）
* "How do you reduce allocation in a hot path?"（复用对象、原始类型数组、避免装箱、避免捕获 lambda、`StringBuilder` 复用。）

**Demo / 课文**：`demos/K03ObjectSize.java`、`demos/K04EscapeAnalysis.java`。

---

### Q12 · `System.arraycopy` vs a hand-written loop vs `Arrays.copyOf` vs `clone` — what's the difference? How does that compare to `std::copy` vs `memcpy`?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（Blind 2023-03，OP §D2，kq06，置信度低）：「`std::copy` vs `memcpy`」。
- **一句话答案**：`System.arraycopy` 是 JIT 内联的 intrinsic，语义是 **memmove**（重叠安全），带边界和类型检查；`Arrays.copyOf` = 新数组（分配 + 清零 + 拷贝）；手写循环在热路径上 C2 常识别成同样的拷贝。C++ 里 `memcpy` 要求不重叠、只能用于平凡可拷贝类型，`std::copy` 会按类型选择最优实现（可退化为 `memmove`）。

**展开**

C++ 侧要点：`memcpy` 按字节拷贝，**重叠区域是 UB**，对非平凡类型（有自定义拷贝构造/虚函数）是错的；`memmove` 允许重叠；`std::copy` 是类型感知的，对平凡类型库实现通常调用 `memmove`，对复杂类型逐个调用赋值运算符。

Java：

```
 System.arraycopy(src, sp, dst, dp, len)
   - 语义 = memmove: 同一数组内重叠拷贝也正确
   - 检查: 下标越界 -> ArrayIndexOutOfBoundsException; 引用数组 -> 元素类型不兼容 -> ArrayStoreException
   - JIT: 被当作 intrinsic, 小的拷贝内联成几条向量指令, 大的调用优化过的 stub
 Arrays.copyOf(a, n)  = 分配新数组(清零) + arraycopy
 a.clone()            = 同上, 数组专用
```

本机 `K12ArrayCopy`：

```
overlap copy (src=0,dst=2,len=4): [1, 2, 1, 2, 3, 4]       <- [1..6] 向后移 2 位, 结果正确(memmove 语义)
ArrayStoreException: arraycopy: element type mismatch: ... destination array, java.lang.String
bounds: arraycopy: last destination index 9 out of bounds for int[6]
64MB:  arraycopy 4 ms | for-loop 5 ms | Arrays.copyOf 11 ms     <- 第 1 轮(预热期)
64MB:  arraycopy 1 ms | for-loop 1 ms | Arrays.copyOf  3 ms     <- 稳态: 循环被 C2 优化到和 arraycopy 一样
16-long arraycopy + store + load: ~1.7 ns/iter
```

读法：稳态下手写循环和 `arraycopy` 一样快 —— C2 能把简单的拷贝循环识别并替换为同样的拷贝（所谓 loop idiom，我从数据推断，没有看汇编）；但在预热期（解释器里）循环慢得多，所以**一般仍用 `arraycopy`**：意图清晰、预热期也快、检查齐全。`Arrays.copyOf` 比 `arraycopy` 慢是因为多了分配 + 清零（64 MB 的新数组）。

注意"引用数组的拷贝是**浅拷贝**"：拷的是引用，不是对象；而且写屏障/卡表（GC 记账）会让引用数组拷贝比原始数组略贵。

**能说出口的 60 秒版本**

> "`memcpy` is a raw byte copy that's undefined on overlapping regions and wrong for non-trivially-copyable types; `std::copy` is type-aware and for trivial types typically ends up as `memmove`. The Java counterpart is `System.arraycopy`, which behaves like `memmove` - overlapping copies are correct, I checked by shifting an array onto itself - but adds bounds and type checks, throwing `ArrayIndexOutOfBounds` or `ArrayStore`. HotSpot treats it as an intrinsic, so it's inlined or uses an optimised stub. `Arrays.copyOf` is arraycopy plus allocation and zeroing, so it's slower for big arrays. In steady state a simple loop gets recognised by C2 and is as fast, but I'd still use arraycopy for clarity and because it's fast during warm-up too."

**面试官可能的下一问**

* "Is `arraycopy` a deep copy of an object array?"（不是，浅拷贝。）
* "How would you copy a large buffer without going through the heap?"（`ByteBuffer.put(ByteBuffer)` 对 direct buffer；`MemorySegment.copy`；`FileChannel.transferTo` 零拷贝。）

**Demo / 课文**：`demos/K12ArrayCopy.java`。

---

### Q13 · How much memory does a Java object take? What's in an object header? How big is `new Integer(5)`, a two-field class, an `int[10]`?

- **难度**：★★
- **来源**：`推断：Java 对应`（kq06 的"内存布局"侧；公司博客 #3「OutOfLine」讲对象大小与缓存行，OP §B2，C++）。
- **一句话答案**：64 位 HotSpot（压缩类指针）：对象头 12 字节（8 字节 mark word + 4 字节类指针），数组再加 4 字节长度 = 16；所有对象大小向 8 字节对齐。所以空对象 16、`Integer` 16、`int[10]` 56。

**展开**

```
 普通对象:   [ mark word 8B ][ klass ptr 4B ][ 字段... ][ 对齐填充到 8 的倍数 ]
 数组:       [ mark word 8B ][ klass ptr 4B ][ length 4B ][ 元素... ][ 填充 ]
```

* **mark word**：哈希码、GC 年龄、锁状态都存在这里。
* **压缩指针**（compressed oops）：堆 < 约 32 GB 时，引用用 4 字节（按 8 字节对齐后左移 3 位寻址）。堆超过阈值，引用变 8 字节，容器内存一下涨一截 —— 这是"堆不要随手设到 32 GB 以上"的由来。本机 `-XX:+PrintFlagsFinal` 显示 `UseCompressedOops = true`，`ObjectAlignmentInBytes = 8`。
* 实测（`K03ObjectSize`，每个构造的字节数）：

```
new Object()                16        (12 头 + 4 填充)
record P2(int,int)          24        (12 头 + 8 字段 = 20 -> 24)
record P3(long,long,long)   40        (12 + 24 = 36 -> 40)
Integer.valueOf(1000)       16        (12 + 4 -> 16)
new int[0]                  16        (数组头)
new int[10]                 56        (16 + 40)
new long[10]                96        (16 + 80)
new Integer[10]             56        (16 + 10×4 个引用, 不含 Integer 对象本身)
"a".repeat(1000)          1040        (String 24 + byte[1000] 的 1016)
"中".repeat(1000)         2040        (UTF16: byte[2000] -> 2016 + 24)
```

* 推论：`ArrayList<Integer>` 100 万元素 = 4 MB（引用数组）+ 16 MB（Integer 对象）= 约 20 MB（`K02` 实测 20,000,208），而 `int[]` 才 4 MB。
* 字段布局：JVM 可重排字段减少填充（把大字段放前面）；你不应依赖声明顺序。
* 观察工具：`jcmd <pid> GC.class_histogram`（本机 `K20Busy` 示例输出了每类实例数和字节数）；JOL 库（第三方，本机未用）。
* 较新的 JDK 有实验性的"紧凑对象头"（把头压到 8 字节），21 里没有，我没在本机验证过版本号，面试时只说"在做"。

**能说出口的 60 秒版本**

> "On 64-bit HotSpot with compressed class pointers, every object has a 12-byte header - 8 bytes of mark word for hash, GC age and lock state, plus a 4-byte class pointer - arrays add a 4-byte length, and everything is padded to 8 bytes. So an empty object is 16 bytes, an `Integer` is 16, a record with two ints is 24, and an `int[10]` is 56. I measured these with the thread-allocated-bytes counter. The practical consequence is that a list of a million boxed Integers is about 20 MB where an `int[]` is 4 MB, and compressed oops, which keep references at 4 bytes, stop working above roughly 32 GB of heap."

**面试官可能的下一问**

* "What happens to the references when the heap exceeds 32 GB?"（压缩指针失效，引用 8 字节，同样数据更占内存。）
* "How would you shrink a structure with a million small objects?"（并行数组/打包到 `long[]`/`ByteBuffer`；`@Contended` 是反方向（加填充）。）

**Demo / 课文**：`demos/K03ObjectSize.java`、`demos/K02Boxing.java`；`S00/cpu_cache_locality.md`。

---

### Q14 · What's the cost of autoboxing? Explain `Integer` caching and why `==` on two `Integer`s can give different answers.

- **难度**：★
- **来源**：`推断：Java 低延迟岗经典`（Java 版 hash map / 容器题的标配前置；hc07 ticker hash map 的追问常涉及，见 `loop/rounds/01_video/hc07_ticker_hash_map/`）。
- **一句话答案**：自动装箱 `int → Integer` 调 `Integer.valueOf`：在 -128..127 返回缓存对象，其它新分配；所以 `==`（比引用）对 127 为 true、对 128 为 false，必须用 `equals`。成本：分配 + 间接访问 + 拆箱时的 NPE 风险。

**展开**

本机 `K02Boxing`：

```
127 == 127 (boxed): true
128 == 128 (boxed): false   equals: true
unboxing null -> NPE
round 1: long sum   10 ms, alloc            0 B | Long sum   17 ms, alloc  239,999,832 B
```

最后一行：2000 万次 `Long boxed += i`（每次拆箱、相加、再装箱），分配了约 240 MB，也就是平均 12 字节/次，而不是一个 `Long` 的 16 字节 —— JIT 把循环展开后消除了一部分中间的装箱（box elimination），但剩下的仍然全部落到堆上；对照组 `long` 的求和分配 0 字节，且更快。（"JIT 消除一部分"是我对 12 字节 < 16 字节的解释，没有用 `-XX:+PrintEliminateAllocations` 之类的方法核实，面试时只说"JIT 可能消除一部分"。）

要点：

* 缓存范围默认 -128..127（`-XX:AutoBoxCacheMax` 可调大 `Integer` 的上界）；`Long`、`Short`、`Byte`、`Character` 也有缓存。
* 常见坑：`Map<String,Integer>` 的 `get` 返回 `null` 然后自动拆箱 → NPE；`List<Integer>.remove(int)` 与 `remove(Object)` 的重载歧义；循环里 `Long sum = 0L; sum += x`。
* 热路径替代：原始类型数组、`LongAdder`、fastutil/Eclipse Collections 的原始类型 map（第三方库，提这一句即可）、`IntStream`。
* 并发里：`Integer` 对象是不可变的，所以 `synchronized(integerField)` 几乎总是 bug（值变了锁就变了）。

**能说出口的 60 秒版本**

> "Autoboxing calls `Integer.valueOf`, which returns a cached instance for values between -128 and 127 and allocates a new object otherwise - so `==` on boxed values compares references and works by accident for small numbers and fails for 128. Always use `equals`. The cost is an allocation, an extra pointer hop, and a potential NPE on unboxing null. In a quick test a boxed `Long` accumulator over 20 million iterations allocated around 240 MB while the primitive loop allocated nothing. In latency-sensitive code I use primitive arrays, `LongAdder`, or primitive-specialised maps."

**面试官可能的下一问**

* "Why does the cache exist and why those bounds?"（小整数使用频繁，省分配；JLS 要求至少覆盖 -128..127。）
* "How would you implement a `long → int` map without boxing?"（开放寻址哈希表：两个数组 `long[] keys; int[] vals`，线性探测，2 的幂容量，位与取模。）

**Demo / 课文**：`demos/K02Boxing.java`；`S30/hc07_ticker_hash_map.md`。

---

### Q15 · How are Java `String`s implemented? Immutability, interning, `+` in a loop, hash caching, `substring`.

- **难度**：★★
- **来源**：`推断：Java 低延迟岗经典`（Java 对 C++ `std::string`/`string_view` 问题的翻译；博客 #3 的例子是 `std::string` 让对象变大，OP §B2）。
- **一句话答案**：`String` 不可变，内部是 `byte[]` + 编码标志（紧凑字符串：Latin-1 一字节、否则 UTF-16），`hashCode` 缓存在对象里，字面量进常量池可 `intern`，`substring` 拷贝，循环里 `+=` 是 O(n²)。

**展开**

```
 String s = "hello"
 [header 12B][value -> byte[]: 5 个字节][coder: 0=LATIN1 1=UTF16][hash: int 缓存][hashIsZero]...
```

本机 `K05Strings`：

```
literal == folded literal : true      <- "hel"+"lo" 编译期常量折叠成同一个常量池对象
literal == runtime concat : false     <- 运行时拼接得到新对象
literal == new String     : false
literal == s3.intern()    : true      <- intern() 返回常量池里的那一份
hashCode of 50M chars: first 31776 us, second 0 us (cached)
n= 80000  +=     94 ms | StringBuilder   0 ms     <- 循环 += 是 O(n²), n 翻倍时间约 3-4 倍
```

要点：

* **不可变** 带来：可安全共享、线程安全、可缓存 hash、可作 map key、字面量池化。代价：每次修改产生新对象。
* **`+` 的实现**：`javac` 生成 `invokedynamic makeConcatWithConstants`（9+，本机 `javap` 可见），运行时选择策略，比旧 `StringBuilder` 链好；**但循环里的 `s += x` 每次仍新建字符串**，所以 O(n²)，要用 `StringBuilder`。
* **紧凑字符串**：`"a".repeat(1000)` = 1040 字节，`"中".repeat(1000)` = 2040 字节（Q13）。
* **`substring`**：7u6 起拷贝（不再共享底层数组），所以小子串不会钉住大字符串，也意味着 `substring` 是 O(k) 拷贝。
* **`intern()`** 与 `-XX:+UseStringDeduplication`（G1，默认关，本机 `PrintFlagsFinal` 显示 `false`）：前者手动、后者 GC 在后台去重底层数组。
* 交易系统的 tick 符号（symbol）：不要拿 `String` 做热路径 key；预先映射到 `int` id，或自己存 `byte[]`/`long`（8 字符 packed）。（这与 hc07 ticker hash map 同一思路。）
* 对比 C++ `std::string_view`：Java 没有零拷贝视图，`CharSequence`/`ByteBuffer.slice()` 是近似物。

**能说出口的 60 秒版本**

> "A `String` is immutable and backed by a byte array plus a coder flag - since Java 9 Latin-1 text takes one byte per character. The hash code is cached in the object, so the second `hashCode()` on a 50-million-character string took zero microseconds in my test versus 32 milliseconds the first time. Literals live in a constant pool and `intern()` returns the pooled instance, which is why `==` on strings is a trap. `+` compiles to `invokedynamic`, but concatenating in a loop is still quadratic - 80,000 appends took about 100 ms versus under a millisecond with `StringBuilder`. `substring` copies since Java 7u6. On a hot path I wouldn't use strings as keys - I'd map symbols to ints or packed longs."

**面试官可能的下一问**

* "Why is `String` a good `HashMap` key?"（不可变 + 缓存 hash。）
* "Does `final String` make `+` constant-folded?"（只有编译期常量变量才折叠。）

**Demo / 课文**：`demos/K05Strings.java`、`demos/K05Concat.java`、`demos/K03ObjectSize.java`；`S10/J07_text_blocks.md`；`S10/J15_math_string_utils.md`。

---

### Q16 · When and how would you use off-heap memory in Java? What are the risks?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`；对应 C++ 的"自己管内存"（kq06 的 `malloc` 问法的 Java 对偶）；FFM API 见 CONVENTIONS 特性矩阵 J17。
- **一句话答案**：堆外 = 不受 GC 管理的内存：`ByteBuffer.allocateDirect`（受 `-XX:MaxDirectMemorySize` 限制）、`MappedByteBuffer`（mmap 文件）、`sun.misc.Unsafe`（内部）、**FFM API**（`Arena` + `MemorySegment`，21 预览）。用在大数据缓存、避免 GC 扫描/拷贝、与 native/IO 零拷贝、跨进程共享。风险：手动生命周期、越界/悬空（FFM 帮你检查）、泄漏不可见于堆 dump。

**展开**

```
  堆内:  byte[] 在 GC 堆里 -> 会被扫描/移动; 做 IO 时要先拷到临时 direct buffer
  堆外:  [ native memory, 地址固定, GC 不扫描内容 ]  <- Java 里只有一个小小的句柄对象
```

本机 `K11OffHeap`（`--enable-preview`）：

```
allocateDirect(64MB) with MaxDirectMemorySize=16m -> java.lang.OutOfMemoryError: Cannot reserve 67108864 bytes of direct buffer memory (allocated: 0, limit: 16777216)
direct buffer isDirect=true readback=123456789
1M longs off-heap, sum=999999000000, byteSize=8000000
out of bounds -> IndexOutOfBoundsException
use after Arena.close() -> IllegalStateException: Already closed
struct Order size=24 alignment=8
```

* 好处：(1) 堆小 → GC 快；(2) 大数据结构（上亿条 tick）不进堆；(3) `FileChannel`/socket 对 direct buffer 零拷贝；(4) 布局自己控制（`StructLayout` 描述 C 风格 struct，本机演示 24 字节 Order 记录）。
* 风险：(1) **生命周期**：`DirectByteBuffer` 的内存要等对象被 GC 才释放（`Cleaner`），堆压力小时可能很久不释放 → 堆外 OOM；FFM 的 `Arena` 给了确定的关闭，关闭后访问抛 `IllegalStateException`（上面最后一行实测）；(2) **越界**：`ByteBuffer` 和 `MemorySegment` 都检查边界（实测抛异常），`Unsafe` 不检查，写错直接崩 JVM；(3) **不可见**：堆 dump 里看不到，需 `-XX:NativeMemoryTracking=summary` + `jcmd VM.native_memory`；(4) 序列化：必须自己定义字节格式，字节序用 `ByteOrder.nativeOrder()`。
* 21 里 FFM 仍是**预览**（要 `--enable-preview`），22 正式；生产上很多公司仍用 `ByteBuffer`/Unsafe 的库（Chronicle、Aeron 之类，第三方）。

**能说出口的 60 秒版本**

> "Off-heap means memory the GC doesn't manage or scan: direct byte buffers, memory-mapped files, and in Java 21 the preview Foreign Function and Memory API with `Arena` and `MemorySegment`. I'd use it for very large, long-lived data like tick history so the heap stays small and collections stay short, for zero-copy I/O, and for fixed-layout records or sharing between processes. The risks are lifetime and visibility: a direct buffer is only freed when its owner object is collected, so you can hit the direct-memory limit - I reproduced that error with a 16 MB cap - and leaks don't show up in heap dumps. FFM improves that with deterministic `Arena` closing and bounds checks: using a segment after close throws instead of crashing."

**面试官可能的下一问**

* "Why not just use `Unsafe`?"（内部 API，不安全，将被弃用；FFM 是正式替代。）
* "How would you detect an off-heap leak?"（NMT：`-XX:NativeMemoryTracking=summary`，`jcmd <pid> VM.native_memory`；`BufferPoolMXBean`。）

**Demo / 课文**：`demos/K11OffHeap.java`、`demos/K16Ipc.java`；`S10/J17_ffm_api.md`。

---

### Q17 · How do CPU caches affect Java performance? Why is `long[]` faster than `List<Long>`? What is false sharing?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`；公司博客 #3「OutOfLine – A Memory-Locality Pattern」讲热/冷数据、缓存行（O-B2，C++，面试官最可能引用）。
- **一句话答案**：CPU 读内存以 64 字节**缓存行**为单位；顺序访问连续数组命中缓存、预取器能提前加载，追指针（每个 `Long` 一个对象，位置随机）每次都可能 miss（约 100 ns）；**伪共享**：两个线程各写同一缓存行里的不同变量，缓存行在核间来回抢，写变慢。

**展开**

```
  寄存器 ~0.3 ns | L1 ~1 ns (32-64KB) | L2 ~4 ns | L3 ~15 ns | 内存 ~80-100 ns   (量级, 因机器而异)
  long[]:   [v0][v1][v2][v3][v4][v5][v6][v7] <- 一条 64B 缓存行 = 8 个 long, 顺序读几乎全命中 + 预取
  Long[]:   [ref][ref][ref]...  每个 ref -> 堆上随机位置的 Long (16B)   <- 打乱后每次访问 ~ 一次 miss
```

本机 `K21Locality`（1200 万个元素，稳态）：

```
sum of 12,000,000: long[]    2 ms | Long[] (alloc order)    3 ms | Long[] (shuffled)   34 ms
sum of 12,000,000: long[]    8 ms | Long[] (alloc order)    7 ms | Long[] (shuffled)   29 ms
```

读法：`Long[]` 在**分配顺序**遍历时对象本来就是连续放的（TLAB 指针碰撞），所以和 `long[]` 接近；**打乱引用顺序后慢约 10 倍**。这解释了：Java 的 `HashMap`/`LinkedList`/`TreeMap` 为什么在大数据量下比 C++ 同类慢 —— 节点散落在堆里；以及 GC 压缩/复制后对象邻近关系可能变化（对遍历有利或不利，不要承诺）。

**伪共享（false sharing）**：

```
  缓存行 64B:  [ counterA (线程1写) ][ counterB (线程2写) ] ...
  线程1 写 A -> 整行变"已修改"并使其它核的副本失效 -> 线程2 写 B 要重新取整行 -> 互相抢
```

* 修复：在变量之间填充（padding）到 64 字节以上；JDK 内部有 `@jdk.internal.vm.annotation.Contended`（应用代码默认不可用，需 `-XX:-RestrictContended`）；`LongAdder` 的 `Cell` 就用了它。
* 课文有一个专门的 demo：`S10/J16_concurrency_primitives.md` 配套的 `examples/J16/J16Ex8FalseSharing.java`（我没有重复写）。
* 工具：`perf c2c`（Linux，找伪共享，Q36）；本机无 Linux，未实跑。

**能说出口的 60 秒版本**

> "The CPU fetches memory in 64-byte cache lines, so contiguous arrays get both locality and hardware prefetching, while pointer chasing misses cache - roughly 100 nanoseconds per miss compared to a nanosecond for L1. In Java a `long[]` is contiguous but a `List<Long>` is an array of references to separate objects. In my test summing 12 million elements took a couple of milliseconds for the primitive array, about the same for boxed longs walked in allocation order, but around ten times longer once the reference order was shuffled. False sharing is the multi-threaded version: two threads writing different variables on the same cache line keep invalidating each other's copy; the fix is padding or striping, which is what `LongAdder` does internally."

**面试官可能的下一问**

* "How would you lay out an order book for cache efficiency?"（价格档位用数组/紧凑 long 编码，同一档位的订单放连续区；避免每订单一个对象。）
* "Does the JVM prefetch for you?"（硬件预取器顺序访问有效；JVM 本身只有少量预取指令（分配时），别依赖。）

**Demo / 课文**：`demos/K21Locality.java`；`S10/J16_concurrency_primitives.md`；`S00/cpu_cache_locality.md`；`S00/examples/CacheDemo.java`。

---

## [E] JIT 与 GC（JVM 内部）

### Q18 · How does the JIT work? Explain the interpreter, C1, C2, tiered compilation, and OSR.

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（F-A13）：「为什么C++比别的语言快？」的 Java 侧机制层追问；KQ04。
- **一句话答案**：分层编译：tier 0 解释器（收集计数）→ tier 1–3 C1（快速编译，tier 3 带完整 profiling）→ tier 4 C2（用 profile 做激进优化）；热点循环用 OSR 在循环中途切换；编译在后台线程完成，完成前继续用旧版本。

**展开**

```
  字节码 --(调用/回边计数器超阈值)--> 编译队列 --后台线程--> C1 代码(带 profile) --更热--> C2 代码
     ^                                                                                    |
     |                    去优化(deopt): 推测失败, 回到解释器/C1 重新 profile <-------------+
```

* 为什么要分层：C2 编译慢但产出快；C1 编译快产出一般。分层让你**先快速变快，再慢慢变极快**。
* 阈值：本机 `-XX:+PrintFlagsFinal` 实测 `Tier3CompileThreshold=2000`、`Tier4InvocationThreshold=5000`、`Tier4CompileThreshold=15000`、`TieredStopAtLevel=4`（这些是默认值，运行时会按编译队列长度动态缩放）。
* **OSR（on-stack replacement）**：一个 `main` 里只调用一次的长循环，没有"方法调用次数"可数，靠回边计数；达到阈值后在**循环迭代之间**把解释器栈帧换成编译版本。`PrintCompilation` 里带 `%` 的就是 OSR。本机 `K10Jit` 输出里 `K10Jit::run @ 4 (34 bytes)` 前有 `%`：

```
19  133 %     3       K10Jit::run @ 4 (34 bytes)       <- tier3 (C1) OSR
19  134       3       K10Jit::run (34 bytes)           <- tier3 正常入口
20  143 %     4       K10Jit::run @ 4 (34 bytes)       <- tier4 (C2) OSR   (这行被程序自己的输出打断了，行首的 20 就是它)
21  167       4       K10Jit::run (34 bytes)           <- 正常方法入口的 C2 版本
```

* 观察：`-XX:+PrintCompilation`；`-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining`；`jcmd <pid> Compiler.codecache`（本机 `jcmd help` 列出了 `Compiler.codecache`）；JFR 的编译事件。
* 编译线程会和业务线程**抢 CPU**，小核数容器里会放大预热期延迟（推断，常见经验）。

**能说出口的 60 秒版本**

> "HotSpot uses tiered compilation. Code starts in the interpreter, which counts invocations and loop back-edges. Past a threshold, the method is compiled by C1 - fast to compile, moderately optimised, with profiling - and if it stays hot, by C2, which uses the collected profile to do aggressive optimisation like inlining on observed types. Compilation happens on background threads. A hot loop in a method that's called only once is handled by on-stack replacement, which swaps the running frame between iterations. If a speculation turns out wrong, the JVM deoptimises back to the interpreter and starts again. You can watch all of that with `-XX:+PrintCompilation`: the lines with a percent sign are OSR compilations."

**面试官可能的下一问**

* "What is the code cache and what happens when it's full?"（编译后代码存放区；满了 JIT 停止编译，性能下降；`-XX:ReservedCodeCacheSize`。）
* "Can you force compilation or disable it?"（`-Xint` 纯解释，`-XX:TieredStopAtLevel=1` 只用 C1；诊断用，生产别这么做。本机 `-Xint` 在 K01 里改变了可见性行为，见 Q25。）

**Demo / 课文**：`demos/K10Jit.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q19 · What is inlining and why is it "the mother of all optimisations"? How does the JIT inline virtual calls?

- **难度**：★★★
- **来源**：`推断：Java 对应`（C++ 的"模板/内联/虚函数代价"问法的 Java 版）。
- **一句话答案**：内联把被调方法的代码拷进调用者，消除调用开销，并让后续优化（常量传播、逃逸分析、循环优化）能跨方法工作。接口/虚调用靠 **类层次分析（CHA）+ 类型 profile**：只有一个实现就直接内联（带"类没变"的依赖），1–2 种见过的类型用类型检查 + 内联，见过 ≥3 种（megamorphic）退回虚表/接口表调用。

**展开**

```
  s.area(i)     s 的静态类型是接口 Shape
  1 种实现:     直接内联 Sq.area, 无需检查 (CHA: 当前只加载了 Sq; 若以后加载了新实现类 -> 失效 -> 去优化)
  2 种见过:     if (s.class == Sq) {内联Sq} else if (s.class == Tri) {内联Tri} else {去优化或虚调用}   (bimorphic)
  >=3 种:       通过 itable/vtable 间接调用, 不内联 (megamorphic), 每次一次间接跳转 + 无法跨调用优化
```

本机 `K10Jit`（steady state）：

```
1 type  (Sq)            0.27–0.38 ns/call
2 types (Sq,Tri)        0.34–0.36 ns/call
3 types (Sq,Tri,Cir)    0.9 → 1.35 ns/call    <- 约 4 倍, 因为 megamorphic 不再内联
```

`-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining` 的输出（去重后）：

```
@ 19   K10Jit$Sq::area (4 bytes)   inline (hot)             (出现 4 次)
@ 19   K10Jit$Tri::area (6 bytes)  inline (hot)
@ 19   K10Jit$Shape::area (0 bytes)   virtual call           <- 没内联: 见过的类型太多
@ 19   K10Jit$Shape::area (0 bytes)   no static binding
```

* 阈值（本机 `PrintFlagsFinal`）：`MaxInlineSize=35`（字节码字节数；冷方法超过 35 不内联）、`FreqInlineSize=325`（热方法上限）、`MaxInlineLevel=15`（内联深度）。**所以保持热方法小**：一个 400 字节码的巨型方法不会被内联进调用者。
* 影响设计：热路径上的接口/抽象类若运行时实现类 ≥ 3 种，就付虚调用代价；常见做法是（a）把热路径特化成 `final` 类/单一实现，（b）用 `switch` 在调用者里分派（`sealed` + 模式 `switch` 是 `invokedynamic` typeSwitch，不一定更快，要测）。
* 对比 C++：模板在编译期单态化并内联；虚函数调用（`virtual`）不能内联除非编译器能证明具体类型或用 PGO/LTO 做 devirtualization。Java 是在**运行时**根据实际观察到的类型做。
* `final` 方法/类、`static`、`private` 方法天然可以直接内联（不需要 CHA）。

**能说出口的 60 秒版本**

> "Inlining removes call overhead but more importantly it opens up other optimisations - once the callee's body is in the caller, the JIT can propagate constants, eliminate allocations by escape analysis, and hoist checks out of loops. For virtual and interface calls, HotSpot uses class-hierarchy analysis and the type profile: if only one implementation is loaded it inlines directly, and if the call site has seen one or two receiver types it inlines with a type check. With three or more it goes megamorphic and does a table dispatch. I measured that: about 0.3 ns per call with one or two implementations and about 1.35 ns with three. Methods also have to be small enough: 35 bytecodes when cold, 325 when hot, by default."

**面试官可能的下一问**

* "How would you restructure code to avoid a megamorphic call on the hot path?"（按事件类型拆分处理循环、让每个调用点只见到少量类型、或用 `switch`。）
* "Does a lambda call get inlined?"（lambda 是 `invokedynamic` 生成的类；调用点见到的 lambda 种类少时可内联；多种 lambda 经过同一个 `Function.apply` 点同样会 megamorphic。）

**Demo / 课文**：`demos/K10Jit.java`；`S10/J19_runtime_zgc_jit.md`；`S10/J03_pattern_switch.md`（typeSwitch）。

---

### Q20 · What is escape analysis? What optimisations come from it, and when does it fail?

- **难度**：★★★
- **来源**：`推断：Java 对应`（C++ 对应问法：栈对象 vs 堆对象、`new` 的代价，kq06）。JD 层面对应「Address performance limitations」。
- **一句话答案**：C2 分析一个对象是否"逃出"当前编译单元（被存到字段/静态变量/返回/传给未内联的方法）；不逃逸就可以 **标量替换**（对象拆成寄存器里的字段，根本不分配）、**锁消除**；失败的常见原因是方法没被内联、对象存进了集合/字段、分支太复杂。

**展开**

```
  Point p = new Point(i, i+1).plus(new Point(2, 3));  // 三个 Point
  return p.x() + p.y();
  逃逸分析(内联后): 三个 Point 都只在本方法里被读字段 -> 不分配, 变成 4 个 long 局部变量的算术
```

本机 `K04EscapeAnalysis`（`record Point(long x,long y)`，5 轮每轮 5000 万次迭代，`getThreadAllocatedBytes` 统计）：

```
默认:                         round 1–4: ~48 ms, allocated 0 bytes
-XX:-DoEscapeAnalysis:        round 1–4: ~386 ms, allocated 4,800,000,000 bytes   (= 50M × 3 对象 × 32 B)
```

分配被完全消除，速度约 8 倍。注意：

* **EA 是 C2 的优化**；C1 没有。所以它在预热后才出现（上面 round 0 还有 1.6 MB 分配，就是解释/C1 阶段）。
* **依赖内联**：`plus` 没被内联，`new Point` 就"逃逸给了被调用者"（参数逃逸）。所以 Q19 的方法大小限制直接影响 EA。
* **失败场景**：对象放入 `ArrayList`/`Map`、赋给字段、通过 `Object` 参数传入不能内联的方法、被锁在 `synchronized` 之外的线程可见区域、数组太大（`EliminateAllocationArraySizeLimit` 默认 64 个元素，本机 `java -XX:+PrintFlagsFinal` 核对过）、控制流汇合处对象逃逸（C2 不做部分逃逸分析，Graal 做）。
* 与装箱的关系：`Integer` 在循环里装箱后不逃逸时可被消除（Q14 的 12 B/次 < 16 B 就是这个现象的体现）。
* **不要依赖它**：这是优化，不是语言保证。验证办法：`getThreadAllocatedBytes` 差值，或 JFR 分配事件，或 `-XX:+PrintEliminateAllocations`（调试选项，本机未试）。

**能说出口的 60 秒版本**

> "Escape analysis is a C2 optimisation that proves an object never leaves the compiled method - it's not stored in a field, returned, or passed to a call that wasn't inlined. If so, the JVM can do scalar replacement: the object's fields live in registers and the allocation disappears; it can also elide locks on such objects. I measured it on a small immutable `Point` record in an arithmetic loop: with it on, steady state allocated zero bytes and ran in about 48 ms; with `-XX:-DoEscapeAnalysis` it allocated 4.8 GB and took about 386 ms. It depends on inlining, so it fails when the method is too big or the object is stored somewhere. I treat it as a bonus rather than a guarantee, and verify with allocation counters."

**面试官可能的下一问**

* "Does that mean allocation is free in Java?"（只在被消除时；否则仍是 TLAB 分配 + 之后的 GC 压力，Q11。）
* "How would you write code to help escape analysis?"（小方法、短生命周期不可变值对象、不把它们存进容器或字段；热点处别用 lambda 捕获大量变量。）

**Demo / 课文**：`demos/K04EscapeAnalysis.java`、`demos/K02Boxing.java`；`S10/J01_record.md`。

---

### Q21 · What is deoptimisation? Give an example of when the JVM throws away compiled code.

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`（Java 与 C++ 的核心差异之一：投机优化）。
- **一句话答案**：JIT 为了快会做**投机**（只见过一种类型、某分支从没走过、没有第二个实现类）；假设被破坏时，JVM 在一个 uncommon trap 处把执行**回退到解释器**并丢弃/作废编译版本（日志里 `made not entrant`），之后重新 profile 再编译。

**展开**

触发例：(1) 类加载使 CHA 的"只有一个实现"失效；(2) 类型 profile 变化（见到新类型）；(3) 从没走过的分支被走到（`unstable_if`）；(4) 空指针/除零等"不应发生"的路径发生。

本机 `K10Jit` 的真实日志（`-XX:+PrintCompilation`）。程序先只用 `Sq`，然后第一次出现 `Tri`，再出现 `Cir`：

```
 19  134       3  K10Jit::run (34 bytes)
 21  167       4  K10Jit::run (34 bytes)                  <- C2 版本, 只见过 Sq
 61  174       3  K10Jit$Tri::area (6 bytes)              <- Tri 第一次被用到
 61  143 %     4  K10Jit::run @ 4 (34 bytes)   made not entrant   <- 旧的投机版本作废
 79  167       4  K10Jit::run (34 bytes)       made not entrant
 79  182       3  K10Jit::run (34 bytes)                  <- 回到 tier3 重新 profile
114  185       3  K10Jit$Cir::area (4 bytes)              <- Cir 第一次被用到
114  175 %     4  K10Jit::run @ 4 (34 bytes)   made not entrant   <- 再作废一次
115  189       4  K10Jit::run (34 bytes)                  <- 新 C2 版本: 3 种类型, megamorphic
```

读法：每次出现新实现类，之前依据"只有 1 个/2 个实现"编译的 `run` 都被作废并重新编译；代价是这几十毫秒里在慢路径上跑 + 编译开销。

对低延迟系统的含义：

* **预热要覆盖真实的类型和分支多样性**。只用 `BUY` 订单预热，上线第一个 `SELL` 会触发去优化 → 一次可见的延迟尖刺。
* 分支投机（`unstable_if`）同理：预热里"从不执行"的错误处理路径，在生产中第一次执行会去优化。
* 观察：`-XX:+PrintCompilation` 里的 `made not entrant`；JFR 有 `Deoptimization` 事件（我没在本机查看事件，名字来自记忆）。

**能说出口的 60 秒版本**

> "The JIT optimises speculatively - for example 'this call site has only ever seen one class', or 'this branch is never taken' - and puts an uncommon trap on the unlikely path. If the assumption breaks, the JVM deoptimises: it transfers the running frame back to the interpreter, marks the compiled method 'not entrant', and recompiles later with fresh profile data. I watched it with `PrintCompilation`: my hot method was compiled assuming one implementation, and the moment a second and then a third class were loaded the compiled versions were marked 'made not entrant' and rebuilt. The practical lesson for a latency-sensitive service is to warm up with a realistic mix of types and branches, otherwise the first real SELL order or error path pays for a deopt."

**面试官可能的下一问**

* "Can deopt be a source of tail latency in production? How would you find it?"（可以；`PrintCompilation` / JFR；对比预热流量与生产流量的分布。）
* "What's the difference between 'not entrant' and 'zombie'?"（not entrant：不再被新调用进入；zombie 是更老版本里待清除的状态，现在由代码缓存清扫处理。这一条我只记得大意，不要在面试里深入。）

**Demo / 课文**：`demos/K10Jit.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q22 · How does garbage collection work? Explain generations, roots, and the differences among Parallel, G1 and ZGC.

- **难度**：★★
- **来源**：`推断：Java 对应`（C++ `malloc/free`、智能指针问题的 Java 对偶；kq04–06）。
- **一句话答案**：GC 从根（线程栈、静态变量、JNI 引用）沿引用标记存活对象，其余回收。分代假说：大部分对象朝生夕死，所以把年轻代频繁小回收、老年代少回收。Parallel = 全停顿、吞吐高；G1 = 分 Region、按预期暂停时间增量回收（默认）；ZGC = 并发标记 + 并发整理，暂停亚毫秒、与堆大小基本无关，代价是吞吐/内存开销。

**展开**

```
 根:  线程栈局部变量, static 字段, JNI 全局引用, ...
       |
       v   标记(mark): 沿引用图遍历
   [A]->[B]->[C]      [D]->[E] <- 不可达 -> 垃圾
 回收方式: 复制(把存活者搬到新区, 剩下整块空闲) / 清除 / 整理(压缩)
```

* **分代假说**：young（Eden + 两个 Survivor）频繁回收，存活多次的晋升 old。年轻代 GC 的代价**正比于存活对象数**，而不是堆大小 —— 所以分配很多短命垃圾本身不贵。
* 本机观察（`K20Busy` + `jstat -gcutil`，G1，256 MB 堆，一个线程持续分配）：

```
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT   CGC   CGCT     GCT
   -  97.37  68.64  88.79  40.17   8.74   1245    0.273     0   0.000    22  0.001   0.274
   -  95.77   2.59  57.90  40.17   8.74   1477    0.321     0   0.000    28  0.002   0.323
   -  81.91  31.50  60.98  40.17   8.74   1685    0.366     0   0.000    32  0.002   0.368
```

  读法：两次采样间隔 0.5 秒，YGC 从 1245 涨到 1685（每秒数百次 young GC），累计 GC 时间 0.27→0.37 秒，没有 Full GC（FGC=0）。

| 收集器 | 暂停 | 适合 | 备注 |
|---|---|---|---|
| Parallel | 全停顿，随存活数据线性增长 | 批处理，吞吐优先 | 本机 K19：最大间隔 22 ms |
| G1（9 起默认） | 按 `MaxGCPauseMillis` 目标增量回收 Region | 通用 | 本机 K19：8 ms；mixed 回收清理老年代 |
| ZGC（15 正式；分代 21） | 并发标记+并发整理（读屏障 + 染色指针），暂停亚毫秒 | 低延迟、大堆 | 本机 K19：0.14 ms；需要留出堆余量，否则分配停顿（allocation stall） |
| Shenandoah / Epsilon | 另两种；Epsilon = 不回收 | — | 本机没跑 |

* **GC 根的陷阱**：静态集合/缓存/ThreadLocal 里的对象永远可达 → "内存泄漏"（Java 里的泄漏就是"不再需要但仍可达"）。
* 观察：`-Xlog:gc*`，`jstat -gcutil <pid> 500`，JFR，`jcmd <pid> GC.heap_info`，`GC.class_histogram`（Q37）。

**能说出口的 60 秒版本**

> "A tracing collector starts from roots - thread stacks, statics, JNI handles - marks everything reachable and reclaims the rest. Because most objects die young, the heap is split into generations: young collections are cheap because their cost scales with live objects, not with garbage. Parallel GC stops the world for the whole collection and is best for throughput. G1, the default since 9, splits the heap into regions and collects incrementally toward a pause-time target. ZGC marks and relocates concurrently with the application using load barriers, so pauses stay sub-millisecond regardless of heap size, at the cost of some throughput and needing headroom. On a test I ran, the worst stall was about 22 ms with Parallel, 8 ms with G1, and 0.14 ms with generational ZGC."

**面试官可能的下一问**

* "What's a Java memory leak?"（静态 map、监听器未注销、ThreadLocal、缓存无上限 —— 对象仍可达。）
* "What's the generational hypothesis and when does it fail?"（缓存/大量中等寿命对象 → 晋升多，老年代压力大。）

**Demo / 课文**：`demos/K19Pauses.java`、`demos/K20Busy.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q23 · Your Java trading component has latency spikes. How do you choose and tune the GC? When ZGC, when G1?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`；JD「Address performance limitations …」「Develop and improve monitoring and proactive detection」（O-C2）。
- **一句话答案**：先量化：谁在暂停？（`-Xlog:gc*,safepoint`）。再选：延迟敏感且堆大 → 分代 ZGC（21 用 `-XX:+UseZGC -XX:+ZGenerational`）；通用/吞吐 → G1。然后治本：降低分配率（热路径零分配）、堆大小留余量（`-Xms=-Xmx`）、`-XX:+AlwaysPreTouch`，最后才是微调。

**展开**

诊断流程（先测量，不要先调参）：

```
 1. 现象: p99/p999 尖刺。是 GC? 对齐时间线: -Xlog:gc*,safepoint:file=gc.log (统一日志)
 2. GC 暂停?  -> 看 "Pause Young/Remark/Cleanup" 时长; ZGC 看 allocation stall
 3. 不是 GC?  -> safepoint 其它原因(去优化, 偏向锁撤销已无), 页错误, 操作系统调度(Q24, Q36)
 4. 降分配率:  JFR 分配 profile / getThreadAllocatedBytes (K02/K03) -> 消除热路径装箱/临时对象
 5. 再选/调 GC
```

本机对照（`K19Pauses`，同一负载，不同收集器）：Parallel 22.4 ms / G1 8.2 ms（另一次带 `-Xlog:gc` 的实跑是 14.0 ms，G1 抖动较大）/ ZGC 0.14 ms 最大间隔。G1 的 `-Xlog:gc` 同一时段里的暂停行：

```
[7.960s][info][gc] GC(115) Pause Young (Normal) (G1 Evacuation Pause) 781M->267M(1024M) 5.288ms
```

选择与参数：

* **ZGC（分代）**：目标暂停 <1 ms，与堆大小无关；吞吐略低、需要 CPU 余量（并发线程）和**堆余量**。21 里分代需显式 `-XX:+ZGenerational`（后续版本逐步改为默认，别在 21 里假设）。
* **G1**：`-XX:MaxGCPauseMillis`（软目标）；停顿随存活数据量/晋升量波动。
* 通用：`-Xms == -Xmx` 避免动态扩缩；`-XX:+AlwaysPreTouch` 启动时触碰所有页，避免运行时页错误；大页（THP/HugePages）有利有弊，需测；容器里确认 JVM 看到的核数（GC 线程数）。
* 不要靠 `System.gc()`；`-XX:+DisableExplicitGC` 视情况。
* **最强的杠杆是降分配率**，不是换 GC：没垃圾就没 GC（Q03 checklist）。

**能说出口的 60 秒版本**

> "I'd start by measuring, not tuning: unified GC and safepoint logging, aligned with the latency spikes, to see whether the spikes are really GC pauses. If they are, the biggest lever is reducing allocation rate on the hot path - primitives, no boxing, reuse. Then collector choice: for latency-sensitive services with big heaps I'd use generational ZGC, which keeps pauses sub-millisecond - in my test, 0.14 ms versus 8 ms for G1 and 22 ms for Parallel - and keep the heap fixed-size with headroom and pre-touched. G1 is fine when a few milliseconds of pause are acceptable and throughput matters more. And I'd confirm with logs after each change instead of tuning by folklore."

**面试官可能的下一问**

* "What is an allocation stall in ZGC?"（应用分配速度超过回收速度，线程被迫等待；解决：加堆、降分配率、加 GC 线程。）
* "What does `AlwaysPreTouch` cost?"（启动更慢、RSS 一次性占满。）

**Demo / 课文**：`demos/K19Pauses.java`；`S10/J19_runtime_zgc_jit.md`。

---

### Q24 · Besides GC, what else makes a JVM pause? What's a safepoint?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`。
- **一句话答案**：**safepoint** 是所有 Java 线程都停在已知安全位置的时刻，JVM 在其中做 GC、去优化、类重定义、线程转储等操作；等所有线程到达的时间（time-to-safepoint）和 safepoint 里的工作都算暂停。GC 之外的抖动来源还有：页错误/内存回收、操作系统调度与 CPU 争用（含 JIT 编译线程）、类加载、日志与 I/O。

**展开**

```
  线程A: ...运行........ 到达 safepoint 检查点 -> 停
  线程B: ...运行.......................... (一个很长的计数循环没有检查点) -> 迟迟不停
  VM 线程: 请求 safepoint --等待所有线程到达(time-to-safepoint)--> 执行操作 --> 释放
```

* 本机 `-Xlog:safepoint`，G1 的 young GC 作为 safepoint 操作的日志行：

```
[0.034s][info][safepoint] Safepoint "G1CollectForAllocation", Time since last: 22903042 ns,
   Reaching safepoint: 97125 ns, Cleanup: 8166 ns, At safepoint: 1463917 ns, Leaving safepoint: 3875 ns, Total: 1573083 ns
```

  字段含义：`Reaching safepoint`（到达时间，约 0.1 ms）+ `At safepoint`（真正做事，约 1.5 ms）= 总暂停约 1.6 ms。同一次运行的后续几行，At safepoint 涨到 2.9–3.1 ms（活跃数据在增长）。
* 常见 safepoint 原因：GC、`Deoptimize`、`ThreadDump`（`jstack`/`jcmd Thread.print` 本身会造成一次）、类重定义、`RevokeBias`（偏向锁，已移除）。
* 非 JVM 因素：本机 `K19Pauses nochurn`（没有任何垃圾）同样会看到毫秒级的间隔 —— 两次独立实跑的最大间隔分别是 0.02 ms 和 2.26 ms，另一次带 `-Xlog:safepoint` 的跑出过 12 ms。**结论：在没有 CPU 隔离的笔记本上，分不清是 JVM 还是 OS 的抖动；生产用独占核（隔离核 + 绑核）才能把 OS 抖动压下去。**
* 页错误/内存：新堆页首次触碰要内核清零（`AlwaysPreTouch`）；透明大页（THP）压缩可能引起停顿；交换（swap）是灾难。
* 计数循环：旧版本里 `int` 计数的长循环没有 safepoint 检查，会拖慢到达；现在 loop strip mining 缓解（我记得大意，细节未核对）。

**能说出口的 60 秒版本**

> "A safepoint is a point where every Java thread is parked in a known state so the VM can do work that needs a consistent view: GC, deoptimisation, class redefinition, thread dumps. The pause has two parts - the time to reach the safepoint, which a long loop without a poll can stretch, and the time spent in the operation. `-Xlog:safepoint` prints both; for a G1 young collection I saw roughly 0.1 ms to reach and 1.5 ms of work. And not every spike is the JVM: page faults, THP compaction, CPU contention and the scheduler all show up too, which is why production latency boxes use isolated cores, pinned threads and pre-touched memory."

**面试官可能的下一问**

* "How would you tell a GC pause from an OS scheduling delay?"（GC 日志/JFR 有记录；`perf sched`/`runqlat`、`vmstat` 的 `r` 和 `cs`，Q36。）
* "Does ZGC have safepoints?"（有，但极短，只做根扫描等小操作。）

**Demo / 课文**：`demos/K19Pauses.java`、`demos/OUTPUTS.txt`；`S10/J19_runtime_zgc_jit.md`。

---

## [F] 并发与内存模型（kq01）

### Q25 · What is the Java Memory Model? What does "happens-before" mean, and why do we need it?

- **难度**：★★★
- **来源**：`推断：Java 对应`。C++ 报告（Glassdoor RVW89062704，F-G2，2026-02）：「Later rounds covered algorithms, OS concepts, concurrency, and open-ended systems questions」→ https://fr.glassdoor.ca/Entretien/Headlands-Technologies-Entretien-E715901-RVW89062704.htm ；CATALOG kq01 的 Java 对应写作「JMM / 线程与锁」。
- **一句话答案**：JMM 规定了"一个线程的写在什么条件下**一定**对另一个线程的读可见、以及指令可以怎样重排"。**happens-before** 是这套规则的核心：若 A happens-before B，则 A 的写对 B 可见且 A 不会被重排到 B 之后；没有 happens-before 关系的读写就是**数据竞争**，结果不保证。

**展开**

为什么需要：现代硬件和编译器为了快会**重排指令**、把变量缓存在**寄存器/核私有缓存**里。单线程里看不出来（保证"好像按顺序"），多线程里就出问题。

```
 线程1:  data = 42;  ready = true;           线程2:  while (!ready) {}   print(data)
 没有同步时可能: (a) 线程2 永远看不到 ready=true (JIT 把读提到循环外, 寄存器里的旧值)
                 (b) 看到 ready=true 但 data 还是 0 (重排或缓存未刷新)
```

本机 `K01Visibility`：

```
$ java K01Visibility              plain   : reader finished within 1.5s after the write? false
                                  volatile: reader finished within 1.5s after the write? true
$ java -Xint K01Visibility        plain   : reader finished within 1.5s after the write? true
```

非 volatile 的读线程在 JIT 编译后**永远看不到**更新；用 `-Xint`（纯解释）反而"碰巧正常"。教训：**没有同步的代码"能跑"不说明正确，换个 JIT 状态就坏**。

happens-before 的主要规则（JLS §17.4.5，https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html ）：

1. 同一线程内：程序顺序（前面的动作 hb 后面的）。
2. 监视器：`unlock` hb 之后对**同一个**锁的 `lock`。
3. `volatile`：对 volatile 变量的写 hb 之后对它的读。
4. `Thread.start()` hb 被启动线程里的任何动作；线程里的所有动作 hb 另一线程从 `join()` 返回。
5. `final` 字段：构造器结束时的冻结语义（Q33）。
6. 传递性：A hb B 且 B hb C ⇒ A hb C。

规则 3 + 6 就是"发布"套路：写 data（普通写），再写 volatile `ready`；读 `ready`（volatile 读），再读 data —— 能保证读到 42。

**能说出口的 60 秒版本**

> "The memory model defines when one thread's writes are guaranteed to be visible to another, because compilers and CPUs reorder instructions and cache values. The central concept is happens-before: if A happens-before B, A's effects are visible to B and can't be reordered past it. The rules are program order within a thread, unlock-before-later-lock on the same monitor, a volatile write before later reads of it, `Thread.start` and `join`, and transitivity. Without such an edge you have a data race and no guarantees. I can show it: a plain boolean flag read in a spin loop never became visible to the reader thread once the JIT compiled the loop, while the volatile one did - and with the JIT disabled the plain one even 'worked', which is exactly why such bugs are hard to find."

**面试官可能的下一问**

* "What's the difference between visibility and atomicity?"（Q26）
* "Does `synchronized` give visibility too?"（是：unlock hb 随后的 lock；进入时重新读、退出时写回。）

**Demo / 课文**：`demos/K01Visibility.java`；`S10/J16_concurrency_primitives.md`（第 1 节从零讲 JMM）。

---

### Q26 · What does `volatile` guarantee and what doesn't it? Is `volatile int count; count++` thread-safe?

- **难度**：★★
- **来源**：`推断：Java 对应`（kq01 并发类；Java 面试第一高频题）。
- **一句话答案**：`volatile` 保证 **可见性**（写立刻对后续读可见）和 **有序性**（写前的操作不会被重排到写后；读后的操作不会被重排到读前），**不保证复合操作的原子性**；`count++` 是读-改-写三步，不安全。

**展开**

本机 `K22VolatileCounter`：4 个线程各 `++` 100 万次：

```
expected 4,000,000 | volatile++ 684,857 | synchronized 4,000,000 | AtomicInteger 4,000,000
```

（这是第一次实跑；复跑一次得到 2,148,166，见 `demos/OUTPUTS.txt` 末尾。**每次不同但都远小于 4,000,000**，正是数据竞争的特征。）丢了几十万到三百多万次更新。过程：

```
 线程1 读 count=5      线程2 读 count=5
 线程1 算 6 写回 6     线程2 算 6 写回 6    <- 两次加 1 只加了一次
```

volatile 适用：**一个线程写、其它线程读的状态标志**（`running`、`ready`）、安全发布不可变对象的引用、DCL 的单例引用（Q33）。不适用：计数器、"检查再行动"（check-then-act）。

硬件层面（概念）：volatile 写后需要内存屏障保证 StoreLoad 顺序（x86 上常见为一条带锁前缀的指令或 `mfence`，ARM 上用 `stlr/ldar` 指令或 `dmb`），所以 volatile 写比普通写贵；volatile 读在 x86 上几乎免费。这条是一般认识，本机（arm64）未看汇编。

其它细节：

* 非 volatile 的 `long`/`double` 在 JLS 里允许被拆成两次 32 位写（理论上的"撕裂"）；64 位 HotSpot 上实际是原子的，但规范不保证 —— 声明为 `volatile` 即保证。
* `volatile` 数组：只有引用是 volatile，元素不是。要元素级语义用 `VarHandle`/`AtomicLongArray`（`S10/J16_concurrency_primitives.md`）。

**能说出口的 60 秒版本**

> "`volatile` gives you visibility and ordering: a write is seen by subsequent reads in other threads, and the compiler and CPU won't reorder around it in a way that breaks that. It does not make compound operations atomic - `count++` on a volatile is a read, an add and a write, and two threads can interleave. I tested it: four threads each doing a million increments ended at 685,000 on one run and 2.1 million on another instead of four million, while `synchronized` and `AtomicInteger` were exact. I use volatile for status flags and for publishing immutable state; for counters I use atomics or `LongAdder`."

**面试官可能的下一问**

* "Is a volatile array's content volatile?"（不是。）
* "How is volatile implemented?"（屏障/特殊指令；禁止 JIT 把读提出循环。）

**Demo / 课文**：`demos/K22VolatileCounter.java`、`demos/K01Visibility.java`；`S10/J16_concurrency_primitives.md`。

---

### Q27 · `synchronized` vs `ReentrantLock` — differences, cost, and what changed with virtual threads?

- **难度**：★★
- **来源**：`推断：Java 对应`（C++ 的 `std::mutex` / `lock_guard` 问法在 Java 的对应）。
- **一句话答案**：两者语义相近（互斥 + 可见性 + 可重入）；`ReentrantLock` 多了 `tryLock`、可中断、公平性、多个 `Condition`，需要手动 `unlock`（放进 `finally`）；`synchronized` 简洁、自动释放、JIT 可做锁消除/粗化。**JDK 21 里虚拟线程在 `synchronized` 里阻塞会 pin 住载体线程，`ReentrantLock` 不会。**

**展开**

```
 synchronized (obj) { ... }            lock.lock(); try { ... } finally { lock.unlock(); }
  - 对象头 mark word 里的锁状态          - 基于 AQS(AbstractQueuedSynchronizer), 纯 Java
  - 无竞争: 轻量; 有竞争: 膨胀成 monitor  - tryLock(timeout), lockInterruptibly(), 公平锁, 多条件队列
```

本机 `K08Counters`（每个线程 500 万次受保护的 `++`，粗糙计时）：

```
threads=1  synchronized  13 ms | ReentrantLock  16 ms | AtomicLong   6 ms | LongAdder  12 ms
threads=4  synchronized 115 ms | ReentrantLock 131 ms | AtomicLong 195 ms | LongAdder  13 ms
threads=8  synchronized 228 ms | ReentrantLock 236 ms | AtomicLong 320 ms | LongAdder  17 ms
```

两种锁在这里**同一数量级**；不要告诉面试官"ReentrantLock 比 synchronized 快"（Java 6 之后基本拉平）。偏向锁已移除（Q06 实测选项不存在）。

**虚拟线程与 pinning**（`K09Pinning`，只留 1 个载体线程，8 个任务各睡 200 ms）：

```
sleep inside synchronized : 2455 ms   <- 载体被钉住, 8 个任务近似串行 (理想串行 1600 ms, 加上调度开销)
sleep outside synchronized:  348 ms   <- 睡眠时虚拟线程让出载体, 近似并行 (理想 200 ms)
```

结论：在 JDK 21，对"可能阻塞"的临界区用 `ReentrantLock`，避免在 `synchronized` 里做 I/O/睡眠。该限制由 JDK 24 的 JEP 491 取消（课文 `J16` 也提到；24 超出本机环境，未验证）。可用 `-Djdk.tracePinnedThreads=full` 打印 pin 事件（`J10Ex4Pinning` 示例）。

选择：简单互斥 → `synchronized`；需要超时、可中断、公平、多条件 → `ReentrantLock`；读多写少 → `StampedLock`/`ReadWriteLock`（要测）。

**能说出口的 60 秒版本**

> "Both give mutual exclusion, visibility and reentrancy. `synchronized` is built into the language, releases automatically, and the JIT can elide or coarsen locks. `ReentrantLock` is a library lock built on AQS with `tryLock`, interruptible and timed acquisition, optional fairness and multiple conditions, at the price of a manual `unlock` in `finally`. Performance is about the same since Java 6 - in my test with eight contended threads they were within a few percent. The practical difference in Java 21 is virtual threads: blocking inside `synchronized` pins the carrier thread - with one carrier, eight 200-ms sleeps took 2.4 seconds inside `synchronized` versus 0.35 seconds outside - whereas `ReentrantLock` lets the virtual thread unmount."

**面试官可能的下一问**

* "What is lock inflation?"（对象头从无锁→轻量→重量 monitor；偏向锁已不在。）
* "Fair vs unfair lock?"（公平锁排队、吞吐低；非公平允许插队、吞吐高、可能饥饿。）

**Demo / 课文**：`demos/K08Counters.java`、`demos/K09Pinning.java`；`S10/J16_concurrency_primitives.md`；`S10/J10_virtual_threads.md`。

---

### Q28 · What is CAS? How do atomics work? Is lock-free always faster than locking? What is `LongAdder`?

- **难度**：★★★
- **来源**：`推断：Java 对应`；C++ 报告里反复出现的"lock-free"主题：C++ JD「lock-free data structures」（O-C3）。
- **一句话答案**：CAS（compare-and-swap）是一条原子指令："如果内存值 == 期望值就写入新值，否则失败"，`AtomicLong` 在循环里重试它。无锁 ≠ 更快：高竞争下 CAS 重试风暴会比锁还慢；`LongAdder` 把一个热点计数器拆成多个 `Cell`（分段），读时求和，写扩展性极好。

**展开**

```
 AtomicLong.incrementAndGet() ≈  do { old = get(); new = old + 1 } while (!CAS(addr, old, new))
 x86: lock cmpxchg / lock xadd      ARM64: LL/SC 或 LSE 的 CAS 指令
```

本机 `K08Counters`（8 线程竞争一个计数器，各 500 万次）：

```
synchronized 228 ms | ReentrantLock 236 ms | AtomicLong 320 ms | LongAdder 17 ms
```

观察：

* **低竞争（1 线程）**：`AtomicLong` 最快（6 ms vs 13 ms）。
* **高竞争**：`AtomicLong` 比 `synchronized` 还慢 —— 所有核反复争抢同一个缓存行，CAS 失败重试，每次重试都浪费一次缓存行传输；锁则让线程排队/睡眠，避免了空转。
* **`LongAdder` 快一个数量级**（17 ms）：每个线程（哈希后）更新自己的 `Cell`（各占一条缓存行，Q17），只有 `sum()` 时才汇总；代价是 `sum()` 不是原子快照、占内存更多。适用：统计计数器；不适用：需要精确同步判断的值（如序列号分配）。
* **ABA 问题**：线程1 读到 A，线程2 把 A→B→A，线程1 的 CAS 成功但中间状态已变。解决：带版本戳（`AtomicStampedReference`）或让数据不可变。
* **何时无锁值得**：竞争低、临界区极短、不能阻塞（实时/热路径）、避免优先级反转/锁护航。不值得：竞争高、需要多变量一致性。
* 自己做无锁结构很难，用现成的：`ConcurrentLinkedQueue`、`ConcurrentSkipListMap`、`ArrayBlockingQueue` + 单线程所有者模式（"mechanical sympathy"：让一个线程拥有数据，其它线程通过队列发消息）。

**能说出口的 60 秒版本**

> "CAS is an atomic instruction that writes a new value only if the current value still equals the expected one; atomics retry it in a loop. It's lock-free but not automatically faster. In my test with eight threads hammering one counter, `AtomicLong` took 320 ms, slightly slower than `synchronized` at 228 ms, because every failed CAS bounces the cache line between cores. `LongAdder` took 17 ms because it stripes the counter across cells, one per thread roughly, and sums on read. The trade-offs are that `sum()` isn't an atomic snapshot and you can't use it for sequence numbers. Also watch for ABA, which needs a version stamp or immutable nodes. For hot paths I prefer single-writer designs with queues over clever lock-free structures."

**面试官可能的下一问**

* "Implement a thread-safe counter / a lock-free stack."（Treiber stack：`AtomicReference<Node>` + CAS push/pop。）
* "What's `VarHandle` for?"（对字段/数组元素/堆外缓冲的细粒度内存序：`getAcquire/setRelease/compareAndSet`；`K16Ipc` 用它做跨进程可见。）

**Demo / 课文**：`demos/K08Counters.java`；`S10/J16_concurrency_primitives.md`（含 CAS、`VarHandle`、`LongAdder`）。

---

### Q29 · How does `HashMap` work internally? Resizing, collisions, treeification, why is the capacity a power of two?

- **难度**：★★
- **来源**：`推断：Java 低延迟岗经典`；关联 Blind 2024-08（F-B1）第二题「optimizing a C++ unordered_map for stock tickers」→ 的 Java 版是 hc07（`loop/rounds/01_video/hc07_ticker_hash_map/`）。
- **一句话答案**：数组 + 链表/红黑树。`index = (n-1) & (h ^ (h >>> 16))`；负载因子 0.75 触发翻倍扩容；同一桶链表 ≥ 8 且表容量 ≥ 64 时转红黑树（≤ 6 退回）。容量取 2 的幂，是为了用位与代替取模。

**展开**

```
 table: [0][1][2]...[15]            put(k,v):  h = k.hashCode(); h ^= h>>>16;  i = h & (n-1)
           |                          桶空  -> 放 Node
           Node(k1)->Node(k2)->...    桶非空 -> 比较 hash 与 equals, 相同则覆盖, 否则挂链尾
```

本机 `K06HashMap`（`--add-opens` 反射读 `table`，全部是实测）：

```
new HashMap(): table = null (lazy allocation)           <- 第一次 put 才分配
after 1 puts: table.length = 16
after 13 puts: table.length = 32                        <- 12 = 16 × 0.75, 第 13 个触发翻倍
after 25 puts: 64 ; after 49 puts: 128 ; after 97 puts: 256
"Aa".hashCode()=="BB".hashCode(): true (2112)           <- 字符串 hash 容易构造碰撞
spread(0x12345678)=0x1234444c ; index in 16 buckets = 12  <- 高 16 位异或进低 16 位, 否则只用低位, 高位信息浪费

colliding put #8:  table.length=16, bin type=Node
colliding put #9:  table.length=32, bin type=Node       <- 桶里 ≥8 个节点, 但表 < 64: 先扩容, 不转树
colliding put #10: table.length=64, bin type=Node
colliding put #11: table.length=64, bin type=TreeNode   <- 表已达 64, 才真正转成红黑树
Comparable-colliding       8000 lookups: ~3.4 ms  (树内按 compareTo 二分)
non-Comparable-colliding   8000 lookups: ~20 ms (树内无法比较, 只能比 hash 再 tieBreak, 要遍历子树)
```

要点：

* **2 的幂**：`hash & (n-1)` 比 `hash % n` 快，扩容时每个节点要么留在原位置、要么移到 `原位置 + 旧容量`（看新增的一位），不用重新算 hash。
* **Java 8 改动**：链表转红黑树（防碰撞攻击，最坏 O(log n) 而不是 O(n)）；尾插法（Java 7 头插 + 并发扩容可能形成环 → 死循环）。
* 键需要稳定的 `hashCode/equals`；可变键放进去后改了字段 → 找不到。
* **交易场景的追问**：为股票代码设计专用 map：键是固定长度字符串 → 打包成 `long`；开放寻址 + 线性探测 + `long[] keys/int[] vals`；容量 2 的幂；负载因子 ≤ 0.5；避免装箱和 Node 对象（Q14、Q17）。见 hc07。
* 初始容量：已知元素数 n 时 `new HashMap<>(n * 4 / 3 + 1)` 避免多次扩容。`HashMap.newHashMap(n)` 是 Java 19 新增的便利方法。

**能说出口的 60 秒版本**

> "`HashMap` is an array of buckets; the index is the spread hash masked by capacity minus one, which is why capacity is a power of two - a bit-and instead of a modulo, and on resize each node either stays or moves by exactly the old capacity. The spread step XORs the high 16 bits into the low ones. At 0.75 load it doubles. If a bucket gets eight or more nodes it converts to a red-black tree, but only when the table has at least 64 buckets - below that it resizes instead; I verified that by reflecting into the table: the bin became a `TreeNode` at the eleventh colliding put. Trees need `Comparable` keys to be efficient; otherwise lookups scan. For a ticker-symbol map on a hot path I'd pack symbols into longs and use open addressing over primitive arrays."

**面试官可能的下一问**

* "Is `HashMap` thread-safe? What goes wrong?"（Q30 的 demo：并发 merge 丢更新。）
* "What's the iteration order of `HashMap`?"（不保证；`LinkedHashMap` 保插入序。）

**Demo / 课文**：`demos/K06HashMap.java`；`S30/hc07_ticker_hash_map.md`；`loop/rounds/01_video/hc07_ticker_hash_map/REPORT.md`（若已写完）。

---

### Q30 · How does `ConcurrentHashMap` achieve thread safety? How is it different from `Collections.synchronizedMap`? Why no null keys/values?

- **难度**：★★
- **来源**：`推断：Java 对应`；CATALOG kq01 的 Java 对应列表中明确写了「ConcurrentHashMap」。
- **一句话答案**：Java 8+ 的 CHM：空桶用 **CAS** 放入首节点；非空桶只对**该桶的头节点** `synchronized`（细粒度锁）；读不加锁（`volatile` 读）；计数用分段 `CounterCell`。所以并发度 ≈ 桶数。不允许 `null` 是为了让 `get` 返回 `null` 无歧义（"没有"而不是"值是 null"）。

**展开**

本机 `K07Chm`（8 线程各 20 万次 `merge(i&15, 1, Integer::sum)`，16 个 key，总预期 160 万）：

```
HashMap              expected 1,600,000  got 1,231,627  lost 368,373
ConcurrentHashMap    expected 1,600,000  got 1,600,000  lost 0
CHM.put(k, null) -> NPE
check-then-act race: if(!containsKey) put  vs  putIfAbsent -> 1 (returned existing)
```

* `HashMap` 并发更新同一个 key：读-改-写交错 → 丢更新（约 23%）。
* **CHM 的方法是原子的**：`putIfAbsent`、`computeIfAbsent`、`merge`、`compute`。**但**两个独立的 CHM 调用组合不是原子的：`if (!m.containsKey(k)) m.put(k, v)` 有竞态，要用 `putIfAbsent`。
* **不要在 `computeIfAbsent` 的函数里修改同一个 map**（可能死锁/抛 `IllegalStateException`）；函数要短（持有桶锁）。
* vs `Collections.synchronizedMap`：后者**整个 map 一把锁**，所有操作串行；迭代还要手动在 map 上同步。
* 历史：Java 7 是 16 个 `Segment`（分段锁），Java 8 改成桶级 `synchronized` + CAS。
* `size()` 是近似快照（并发下）；弱一致性迭代器（不抛 `ConcurrentModificationException`）。
* 为什么 CHM 不允许 null：并发下无法区分"key 不存在"和"key 映射到 null"（`containsKey` 之后值可能已变）。

**能说出口的 60 秒版本**

> "Since Java 8 `ConcurrentHashMap` uses CAS to insert into an empty bucket and synchronises only on the head node of a non-empty bucket, so concurrent writers to different buckets don't block each other, and reads are lock-free via volatile reads. The old segment design is gone. Individual operations like `merge` and `putIfAbsent` are atomic, but compositions of separate calls aren't. In a test with eight threads incrementing 16 keys, `HashMap` lost about 370,000 of 1.6 million updates and CHM lost none. It rejects nulls so that `get` returning null unambiguously means absent. `synchronizedMap` by contrast locks the whole map on every call."

**面试官可能的下一问**

* "Is `size()` accurate?"（并发下是估计值。）
* "How would you build an atomic counter per key?"（`map.computeIfAbsent(k, x -> new LongAdder()).increment()` 或 `merge`。）

**Demo / 课文**：`demos/K07Chm.java`；`S10/J16_concurrency_primitives.md`。

---

### Q31 · What are virtual threads? How do they differ from platform threads, and when should you NOT use them?

- **难度**：★★
- **来源**：`推断：Java 对应`（Java 21 的招牌特性；CATALOG kq01/kq02 的 Java 对应）。
- **一句话答案**：虚拟线程是 JVM 调度的轻量线程（挂在少量载体平台线程上）。阻塞操作（I/O、sleep、锁）时**卸载**载体线程让别人用，所以可以一个请求一个线程且同时有几十万个。对 **CPU 密集**没帮助、池化它们没意义；在 21 里 `synchronized` 阻塞会 pin 载体。

**展开**

```
 平台线程:  1 : 1 对应 OS 线程   (栈 ~1MB 虚拟地址, 创建/切换要进内核, 数千个就吃力)
 虚拟线程:  M : N              (栈是堆上的可增长对象, 阻塞时被"卸载", 载体线程去跑别的虚拟线程)
   VT1 --run--> [carrier-1]       VT1 在 sleep -> 卸载; carrier-1 继续跑 VT2
```

本机 `K09VirtualThreads`（12 核）：

```
inside: VirtualThread[#20,v1]/runnable@ForkJoinPool-1-worker-1
10,000 virtual threads each blocking 1 s: finished=10000 in 1195 ms
100,000 virtual threads each blocking 1 s: finished=100000 in 1592 ms
2,000 tasks on a 200-thread platform pool: 11281 ms (= 2000/200 * 1 s)
```

* 10 万个各睡 1 秒的任务总共约 1.6 秒完成（几乎全并行）；200 线程的平台池做 2000 个同样的任务要 11 秒（吞吐被线程数卡住）。
* **适合**：大量 I/O 阻塞的并发（每请求一线程的服务、扇出调用）。
* **不适合**：CPU 密集（核数才是限制，再多虚拟线程也一样）；长时间持有 `synchronized` 内阻塞（pin，Q27）；依赖 `ThreadLocal` 缓存大对象（每个虚拟线程一份）；用池复用虚拟线程（它们本来就便宜，别池化；限并发用 `Semaphore`）。
* 与结构化并发/ScopedValue 配套（21 预览）：`S10/J11_structured_concurrency.md`、`J12_scoped_values.md`。
* 对低延迟交易热路径：**不是它的场景** —— 热路径通常是固定线程 + 绑核 + 忙等；虚拟线程适合研究平台/基础设施里的 I/O 并发（JD 的 research infrastructure）。

**能说出口的 60 秒版本**

> "Virtual threads, final in Java 21, are threads scheduled by the JVM onto a small pool of carrier threads. When one blocks on I/O, sleep or a lock, it's unmounted so the carrier can run another, which makes thread-per-request affordable at hundreds of thousands of threads. I ran 100,000 virtual threads each sleeping a second and it finished in about 1.6 seconds, whereas a 200-thread pool took 11 seconds for just 2,000 such tasks. They don't help CPU-bound work, you shouldn't pool them, and in 21 blocking inside `synchronized` pins the carrier. For a latency-critical hot path I'd still use dedicated pinned platform threads; virtual threads fit I/O-heavy infrastructure."

**面试官可能的下一问**

* "How does a virtual thread block without blocking the OS thread?"（栈帧拷到堆，continuation 挂起；I/O 走非阻塞 + poller。）
* "What replaces `ThreadLocal`?"（`ScopedValue`，21 预览。）

**Demo / 课文**：`demos/K09VirtualThreads.java`、`demos/K09Pinning.java`；`S10/J10_virtual_threads.md`；`S00/os_processes_threads_ipc.md`。

---

### Q32 · How do you size a thread pool? What are the pitfalls of `Executors`?

- **难度**：★★
- **来源**：`推断：Java 对应`（C++ 的"线程数/任务队列"问法；hc02「多线程无阻塞合并数据流」追问相关，见 `loop/rounds/01_video/hc02_merge_k_streams/`）。
- **一句话答案**：CPU 密集 ≈ 核数（+1）；I/O 密集 ≈ 核数 × (1 + 等待时间/计算时间)，或直接用虚拟线程；队列必须有界、拒绝策略显式；别用 `Executors.newFixedThreadPool` 的无界队列和 `newCachedThreadPool` 的无界线程。

**展开**

* **Little 定律**：并发度 L = 吞吐 λ × 延迟 W。要 1000 请求/秒、每个 50 ms → 平均需要 50 个在途请求。
* 算术（本机 `K09VirtualThreads` 的对照）：200 线程、每任务阻塞 1 s ⇒ 吞吐上限 200/s ⇒ 2000 个任务需要 10 s（实测 11.3 s），与 CPU 核数无关 —— 说明 I/O 密集型的池大小由"阻塞时间"决定。
* `ThreadPoolExecutor` 的参数：core / max / 队列 / 拒绝策略。注意**行为顺序**：先到 core，再入队，队满才扩到 max，再满拒绝 —— 所以无界队列时 max 永远不起作用。
* `Executors.newFixedThreadPool`：无界 `LinkedBlockingQueue` → 过载时内存爆；`newCachedThreadPool`：无上限线程 → 过载时线程爆。
* 命名线程（便于 `jstack`/`jcmd Thread.print`）、未捕获异常处理、`Future.get()` 超时、关闭（`shutdown` + `awaitTermination`）。
* ForkJoinPool/并行 Stream 共用 `commonPool`；别在里面做阻塞 I/O。
* 热路径：线程数 = 绑核数，每线程独占一个核，不用池。

**能说出口的 60 秒版本**

> "For CPU-bound work I'd use about the number of cores; for I/O-bound work, cores times one plus wait over compute, or just virtual threads. Little's law is the sanity check: concurrency equals throughput times latency. The pitfalls are in `Executors`: the fixed pool has an unbounded queue and the cached pool has unbounded threads, so overload turns into out-of-memory. With `ThreadPoolExecutor` the order is core threads, then queue, then up to max, then reject - so an unbounded queue means max is never used. I'd use a bounded queue, a rejection policy that applies back-pressure, named threads, and proper shutdown. In my test a 200-thread pool doing one-second blocking tasks capped out at 200 tasks per second regardless of CPU count."

**面试官可能的下一问**

* "How would you implement back-pressure?"（有界队列 + `CallerRunsPolicy`，或信号量，或拒绝并返回错误。）
* "Why is `parallelStream()` risky in a server?"（共享 commonPool，阻塞任务会饿死别人。）

**Demo / 课文**：`demos/K09VirtualThreads.java`；`S10/J16_concurrency_primitives.md`；`S10/J10_virtual_threads.md`。

---

### Q33 · What is safe publication? Why is double-checked locking broken without `volatile`? What do `final` fields guarantee?

- **难度**：★★★
- **来源**：`推断：Java 低延迟岗经典`（JMM 追问；可由 Q25 引出）。
- **一句话答案**：对象构造完成后，如果通过数据竞争（无同步）发布引用，别的线程可能看到引用但看到**未初始化完的字段**（重排）。安全发布方式：volatile 字段、`final` 字段、静态初始化器、持锁发布、线程安全容器。DCL 单例的引用必须 `volatile`；`final` 字段在构造器结束时有"冻结"保证，其它线程看到引用就保证看到 final 字段的值。

**展开**

```
 单例 DCL (错误):                                  正确:
 if (inst == null) synchronized(L) {                private static volatile Foo inst;
   if (inst == null) inst = new Foo();              ... 同样的 DCL, 但 inst 是 volatile
 }
 new Foo() 可能被拆成: 1 分配  2 把引用写给 inst  3 执行构造器
 重排成 1,2,3 之后: 另一线程看到 inst != null 却读到没构造完的对象
```

最干净的写法是不用 DCL：**静态内部类持有者**（类初始化由 JVM 保证线程安全且惰性）或枚举单例：

```java
class Holder { static final Foo INSTANCE = new Foo(); }
```

* **`final` 字段语义**（JLS §17.5）：只要构造器里没有让 `this` 逃逸，其它线程通过引用读到的所有 final 字段（及它们可达的对象在构造器结束时的状态）都是构造完成后的值。这就是**不可变对象天然线程安全**的原因，也是 `record`（字段全 final）适合在线程间传递事件的原因（`S10/J01_record.md`）。
* 陷阱：`this` 逃逸（构造器里注册监听器/启动线程）；用普通字段发布可变对象；`HashMap` 放进去后不再修改并通过 volatile/final 发布，读取是安全的（"有效不可变"）。
* 本机说明：这类重排 bug 在 arm64/x86 + JIT 下**不易稳定复现**，我没有写 demo（强行写会写出不稳定的演示）。课文 `J16Ex2Reorder.java` 有专门的重排 demo。

**能说出口的 60 秒版本**

> "Safe publication means making an object's reference visible to another thread in a way that also makes its fields visible, using a happens-before edge: a volatile field, a final field, a static initializer, a lock, or a concurrent collection. Double-checked locking without `volatile` is broken because the reference write can be reordered before the constructor's writes, so another thread can see a non-null but half-built object; marking the field volatile fixes it, but a holder class or enum is simpler. `final` fields get a special guarantee: once the constructor finishes, any thread that sees the reference sees the final fields correctly, which is why immutable objects and records are safe to hand across threads as long as `this` doesn't escape during construction."

**面试官可能的下一问**

* "Write a thread-safe lazy singleton."（Holder idiom。）
* "Is a `record` always thread-safe?"（字段是 final，但若组件是可变对象（`List`），仍需防御性拷贝/不可变集合。）

**Demo / 课文**：`S10/J16_concurrency_primitives.md`（含 `J16Ex2Reorder`）；`S10/J01_record.md`。

---

## [G] 操作系统与 Linux 性能工具（kq01 + JD）

> **诚实声明**：本机是 macOS，没有 `perf`、`strace`、`vmstat`（只有 `top`、`vm_stat`）。本节涉及 Linux 工具的命令与输出格式是**常识性讲解，没有在本机实跑**，输出示意都标了「示意」。
> JDK 自带的诊断工具（`jcmd`/`jstat`/`jfr`/NMT）在本机实跑，输出见 `demos/OUTPUTS.txt`。

### Q34 · Process vs thread vs virtual thread: what is a context switch and what does it cost? How do you pin a thread to a core?

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 报告（Glassdoor RVW89062704，F-G2）：「OS concepts, concurrency」；54skyxenon 博客：onsite 约 6 轮低层概念（GH §1 #9；OSTEP 级别）。
- **一句话答案**：进程 = 独立地址空间 + 资源；线程 = 同一进程内共享地址空间的调度单位；虚拟线程 = JVM 里的用户态线程。上下文切换要保存/恢复寄存器、换调度实体（进程切换还要换页表，TLB 失效），**直接成本是微秒级，间接成本（缓存变冷）通常更大**；Java 标准库没有绑核 API，用 `taskset`/`numactl` 或第三方库。

**展开**

```
 进程 A: [代码|数据|堆|栈]  进程 B: [代码|数据|堆|栈]     <- 各自的虚拟地址空间, 隔离
 线程:   进程内共享 代码|数据|堆, 各有独立栈 + 寄存器
 切换:   保存 A 的寄存器 -> 调度器选 B -> 恢复 B 的寄存器 (进程间: 还要切换页表, TLB 部分失效)
 Java:   Thread = 1:1 OS 线程 (pthread);  虚拟线程 = JVM 在用户态切换栈 (Q31)
```

* **直接成本**：内核态切换指令序列，量级是 1–几微秒（常见经验数字，本机没测）。**间接成本**：被换走的线程的 L1/L2 缓存和分支预测状态被冲掉，回来后要重新热身 —— 这就是"线程数远多于核数反而更慢"的原因，也是低延迟系统"一线程一核、不让出"的原因。
* **本机线程栈**：`-XX:+PrintFlagsFinal` 显示 `ThreadStackSize = 2048`（KB，macOS arm64）；Linux x86_64 默认 1024 KB。栈是虚拟内存预留，按需提交。
* **系统调用**也有成本：用户态→内核态切换（`read/write/futex`），一次约百纳秒到微秒量级（量级，未测）。`synchronized`/`LockSupport.park` 竞争严重时会走 `futex`。
* **绑核**：`taskset -c 2,3 java …` 把整个 JVM 限制在核 2、3；`numactl --cpunodebind` 控制 NUMA；内核启动参数 `isolcpus`/`nohz_full` 把核从调度器和时钟中断里隔离出来；Java 里单线程绑核需要库（如 OpenHFT Affinity 通过 JNA/JNI；第三方，本机未试）。
* GC/JIT 线程数：`ParallelGCThreads=10`、`ConcGCThreads=3`、`CICompilerCount=4`（本机 12 核的默认值），低延迟机器上要给它们留核，否则抢业务线程。

**能说出口的 60 秒版本**

> "A process has its own address space; threads within a process share it and are what the OS schedules. A context switch saves one thread's registers and loads another's - and for a different process also switches page tables. The direct cost is on the order of microseconds, but the bigger cost is indirect: the cache and branch predictor are cold when you come back. That's why latency-critical systems use a thread per core and avoid blocking. Java platform threads map one-to-one to OS threads; virtual threads are scheduled in user space by the JVM. For pinning, Java has no standard API, so I'd use `taskset` or `numactl` for the process, plus isolated cores via `isolcpus`, or a library such as OpenHFT Affinity for per-thread pinning."

**面试官可能的下一问**

* "What happens when you call `read()` on a socket from Java?"（Q41。）
* "How many threads can one JVM create?"（受 OS 限制（`ulimit -u`、内存、`max_map_count`）；虚拟线程解决规模问题。）

**Demo / 课文**：`S00/os_processes_threads_ipc.md`；`S00/examples/IpcDemo.java`（线程交接延迟、系统调用成本的 demo，已存在）。

---

### Q35 · Explain virtual memory, the page cache and page faults. Why is a JVM's RSS bigger than `-Xmx`?

- **难度**：★★
- **来源**：`推断：JD`（「Strong knowledge of the details of computing all throughout the technical stack」「Address performance limitations within … Linux」，O-C2）；OSTEP 类题（GH §1 #9）。
- **一句话答案**：每个进程看到自己的**虚拟地址空间**，MMU 通过页表映射到物理页；没映射的页被访问触发**缺页（page fault）**，内核按需分配/从文件读入；文件 I/O 先经过 **page cache**（内核缓存）。JVM 的 RSS = 堆 + 元空间 + 代码缓存 + 线程栈 + GC 数据结构 + 直接内存 + 共享库，所以必然大于 `-Xmx`。

**展开**

```
 虚拟地址 --页表(MMU/TLB)--> 物理页
   未映射/换出 -> page fault -> 内核: 分配并清零一页(匿名页) 或 从磁盘读入(文件页) -> 继续
 文件读写: 应用 buffer <-> page cache <-> 磁盘     (写: 先写 page cache, 稍后回写; fsync 强制落盘, Q43)
```

本机 `NativeMemoryTracking`（`-Xmx256m`，一个会分配垃圾的 JVM）：

```
Total: reserved=1819114KB, committed=419594KB
  Java Heap (reserved=270336KB, committed=225280KB)
  Thread    (reserved=68072KB,  committed=68072KB)
  GC        (reserved=59334KB,  committed=58630KB)      <- G1 的记忆集/标记位图等
  Code      (reserved=247815KB, committed=7831KB)
  Shared class space (reserved=16384KB, committed=12880KB)
  Metaspace (reserved=65549KB, committed=3405KB)
$ ps -o rss= -p PID   ->  321808 KB
```

读法：堆最大 256 MB，进程驻留内存 **约 314 MB**，其中约 58 MB 是 GC 自己的簿记，约 68 MB 是线程相关，还有类空间/代码缓存等。排查工具：`-XX:NativeMemoryTracking=summary` + `jcmd <pid> VM.native_memory summary`；Linux 上看 `/proc/<pid>/smaps`、`pmap`。

* **缺页与低延迟**：堆里新页首次触碰要内核清零 → 运行中偶发延迟。`-XX:+AlwaysPreTouch` 把这个代价挪到启动期（本机默认 `false`）。
* **透明大页（THP）**：减少 TLB 未命中，但内核做页合并时可能造成停顿；是否开启要实测（推断，常见经验）。
* **swap**：延迟敏感系统一般关掉或锁内存（`mlock`），页被换出一次就是毫秒级停顿。
* **OOM killer**：容器里 RSS 超过 cgroup 限制会被内核杀（不是 `OutOfMemoryError`）；所以 `-Xmx` 要小于容器限制并留出堆外/线程空间。
* **page cache 对 Java 的意义**：读刚写过的文件很快（Q43：本机 31 MB 重读 11 ms）；mmap 直接把 page cache 映射进进程（Q44）。

**能说出口的 60 秒版本**

> "Each process has a virtual address space that the MMU maps to physical pages through page tables, with the TLB caching translations. Touching an unmapped page triggers a page fault and the kernel supplies a zeroed page or reads the file in. File I/O goes through the page cache, so writes are buffered until writeback or an fsync. A JVM's resident memory is more than `-Xmx` because it also holds metaspace, the code cache, thread stacks, GC bookkeeping, direct buffers and shared libraries - on a test JVM with a 256 MB heap I saw about 314 MB resident, with roughly 58 MB of that being GC structures, according to native memory tracking. For latency, I'd pre-touch the heap so page faults happen at start-up, and avoid swap."

**面试官可能的下一问**

* "Container is OOM-killed but the heap was fine. Why?"（RSS 含堆外/线程/元空间；NMT 排查。）
* "What is a TLB miss?"（页表项不在 TLB 缓存里，要走页表遍历；大页减少 miss。）

**Demo / 课文**：`demos/run_tools.sh`（NMT + RSS）；`S00/os_processes_threads_ipc.md`。

---

### Q36 · A Java service is slow in production. Walk me through how you would investigate with `top`, `vmstat`, `perf` and `strace`.

- **难度**：★★★
- **来源**：`推断：JD`。JD 原话：「Address performance limitations within our own software, open-source libraries and applications, Linux, etc.」「Develop and improve monitoring and proactive detection capabilities」「Plus: Linux」（O-C2）。**没有任何面经报告过这类题**，这是 Java 基础设施岗最可能的 JD 派生问法。
- **一句话答案**：先看全局再下钻（USE 方法：对每种资源看 利用率、饱和度、错误）：`top`/`vmstat`/`iostat`/`ss` 判断是 CPU、内存、磁盘还是网络的问题 → `top -H`/`pidstat -t` 找热线程 → `perf`（或 JFR）看热点函数 → `strace -c`/`-T` 看系统调用 → 回到代码/配置。

**展开**

```
 症状: 延迟高 / 吞吐低
  |
  v  1. 机器层面     top          负载(load avg)、%us %sy %wa %st、哪个进程占 CPU
                    vmstat 1     r(可运行队列) b(阻塞) si/so(换页) bi/bo(块I/O) in(中断) cs(上下文切换) us/sy/id/wa/st
                    iostat -x 1  磁盘 util、await(平均等待)、队列长度
                    ss -s / ss -ti  连接数、重传、rtt、拥塞窗口
  |
  v  2. 进程/线程    top -H -p PID   哪个线程忙 (nid 是十六进制线程号 -> 对照 jstack 的 nid)
  |
  v  3. 热点        perf top -p PID / perf record -g -p PID -- sleep 30; perf report   (CPU 采样)
                    perf stat -p PID -- sleep 10    (IPC、cache-misses、branch-misses、context-switches)
  |
  v  4. 系统调用    strace -c -f -p PID   (按系统调用汇总次数/耗时);  strace -T -e trace=network,write -p PID
  |
  v  5. 回到 JVM    jcmd PID Thread.print / JFR / GC 日志 (Q37)
```

**怎么读 `vmstat 1`**（示意输出，**手写，未实跑**）：

```
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
12  0      0 812000  90000 6100000    0    0     4    20 9000 52000 71 25  4  0  0
```

读法示例：`r=12` 远大于核数 → CPU 饱和（可运行队列长）；`sy=25%` 偏高且 `cs=52000` → 系统态和上下文切换多，怀疑锁竞争/过多线程/频繁系统调用；`wa` 高 → 等磁盘；`si/so` 非 0 → 在换页，延迟灾难；`st` 高 → 虚拟机被宿主机抢占。

**perf 要点**：

* `perf stat` 看 IPC（每周期指令数）：低 IPC（< 1）通常是等内存（缓存未命中）；`cache-misses`、`branch-misses`。
* `perf record -g` 采样调用栈，`perf report`/火焰图。**Java 的陷阱**：JIT 生成的代码在 perf 眼里没有符号。方案：`-XX:+PreserveFramePointer`（保留帧指针；本机 `PrintFlagsFinal` 里有这个选项）+ 用 perf-map-agent 或 async-profiler 生成符号；JDK 17+ 有 `jcmd <pid> Compiler.perfmap`，**但它是 Linux 专属，本机 `jcmd help` 没有这个命令，未验证**。
* `perf c2c`：找伪共享（Q17）；`perf sched`：看调度延迟；`perf trace`：类似 strace 但开销低。

**strace 要点**：`strace -c -f -p PID`（`-f` 跟随线程）汇总各系统调用的次数与时间；`-T` 显示每个调用耗时；`-e trace=network`/`file`。注意：**strace 本身用 ptrace，会把目标进程拖慢一个数量级**，生产上谨慎，优先 `perf trace`/eBPF。典型发现：`futex` 占比大 → 锁竞争；`write` 小而多 → 缺批量/Nagle（Q40）；`fsync` 慢 → 存储（Q43）；`epoll_wait` 占比高但 CPU 低 → 其实在等 I/O。

**能说出口的 60 秒版本**

> "I'd go top-down using the USE method. First the machine: `top` for CPU split and load, `vmstat 1` to read the run queue, context switches, swap and I/O wait, `iostat -x` for disk and `ss -ti` for network retransmits. If it's CPU, `top -H` gives me the hot thread, and I map its hex id to the `jstack` nid. Then `perf stat` to see IPC and cache misses - low IPC means memory stalls - and `perf record -g` for a flame graph; for Java I need frame pointers or async-profiler to get JIT symbols. Then `strace -c -f` to see where syscalls go - a lot of `futex` means lock contention - remembering strace is intrusive, so in production I'd prefer `perf trace` or eBPF. Finally back into the JVM with JFR, GC logs and thread dumps."

**面试官可能的下一问**

* "`load average` is high but CPU is idle. What's going on?"（Linux 负载包含不可中断睡眠（D 状态，常是磁盘/NFS 等待）；看 `vmstat` 的 `b`、`wa`。）
* "How do you map a hot thread from `top -H` to Java code?"（线程号转十六进制 = jstack 里的 `nid=0x…`。）

**Demo / 课文**：`S00/os_processes_threads_ipc.md`。本机可跑的对应物见 Q37。

---

### Q37 · How do you profile and diagnose a JVM: JFR, `jcmd`, thread dumps, heap histograms? Show me what you would look at.

- **难度**：★★
- **来源**：`推断：JD`（「Develop and improve monitoring and proactive detection capabilities」，O-C2）；Java 低延迟岗经典。
- **一句话答案**：JDK 自带的就够用：`jcmd <pid> Thread.print`（线程栈与锁）、`jstat -gcutil`（GC 概况）、`jcmd GC.class_histogram`（谁占堆）、`jcmd VM.native_memory`（堆外）、**JFR**（低开销事件录制，含 CPU 采样、分配、锁、GC）。本机都跑过。

**展开**

被诊断对象 `K20Busy`：一个 CPU 热线程 `cpu-hog`（递归 fib）、一个持续分配的线程 `alloc-churn`、一个持锁睡眠的线程 `holds-lock` 和一个等它的线程 `waits-for-lock`。

* **线程转储**（`jcmd <pid> Thread.print`，节选实测）：

```
"waits-for-lock" #23 ... waiting for monitor entry
   java.lang.Thread.State: BLOCKED (on object monitor)
	at K20Busy.lambda$main$3(K20Busy.java:13)
	- waiting to lock <0x00000001238020d0> (a java.lang.Object)
"holds-lock" #22 ... TIMED_WAITING (sleeping)
	at java.lang.Thread.sleep(...)
	- locked <0x00000001238020d0> (a java.lang.Object)      <- 同一个地址: 谁持锁、谁在等一目了然
```

  死锁时 `Thread.print` 末尾会直接报告 deadlock。
* **GC 概况**：`jstat -gcutil <pid> 500`（Q22 的表）。**堆里是什么**：`jcmd <pid> GC.class_histogram`（实例数 + 字节数，Q13）。**堆外**：Q35 的 NMT。
* **JFR**：`java -XX:StartFlightRecording=duration=6s,filename=k20.jfr,settings=profile …`（或运行中 `jcmd <pid> JFR.start`），然后 `jfr view hot-methods k20.jfr`（实测，JDK 21 的 `jfr view`）：

```
Method                                Samples Percent
K20Busy.fib(int)                           30  78.95%
java.util.Random.nextInt(int)               7  18.42%
K20Busy.lambda$main$1()                     1   2.63%
```

  它正确地指出 CPU 热点是 `fib`（热线程）和 `Random.nextInt`（分配线程）。JFR 的开销低到可以在生产常开（官方定位；本机没量开销）。其它 `jfr view` 视图：`gc`、`allocation-by-site`、`contention-by-site`（视图名凭记忆，未逐个试）。
* **第三方**：async-profiler（基于 `perf_events` + `AsyncGetCallTrace`，不受 safepoint 偏差影响）；VisualVM 等。
* **线程转储本身会进 safepoint**（Q24），密集抓取会引入停顿。

**能说出口的 60 秒版本**

> "For a live JVM I start with `jcmd Thread.print` - it shows thread states and which monitor each thread holds or waits for, so contention and deadlocks are visible immediately. `jstat -gcutil` shows GC frequency and time, and `GC.class_histogram` shows what's filling the heap. For CPU I use Java Flight Recorder: start it with a flag or `jcmd JFR.start`, then `jfr view hot-methods` - on a test JVM it identified the recursive function at 79% of samples. For native memory, native memory tracking with `VM.native_memory`. JFR is low overhead enough to leave on in production, and async-profiler is the usual choice when I need accurate native and JIT frames."

**面试官可能的下一问**

* "Why can sampling profilers be biased in Java?"（safepoint bias：只在 safepoint 处采样会偏；JFR 和 async-profiler 不依赖 safepoint 采样。）
* "How would you find an allocation hotspot?"（JFR allocation 事件 / `allocation-by-site`；或 `getThreadAllocatedBytes` 差值。）

**Demo / 课文**：`demos/K20Busy.java`、`demos/run_tools.sh`、`demos/OUTPUTS.txt`；`S10/J19_runtime_zgc_jit.md`（JFR 简介）。

---

## [H] 进程间通信（kq03）

### Q38 · What are the ways processes can communicate on one machine? Compare pipes, sockets, shared memory, message queues, files.

- **难度**：★★
- **来源**：`推断：Java 对应`。C++ 原题（1p3a 974931，F-A16，2023-03）：「IPC methods」→ https://www.1point3acres.com/interview/thread/974931 ；1p3a 938472（F-A18，2022-10）：「interprocess communication topics」→ https://www.1point3acres.com/interview/thread/938472 ；1p3a 1011799（F-A13）：「shared memory」。
- **一句话答案**：管道（单向字节流）、Unix 域/TCP 套接字（双向、可跨机器）、**共享内存**（最快：零拷贝，但要自己同步）、消息队列、信号（通知）、文件。取舍：越靠近共享内存延迟越低、越需要自己处理同步与崩溃恢复；越靠近套接字越通用、越慢。

**展开**

| 机制 | 数据路径 | 同步 | 备注 |
|---|---|---|---|
| 管道 / FIFO | 进程 → 内核缓冲 → 进程（2 次拷贝） | 内核阻塞读写 | 单向；父子进程最简单；Java：`ProcessBuilder` 的 stdin/stdout |
| 套接字（Unix 域 / TCP loopback） | 同上 + 协议栈开销（TCP） | 内核 | 双向，可换成跨机器；Java 16+ 支持 Unix 域套接字（JEP 380） |
| 共享内存（mmap / `shm_open`） | **同一物理页被映射进两个进程**，无拷贝 | **自己做**（原子变量/自旋/futex） | 最快；崩溃一方会留下半写状态 |
| 消息队列（POSIX/SysV） | 内核队列 | 内核 | 有消息边界；Java 无标准 API |
| 信号 | — | — | 只有通知，信息量极小 |
| 文件 | 磁盘/page cache | 文件锁 | 慢、持久 |

**本机实测**（`K16Ipc`：两个 JVM 进程，各做 5 万次往返 ping-pong，1 字节/1 个 long；macOS arm64）：

```
pipe (stdin/stdout)                    3.08 us per round trip
loopback TCP (NODELAY)                12.32 us per round trip
shared mmap, spin on volatile seq      0.15 us per round trip
```

共享内存比套接字快约两个数量级（0.15 µs vs 12 µs），因为不进内核、不拷贝，代价是**忙等占满一个核**（上面的 spin）。macOS 上管道比 loopback TCP 快（协议栈开销）；Linux 上相对顺序通常类似，具体数字会不同（未测）。

选型直觉：控制面/低频 → 套接字（或 gRPC）；同机高频、延迟敏感 → 共享内存环形缓冲（Q39）；父子进程简单管道 → `ProcessBuilder`。

**能说出口的 60 秒版本**

> "The main options are pipes, sockets including Unix domain sockets, shared memory, message queues, signals and files. Pipes and sockets go through the kernel and copy data twice; shared memory maps the same physical pages into both processes, so there's no copy and no syscall on the fast path, but you have to do your own synchronisation and handle a peer crashing mid-write. I measured round trips between two JVMs on my laptop: about 3 microseconds through a pipe, 12 through loopback TCP, and 0.15 through a memory-mapped file with spinning on a volatile sequence number. So I'd use sockets for generality and control traffic and shared-memory ring buffers when two processes on the same host need microsecond latency."

**面试官可能的下一问**

* "How do you synchronise two processes on shared memory?"（Q39：原子序号 + 单生产者单消费者环形缓冲，release/acquire 语义。）
* "What are the downsides of busy-spinning?"（占满一个核、耗电、超线程兄弟受影响；可 `Thread.onSpinWait()`，或退避后 park。）

**Demo / 课文**：`demos/K16Ipc.java`；`S00/os_processes_threads_ipc.md`；`S00/examples/IpcDemo.java`（SPSC 环形缓冲，两个 JVM 进程通过映射文件共享，已存在）。

---

### Q39 · How would you implement shared memory IPC in Java? How do you get correct visibility across processes?

- **难度**：★★★
- **来源**：`推断：Java 对应`。C++ 原题族（F-A13「shared memory」、F-A16/F-A18「IPC」）；1p3a 1011799 摘要中的 `language features, shared memory, system design`。
- **一句话答案**：用 `FileChannel.map` 把同一个文件（Linux 上放 `/dev/shm`）映射进两个 JVM，得到 `MappedByteBuffer`；用 `VarHandle`（`MethodHandles.byteBufferViewVarHandle`）对映射内存做 `getVolatile/setVolatile`（或 acquire/release），设计成**单生产者单消费者环形缓冲**：各自只写自己的序号，先写数据后发布序号。

**展开**

```
  mapped file:  [ head(8B) | pad..(64B 对齐, 防伪共享) | tail(8B) | pad.. | ring data ... ]
  生产者: 写数据到 slot[tail % N]  --然后-->  setRelease(tail, tail+1)        (发布)
  消费者: 读 getAcquire(tail) > head  -->  读 slot[head % N]  -->  setRelease(head, head+1)
```

本机 `K16Ipc` 里的 mmap 往返只有一个字：父写序号 `i` 到偏移 0，子看到后把 `i` 回写到偏移 64，父自旋读偏移 64。关键代码：

```java
static final VarHandle LONGS = MethodHandles.byteBufferViewVarHandle(long[].class, ByteOrder.nativeOrder());
LONGS.setVolatile(mb, 0, i);                       // 发布
while ((long) LONGS.getVolatile(mb, 64) != i) Thread.onSpinWait();   // 等回应
```

结果 0.15 µs/往返（Q38）。要点：

* **偏移 0 和 64 分在不同缓存行**（Q17 伪共享）。
* **可见性**：两个进程里的 JMM 并不互相知道；但 `VarHandle` 的 volatile/acquire/release 访问会生成相应的内存屏障/指令，在同一台机器的同一页上跨进程同样有效（硬件缓存一致性）。普通的 `ByteBuffer.putLong` **没有**这个保证（可能被编译器缓存/重排）。
* **崩溃一致性**：对方在写一半时崩溃 → 用序号 + 校验和，消费者能发现半写记录；重启时从 head/tail 恢复。
* **对齐与字节序**：用 `ByteOrder.nativeOrder()`；定长记录（`StructLayout`，Q16）避免序列化。
* **生命周期**：`MappedByteBuffer` 没有显式 unmap（Q44）；删除文件后映射仍有效直到最后一个映射消失。
* 生产上多用现成库（Chronicle Queue、Aeron IPC，第三方，本机未用）而不是手写。
* 21 里 FFM（`MemorySegment`、`Arena`）可替代 `MappedByteBuffer`，用 `long` 下标突破 2 GB 限制（`FileChannel.map(mode, offset, size, arena)` 在 21 预览里存在，我没有在本机跑这一项）。

**能说出口的 60 秒版本**

> "I'd map one file into both JVMs - on Linux in `/dev/shm` so it's pure memory - and build a single-producer single-consumer ring buffer on it. Each side owns one sequence number: the producer writes the slot, then publishes the new tail with release semantics; the consumer reads the tail with acquire semantics, processes the slot, then publishes the head. For the atomic accesses on mapped memory I use a `VarHandle` from `byteBufferViewVarHandle`, because plain `putLong` has no visibility guarantee. Head and tail go on separate cache lines to avoid false sharing. I tried the simplest version, a ping-pong between two JVMs, and got about 0.15 microseconds per round trip. For production I'd consider Aeron or Chronicle Queue, and I'd add checksums so a crashed writer doesn't leave a half-written record visible."

**面试官可能的下一问**

* "What if the consumer is slower than the producer?"（环满：生产者等待/丢弃/背压；序号差即队列深度。）
* "Why not use `synchronized`/locks across processes?"（JVM 内的锁只在本进程内有效；跨进程要用文件锁或基于共享内存的原子协议。）

**Demo / 课文**：`demos/K16Ipc.java`；`S00/examples/IpcDemo.java`；`S10/J17_ffm_api.md`；`S10/J16_concurrency_primitives.md`（`VarHandle`）。

---

## [I] 网络

### Q40 · Explain TCP basics relevant to latency: handshake, Nagle's algorithm, delayed ACK, `TCP_NODELAY`.

- **难度**：★★
- **来源**：`推断：JD`。「Good knowledge of networking and storage systems」「Improve networking communication between different components of the system to achieve optimal latency and throughput」（O-C2）；C++ 岗 JD 额外有「low-level networking protocols」（O-C3）。kq01 的 Java 对应列表含「NIO 与 TCP」。
- **一句话答案**：TCP 是可靠的字节流（三次握手建连、序号+确认、重传、拥塞控制）。**Nagle** 为减少小包，会把小写入攒着等前一个包的 ACK；**延迟 ACK** 让接收方等一会儿再确认；两者叠加会让「写-写-读」模式卡几十毫秒。低延迟程序设置 `TCP_NODELAY` 并把一条消息合成一次写入。

**展开**

```
 握手:  C --SYN--> S ; C <--SYN+ACK-- S ; C --ACK--> S       (1 RTT 后才能发数据; 连接复用/长连接避免这个成本)
 Nagle:   有未确认数据时, 小于 MSS 的新数据先缓存, 等 ACK 或凑满再发
 延迟ACK: 接收方收到数据不立刻 ACK, 等最多 ~40ms (Linux 常见) 看有没有数据可以捎带
 叠加:    发送方 write(header 4B); write(body 4B)   -> 第二个小包被 Nagle 扣住等 header 的 ACK
          接收方等第二块数据才处理/回包 -> 不回数据 -> 延迟 ACK 等到超时才确认 -> 约 40ms 的卡顿
```

Java：`socket.setTcpNoDelay(true)` / NIO `StandardSocketOptions.TCP_NODELAY`。**更好的做法是一次 `write` 发完整条消息**（或 `gather write`），不依赖关掉 Nagle。

**本机实验**（`K17Nagle`：NIO Selector 服务端 + 阻塞客户端，客户端把 8 字节请求拆成两次 4 字节写，等 1 字节回应）：

```
TCP_NODELAY=true  two small writes then wait:      17.0 us per request (n=20000)
TCP_NODELAY=false two small writes then wait:      21.0 us per request (n=200)
```

**没有复现经典的 40 ms 卡顿**：macOS 的 loopback 与 Linux 的延迟 ACK/Nagle 实现不同，这个 demo 在 macOS 上两种设置只差 20% 左右。所以 40 ms 的数字是来自一般知识（Linux 上常见），**没有被本机验证**；面试时可以讲机制，不要说"我测过 40 ms"。

其它要点：拥塞控制（慢启动、拥塞窗口）影响新连接的吞吐；`SO_RCVBUF/SO_SNDBUF` 缓冲大小；`SO_REUSEADDR`；`TIME_WAIT`；重传（RTO）造成的尾延迟尖刺；`ss -ti` 看 rtt、cwnd、retrans（Q36）。

**能说出口的 60 秒版本**

> "TCP gives a reliable ordered byte stream: a three-way handshake, sequence numbers and acknowledgements, retransmission, and congestion control. For latency, the classic trap is Nagle's algorithm interacting with delayed ACKs: if you write a header and a body as two small writes, Nagle holds the second until the first is acknowledged, while the receiver delays that ACK waiting to piggyback - on Linux that can add tens of milliseconds. The fix is to send each message in one write and set `TCP_NODELAY`. In Java it's `setTcpNoDelay(true)`. I tried a two-write pattern on my Mac and didn't reproduce the stall - loopback behaves differently - so I'd confirm on the target Linux with `ss -ti` and a packet capture."

**面试官可能的下一问**

* "Why are long-lived connections better for trading systems?"（避免握手 RTT、慢启动；预热拥塞窗口。）
* "TCP vs UDP for market data?"（行情常用 UDP 多播：无连接、无重传延迟，丢包由序号检测并另路补发；订单用 TCP。）

**Demo / 课文**：`demos/K17Nagle.java`；`S00/networking_basics.md`（Nagle、`TCP_NODELAY`、组播、内核旁路）。

---

### Q41 · Blocking I/O vs NIO vs epoll vs Netty vs virtual threads: how do you serve many connections? What does `read()` do inside the kernel?

- **难度**：★★★
- **来源**：`推断：Java 对应`；CATALOG kq01「NIO 与 TCP」；Glassdoor G2「OS concepts, concurrency」（F-G2）。
- **一句话答案**：三种模型——(1) 每连接一线程 + 阻塞 I/O（简单，线程数受限）；(2) **反应器（reactor）**：少量线程用 `Selector`（Linux 下是 `epoll`）监听就绪事件，非阻塞读写（Netty 的模型）；(3) 虚拟线程：写回阻塞风格的代码，JVM 在底层用非阻塞 I/O 调度。`select/poll` 每次要扫描所有 fd（O(n)），`epoll` 只返回就绪的（O(就绪数)）。

**展开**

```
 阻塞 read(fd):  线程进内核 -> 数据没到 -> 线程睡眠(让出 CPU) -> 数据到达中断 -> 内核拷贝到用户 buffer -> 线程被唤醒
 epoll:          epoll_ctl 注册 fd 集合; epoll_wait 睡到有 fd 就绪, 返回就绪列表 -> 对每个就绪 fd 做非阻塞 read
 Java NIO:       Selector.select() ≈ epoll_wait (Linux) / kqueue (macOS);  SocketChannel 非阻塞
```

`K17Nagle` 的服务端是一个**单线程 Selector 事件循环**：accept、read、write 都在一个线程里，处理了 2 万次请求（约 17 µs 每次，含客户端和服务端两端的 loopback 往返）。核心结构：

```java
sel.select();                                  // 睡到有事件
for each ready key: acceptable -> accept + register(OP_READ)
                    readable   -> channel.read(buf) -> 处理 -> channel.write(...)
```

* **反应器的优点**：连接数多时线程少、没有线程切换（Q34）、可以绑核；**缺点**：回调式/状态机代码复杂，任何一处阻塞（慢处理、GC、日志）会卡住该线程上的所有连接。
* **直接缓冲区**：`ByteBuffer.allocateDirect` 让内核直接读写，少一次堆内拷贝（Q16）。
* **虚拟线程**（Q31）：写阻塞风格的 `socket.getInputStream().read()`，JDK 在底层把它转成非阻塞 + poller，所以吞吐接近反应器，代码像线程模型；热路径延迟仍不如手写反应器 + 绑核（推断）。
* `io_uring`（Linux 的新异步 I/O 接口）：JDK 21 没有官方支持，了解名字即可。
* 常见追问：`C10K` 问题的答案就是 epoll + 非阻塞。

**能说出口的 60 秒版本**

> "There are three models. Thread-per-connection with blocking I/O is simplest but limited by thread count and context-switch cost. The reactor model uses a few threads, each running a selector loop - in Java `Selector`, backed by epoll on Linux - that waits until sockets are ready and then does non-blocking reads and writes; Netty is built on that. `epoll` beats `select` and `poll` because it returns only ready descriptors instead of scanning all of them. With Java 21 virtual threads I can write the simple blocking style again and the JDK multiplexes underneath. For the very lowest latency I'd still use a hand-written single-threaded event loop pinned to a core with direct buffers, because nothing in it can block or be descheduled by anything else."

**面试官可能的下一问**

* "What happens if a handler in the event loop blocks?"（该线程上所有连接停顿；耗时工作丢给另一个线程池。）
* "What's the difference between level-triggered and edge-triggered epoll?"（水平：只要可读就持续通知；边缘：只在状态变化时通知一次，必须读到 EAGAIN。Java `Selector` 用水平触发。此条凭记忆。）

**Demo / 课文**：`demos/K17Nagle.java`；`S10/J10_virtual_threads.md`；`S00/networking_basics.md`（NIO `Selector`、虚拟线程 vs NIO）。

---

### Q42 · How would you reduce network latency between two components of a trading or research system?

- **难度**：★★★
- **来源**：`推断：JD`。「Improve networking communication between different components of the system to achieve optimal latency and throughput」（O-C2）；博客 #5 讲实盘链路 market data parser → strategy → order gateway 与延迟量级（O-B2）。
- **一句话答案**：先量：每一跳的延迟分布（p50/p99/p999，不是平均）。再减：少拷贝少序列化（二进制定长协议，不用 Java 序列化/JSON）、一次 `write` 一条消息 + `TCP_NODELAY`、长连接、专用线程绑核忙轮询、缓冲区合理、避免 GC 与锁、必要时 UDP 多播/内核旁路。

**展开**

延迟预算（**量级，一般认识，非本机测量**）：

```
 同机 共享内存 ~0.1–1 us  |  同机 loopback TCP ~10 us (本机 12 us)  |  同机房 网络一跳 ~10–100 us  |  跨城市 ~ms
```

可操作的清单（按收益大致排序，具体要测）：

1. **协议与序列化**：定长二进制（`ByteBuffer`/`MemorySegment` + 定义好的偏移，Q16），读字段不解析；避免 `ObjectOutputStream`（慢、占内存、有安全问题）与每条消息分配对象。
2. **写合并**：一条消息一次 `write`；多条消息批处理 vs 延迟的权衡；`TCP_NODELAY`（Q40）。
3. **线程模型**：专用网络线程，忙轮询（busy-poll）而不是睡眠唤醒（唤醒要几微秒到几十微秒）；绑核、隔离核（Q34）；GC 不能抢它（Q23）。
4. **内核层**：增大/调小 socket 缓冲区；中断亲和性（IRQ affinity）；`SO_BUSY_POLL`；关闭节能状态（C-states）——**这些是 Linux 调优常识，未在本机验证**。
5. **内核旁路**（Solarflare Onload、DPDK 等）：用户态直接收发包，绕过内核协议栈；Java 里没有原生一等支持，通常通过 JNI/FFM 或厂商库，这是 C++ 更占优的领域（Q03）。
6. **UDP 多播**：交易所行情常见；无重传所以序号检测丢包、另路补发。
7. **度量**：硬件时间戳、`ss -ti`、抓包；应用内用单调时钟（`System.nanoTime`）测每跳，分位数而非平均。

**能说出口的 60 秒版本**

> "First I'd measure per-hop latency as percentiles so I know where the time goes. Then, in order of payoff: a compact fixed-layout binary protocol with no per-message allocation or Java serialization; one write per message with `TCP_NODELAY` over a long-lived connection; a dedicated networking thread that busy-polls instead of sleeping, pinned to an isolated core, with the GC and other threads kept off it; sensible socket buffers; and where it matters, UDP multicast for fan-out and kernel-bypass stacks. That last part is where I'd expect to hand over to C++ or vendor libraries, since Java's tooling there is thinner. And I'd re-measure after every change rather than trust folklore."

**面试官可能的下一问**

* "Why measure percentiles instead of averages?"（尾延迟决定交易结果；平均会掩盖尖刺。）
* "Why is `System.nanoTime` preferred to `currentTimeMillis` for intervals?"（单调、高分辨率；后者会随系统时钟调整。）

**Demo / 课文**：`demos/K16Ipc.java`、`demos/K17Nagle.java`；`S00/networking_basics.md`（延迟 vs 吞吐、组播、内核旁路）。

---

## [J] 存储

### Q43 · What happens when you `write()` to a file? What are the page cache and `fsync`? How do you make writes durable and fast?

- **难度**：★★
- **来源**：`推断：JD`。「Design, implement, and maintain distributed storage systems with various performance and reliability requirements」「Good knowledge of networking and storage systems」（O-C2）。
- **一句话答案**：`write()` 只是把数据拷进内核 **page cache** 就返回（很快，但还没落盘，断电会丢）；`fsync`/`FileChannel.force()` 才等待数据到达持久介质（慢，毫秒级）。做法：批量写 + **组提交（group commit）**：很多记录共享一次 fsync；顺序追加（WAL）而不是随机写。

**展开**

```
 应用 --write()--> page cache (内存, 标记 dirty) --(内核稍后回写)--> 磁盘/SSD
                     ^ 读也先查这里 (命中很快)
 force()/fsync: 等 dirty 页 + 元数据真正写到设备并确认  <- 这一步才耐久
```

本机 `K18Storage`（2000 条 4 KB 记录，`FileChannel.write`，`force(false)` 是只刷数据不刷元数据，对应 `fdatasync`）：

```
write only (page cache)                2000 recs x 4KB:      7 ms
write + force() after EVERY record     2000 recs x 4KB:   6286 ms     <- 每条约 3 ms
write all, one force() at end          2000 recs x 4KB:     30 ms
mmap store + force() at end            2000 recs x 4KB:     16 ms
re-read 31 MB just written: 11 ms (served from page cache)
os.name=Mac OS X
```

* 每条都 fsync 比只写 page cache **慢约 900 倍**；攒一批再 fsync 只比不 fsync 慢 4 倍 —— 这就是 **group commit**（数据库、Kafka 的刷盘策略）：用"几毫秒内的一批共享一次 fsync"换吞吐，延迟增加一点点。
* **macOS 注意**：这里每次 `force` 约 3 ms，说明确实在等设备（我记得 JDK 在 macOS 上用 `F_FULLFSYNC`，没核对源码）。Linux + NVMe（带断电保护）上单次 fsync 可以是几十到几百微秒，数字完全不同；**不要把这些毫秒数当成通用结论，只看比例。**
* **元数据**：新建文件后要 fsync 目录项才保证文件名也持久；追加写扩展文件大小是元数据（`force(true)` vs `force(false)`）。预分配文件（`fallocate`）避免每次扩展元数据。
* **绕过 page cache**：`O_DIRECT`（Java：`ExtendedOpenOption.DIRECT`，要求缓冲区和偏移对齐到块大小，本机未试）。数据库自己管缓存时用。
* **读路径**：刚写的数据重读来自 page cache（上面 11 ms）；冷读才碰设备。

**能说出口的 60 秒版本**

> "`write` copies into the kernel page cache and returns; the data is only durable after `fsync`, which in Java is `FileChannel.force`. That's why you can't confuse a fast write with a safe one. On my laptop 2,000 4-KB appends took 7 ms without syncing, about 6 seconds when I forced after every record - roughly three milliseconds each - and 30 ms when I forced once at the end. That gap is why storage systems use group commit: many records share one fsync, so you keep durability but amortise the cost, trading a little latency. The usual design is an append-only write-ahead log, sequential I/O, preallocated files, and only acknowledging after the sync. The absolute numbers depend on the device and OS - Linux with a power-loss-protected NVMe is much faster - but the ratios hold."

**面试官可能的下一问**

* "`fsync` vs `fdatasync`?"（后者不强制刷非必要的元数据，更快；Java `force(false)`。）
* "What if the process crashes but the OS doesn't?"（page cache 里的数据不丢；只有 OS/断电才丢未 fsync 的数据。）

**Demo / 课文**：`demos/K18Storage.java`。

---

### Q44 · `mmap` vs `read/write` for files: when would you use a `MappedByteBuffer`, and what are its pitfalls?

- **难度**：★★★
- **来源**：`推断：JD`（storage systems）；`推断：Java 对应` 于 kq03/kq06 的 mmap / 共享内存话题（Q39）。
- **一句话答案**：`mmap` 把文件的 page cache 页直接映射进进程地址空间，访问像读内存（缺页时才读盘），省去 `read` 的一次内核到用户拷贝，适合大文件的随机访问和多进程共享；坑：缺页延迟不可预期、Java 里无法确定性 unmap、大小/下标限制、I/O 错误变成 `InternalError`/崩溃。

**展开**

```
 read():  磁盘 -> page cache -> (拷贝) -> 你的 buffer          每次一次系统调用 + 一次拷贝
 mmap:    磁盘 -> page cache <==映射==> 你的指针               访问时若页不在内存 -> 缺页 -> 内核读入; 之后就是内存访问
```

本机 `K18Storage` 的 mmap 行：2000 条记录写入映射区再 `force()`，16 ms，与"批量写 + 一次 force"（30 ms）同一量级 —— 因为写的都是 page cache。要点：

* **适合**：大文件随机读、索引/列式数据、多进程共享（Q39）、避免拷贝。
* **不适合/坑**：
  1. **缺页造成尾延迟**：首次访问冷页要读盘（毫秒），线程直接卡在一次"普通内存读"上，且 JVM 不知道（它也会拖 safepoint 到达时间，推断）。可 `MappedByteBuffer.load()` 预热、`mlock`（原生）。
  2. **无法显式 unmap**：`MappedByteBuffer` 的映射在对象被 GC 时才释放（21 的 FFM 预览带 `Arena` 的映射可以确定性关闭，我没在本机跑这一项）。
  3. **大小**：`ByteBuffer` 下标是 `int`，单个映射 ≤ 2 GB（要分段映射）；FFM `MemorySegment` 用 `long`（Q16 的 demo 用了 long 下标）。
  4. **I/O 错误**（磁盘满、文件被截断）发生在访问内存时，Java 里表现为 `InternalError`/JVM 崩溃，不是好处理的 `IOException`。
  5. 持久化语义同 Q43：`MappedByteBuffer.force()` ≈ `msync`。
* 与 `read/write` 比：顺序读大文件时 `read` + 预读也很好，mmap 不一定更快（推断，要测）。

**能说出口的 60 秒版本**

> "`mmap` maps the file's page-cache pages directly into the process, so reading is a memory access and there's no syscall or extra copy per read; a page that isn't resident faults in from disk. It's great for large random-access files and for sharing memory between processes. The pitfalls: a cold page makes a plain memory read block for milliseconds, which hurts tail latency; in Java the mapping can't be deterministically unmapped before Java 22's FFM, a single `ByteBuffer` mapping is capped at 2 GB, and I/O errors surface as `InternalError` rather than `IOException`. For durability you still need `force`, which is `msync`. For sequential streaming I'd happily use plain `FileChannel` reads."

**面试官可能的下一问**

* "Does mmap give you durability?"（不；只有 `force()`/msync 之后。）
* "How would you build an append-only log with mmap?"（预分配固定大小段文件 + 映射 + 原子推进写指针；写满切下一段。）

**Demo / 课文**：`demos/K18Storage.java`、`demos/K16Ipc.java`；`S10/J17_ffm_api.md`。

---

### Q45 · Distributed storage: replication, consistency and the trade-offs between LSM trees and B-trees. What would you think about when designing a storage layer for research data?

- **难度**：★★★
- **来源**：`推断：JD`。「Design, implement, and maintain distributed storage systems with various performance and reliability requirements」「Investigate new technologies to improve stability, scalability, and performance of a distributed computing farm」（O-C2）；quant 公司背景：回测 tick 数据「每天数百 GB」（博客 #5，O-B2）。**没有面经报告过这类题，纯 JD 推断。**
- **一句话答案**：先问需求（读写比、延迟 vs 吞吐、顺序 vs 随机、一致性、规模、故障容忍），再选：**B 树**读友好、原地更新、写放大随机；**LSM 树**写友好（顺序追加+后台合并），读放大和合并放大要管；跨机器用复制（同步/异步）或纠删码，用共识（Raft/Paxos）保证一致，权衡 CAP 与延迟。

**展开**

```
 B-tree:   页式结构, 读 O(log n) 次页访问; 更新 = 读页-改-写页 (随机写, 可能写放大); 范围查询好
 LSM-tree: 写 -> WAL + 内存表(memtable) -> 刷成不可变有序文件(SSTable) -> 后台合并(compaction)
           写: 顺序追加, 快;  读: 可能要查多个文件(靠 Bloom filter/索引缩小);  合并带来写放大 + 空间放大
```

| 维度 | B-tree | LSM-tree |
|---|---|---|
| 写 | 随机 I/O，延迟尖刺来自页分裂 | 顺序 I/O，吞吐高；合并时有后台负载 |
| 读 | 点查/范围好 | 点查靠 Bloom filter；范围要合并多路 |
| 写放大 | 页大小 vs 记录大小 | 合并反复重写数据 |
| 典型 | PostgreSQL、MySQL InnoDB | RocksDB、Cassandra、HBase |

分布式层面的问题清单：

* **复制**：同步复制（写要等多数副本确认，延迟高、强一致）vs 异步（快、可能丢最近写）；**共识**协议（Raft）保证多数派一致；写入延迟 ≈ 最慢多数派副本的 fsync + 网络（Q43、Q40）。
* **容错**：副本数 vs **纠删码**（省空间、重建成本高）；故障检测与重平衡；数据校验和防静默损坏。
* **研究数据特征**（推断，贴合 quant 研究平台）：一次写多次读、按时间/品种分区、列式压缩、批量扫描为主 —— 更像"不可变文件 + 元数据索引"（Parquet 类思路）而不是通用事务数据库；热数据放本地 NVMe/page cache，冷数据放对象存储。
* **运维**：监控（队列深度、compaction 积压、fsync 延迟分位）、容量规划（JD：「basic data analysis to … plan for future growth」）、基准测试时区分冷/热缓存。

**能说出口的 60 秒版本**

> "I'd start from the access pattern: read/write ratio, sequential versus random, latency targets, consistency and failure tolerance. A B-tree updates pages in place so reads and range scans are good but writes are random; an LSM tree turns writes into sequential appends to a log and memtable, flushes sorted immutable files and compacts in the background, so writes are cheap while reads and compaction cost more - Bloom filters help the reads. Across machines I'd decide between synchronous replication through a consensus protocol like Raft - strong consistency, write latency bounded by the slowest majority's fsync and network - and asynchronous replication that's faster but can lose the latest writes. For research data, which is mostly write-once, append-heavy and scanned in bulk, immutable partitioned files with a metadata index tends to fit better than a general transactional store. I'd also build the monitoring in from the start."

**面试官可能的下一问**

* "What's write amplification and how do you measure it?"（实际写入设备的字节 / 应用写入字节；`iostat`、设备 SMART、存储引擎统计。）
* "How would you checksum data end to end?"（写入时算校验和与数据同存，读时验证；跨层校验防静默损坏。）

**Demo / 课文**：`demos/K18Storage.java`（fsync 成本的实测）；`S00/ordered_maps_trees.md`。
