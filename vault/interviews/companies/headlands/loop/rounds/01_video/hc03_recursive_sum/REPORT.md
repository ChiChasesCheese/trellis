# hc03 · REPORT

## 概要

Headlands 视频面（一小时、一位工程师）的第一题就是这个热身：Blind 评论者说「先要求不用公式求 1..n 之和，面试官不断加优化追问」，
1p3a 的两个帖子只留下关键词 overflow / recursion optimizations / tail recursion。**题本身一分钟写完，评分在追问里**：
每一句追问对应你对 JVM 的一个层面有没有概念。所以这套题按「追问链」切成 4 个 Part，REPORT 重点写**面试官每一步在探什么**。

## 来源与置信度

见 `problem.md` §来源。主线（递归 → 溢出 → 栈/尾递归 → 优化）**有证据**（置信度高，#refs=4）；Part 3（区间 / 负数 / BigInteger）、
Part 4（并行 / 虚拟线程）以及 `Width`、`Overflow(exact)`、`Wide` 的设计全部是 **(reconstructed)**。

## 逐 Part 思路 + 面试官在探什么

### Part 1 · 递归 + checked overflow

* 写法：`n == 0 ? 0 : w.add(n, addUp(n-1, w))`；`ArithmeticException` 在**入口**转成 `Overflow(exactTo(n))`，递归内部不碰结果类型。
* **探针**：(1) 返回类型——抛异常、返回 `-1`、静默回绕，还是定义结果类型？sealed `Ok/Overflow` 让调用方被迫处理（switch 穷尽性）。
  (2) 你知不知道 `int` 的和在 n = 65536 就溢出，`long` 在 n = 4 294 967 296。(3) 你会不会注意到**栈比整数先出事**：
  本机默认 1 MiB 栈上，`sumToRecursive(65536)` 抛 `StackOverflowError`，`40000` 还能过——于是 INT 溢出的测试必须放到大栈线程里。

### Part 2 · 栈深：为什么 Java 没有 TCO，怎么办

* **为什么没有 TCO**：JVM 字节码没有尾调用指令；`javac` 不做尾调用消除。主要原因是栈帧对语义可见（异常栈轨迹、`StackWalker`、
  调试器、历史上的安全栈检查），消除帧会让它们对不上。Scala `@tailrec` / Kotlin `tailrec` 是**编译期把自递归改写成循环**，只覆盖自递归，互递归不行。
* **测量阈值**（本机，M 系列，JDK 21.0.12，`measureDepth`）：

  | 线程栈 | 冷启动第一次 | 同 JVM 预热之后 |
  |---|---|---|
  | 512 KiB | 6 161 | 25 228 |
  | 1 MiB | 17 258（`-Xint`：8 284） | 57 996 |
  | 8 MiB | — | 516 748 |
  | 64 MiB | — | 4 186 764 |

  阈值**不是常数**：同一个 JVM 里随 JIT 编译（解释器帧大、C1/C2 帧小）变化 3–4 倍；随 `-Xss`、栈帧里的局部变量个数、是否内联变化。
  面试答法：「量级是 栈大小 / 栈帧大小，大约每 MiB 栈几万层；我不会依赖它。」
* **三条出路**：(a) 迭代（`sumToIterative`，栈深 O(1)）；(b) trampoline——把「递归调用」变成「返回一个待办」，`run` 用 `while` + 模式匹配 switch 循环执行；
  (c) 加大栈（`new Thread(null, r, name, size)`，治标）。`isEven/isOdd` 互递归说明 trampoline 比「改写成循环」通用。
* **JIT / 内联**（面试官真正想听的）：C2 对**递归调用**只内联 `MaxRecursiveInlineLevel`（默认 1）层。实测
  `-XX:+PrintInlining` 对 `addUp` 的输出是 `@ 14 Inl::addUp inline` 之后 `recursive inlining too deep`——所以每一层仍是一次真调用：
  压帧、栈检查（stack banging）、返回后才做 `addExact`；循环里的 `addExact` 则能被展开、去掉冗余检查。
  实测 `n = 10 000` 重复 20 000 次（2×10⁸ 步）：递归 ≈ 570–650 ms（≈ 3 ns/步），迭代 ≈ 50 ms（0.25 ns/步），trampoline ≈ 460–535 ms（≈ 2.5 ns/步：每步分配一个 `More` + 一个 lambda，
  逃逸分析救不了，因为它们被 `Supplier` 接口返回出去）。**trampoline 解决的是「不爆栈」，不是「更快」**。
* **探针**：你能不能把「JVM 没有 TCO」讲清楚；会不会给自己的 trampoline 算开销；知不知道 `StackOverflowError` 是 `Error`，捕获它只能用来**测量**，业务上不该靠它兜底。

### Part 3 · 区间、负数、long / BigInteger、闭式

* 闭式 `Σ = (a+b)·(b−a+1)/2`。三个数值陷阱：
  1. `n*(n+1)/2` 的乘积先溢出：`n = 4 294 967 295` 时乘积是 2⁶⁴−2³²，在 long 里变成 −4 294 967 296，除 2 得 **−2 147 483 648**（`naiveClosedForm`，静默错误）；
  2. 正确顺序：`(a+b)` 与 `(b−a+1)` 奇偶相反（`b−a+1 = (a+b) − 2a + 1`），**哪个是偶数就先除 2**，再 `multiplyExact`；
  3. `a+b`、`b−a+1` 自己也会溢出，但中间量溢出 ≠ 结果溢出：`MIN..MAX` 的和是 `Long.MIN_VALUE`，`MAX..MAX` 的 `a+b` 溢出而和是 `MAX`。快路径抛 `ArithmeticException` 就退到 `BigInteger`，再 `bitLength() <= 63` 判断装不装得下。
* 负数：公式对负数同样成立；用 `s/2`（s 为偶且可负）是精确除法，没有向零取整的问题——这是「先除偶数」比「先乘再除」更好的另一个理由。
* **探针**：你是**凭直觉**写 `n*(n+1)/2`，还是想到了乘积溢出；`Math.multiplyExact` 抛了你怎么办（BigInteger 兜底，而不是报溢出）；会不会自己找出 `MIN..MAX` 这类反例。

### Part 4 · 并行求和 + 虚拟线程为什么不适合 CPU 密集

* **为什么要 `Wide`（128 位）**：逐步 `addExact` 的结果取决于顺序（`[MAX,1,-1]` 逐步会抛，真实和是 `MAX`），并行切块后每块的顺序更任意。
  128 位补码加法满足结合律：`plus(x)` 把 x 符号扩展进 hi、lo 做无符号进位；`merge` 同理；最后只判一次 `hi == lo >> 63`。
* `parallelSumForkJoin`：fork 左半、本线程算右半、再 join 左半——**不要两半都 fork**（多一次调度）。threshold 的取舍：太小 → 任务对象 + 调度比加法本身贵（本机 50 M 元素，threshold 100 为 7–8 ms，threshold 10⁵ 为 3–4 ms）；
  太大 → 负载不均。`parallelSumStream` 按「块下标」并行，不要 `Arrays.stream(boxed)`。
* **实测（本机 12 核，50 M 个 long，取最好一次）**：

  | 实现 | ms |
  |---|---|
  | 顺序 `checkedSum`（128 位） | 16–18 |
  | ForkJoin，threshold = 10⁵ | 3–4 |
  | ForkJoin，threshold = 100 | 7–8 |
  | parallel stream（块下标） | 4 |
  | 虚拟线程，12 块 | 4–5 |
  | 虚拟线程，10 000 块 | 4–8 |
  | 虚拟线程，1 000 000 块 | 190–204 |
  | 虚拟线程 12 块，且 `-Djdk.virtualThreadScheduler.parallelism=1` | 17（≈ 顺序） |

  加速只有 ≈ 4–5 倍（12 核）：50 M × 8 B = 400 MB，**受内存带宽限制**，不是核数限制。
* **为什么虚拟线程不适合 CPU 密集**：虚拟线程被调度到一个 `ForkJoinPool`（carrier，默认并行度 = 核数）上，只在**阻塞点**（I/O、锁、`sleep`）才卸载；
  CPU 密集线程永远不让出 carrier，没有时间片抢占。它**不会多出并行度**（把 parallelism 设成 1，12 个虚拟线程就退化成顺序，表里最后一行），
  百万个虚拟线程只增加创建 / 调度 / 栈块（heap 里的 stack chunk）开销（表里 190 ms vs 4 ms）。它解决的是「线程太贵、阻塞 I/O 太多」，不是「核不够用」。
  所以：CPU 密集 → ForkJoin / parallel stream，线程数 ≈ 核数；I/O 密集 → 虚拟线程。
* **探针**：你能不能区分「并发」与「并行」；知不知道虚拟线程的 carrier 与 pinning；`parallel()` 是否会选择装箱流、共享 common pool 的副作用（别的任务被饿死）。

### JIT 背景一页纸

* 热方法先被 C1 编译（tier 3，带 profile）再被 C2（tier 4）；**递归只能内联一层**，所以递归版永远有 call 开销；循环版会被展开、去掉边界检查，`addExact` 是 intrinsic（一条加法 + 溢出标志跳转）。
* 栈深测量被 JIT 污染：解释器帧 ≫ 编译帧，所以「第一次」和「预热后」差几倍，这也是 `measuredDepthGrowsWithStackSize` 只断言「64 MiB > 4 × 512 KiB」而不断言具体数字的原因。
* `Math.addExact` 是 intrinsic：热路径上一条加法加一个溢出标志判断，溢出分支走 uncommon trap（回到解释器再抛异常，HotSpot 实现细节，口述时留余地）；我们只在真的溢出时抛一次，不构成问题。
* 基准做法：预热 + 取多次最小值；单次 `System.nanoTime` 差只能说明数量级（本 REPORT 的数字都是这样得到的，不是 JMH）。

## 隐藏测试会打的坑

* 只在小 n 上测、从没碰过 `StackOverflowError`；`catch (StackOverflowError)` 把它吞成 0。
* `n*(n+1)/2` 先乘后除；对 `Long.MAX_VALUE` 附近的 n 返回负数。
* 区间 `a > b` 返回 0 还是抛异常（本题：抛 IAE，(reconstructed)）；`a == b`；`a` 为负数时用 `n*(n+1)/2` 套用。
* `MIN..MAX`：count 溢出但和装得下——只会在 `multiplyExact` 失败就报 Overflow 的实现上挂。
* 并行：每块各自 `addExact` 再合并（`MAX×2000 + MIN×2000` 每块里溢出，总和 −2000 装得下）；`threshold` 写成 0 造成无限递归；块数 > 元素数时 `from > to`。
* 虚拟线程版里把 `InterruptedException` 吞掉。

## 复杂度 + 实测时间

| 实现 | 时间 | 额外空间 / 栈 |
|---|---|---|
| 递归 | O(n) | 栈 O(n) |
| 迭代 | O(n)（`n = 3×10⁸`：77 ms） | O(1) |
| trampoline | O(n)（`n = 5×10⁶`：14 ms） | 堆 O(1) 活跃对象，GC 压力 O(n) |
| `rangeSum` 闭式 | O(1) | O(1)（快路径无分配） |
| 并行求和 | O(N / p + log p) | 任务 O(p) |

整个 `reference` 套件（29 个测试，含 `perf` 的 1×10⁷ 元素和 `conc` 的 20 轮）在本机运行约 0.6 s。

## 测试清单

`python3 tools/jtest.py run loop/rounds/01_video/hc03_recursive_sum --impl reference`：共 **29** 个测试（含参数化展开）。
按 tag（脚本计数）：part1 = 7 · part2 = 8 · part3 = 7 · part4 = 7；另 edge = 15 · perf = 2 · conc = 1 · fmt = 0（本题不涉及格式化输出）。
`conc`：20 轮 × 6 个线程用 `CountDownLatch` 对齐起跑，同时调用三种并行实现，断言所有结果与顺序答案相等。

## Java 21 特性

| id | 用在哪 | 比旧写法好在哪 |
|---|---|---|
| J01 record | `Ok` · `Overflow` · `Done` · `More` · `Wide` | 值语义 + `equals` 白送，测试直接 `assertEquals(new Ok(55), …)`，包括比较 `Overflow` 里的 BigInteger |
| J02 sealed | `SumResult permits Ok, Overflow` · `Trampoline permits Done, More` | 结果集合封闭，新增变体时所有 switch 编译报错；旧写法是返回 `-1` / 抛异常 / `Optional` |
| J03 + J04 模式匹配 switch + record 解构 | `run`：`case Done<T>(var v)`、`case More<T>(var next)`；测试里 `case Ok(var v)` | 不需要 `instanceof` + 强转 + `default`；穷尽性由编译器检查 |
| J05 switch 表达式 | `Width.add` 的 `INT/LONG` 分支 | 枚举穷尽、无 fallthrough |
| J08 `var` | `run` 的 `var cur`、`sumVirtual` 的 `var scope` | 类型显然时去掉重复 |
| J10 虚拟线程 | `sumVirtual` 里 `scope.fork` 默认就是虚拟线程；`Thread.ofPlatform()` 做对照 | 一块一个线程不再是「线程太贵」问题——但 CPU 密集仍不该用（见 Part 4） |
| J11 `StructuredTaskScope`（预览） | `sumVirtual`：`ShutdownOnFailure` + `fork` + `join().throwIfFailed()` | 子任务同生共死，任一失败其余被取消；手写 `ExecutorService` + `Future.get` 要自己清理 |
| J13 未命名变量 `_`（预览） | `measureDepth` 的 `catch (StackOverflowError _)` | 明说不用这个异常对象 |
| J14 Stream API | `IntStream.range(..).parallel().mapToObj(..).reduce(..)`；`Stream.toList()` | 按块下标并行，避免装箱；`toList()` 不可变 |
| J15 数学小工具 | `Math.addExact/subtractExact/multiplyExact/toIntExact`、`Math.ceilDiv`、`Long.compareUnsigned` | 溢出直接抛，不静默回绕；`ceilDiv` 代替 `(a + b - 1) / b` 的二次溢出 |
| J19 JIT 基础 | 口头：`-XX:+PrintInlining`、递归内联深度、解释器 vs 编译帧 | 能解释「为什么递归比循环慢、栈深为什么不稳定」 |

## 面试官可能的追问

1. **「为什么 Java 不做 TCO？Scala/Kotlin 怎么做到的？」**——JVM 没有尾调用指令，栈帧对异常轨迹 / `StackWalker` / 调试器可见；Scala `@tailrec`、Kotlin `tailrec` 在编译期把**自递归**改写成循环；互递归仍会爆栈，要 trampoline（Scala `TailCalls`、本题 `Trampoline`）。
2. **「你怎么知道会在多深爆栈？」**——量不出常数：阈值 ≈ 栈大小 / 帧大小，受 JIT 层级影响（本机 1 MiB：冷 17 258 → 热 57 996）；要么 `Thread(null, r, name, stackSize)` 给大栈，要么改成迭代 / trampoline；`-Xss` 影响所有线程，代价是内存。
3. **「溢出时返回什么？为什么不抛异常？」**——溢出是**业务可预期**的结果，用 sealed `Overflow(exact)` 让调用方在编译期被迫处理，并带精确值方便降级；`ArithmeticException` 留在实现内部，在公共边界转成值。热路径上抛异常很贵，但这里只抛一次。
4. **「`n*(n+1)/2` 对 `n = 2³²−1` 会怎样？」**——乘积 2⁶⁴−2³² 在 long 里回绕成 −2³²，除 2 得 −2³¹，静默错误；解法：先把偶数那个除 2，再 `multiplyExact`；中间量溢出时退到 `BigInteger`。
5. **「并行求和为什么不能每块 `addExact` 再合并？」**——`addExact` 的结果依赖顺序（`[MAX,1,-1]`），块边界会改变是否抛；用 128 位累加（结合律）或 `BigInteger`，最后判一次。
6. **「为什么不用虚拟线程做并行求和？」**——carrier 数 = 核数，虚拟线程不抢占、不增加并行度；表里 `parallelism=1` 时 12 个虚拟线程 ≈ 顺序，100 万块比 ForkJoin 慢 50 倍。CPU 密集用 ForkJoin / parallel stream，I/O 密集才用虚拟线程。
7. **「浮点数求和能并行吗？」**——`double` 加法不满足结合律，并行结果与切块有关（Kahan / pairwise 求和能减小误差，但不能消除顺序依赖）。
