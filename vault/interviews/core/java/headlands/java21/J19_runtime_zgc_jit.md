# J19 · 运行时：Generational ZGC、JIT 分层编译、逃逸分析，以及怎么在低延迟面试里把它们讲清楚

> 版本：**Generational ZGC：JDK 21 正式，需 `-XX:+UseZGC -XX:+ZGenerational`**；JDK 23 起默认就是分代；JDK 24 起移除非分代模式。JFR 11 起开源可用。
> 这一课**不是 API**，是 JVM 如何运行你的代码；面试里常以口头题出现：「低延迟 Java 怎么调？」
> 可运行代码：`examples/J19/`（Apple Silicon，12 核，机器有负载）；延迟数字**只看量级和方向**。前置：J16 读过更好；GC 与 JIT 从零讲。

---

## 1. 先看痛点：为什么「低延迟」对 Java 特别难

交易系统关心的不是平均延迟，而是**尾部延迟**（tail latency，p99、p99.9、最大值）：绝大多数订单 50µs 处理完，但每一万个里有一个用了 100ms，就足以错过行情。Java 有两个"别的语言没有"的尾部延迟成因：

### 1.1 原因一：垃圾回收暂停

**从零讲：什么是 GC。** Java 里 `new` 对象从不手动释放。**垃圾回收器**（Garbage Collector，GC）定期找出"没人再引用"的对象回收内存：得**遍历**所有还活着的对象（标记，mark）；为避免碎片，还会把活对象**搬家**到连续区域（复制/整理，compact）。

**为什么要"暂停"。** 搬家时应用线程若同时读写这些对象，会读到搬了一半的东西。最简单的办法：**让所有应用线程停下**（stop-the-world，STW），GC 干完再放行。停顿时长与"要搬多少活对象"相关。

**分代假说**（generational hypothesis）：**绝大多数对象很快就死**（临时字符串、迭代器、请求对象），少数活得很久（缓存、订单簿）。所以把堆分成**年轻代**（young，新对象，常回收，便宜）和**老年代**（old，长寿对象，偶尔回收，贵）。

**G1**（Garbage-First，JDK 9 起默认）：把堆切成很多等大的**区域**（region，1–32 MB），每个区域逻辑上属年轻或老年。
* 年轻代回收：STW，多线程并行，把存活对象复制到新区域。
* 老年代：后台**并发标记**（不停应用），之后以"混合回收"（mixed）逐步回收收益最高的区域。
* 有**暂停目标** `-XX:MaxGCPauseMillis`（默认 **200 ms**），G1 调整每次回收多少区域尽量不超过——软目标，不是保证。
* 当分配得比回收得快（并发标记没跟上），G1 退化为 **Full GC**：整堆 STW，暂停可达数百毫秒到秒级。

**实验（`J19Ex5Jfr`，约 400 万个长寿对象 + 持续分配，2GB 堆，8 秒）：**

```
G1:        jdk.GCPhasePause 事件 277 个, 总暂停 1480.7 ms, 平均 5.345 ms, p99 75.045 ms, 最长 77.890 ms
Gen ZGC:   jdk.GCPhasePause 事件 2189 个, 总暂停 4.8 ms, 平均 0.002 ms, p99 0.006 ms, 最长 0.011 ms
```

G1 平均 5ms 但 p99 达 75 ms；ZGC 最长 0.011 ms（11 µs）。8 秒里 G1 共停了约 1.5 秒，ZGC 共停 4.8 ms。

### 1.2 原因二：JIT 预热与"去优化"

Java 程序**刚启动时是慢的**：字节码先由解释器逐条执行，比机器码慢 5–10 倍以上（3.3），等方法"热"了才被 JIT 编译。开盘第一笔订单撞上冷代码，延迟可能是稳态的几十倍。

### 1.3 Java 8 时代的"土办法"

在 ZGC 之前，低延迟 Java 的经验是**避开 GC**而不是调 GC：

* **预分配 + 对象池**：启动时建好所有要用的对象，运行时只复用；
* **堆外内存**（数据放在 GC 看不到的地方）；
* **基本类型数组代替对象集合**（避免装箱）；
* **小堆 + 频繁 Young GC**，或买商业 JVM（Azul Zing 的 C4 收集器）。

有效，但代码难写难维护。ZGC 的目标是让"普通写法"也有亚毫秒暂停。

---

## 2. 语法（其实是命令行）逐条讲

### 2.1 选择收集器（JDK 21）

| 参数 | 含义 |
|---|---|
| `-XX:+UseG1GC` | G1（JDK 21 默认） |
| `-XX:+UseZGC` | ZGC。**JDK 21 里默认是非分代的老版本！** |
| `-XX:+UseZGC -XX:+ZGenerational` | **Generational ZGC**（JDK 21 要两个都写；默认 `ZGenerational = false`） |
| `-XX:+UseParallelGC` | 吞吐优先，不适合低延迟 |
| `-XX:+UseEpsilonGC` | 不回收的"空"收集器，用于短命进程或基准测试 |
| `-Xms8g -Xmx8g` | 初始堆 = 最大堆，避免运行时扩缩容 |
| `-XX:+AlwaysPreTouch` | 启动时就触碰所有堆页面，避免运行时才缺页 |
| `-XX:SoftMaxHeapSize=...` | ZGC 的"软上限"，尽量不超过它，但需要时可超 |

**后续版本**：JDK 23 起 `-XX:+UseZGC` 默认就是分代，`-XX:-ZGenerational` 触发弃用警告；JDK 24 彻底移除非分代模式，`ZGenerational` 选项被废弃（设了只会警告）。

### 2.2 观察 GC：日志与 JFR

```
-Xlog:gc                     # 每次 GC 一行
-Xlog:gc*:file=gc.log        # 详细，写文件
-XX:StartFlightRecording:filename=rec.jfr,settings=profile      # 启动时开 JFR
jcmd <pid> JFR.start / JFR.dump ...                              # 运行中开/导出
jfr print --events jdk.GCPhasePause rec.jfr                      # 命令行读事件
```

**JFR**（Java Flight Recorder）是 JVM 内置的事件记录器，开销很低（量级约 1%），可在生产常开。记录 GC 暂停、JIT 编译、线程阻塞、锁竞争、分配热点、`jdk.VirtualThreadPinned` 等。

### 2.3 观察 JIT

```
-XX:+PrintCompilation                                    # 每个方法被编译时一行
-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining        # 内联决策（需要诊断选项）
-XX:TieredStopAtLevel=1                                  # 只用 C1
-Xint                                                    # 只解释执行，关闭 JIT（调试用）
-XX:-DoEscapeAnalysis                                    # 关掉逃逸分析（做对照实验用）
```

---

## 3. JVM 到底做了什么

### 3.1 ZGC：把"搬家"挪到后台，让应用线程自己发现并修正

**核心思想**：标记和**移动对象**都在**应用线程运行的同时**（并发）完成；STW 只剩极短的"根扫描"同步点，时长**与堆大小、存活对象数量无关**（目标：暂停"不应超过 1 毫秒"）。

怎么做到"搬家时应用还在读写"？两个机制（概念版）：

1. **着色指针**（colored pointers）：对象引用里挪出几位当"状态标记"（引用是否已检查过、指向的对象是否已被搬走）。这也是 ZGC 不用压缩指针（compressed oops）的原因之一，同样的对象图占内存略多。
2. **加载屏障**（load barrier）：**应用线程每从堆里读一个引用**，JIT 都在后面插一小段检查；若"颜色"表示对象已搬家，屏障就帮着找到新地址、修好这个引用（self-healing），应用线程继续往下走。

代价：
* 每次引用读取多一小段屏障 → **吞吐比 G1 略低**；
* 需要**额外堆空间**（headroom）：并发回收期间应用还在分配，新分配快过回收就发生 **allocation stall**（分配线程被迫等回收，成了新的延迟来源）；
* 并发工作占 CPU：GC 线程与应用线程抢核。

### 3.2 为什么要"分代"

非分代 ZGC 每一轮都标记**整个堆**（包括很久没变的长寿对象），尽管大多数垃圾是刚分配的短命对象。分代 ZGC 增加年轻代：

* 常回收年轻代（便宜，只处理最近分配的对象）；
* 老年代很少回收；
* 目标：**更低的分配停顿风险、更低的堆内存开销、更低的 GC CPU 开销**，不明显牺牲吞吐。（一项公开基准：Generational ZGC 用四分之一的堆、拿到四倍吞吐，暂停仍在 1 ms 内。）

**日志长什么样**（`-Xlog:gc`，`J19Ex5Jfr`）：

```
G1:
[0.035s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 119M->118M(2048M) 6.720ms
[2.110s][info][gc] GC(59) Pause Young (Normal) (G1 Evacuation Pause) 1942M->957M(2048M) 3.404ms

ZGC:
[0.002s][info][gc] Using The Z Garbage Collector
[0.195s][info][gc] GC(2) Minor Collection (Allocation Rate)
[0.238s][info][gc] GC(2) Minor Collection (Allocation Rate) 742M(36%)->1198M(58%) 0.043s
```

**读法的差别**：G1 那行最后的 `6.720ms` 是**应用被暂停的时间**；ZGC 那行最后的 `0.043s` 是**这一整轮并发回收的耗时**，应用期间一直在跑，真正的暂停另有记录（JFR 的 `jdk.GCPhasePause` 或 `-Xlog:gc+phases`）。面试别把两个数字混为一谈。

### 3.3 JIT：解释器 → C1 → C2 的分层编译

`javac` 把源码编译成**字节码**（bytecode，与机器无关的指令）。JVM 有两种办法运行它：
* **解释器**（interpreter）：逐条读字节码执行，启动快但慢。
* **JIT**（Just-In-Time）编译器：把"热"方法编译成 CPU 的**机器码**，编译花时间但之后快得多。

HotSpot 有**两个** JIT，配合使用，叫**分层编译**（tiered compilation）：

| 层级（`PrintCompilation` 里的数字） | 谁执行 | 特点 |
|---|---|---|
| 0 | 解释器 | 慢，同时收集**剖析数据**（哪个分支常走、虚方法调用实际是哪个类） |
| 1 | C1，无剖析 | 极简单的方法（getter 等）编译一次就完事 |
| 2、3 | C1，带剖析 | 3 是常规路径：编译快、代码比较快，**且继续收集剖析数据** |
| 4 | **C2** | 慢编译（占 CPU）、激进优化、代码最快 |

典型路径：**0（解释） → 3（C1+剖析） → 4（C2）**。默认阈值：`Tier3InvocationThreshold = 200`（调用 200 次进 C1）、`Tier4InvocationThreshold = 5000`（再调用 5000 次进 C2）；循环回边另有 `Tier3BackEdgeThreshold = 60000`、`Tier4BackEdgeThreshold = 40000`。触发逻辑比这复杂，面试说"几百次进 C1，几千次进 C2"即可。

**实验（`J19Ex1Jit`）**：同一方法 `work()` 每一轮的平均耗时：

```
round  1:       50 次调用, 平均   801.7 ns/次     <- 解释器
round  2:      100 次调用, 平均   726.7 ns/次
round  3:      200 次调用, 平均   212.7 ns/次     <- C1 编译好了
round  4:      400 次调用, 平均   173.5 ns/次
...
round  9:   12,800 次调用, 平均   147.2 ns/次
round 10:  400,000 次调用, 平均   125.8 ns/次     <- C2
round 14:  400,000 次调用, 平均   123.4 ns/次
```

稳态对照（同一段代码，三种模式）：

```
-Xint（只解释）          : 565 ns/次
-XX:TieredStopAtLevel=1（只 C1）: 140 ns/次
默认（C1 -> C2）         : 123 ns/次
```

第 1 轮比稳态慢约 **6.5 倍**。`-XX:+PrintCompilation` 看编译时间线：

```
17  122       3       J19Ex1Jit::work (58 bytes)
19  138       4       J19Ex1Jit::work (58 bytes)
19  122       3       J19Ex1Jit::work (58 bytes)   made not entrant
```

读法：第一列 = JVM 启动后毫秒；第二列 = 编译任务编号；第三列 = 编译标志（`%` 表示 OSR）；第四列 = **层级**；然后是方法与字节码大小。`work` 在 17ms 被 C1（层级 3）编译，2ms 后被 C2（层级 4）编译；C2 版本就绪后旧的 C1 版本被标为 `made not entrant`（不再被新调用进入）。`main @ 35` 带 `%` 是 **OSR**（On-Stack Replacement，栈上替换）：`main` 只调用一次但里面的循环非常热，JVM 在循环运行中途把解释执行"换"成编译版本。

### 3.4 JIT 最重要的几个优化

1. **内联**（inlining）：把被调方法的代码直接贴进调用处。去掉调用开销；更重要的是让后面的优化看到**更大的代码块**（逃逸分析、常量折叠、循环优化都靠它）。默认：热点方法体 ≤ 325 字节码（`FreqInlineSize`）才内联；非热点 ≤ 35（`MaxInlineSize`）（`J19Ex2Inline`，`-XX:+PrintInlining`）：

```
@ 13   J19Ex2Inline::add (7 bytes)   inline
  @ 2   J19Ex2Inline::square (4 bytes)   inline
@ 20   J19Ex2Inline::tooBig (492 bytes)   hot method too big
@ 20   J19Ex2Inline::tooBig (492 bytes)   callee is too large
```

   `add`、`square` 很小被内联；故意写成 492 字节的 `tooBig` 被拒绝（`hot method too big`）。**经验：热路径上的方法保持短小。**

2. **类型剖析与去虚化**：`list.get(i)` 看似虚调用，但运行时 99% 的调用点只见到 `ArrayList`——JIT 据剖析数据做**投机**（speculation）：直接内联 `ArrayList.get`，前面放一个"类型真是 ArrayList 吗"的检查。以后真来了别的类型，检查失败 → **uncommon trap** → **去优化**（deoptimization）：丢掉编译代码，退回解释器，重新收集数据再编译。这是 `made not entrant` 的另一个来源。

3. **逃逸分析**（escape analysis）+ **标量替换**：JIT 分析"`new` 出来的对象是否会被存到堆里、传给别的线程、从方法返回"。**不逃出方法**就根本不必在堆上分配——把字段拆成几个**局部变量**（寄存器），连对象头都不要。2000 万次循环、每次 `new Point(i, i+1)`（`J19Ex3Escape`）：

```
默认:                  不逃逸: 分配 5,504,992 字节 (0.3 字节/次)   逃逸: 分配 640,000,000 字节 (32.0 字节/次)
-XX:-DoEscapeAnalysis: 不逃逸: 分配 640,000,000 字节 (32.0 字节/次)  逃逸: 分配 640,000,000 字节 (32.0 字节/次)
```

   不逃逸的版本默认下 2000 万个对象**只分配了 5.5 MB（≈0）**；关掉逃逸分析后同样代码分配 640 MB（每个 Point 32 字节）；逃逸版本（存进静态字段）无论如何都要分配。
   **对低延迟的意义**：分配得少 → GC 触发得少 → 暂停得少。所以"写出让 JIT 看穿的代码"（小方法、不把临时对象存进字段、`record` + 局部使用）是 Java 低延迟的第一原则。逃逸分析**依赖内联**：对象一传进没被内联的方法，对 JIT 来说就逃逸了。

4. **循环优化与边界检查消除**：展开循环、把数组下标检查外提；对 `long` 计数循环尤其明显。

### 3.5 预热与去优化的实际后果

* **冷启动**：刚起来的前几千次请求在解释器 / C1 里跑，延迟是稳态的数倍；JIT 编译线程本身也占 CPU。
* **去优化尖刺**：流量模式变化（开盘后第一次走"撤单"路径），基于旧剖析数据的优化被推翻，该路径重新经历解释 → 编译。
* **对策**：
  1. **预热**（warm-up）：上线前用回放的真实/合成流量跑够次数，让关键路径完成 C2 编译，再接真实订单。
  2. 让热路径行为**稳定**：避免热点处出现"罕见分支突然被走到"、多态调用点（一个调用点出现 3 种以上类型就成真正的虚调用，无法内联）。
  3. 新方向：**AOT 缓存**（Project Leyden），JDK 24 起能把启动时类加载/链接的结果存进缓存缩短启动；对 JDK 21 面试只需知道"有这个方向"。

### 3.6 实验：GC 对尾部延迟的影响（`J19Ex4Hiccup`）

"hiccup meter"（jHiccup 的做法）：一个线程每 1ms 睡一次，记录**实际醒来比预期晚多少**；若 JVM 全局 STW，它必然晚醒。同时 4 个线程制造分配压力，另有约 600MB 长寿对象，2GB 堆（`J19Ex4Hiccup`）：

```
G1:       GC: G1 Young Generation(1845次) G1 Concurrent GC(146次) G1 Old Generation(15次)
          晚醒 p50=7.24 ms  p99=13.27 ms  p99.9=116.53 ms  max=132.02 ms
Gen ZGC:  GC: ZGC Minor Cycles(6295次) ZGC Minor Pauses(18902次) ZGC Major Cycles(52次) ZGC Major Pauses(246次)
          晚醒 p50=6.94 ms  p99=8.14 ms  p99.9=9.00 ms  max=11.83 ms
基线(G1, 无分配压力): 晚醒 p50=6.67 ms  p99=8.02 ms  p99.9=8.47 ms  max=13.50 ms
```

**怎么读**：
* p50 ≈ 7 ms 不是 GC，是 macOS 上 `Thread.sleep(1)` 本身的误差（无 GC 压力的基线也是 6.67ms）——**测量工具自己的噪声必须先测**。
* G1 的 **p99.9 = 116 ms、max = 132 ms** 远高于基线（8.5 / 13.5 ms）：是 G1 的 Full GC（`G1 Old Generation(15次)`）——分配快过并发回收，退化成整堆 STW。
* ZGC 的 max = 11.8 ms，与基线 13.5 ms 同量级——**GC 没有产生可测的尾部延迟**（`Pauses` 的 18902 次是极短的同步点，JFR 实测最长 0.011 ms）。

**局限**：2 GB 堆、4 个分配线程的合成负载；真实订单簿、不同存活集大小、更大的堆结果会不同；ZGC 的代价（吞吐、CPU、内存头部空间）没有测量。

---

## 4. 例子（由浅入深）

例子已分散在第 3 节；每个例子的"运行方式"和"要看什么"：

| 例子 | 运行 | 要看什么 |
|---|---|---|
| `J19Ex1Jit` 预热 | 加 `-XX:+PrintCompilation`；对照 `-Xint`、`-XX:TieredStopAtLevel=1` | 第 1 轮 801 ns → 稳态 123 ns；层级 3→4；`made not entrant`；`%` OSR |
| `J19Ex2Inline` 内联 | `-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining` | `inline` / `hot method too big` |
| `J19Ex3Escape` 逃逸分析 | 默认；再加 `-XX:-DoEscapeAnalysis` | 5.5 MB vs 640 MB |
| `J19Ex5Jfr` JFR 暂停统计 | `-Xmx2g -Xms2g -XX:+UseG1GC`；`-XX:+UseZGC -XX:+ZGenerational` | 暂停事件数、总暂停、p99、最长 |
| `J19Ex4Hiccup` 尾延迟 | 同上，加参数 `idle` 测基线 | p99.9/max；先测基线噪声 |

---

## 5. 坑与限制

1. **别自己写 `System.nanoTime()` 循环就当基准**：没有预热、死代码被消除（`J19Ex1Jit` 用 `sink` 输出结果防止被删）、常量折叠、OSR 干扰。正式测量用 **JMH**（OpenJDK 微基准工具）。本课数字是**演示现象**，不是基准结论。
2. **ZGC 不是白送的**：吞吐略降、需额外堆空间和 CPU、不用压缩指针（同样数据占更多内存）。堆太小、分配太快 → allocation stall，延迟反而不如 G1。要在你的负载上测。
3. **JDK 21 里别忘了 `-XX:+ZGenerational`**：只写 `-XX:+UseZGC` 在 21 得到旧的非分代版本。
4. **`-Xms` 与 `-Xmx` 设成一样**，加 `-XX:+AlwaysPreTouch`：避免运行中扩堆与缺页。
5. **容器里的 JVM**：内存限制、CPU 配额影响默认堆大小与 GC / JIT 编译线程数（`CICompilerCount`）。CPU 限额太小，JIT 与 GC 线程会和应用抢核。
6. **平均值掩盖尾部**：报延迟用分位数（p99、p99.9、max）。测量时避免"协同遗漏"（coordinated omission）——测量线程在系统停顿时也停止发请求，漏记了停顿期间本该发生的慢请求。
7. **逃逸分析不保证**：不逃逸对象"通常"被消除，但依赖内联深度、方法大小、控制流复杂度。不要靠它保证正确性；用 JFR 分配剖析或 `getThreadAllocatedBytes` 验证。
8. **GC 调参有"货物崇拜"风险**：从网上抄一串 `-XX:` 标志却不知其作用。先测量（`-Xlog:gc`、JFR），再一次改一个变量。
9. **虚拟线程的栈在堆上**：大量活跃虚拟线程增加堆压力与 GC 扫描量。

---

## 6. 真实代码里的运行时考量

* **测试运行命令**：`java --enable-preview -XX:+UseZGC -XX:+ZGenerational ...`，所以参考解都跑在 Generational ZGC 上——也是 JDK 21 必须写两个标志的活例子。
* **`TickBook`**（热路径版订单簿）头部注释：

```
// 为什么需要这一版：Part 2 的 OrderBook 每个订单是一个 Node 对象 + TreeMap/HashMap 的装箱 Long key + 每次调用的 Event 列表，
// 实测每个操作约 400 字节垃圾（见 REPORT）；垃圾多 → GC 停顿 → 尾延迟抖动。低延迟系统要的是「稳态零分配」：
```

  这就是 1.3 "避开 GC 的土办法"的落地：价格是有界范围内的 `long` tick，用数组/位图索引，不装箱。面试被问"这个订单簿怎么降低 GC 压力"，答 `TickBook` 的设计：primitive 数组 + 开放寻址 + 预分配。
* **`LongTickerMap`** 头部："没有 Long 装箱 —— `add()` 在稳态下一个字节都不分配"，与基于 `HashMap<String, Long>` 的朴素 `TickerMap` 对照。
* **`OffHeapTickerMap`** 类注释："GC 完全看不见它：不管表有多大，GC 扫描/整理的工作量都不变（低延迟系统避免 GC 抖动的常见手段）"。
* **`RecursiveSum.measureDepth`**：新线程里递归到 `StackOverflowError`，演示线程栈大小（`Thread` 构造器第四个参数）——JVM 运行时的另一个可调维度（`-Xss`）。
* 降低 GC 压力的清单（订单簿每条命令约 420 字节垃圾）：对象图改数组、开放寻址、回调代替 `List<Event>`、Generational ZGC、预热 JIT、`-Xms=-Xmx` + `AlwaysPreTouch`，面试可直接引用。

---

## 7. 面试怎么说（这一节是本课的重点产出）

被问"Java 低延迟怎么做"时，不要罗列标志，要讲**因果链**。下面每个问答是"思路 → 可以说出口的话"，英文句子可直接背。

**Q1. 你怎么处理 Java 里的 GC 暂停？**
* 思路：先说"暂停从哪来（搬对象、STW）"，再说两条路：**少产生垃圾**、**选对收集器**。两条都要，先减少分配再选 GC。
* 说出口：「There are two levers. First, allocate less on the hot path — primitive arrays instead of boxed collections, preallocated or pooled objects, off-heap for big tables — so there's little garbage to collect. Second, pick a collector that moves objects concurrently. On JDK 21 that's Generational ZGC, where pauses stay sub-millisecond and don't grow with heap size; G1 can still hit tens or hundreds of milliseconds when it falls behind and does a full collection. I'd measure with JFR and GC logs on our own workload rather than trust defaults.」

**Q2. G1 和 ZGC 的区别？**
* 思路：G1 = 暂停式（STW）、按暂停目标调节，暂停随活对象量增长；ZGC = 并发移动对象，用着色指针 + 加载屏障，暂停与堆大小无关；代价是吞吐/CPU/内存头部空间。
* 说出口：「G1 does evacuation inside stop-the-world pauses, aiming for a pause target — 200 ms by default — so pause time scales with how much live data it has to copy. ZGC marks and relocates concurrently using colored pointers and load barriers, so pauses are tiny and independent of heap size. The price is a bit lower throughput, more CPU for the GC threads, and needing headroom so allocations don't stall.」

**Q3. Generational ZGC 比普通 ZGC 好在哪？**
* 思路：分代假说——大部分对象死得早。非分代 ZGC 每轮标记整堆；分代只常回收年轻代。
* 说出口：「Most objects die young, so Generational ZGC collects the young generation often and cheaply, and the old generation rarely. Compared to single-generation ZGC that means less GC CPU, less heap headroom, and fewer allocation stalls. In JDK 21 you enable it with `-XX:+UseZGC -XX:+ZGenerational`; it became the default in 23 and the old mode was removed in 24.」

**Q4. JIT 预热是什么？上线前怎么处理？**
* 思路：解释器慢，热代码才编译；分层（C1 快编译 + 剖析，C2 慢编译 + 激进优化）；冷代码延迟高；对策是预热 + 稳定热路径。
* 说出口：「The JVM starts in the interpreter and compiles hot methods: first C1 with profiling, then C2 with aggressive optimizations like inlining and escape analysis. Until then, latency is several times worse — I measured about 6x on a toy method. So before taking real orders I'd warm the critical paths with replayed traffic until they're C2-compiled, and keep call sites monomorphic so the JIT's speculative inlining doesn't get deoptimized later.」

**Q5. 什么是逃逸分析？跟延迟有什么关系？**
* 思路：不逃逸的对象不必上堆 → 少分配 → 少 GC；依赖内联。
* 说出口：「If the JIT can prove an object never escapes the method, it can replace it with plain local variables — scalar replacement — so it's never allocated. In my test, twenty million temporary `Point` records allocated about five megabytes with escape analysis on and 640 megabytes with it off. Less allocation means fewer GCs, which means a flatter tail. It relies on inlining, so keeping hot methods small matters.」

**Q6. 线上出现偶发 100ms 尖刺，怎么查？**
* 思路：先分类：GC？JIT 去优化？锁竞争？safepoint？OS 调度？用 JFR（GC 暂停、编译、线程阻塞事件）和 GC 日志对时间线。先测基线，再一次改一个变量。
* 说出口：「First I'd line up the spike's timestamp against GC logs and a JFR recording: is there a pause event, a deoptimization storm, a lock-contention event, or a safepoint? If nothing JVM-side lines up, it's OS-level — CPU frequency, scheduling, transparent huge pages. I'd also check my measurement for coordinated omission before trusting the percentiles.」

**Q7. 为什么不直接把所有东西放堆外？**
* 说出口：「Off-heap removes GC cost for that data but you pay with manual lifecycle management, no automatic resizing, bounds-check overhead, and more complex code. I'd only do it for large, long-lived, fixed-layout tables — like a ticker map or a pooled fill record — after profiling shows GC is the bottleneck.」

**边界**：不要在面试里编造面试公司自己的技术栈。被问"你们用什么 GC"，可答"我了解 ZGC 与 G1 的取舍，我会在目标负载上测"。

---

## 8. 自测题

1. G1 和 Generational ZGC 的日志里各有一个"毫秒/秒"数字，含义有什么根本区别？
2. 说出分层编译的四个层级里你记得的，以及典型路径。 `PrintCompilation` 里的 `made not entrant` 和 `%` 分别是什么意思？
3. 为什么 JDK 21 里只写 `-XX:+UseZGC` 可能不是你想要的？
4. 逃逸分析在什么情况下失效？它与内联的关系？
5. 用自己的话说：为什么"平均延迟 50µs"不能说明系统适合低延迟交易？

<details><summary>答案</summary>

1. G1 的 `6.720ms` 是应用线程被暂停（STW）的时间；ZGC 的 `0.043s` 是这轮并发回收的总耗时，应用在其中一直运行，真正的暂停另算（JFR 的 `jdk.GCPhasePause`）。
2. 0 解释器 → 1/2/3 C1（3 带完整剖析）→ 4 C2；典型 0 → 3 → 4。`made not entrant`：这版编译代码不再被新调用进入（被更高层版本取代，或因去优化）。`%`：OSR，在循环运行中途把解释执行换成编译版本。
3. JDK 21 里 `-XX:+UseZGC` 默认是非分代的旧 ZGC；要分代必须再加 `-XX:+ZGenerational`（JDK 23 起才默认分代）。
4. 对象存进字段/集合、传给未被内联的方法、跨线程可见、从方法返回时被视为逃逸，不能做标量替换。逃逸分析依赖内联：被调方法不内联，对象一传进去就逃逸。
5. 平均值被大量快的请求稀释，掩盖尾部：每一万个里一个 100ms 的请求，平均几乎不变，却足以错过关键行情。应看 p99/p99.9/max，并检查测量是否有协同遗漏。

</details>

---

「延伸」回到 J10、J17：虚拟线程与堆外内存是同一条"少给 GC 添负担"思路的延伸。
