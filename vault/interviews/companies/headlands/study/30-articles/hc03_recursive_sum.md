# hc03 · 递归求 1..n 之和 —— 讲义

> 题面：`loop/rounds/01_video/hc03_recursive_sum/problem.md` · 速查：同目录 `REPORT.md` · 代码：同目录 `reference/RecursiveSum.java`
> 写法说明见 `study/TEXTBOOK.md`。读者设定：会写基本 Java（类、方法、循环、递归、数组），其余从零讲。
> 证据说明：公开信息只有「先不用公式求 1..n 之和，面试官不断加优化追问」「溢出 / 递归优化 / 尾递归」这几个关键词。
> 区间、BigInteger、并行、虚拟线程这几部分是 **(reconstructed)**：按「面试官还会往哪推」补的。

---

## 1. 这道题在问什么

面试官说：「写一个函数，用**递归**求 1 + 2 + … + n。」

这句话本身一分钟写完。这道题的意义在于它是一个**脚手架**：面试官写完之后会不停地问「那如果……呢？」，
每一个“如果”都在试探你对计算机的一个层面是否真的懂：

```
写完递归        →  「结果放 int 还是 long？溢出怎么办？」          （整数在计算机里怎么存）
                →  「n = 一百万会怎样？」                          （函数调用在内存里怎么排）
                →  「能不能不爆栈？尾递归呢？」                    （JVM 的限制、trampoline）
                →  「n 很大时有没有更快的办法？」                  （公式、数值陷阱）
                →  「如果是数组里一亿个数求和，怎么并行？」        （线程、ForkJoin、虚拟线程）
```

### 手算一遍

n = 4：`sum(4) = 4 + sum(3) = 4 + (3 + sum(2)) = 4 + (3 + (2 + sum(1))) = 4 + (3 + (2 + (1 + sum(0))))`，
`sum(0) = 0`（递归的“出口”），所以回头一层层加：`1 + 0 = 1`，`2 + 1 = 3`，`3 + 3 = 6`，`4 + 6 = 10`。答案 10。

本题所有函数的返回类型不是一个裸的 `long`，而是 `SumResult`：要么 `Ok(value)`，要么 `Overflow(exact)`——“装得下”或“装不下”。为什么这样设计，第 4 节会推出来。

---

## 2. 前置知识

### 2.1 递归（recursion）

**是什么**：一个函数在自己的函数体里调用自己，每次调用处理一个更小的同类问题，直到问题小到能直接回答（**基线条件** base case）。

**为什么需要它**：有些问题天然是“大问题 = 一点工作 + 小一点的同类问题”。求和就是：`sum(n) = n + sum(n-1)`。没有基线条件，函数会一直调用下去，永不返回。

**怎么工作**：每次调用都是一次新的“函数执行”，有自己的一份参数和局部变量。外层调用必须**等**内层调用返回，才能继续往下做（这里是做加法）。

**Java 里怎么写**：

```java
static long sum(long n) {
    if (n == 0) return 0;      // 基线条件：出口
    return n + sum(n - 1);     // 递归条件：n 加上“更小的问题”的答案
}
```

### 2.2 调用栈与栈帧（call stack, stack frame）

**是什么**：每个线程有一块专用内存叫**调用栈**。每次调用函数，就在栈顶压入一个**栈帧**，里面放：这次调用的参数、局部变量、“调用完回到哪一行”。函数返回时，栈顶那个帧被弹出。

**为什么需要它**：函数调用会嵌套（A 调 B，B 调 C）。C 返回后要回到 B 的中间继续，B 返回后要回到 A 的中间继续。
“最后进来的最先出去”正是栈（后进先出，LIFO）的行为，所以用栈来记这些“回去继续的地方”。

**怎么工作**：用 `sum(3)` 演示（栈向上长，最上面的是当前正在执行的）：

```
调用 sum(3) → sum(2) → sum(1) → sum(0) 时的栈（最深的时刻）：

   │ sum(0)  n=0   返回到 sum(1) 的 "n + □" 处 │  ← 栈顶（当前执行）
   │ sum(1)  n=1   返回到 sum(2) 的 "n + □" 处 │
   │ sum(2)  n=2   返回到 sum(3) 的 "n + □" 处 │
   │ sum(3)  n=3   返回到 main                 │
   │ main                                      │  ← 栈底
   └────────────────────────────────────────────┘

sum(0) 返回 0  → 弹出它；sum(1) 里 "1 + □" 变成 1 + 0 = 1，返回 1 → 弹出
sum(1) 返回 1  → sum(2) 里 2 + 1 = 3，返回 3 → 弹出
sum(2) 返回 3  → sum(3) 里 3 + 3 = 6，返回 6 → 弹出
```

关键观察：**递归求和有 n+1 个栈帧同时存在**。栈深度 = n。每个帧占若干字节（几十到上百字节），栈的总大小是有限的。

栈满了会怎样：JVM 抛出 `StackOverflowError`（注意是 `Error` 不是 `Exception`：它表示 JVM 自身的资源耗尽，不是你的业务逻辑错）。
默认每个线程栈约 1 MiB（`-Xss` 可改，创建线程时也可以单独指定）。粗略估计：1 MiB ÷ 每帧几十字节 → 一万到几万层。
本机实测见第 4 节。

**Java 里怎么写**：栈帧是 JVM 自动管理的，你写不出来也不用写。你能控制的是：给新线程指定栈大小

```java
Thread t = new Thread(null, runnable, "name", 64L * 1024 * 1024);   // 第四个参数：栈大小（字节），只是“提示”，OS 可能调整
```

### 2.3 整数、补码、溢出（two's complement, overflow）

**是什么**：计算机用固定个数的二进制位存整数。`int` 是 32 位，`long` 是 64 位。位数固定，所以能表示的数有上下限：

| 类型 | 位数 | 最小值 | 最大值 |
|---|---|---|---|
| `int` | 32 | −2 147 483 648（−2³¹） | 2 147 483 647（2³¹−1） |
| `long` | 64 | −9 223 372 036 854 775 808（−2⁶³） | 9 223 372 036 854 775 807（2⁶³−1） |

**负数怎么存**：用**补码**（two's complement）。以 8 位为例（32 位同理，只是位数多）：最高位的权重是**负的**。

```
位置:     7     6    5    4    3    2    1    0
权重:  −128   64   32   16    8    4    2    1

 5   = 0000 0101   =  4 + 1                        = 5
 127 = 0111 1111   =  64+32+16+8+4+2+1             = 127   ← 8 位能表示的最大正数
−1   = 1111 1111   = −128 + 64+32+16+8+4+2+1       = −1
−128 = 1000 0000   = −128                          ← 8 位能表示的最小数
```

**溢出**：算出来的结果超出范围时，硬件只保留低位，结果“绕回去”：

```
  0111 1111   (127)
+ 0000 0001   (  1)
-------------
  1000 0000   = −128       ← 127 + 1 变成了 −128！没有报错。
```

`int` 同理：`Integer.MAX_VALUE + 1 == Integer.MIN_VALUE`。**Java 不会为整数加法抛异常**，这是最危险的地方：答案是错的，程序照常运行。

**为什么对本题重要**：1 + 2 + … + n 增长很快（约 n²/2）。`int` 在 **n = 65 536** 就装不下了：
1+…+65 535 = 2 147 450 880（刚好小于 2 147 483 647），再加 65 536 得 2 147 516 416，超了，绕回成 **−2 147 450 880**。
`long` 在 **n = 4 294 967 296**（2³²）装不下。

**Java 里怎么写**：用“精确”版本的运算，溢出时抛 `ArithmeticException`：

```java
int a = Math.addExact(x, y);          // int 版本
long b = Math.addExact(p, q);         // long 版本
int c = Math.toIntExact(someLong);    // long → int，装不下就抛
// 还有 subtractExact / multiplyExact / negateExact / incrementExact
```

`Math.addExact` 在热点代码里会被 JIT 编译成“一条加法 + 检查溢出标志位”，开销很小。

### 2.4 尾调用与“JVM 为什么没有 TCO”（tail call, TCO）

**是什么**：**尾调用**是函数做的**最后一件事**就是调用另一个函数，并且直接把它的返回值当自己的返回值。

```java
return n + sum(n - 1);        // 不是尾调用：调用返回后还要做 “n +”
return step(n - 1, acc + n);  // 是尾调用：调用就是最后一件事（把 acc 传下去，答案在 acc 里）
```

**为什么需要这个概念**：尾调用返回之后，当前这个栈帧里的东西**再也用不到了**（没有“回来以后还要做的事”）。
所以聪明的编译器可以**复用/丢掉当前帧**，让尾递归像循环一样只占常数个栈帧。这叫**尾调用优化**（Tail Call Optimization, TCO）。
Scheme、Haskell 等语言保证 TCO，函数式风格的代码因此敢用递归当循环。

**Java 里怎么办**：**JVM 没有 TCO**。`javac` 不做，运行时 JIT 也不保证做。常见的理由是栈帧对语义可见：
异常的栈轨迹（stack trace）、`StackWalker`、调试器、历史上的安全检查（根据调用栈判断权限）都依赖“每次调用都有一个帧”，消除帧会让它们对不上。
Scala 的 `@tailrec`、Kotlin 的 `tailrec` 是**编译期把“自己调用自己”的递归改写成循环**——只处理自递归，互相调用（A 调 B、B 调 A）不行。
所以在 Java 里：想要深递归，要么改成循环，要么用 trampoline（下一节），要么加大栈。

### 2.5 Trampoline（蹦床）

**是什么**：一种“手动实现的尾调用优化”：函数不直接调用下一步，而是**返回一个描述‘下一步该做什么’的对象**；由一个外层循环不断取出这个对象、执行它，直到拿到最终答案。

**为什么需要它**：递归爆栈是因为每次调用都叠加一个栈帧。如果每一步都**立刻返回**（帧立刻弹出），把“待办”放到**堆**（heap，容量比栈大得多，由 GC 管理）上，由循环驱动，栈深度就恒定了。

**怎么工作**：

```
普通递归：  step(3) → step(2) → step(1) → step(0)      栈帧叠 4 层
                                                        
trampoline： run 循环                                   栈永远只有 run 的 1 帧
   cur = step(3)      返回 More(下一步)   ← step(3) 的帧已弹出
   cur = cur.next()   返回 More(下一步)   ← step(2) 的帧已弹出
   cur = cur.next()   返回 More(下一步)
   cur = cur.next()   返回 Done(结果)     → 循环结束，返回结果
```

**Java 里怎么写**（本题的写法，用 sealed 接口表达“二选一”）：

```java
sealed interface Trampoline<T> permits Done, More {}
record Done<T>(T value) implements Trampoline<T> {}                       // 算完了
record More<T>(Supplier<Trampoline<T>> next) implements Trampoline<T> {}  // 还有下一步（Supplier = 一个“稍后再算”的函数）
```

代价：每一步在堆上分配一个 `More` 对象和一个 lambda，比普通循环慢（实测见第 4 节）。**trampoline 解决“不爆栈”，不解决“更快”。**

### 2.6 求和公式与奇偶（closed form）

**是什么**：高斯的结论：`1 + 2 + … + n = n(n+1)/2`。把头尾配对：`1+n`、`2+(n−1)`、…每对和为 `n+1`，共 `n/2` 对。
更一般地，a 到 b（含）所有整数之和 `= (a + b) × (b − a + 1) / 2`：首项加末项，乘项数，除以 2。对负数也成立。

**为什么需要它**：O(1) 时间，不爆栈。但直接按公式写有**数值陷阱**：先乘后除时，**乘积会先溢出**，即使最终答案装得下。

**怎么避免**：`(a + b)` 和 `(b − a + 1)` 的奇偶**相反**（它们的差是 `2a − 1`，奇数），所以**必有一个是偶数**。先把偶数的那个除以 2（整除，没有余数），再相乘：乘积只有“先乘后除”的一半大。
例：n = 4 294 967 295（2³²−1）：`n × (n+1) = 2⁶⁴ − 2³²`，超出 `long`（2⁶³−1）；而先除 2 得 `2 147 483 648 × 4 294 967 295 = 9 223 372 034 707 292 160`，装得下。

### 2.7 BigInteger

**是什么**：Java 标准库里“位数不限”的整数类。没有溢出，代价是慢（每个数是堆上的对象，运算是方法调用）。

**为什么需要它**：作为“慢但永远正确”的备选，也用来**验证**快速实现。

**Java 里怎么写**：

```java
BigInteger x = BigInteger.valueOf(a).add(BigInteger.valueOf(b));
x.multiply(y); x.shiftRight(1);   // 右移 1 位 = 除以 2（向负无穷取整；这里被除数是偶数，所以精确）
x.bitLength();                    // 表示这个数（不含符号位）需要的位数，≤ 63 说明 long 装得下
x.longValueExact();               // 装不下就抛 ArithmeticException
```

### 2.8 JIT 编译与内联（JIT, inlining）——概览

**是什么**：JVM 先**解释**执行字节码；发现某个方法被调用得很频繁（“热点”）后，JIT 编译器（HotSpot 里的 C1、C2）把它编译成机器码，之后直接运行机器码。

**内联**（inlining）：把被调用方法的代码**直接贴到调用处**，省掉“压栈、跳转、返回”的开销，还能让编译器看到更大范围的代码做优化。

**为什么对本题重要**：循环能被编译器大幅优化（展开、去掉重复检查）；**递归只能内联一两层**（HotSpot 默认 `MaxRecursiveInlineLevel=1`），所以递归版每一层仍然是真正的函数调用。

本机实测：`-XX:+PrintInlining` 对递归方法输出 `recursive inlining too deep`（见第 4 节）。
副作用：同一个递归方法在**解释执行**时的栈帧比**编译后**大几倍，所以“能递归多深”不是常数。

### 2.9 线程、并行、ForkJoin、虚拟线程（第 4 步 7、8 用到）

**线程**（thread）：程序里一条独立的执行流。**平台线程**（platform thread）就是操作系统线程，创建和切换较贵，数量有限（几千个）。
**CPU 核**：真正同时执行代码的硬件单元。本机有 12 个。线程数多于核数时，OS 轮流让线程用核（时间片）。

**并行**（parallelism）：多个任务**真的同时**在不同核上跑，目的是更快算完。**并发**（concurrency）：多个任务**交替**推进（比如等 I/O 时让别的任务用 CPU），目的是同时处理很多事，不一定更快。

**ForkJoinPool**：Java 的并行计算线程池，专为“把大任务拆成小任务、再合并”设计。`RecursiveTask<T>` 的 `compute()` 里：小任务直接算；大任务拆两半，`fork()` 一半交给池（别的空闲线程可以“偷”走它）、自己算另一半、再 `join()` 取回。

**parallel stream**：`stream.parallel()` 把管道交给公共的 ForkJoinPool（`ForkJoinPool.commonPool()`）。

**虚拟线程**（virtual thread，Java 21 正式）：由 JVM 而不是操作系统调度的轻量线程，创建极便宜，可以开几十万个。它们运行时被“挂”（mount）在少量**载体线程**（carrier thread，一个 ForkJoinPool，默认大小 = 核数）上；
只有当虚拟线程**阻塞**（等网络、等锁、`sleep`）时才会被摘下来（unmount），让载体线程去跑别的虚拟线程。
**所以：虚拟线程让“大量在等待的任务”很便宜，但不增加计算能力**；一个只做计算、从不阻塞的虚拟线程会一直霸占载体线程，没有时间片抢占。

**内存带宽**：对 `long[]` 求和，每个元素只做一次加法，瓶颈是把数据从内存读进 CPU 的速度（内存带宽），而不是加法。所以核再多，加速也有上限。本机 5000 万个 long = 400 MB，顺序求和 17 ms ≈ 23 GB/s，并行只能再快 4–5 倍。

### 2.10 本题用到的 Java 21 语法速览

* `record`：自动生成构造器、访问器、`equals/hashCode/toString` 的不可变数据类。
* `sealed interface X permits A, B`：规定 `X` 只能有 `A`、`B` 两种实现，编译器据此检查 `switch` 是否覆盖了所有情况。
* 模式匹配 `switch`：`switch (x) { case A(var f) -> …; case B b -> … }`，一步判断类型并取出字段。
* 细节见第 6 节与 `study/10-java21/` 中对应的 J01–J05 篇。

---

## 3. 从最笨的解法开始

```java
static int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}
```

* **复杂度**：时间 O(n)（n 次调用，每次一个加法）；栈空间 O(n)（n+1 个栈帧同时存在）。这里 n 是输入的整数本身，不是输入的“长度”。
* **它具体在哪个输入上错 / 慢**：
  1. `sum(65536)`：结果应该是 2 147 516 416，但 `int` 装不下，**静默**变成 −2 147 450 880。程序不报错，答案是错的。
  2. 就算改成 `long`，`sum(1_000_000)` 在默认栈上抛 `StackOverflowError`。本机实测：默认 1 MiB 栈，`sumToRecursive(65536)` 就会爆栈（`40000` 还行）——**栈比 `int` 先出问题**。
  3. 对 `long` 溢出的 n = 4 294 967 296，需要 43 亿次递归，栈永远撑不到那里，递归版**根本测不出 long 溢出**。

这三条就是后面所有改进的动力。

---

## 4. 一步一步改进

### 步骤 1：让溢出“看得见”——checked 加法 + 结果类型

* **发现问题**：静默回绕是最坏的 bug。
* **想法**：用 `Math.addExact`，溢出时抛 `ArithmeticException`。
* **但抛异常不够好**：调用方可能忘了 `catch`；而且“溢出”在这个问题里是**可预期的业务结果**（输入 n 太大），不是程序错误。
  返回特殊值（比如 −1）也不行：区间求和里（第 7 步）负数是合法结果；任何魔法数都会和合法结果混在一起。
* **正确的想法**：把“可能溢出”写进**返回类型**：

  ```java
  sealed interface SumResult permits Ok, Overflow {}
  record Ok(long value) implements SumResult {}
  record Overflow(BigInteger exact) implements SumResult {}   // 顺便带上数学上的精确值，方便调用方降级
  ```

  调用方用 `switch` 处理，**编译器强制它处理 `Overflow`**。`ArithmeticException` 只在实现内部用，在公共入口转换成值。
* **为了测试得动**：加一个 `Width { INT, LONG }` 枚举，让累加器可以是 `int` 宽度。这样 `INT` 在 n = 65 536 就溢出，不需要 43 亿次递归。
* **新复杂度**：不变，时间 O(n)，栈 O(n)。

### 步骤 2：测量栈深——`StackOverflowError` 发生在多深？

* **发现问题**：“n = 100 万会怎样”要用数据回答，而不是猜。
* **想法**：新开一个线程，指定栈大小，递归到爆为止，数递归了多少层（`measureDepth`）。
* **本机实测**（M 系列，JDK 21.0.12）：

  | 线程栈 | 冷启动第一次 | 预热之后 |
  |---|---|---|
  | 512 KiB | 6 161 | 25 228 |
  | 1 MiB | 17 258 | 57 996 |
  | 8 MiB | — | 516 748 |
  | 64 MiB | — | 4 186 764 |

  结论：①大致与栈大小成正比；②**同一个 JVM 里，预热前后能差 3–4 倍**，因为解释执行的栈帧比 JIT 编译后的大；③不能依赖某个固定数字，所以测试只断言“64 MiB 的深度 > 4 × 512 KiB 的深度”。
* **新问题**：我们只是量出了界限，还没解决它。

### 步骤 3：最简单的解决方案——改成循环

* **想法**：递归求和不需要“回来之后继续”，循环里用一个变量 `acc` 累加就够了。
* **代码变化**：

  ```java
  long acc = 0;
  for (long i = 1; i <= n; i++) acc = w.add(acc, i);
  ```

* **新复杂度**：时间 O(n)，栈 O(1)。本机 `n = 3×10⁸` 只需约 77 ms。
* **为什么比递归快这么多**：实测 `n = 10 000` 重复 20 000 次（2×10⁸ 步），递归约 570–650 ms（≈ 3 ns/步），循环约 50 ms（≈ 0.25 ns/步）。
  原因：递归每一步是真正的函数调用（压栈帧、栈检查、返回），JIT 只能内联一层（`-XX:+PrintInlining` 显示 `recursive inlining too deep`）；
  循环则能被展开，`addExact` 变成一条加法加溢出检查。

面试官如果问“如果必须用递归呢”（题目就要求递归），继续往下。

### 步骤 4：尾递归形式 + trampoline

* **发现问题**：我们想保留“递归”的写法，又不要栈深度 O(n)。
* **想法 A：尾递归**——把“到目前为止的和”作为参数传下去，让递归调用成为函数的最后一件事：

  ```java
  static long step(long n, long acc) { return n == 0 ? acc : step(n - 1, acc + n); }
  ```

  这在 Scala/Kotlin（`tailrec`）里会被编译成循环。**在 Java 里不会**（2.4）：它仍然叠 n 层栈帧。
* **想法 B：trampoline**（2.5）：让 `step` 不直接调用自己，而是返回一个“下一步”对象；`run` 里一个 `while` 循环驱动：

  ```java
  static Trampoline<Long> step(long n, long acc, Width w) {
      return n == 0 ? new Done<>(acc) : new More<>(() -> step(n - 1, w.add(acc, n), w));
  }
  ```

  注意：`w.add(acc, n)` 写在 **lambda 里面**，所以它是在 `run` 的循环里被执行的，而不是在 `step` 的帧里叠起来。
* **为什么这样能解决问题**：每个 `step` 调用立刻返回（帧立刻弹出），栈深度恒为 1–2。
* **新复杂度**：时间 O(n)，栈 O(1)，堆上每步一个短命对象（GC 压力 O(n) 但活跃对象 O(1)）。本机 `n = 5×10⁶` 约 14 ms；每步约 2.5 ns（比循环慢 10 倍，和递归同量级）。
* **互递归**：`isEven(n) = n == 0 ? true : isOdd(n-1)`，`isOdd(n) = n == 0 ? false : isEven(n-1)`。这种“A 调 B、B 调 A”连 Scala `@tailrec` 都不处理，trampoline 可以：把两个函数都写成返回 `Trampoline<Boolean>` 的形式即可。测试在 512 KiB 栈上跑到 n = 200 万。

### 步骤 5：闭式公式

* **发现问题**：循环仍是 O(n)。题目要求“更快”吗？对 n = 10¹⁸，循环要几十年。
* **想法**：高斯公式 O(1)（2.6）。
* **新问题（数值陷阱）**：`n * (n + 1) / 2` 里，`n * (n + 1)` 先算。n = 4 294 967 295 时乘积是 2⁶⁴ − 2³²，`long` 装不下，补码绕回 −2³² = −4 294 967 296，除以 2 得 **−2 147 483 648**。
  没有异常，答案还是负数。
* **改进**：先除后乘（2.6）：`(a+b)` 与 `(b−a+1)` 一奇一偶，把偶的那个先除 2，再 `Math.multiplyExact`。

### 步骤 6：区间 [a, b]、负数、中间量溢出 ≠ 结果溢出

* **发现问题**：把公式推广到 a..b（可负）时，`a + b` 和 `b − a + 1` **自己**也会溢出：
  `b − a + 1` 当 `a = MIN, b = MAX` 时是 2⁶⁴，装不下 `long`；`a + b` 当 `a = b = MAX` 时溢出。
* **但是**：这些中间量溢出**不等于最终结果溢出**。`MIN..MAX` 的和：除了 `MIN` 以外的数两两抵消（`−MAX` 与 `MAX`…），剩 `MIN`，所以和恰好是 `Long.MIN_VALUE`，装得下！
  `MAX..MAX` 的和就是 `MAX`。
* **想法**：快路径用 `addExact/subtractExact/multiplyExact`；任何一步抛异常就**退到 `BigInteger`** 算精确值，再用 `bitLength() <= 63` 判断装不装得下 `long`。
* **新复杂度**：O(1)（快路径无分配）；退路径 O(1)（BigInteger 运算，常数大）。

### 步骤 7：数组并行求和，但“求和顺序”会影响溢出判断

* **新场景 (reconstructed)**：不是 1..n，而是一个 `long[]` 里 5000 万个数求和。单线程要扫完全部元素，想用多核。
* **想法**：把数组切块，每块算部分和，再合并（ForkJoin：`fork` 左半、自己算右半、`join`）。
* **陷阱**：如果每块用 `Math.addExact` 累加，再用 `addExact` 合并，那么结果**依赖顺序**。例：`[MAX, 1, -1]`：真实和是 `MAX`，装得下；
  但从左到右加，`MAX + 1` 就抛异常。并行时每块边界是任意的，同一份数据换个切法，会时而抛时而不抛。
* **想法**：用 **128 位累加器** `Wide(hi, lo)` 代替 `long`：它不会溢出，加法满足结合律（先加谁后加谁结果一样），最后只判一次“`hi:lo` 是否在 `long` 范围内”。
  - 加一个有符号 `long x`：`lo` 当作无符号数相加；结果比原 `lo` 小说明发生了进位（回绕），`hi` 加 1；`x` 的“高 64 位”是符号扩展，`x ≥ 0` 为 0，`x < 0` 为 −1（`x >> 63`）。
  - 判断装得下：`hi == (lo >> 63)`（`hi` 必须等于 `lo` 的符号位扩展）。
* **三种并行实现**：`parallelSumForkJoin`（手写 `RecursiveTask`，区间 ≤ threshold 直接算）、`parallelSumStream`（对**块下标**做 parallel stream，不要对装箱的 `Long` 流并行）、`sumVirtual`（见下一步）。

### 步骤 8：虚拟线程——为什么不适合 CPU 密集

* **发现问题**：Java 21 有虚拟线程，“每块开一个虚拟线程”看起来很现代。
* **实测**（本机 12 核，5000 万 long）：

  | 实现 | 时间 |
  |---|---|
  | 顺序 128 位 | 16–18 ms |
  | ForkJoin（threshold = 10⁵） | 3–4 ms |
  | parallel stream（块下标） | 4 ms |
  | 虚拟线程，12 块 | 4–5 ms |
  | 虚拟线程，10 000 块 | 4–8 ms |
  | 虚拟线程，1 000 000 块 | 190–204 ms |
  | 虚拟线程，12 块，且载体线程只有 1 个（`-Djdk.virtualThreadScheduler.parallelism=1`） | 17 ms |

* **解读**：12 块时虚拟线程和 ForkJoin 一样快——但那是因为载体线程恰好有 12 个，**并行度来自载体线程，不是虚拟线程本身**。
  把载体线程限制为 1 个，12 个虚拟线程立刻退化成顺序执行（17 ms ≈ 顺序的 17 ms）。
  一百万个虚拟线程只增加创建和调度开销（慢 50 倍）。因此：**CPU 密集任务用 ForkJoin / parallel stream，线程数 ≈ 核数；虚拟线程用于大量阻塞 I/O。**

---

## 5. 逐段讲参考解

下面按 `reference/RecursiveSum.java` 的顺序，贴关键片段并解释。

### 5.1 结果类型与位宽

```java
public sealed interface SumResult permits Ok, Overflow {}
public record Ok(long value) implements SumResult {}
public record Overflow(BigInteger exact) implements SumResult {}

public enum Width {
    INT, LONG;
    long add(long a, long b) {
        long s = Math.addExact(a, b);
        return switch (this) {
            case INT -> Math.toIntExact(s);
            case LONG -> s;
        };
    }
}
```

* `sealed … permits`：结果只有两种；以后调用方写 `switch` 时漏掉一种，编译不过。
* `Width.add`：入参都在本位宽之内。两个 `int` 范围内的数在 `long` 里相加**绝不会溢出**，所以先用 `long` 算 `s`，`INT` 时再用 `Math.toIntExact(s)` 检查 `s` 是否还在 `int` 范围（不在就抛 `ArithmeticException`）。
  `LONG` 时 `Math.addExact` 本身就检查了。
* 如果换种写法：直接 `int` 相加再比较，需要自己处理回绕判断（`((a ^ s) & (b ^ s)) < 0` 这种位技巧），容易写错。

### 5.2 朴素递归

```java
public static SumResult sumToRecursive(long n, Width w) {
    requireNonNegative(n);
    try {
        return new Ok(addUp(n, w));
    } catch (ArithmeticException e) {
        return new Overflow(exactTo(n));
    }
}
private static long addUp(long n, Width w) {
    return n == 0 ? 0 : w.add(n, addUp(n - 1, w));
}
```

* `try/catch` 在入口，而不是递归里：递归里每层包 `try` 不会让栈帧本质变大，但会让逻辑复杂；把“内部用异常，边界转成值”作为统一风格更清楚。
* **注意 `StackOverflowError` 没有被捕获**，会直接传给调用方。吞掉它（返回 0 或 `Overflow`）会把“栈不够”误报成别的东西。
* `exactTo(n)`：`BigInteger` 版的 `n(n+1)/2`，不会溢出，只在出错路径上算一次。
* 加法发生在递归**返回之后**（`w.add(n, 子结果)`），所以这**不是**尾递归。

### 5.3 栈深测量

```java
private static final class Probe { int depth; void dive() { depth++; dive(); } }

public static int measureDepth(long stackBytes) {
    var probe = new Probe();
    var t = new Thread(null, () -> {
        try { probe.dive(); } catch (StackOverflowError _) { }
    }, "depth-probe", stackBytes);
    t.start();
    t.join();   // (省略了 InterruptedException 处理)
    return probe.depth;
}
```

* 计数放在**对象字段**里：栈溢出的瞬间没法返回任何值，字段是唯一能带出结果的办法。
* `catch (StackOverflowError _)`：`_` 是“不需要这个变量”的未命名变量（Java 21 预览特性）。
* 为什么用新线程：栈大小是**线程**的属性，只有构造 `Thread` 时才能指定；也避免把调用者线程的栈撑爆。

### 5.4 迭代与 trampoline

```java
public static <T> T run(Trampoline<T> start) {
    var cur = start;
    while (true) {
        switch (cur) {
            case Done<T>(var v)    -> { return v; }
            case More<T>(var next) -> cur = next.get();
        }
    }
}
```

* `switch` 对 sealed 类型做**模式匹配**：`case Done<T>(var v)` 同时判断“是 Done”并把字段取出到 `v`。没有 `default`——编译器已知只有两个实现。
* `cur = next.get()`：执行“下一步”，得到新的 `Trampoline`，回到循环顶。
* 栈帧在每次 `next.get()` 返回时已经弹出，所以栈深恒定。

```java
private static Trampoline<Long> step(long n, long acc, Width w) {
    return n == 0 ? new Done<>(acc) : new More<>(() -> step(n - 1, w.add(acc, n), w));
}
```

* `w.add(acc, n)` 在 lambda 里：延迟到 `run` 循环里才执行。如果写成 `new More<>(step(n - 1, w.add(acc, n), w))` 之类的急切求值，就会把递归又写回栈上。
* 溢出时 `w.add` 抛 `ArithmeticException`，从 `run` 一路抛到 `sumToTrampoline` 入口，在那里被转成 `Overflow`。

### 5.5 区间求和

```java
long s = Math.addExact(a, b);
long count = Math.addExact(Math.subtractExact(b, a), 1);
long v = (count & 1) == 0 ? Math.multiplyExact(count / 2, s)
                          : Math.multiplyExact(count, s / 2);
return new Ok(v);
// 任何一步抛 ArithmeticException：
var exact = rangeSumExact(a, b);
return exact.bitLength() <= 63 ? new Ok(exact.longValueExact()) : new Overflow(exact);
```

* `(count & 1) == 0`：用位与判断偶数（`count` 非负时等价于 `count % 2 == 0`）。`count` 为偶则 `s` 必为奇（奇偶相反），所以除的是 `count`；反之除 `s`。`s / 2` 里 `s` 是偶数，即使为负也是精确除法，没有“向零取整”的问题。
* 快路径无分配。慢路径只在中间量溢出时进入，用 `BigInteger` 保证正确。
* `bitLength() <= 63`：`BigInteger.bitLength()` 不含符号位，范围 −2⁶³..2⁶³−1 的数都满足 ≤ 63（对负数，bitLength 指补码里除符号位以外所需的位数，−2⁶³ 恰为 63）。

### 5.6 `Wide` 与三个并行实现

```java
public record Wide(long hi, long lo) {
    public Wide plus(long x) {
        long nlo = lo + x;
        long carry = Long.compareUnsigned(nlo, lo) < 0 ? 1 : 0;
        return new Wide(hi + (x >> 63) + carry, nlo);
    }
    public boolean fitsLong() { return hi == (lo >> 63); }
}
```

* `lo + x` 在 `long` 里按补码相加；把 `lo` 当**无符号**数比较大小，若结果 `nlo` 比 `lo` 小，说明相加时越过了 2⁶⁴，丢了一个进位，补到 `hi`。
* `x >> 63`：算术右移 63 位，非负数得 0，负数得 −1（全 1）——就是 `x` 的符号扩展到高 64 位。
* `hi == (lo >> 63)`：128 位值能用 64 位有符号数表示，当且仅当高 64 位全等于低 64 位的符号位。

```java
@Override protected Wide compute() {
    if (to - from <= threshold) return sumChunk(data, from, to);
    int mid = (from + to) >>> 1;
    var left = new SumTask(data, from, mid, threshold);
    left.fork();
    var right = new SumTask(data, mid, to, threshold).compute();
    return left.join().merge(right);
}
```

* `>>> 1` 而不是 `/ 2`：`from + to` 若溢出成负数，`/ 2` 得负数，`>>> 1`（无符号右移）仍然得到正确的中点。这是经典二分查找 bug。
* 只 `fork` 左半，右半在**当前线程**直接算：避免“两半都 fork，当前线程空等”多一次调度。
* `sumChunk` 的循环里用局部变量 `hi`、`lo`，不创建 `Wide` 对象，否则 5000 万次分配会压垮 GC。

```java
public static SumResult sumVirtual(long[] data, int chunks) {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        var parts = IntStream.range(0, chunks)
            .mapToObj(i -> scope.fork(() -> sumChunk(...)))
            .toList();
        scope.join().throwIfFailed();
        ...
    }
}
```

* `StructuredTaskScope`（Java 21 预览）：把一组子任务绑在一个“作用域”里，`try` 块退出前所有子任务必须结束；其中一个失败，其余被取消。`scope.fork` 默认每个子任务一个虚拟线程。
* 对比旧写法：自己 `new Thread` + `join`，或 `ExecutorService` + `Future.get`，要自己保证异常时关闭、取消其余任务。

---

## 6. Java 21 特性小课

> 每个特性在 `study/10-java21/` 里有独立课本（id 见括号）；这里只讲本题怎么用、与旧写法的对比。

### J01 record（+ J02 sealed）

旧写法（Java 8）：

```java
public final class Ok implements SumResult {
    private final long value;
    public Ok(long value) { this.value = value; }
    public long value() { return value; }
    @Override public boolean equals(Object o) { /* 10 行 */ }
    @Override public int hashCode() { return Long.hashCode(value); }
    @Override public String toString() { return "Ok[value=" + value + "]"; }
}
```

新写法：`public record Ok(long value) implements SumResult {}`。编译器生成构造器、访问器、`equals/hashCode/toString`，字段 `final`。
测试里能直接 `assertEquals(new Ok(55), result)`。**不该用**：需要可变状态、需要继承时。

`sealed interface SumResult permits Ok, Overflow`：旧写法里“结果有两种”只能靠约定（注释、`instanceof` 链加 `else throw`）。现在编译器知道只有这两种。

### J03 + J04 模式匹配 switch 与 record 解构

旧写法：

```java
if (r instanceof Ok) { long v = ((Ok) r).value(); ... }
else if (r instanceof Overflow) { ... }
else { throw new AssertionError(); }
```

新写法：

```java
String text = switch (r) {
    case Ok(var v) -> "ok " + v;
    case Overflow(var exact) -> "overflow " + exact;
};
```

编译器做了：检查所有 `permits` 的类型都被覆盖（**穷尽性**）；一步完成类型判断 + 取字段。加一种新结果类型而没改 `switch`，**编译失败**，而不是运行时才崩。
**不该用 `default`** 来偷懒：`default` 会让编译器不再提醒你漏了新变体。

### J05 switch 表达式

`Width.add` 里 `return switch (this) { case INT -> …; case LONG -> …; };`：每个分支是一个值，没有 `break`，不会 fallthrough；枚举的所有常量必须覆盖。

### J10 虚拟线程 + J11 StructuredTaskScope（预览）

见 5.6 与步骤 8。注意：`StructuredTaskScope` 在 Java 21 是**预览特性**，编译和运行都要 `--enable-preview`（本 kit 的 `jtest.py` 已经加了）。
**不该用虚拟线程的地方**：CPU 密集计算、持有 `synchronized` 的长时间代码（Java 21 里会钉住载体线程）。

### J13 未命名变量 `_`（预览）

`catch (StackOverflowError _)`：声明“我知道有个异常对象，但我不用它”。旧写法 `catch (StackOverflowError e)` 里 `e` 未使用，IDE 会警告。

### J14 Stream API

`IntStream.range(0, chunks).parallel().mapToObj(i -> sumChunk(...)).reduce(Wide.ZERO, Wide::merge)`：对“块下标”并行，而不是对 5000 万个装箱的 `Long`。
`Stream.toList()`（Java 16）返回不可变列表，代替 `collect(Collectors.toList())`。

### J15 数学小工具

`Math.addExact / subtractExact / multiplyExact / toIntExact`、`Math.ceilDiv`（向上取整除法，代替 `(a + b - 1) / b` 的二次溢出风险）、`Long.compareUnsigned`。

### J19 JIT 基础（口头）

见 2.8 与步骤 3。能说出“为什么递归比循环慢”“为什么栈深不稳定”，就够了。

---

## 7. 追问预演

**Q1：为什么 Java 不做 TCO？Scala 和 Kotlin 怎么做到的？**

* 思考过程：先区分“语言规范”和“编译器实现”。Java 规范没有要求；JVM 字节码没有尾调用指令；而栈帧对异常轨迹、调试、`StackWalker` 可见。
* 答案要点：Scala `@tailrec`、Kotlin `tailrec` 在**编译期**把自递归改写成循环（只限自递归）；互递归仍然爆栈，需要 trampoline。
* 可以说出口的话：“JVM 本身没有尾调用优化，因为栈帧对异常轨迹和调试是可见语义的一部分。Scala 和 Kotlin 是在编译期把自递归变成循环，互递归就不行。在 Java 里我会改成循环，或者用 trampoline，把栈换成堆。”

**Q2：你怎么知道会在多深爆栈？**

* 思考过程：这是个“要不要诚实说不确定”的问题。能量出来，但不是常数。
* 答案要点：深度 ≈ 栈大小 ÷ 每帧大小；本机 1 MiB 栈冷启动 17 258 层，预热后 57 996 层；受 JIT（解释帧大、编译帧小）、局部变量个数、`-Xss` 影响。
* 可以说出口的话：“大约每 MiB 栈几万层，但随 JIT 状态变化 3–4 倍，我不会依赖它。要深递归我就用迭代，或给线程指定大栈，或者 trampoline。”

**Q3：溢出时你返回什么？为什么不抛异常？**

* 思考过程：先想“溢出在这个问题里是不是意外”。输入 n 过大是调用方可能遇到的正常情况，所以是业务结果。
* 答案要点：用 sealed `Ok/Overflow`，调用方被迫处理；`Overflow` 带精确值（BigInteger）；内部用 `ArithmeticException`，在公共入口转成值；抛异常有成本，但这里只抛一次。
* 可以说出口的话：“我把溢出定义成返回类型的一部分，编译器强制调用方处理。内部为了简洁用 `addExact` 抛异常，在入口统一转成 `Overflow`。”

**Q4：`n * (n + 1) / 2` 对大 n 有什么问题？**

* 答案要点：乘积先溢出（n = 2³²−1 时乘积是 2⁶⁴−2³²，回绕成 −2³²，除 2 得 −2³¹）；解法：先把偶数那个因子除 2 再乘；`multiplyExact`；中间量溢出时退到 BigInteger。
* 可以说出口的话：“n 和 n+1 一定有一个是偶数，先除再乘，这样乘积只有原来的一半，装得下的范围多一倍。”

**Q5：并行求和，为什么不能每块 `addExact` 再合并？**

* 答案要点：`addExact` 的结果依赖顺序（`[MAX, 1, -1]`）；并行时顺序和块边界任意；用 128 位累加（结合律）或 BigInteger，最后判一次。

**Q6：为什么不用虚拟线程做并行求和？**

* 答案要点：虚拟线程跑在数量 = 核数的载体线程上；不抢占，不增加并行度；实测载体线程限制为 1 个时 12 个虚拟线程 = 顺序；百万个虚拟线程慢 50 倍。CPU 密集用 ForkJoin / parallel stream；I/O 密集才用虚拟线程。

**Q7：浮点数求和能并行吗？**

* 答案要点：`double` 加法不满足结合律（`(a+b)+c ≠ a+(b+c)`），并行结果与切块有关；Kahan 求和 / 成对求和可以降低误差但不消除顺序依赖。

---

## 8. 常见误区

1. **“`catch (StackOverflowError e) { return 0; }`”**——很多人想“让它别崩”。错在：把“栈不够”伪装成合法答案，答案是错的。栈溢出应当让调用方知道，或者从根本上避免（迭代 / trampoline）。
2. **“`n * (n + 1) / 2` 就是正确的 O(1) 解”**——n 在 40 亿量级就会静默出负数（测试 `divideBeforeMultiply`）。正确：先除偶数，再 `multiplyExact`，再用 BigInteger 兜底。
3. **“中间量溢出就报 Overflow”**——`MIN..MAX` 的和是 `Long.MIN_VALUE`，装得下（测试 `intermediateOverflowIsNotResultOverflow`）。要用 BigInteger 复核，而不是看到异常就下结论。
4. **“`a > b` 时返回 0”**——可能是合理的约定，但必须明确；本题约定抛 `IllegalArgumentException`（reconstructed）。面试时要先问清楚。
5. **“并行就是每块各自 `addExact` 再合并”**——顺序相关，见 Q5（测试 `parallelOverflowIsDecidedByTheTrueTotal`：`MAX × 2000 + MIN × 2000` 每块内溢出，总和 −2000 装得下）。
6. **“虚拟线程是更快的线程，所以到处用”**——只对阻塞 I/O 有利，CPU 密集无益（步骤 8）。
7. **“`threshold` 写 0 或 1 都行”**——`threshold = 0` 时区间长度 1 的任务也要继续拆，`mid == from`，无限递归。
8. **“trampoline 能让程序变快”**——不能，每步多一次堆分配（约 2.5 ns/步，比循环慢 10 倍），它只解决栈深。

---

## 9. 自测题

**题 1（概念）**：解释为什么 `sum(n) = n + sum(n-1)` 不是尾递归，而 `step(n, acc) = step(n-1, acc+n)` 是。

<details><summary>答案</summary>

尾递归要求递归调用是函数做的**最后一件事**，返回值直接作为自己的返回值。`n + sum(n-1)` 在调用返回后还要做一次 `n +` 加法，所以必须保留当前栈帧来记住 `n`。
`step` 把已经算好的部分（`acc`）作为参数传下去，递归返回后无事可做，当前帧没用了（理论上可以丢掉）。
</details>

**题 2（计算）**：`int` 里，`sum(65536)` 静默返回什么？为什么？

<details><summary>答案</summary>

真实值 2 147 516 416，超过 2 147 483 647，补码回绕：2 147 516 416 − 2³² = **−2 147 450 880**。
</details>

**题 3（概念）**：为什么 trampoline 能避免 `StackOverflowError`，它的代价是什么？

<details><summary>答案</summary>

每一步函数立即返回一个“待办”对象（栈帧立刻弹出），由外层 `while` 循环取出并执行，所以栈深度恒定。代价：每步在堆上分配对象（`More` + lambda），时间常数比循环大约 10 倍，GC 有压力。
</details>

**题 4（小编程）**：写 `static long sumTo(long n)`：返回 1..n 的和，O(1)，`n < 0` 抛 `IllegalArgumentException`，结果装不下 `long` 就抛 `ArithmeticException`。不准用循环。

<details><summary>答案</summary>

```java
static long sumTo(long n) {
    if (n < 0) throw new IllegalArgumentException("n < 0");
    long b = Math.addExact(n, 1);                       // n = Long.MAX_VALUE 时抛：此时和也必然装不下
    return (n % 2 == 0) ? Math.multiplyExact(n / 2, b)  // n 为偶：先除 n
                        : Math.multiplyExact(n, b / 2); // n 为奇则 n+1 为偶：先除 n+1
}
```

检查：`sumTo(4_294_967_295L)`：n 为奇，`multiplyExact(4294967295, 2147483648) = 9223372034707292160`，装得下；
`sumTo(4_294_967_296L)`：n 为偶，`multiplyExact(2147483648, 4294967297)` 超过 2⁶³−1，抛异常。若先乘后除，前一个例子就会错。
</details>

**题 5（设计）**：把数组并行求和的“块数”设成 1 000 000，会发生什么？设成 1 呢？

<details><summary>答案</summary>

块数过多：任务创建、调度、合并的开销超过每块的计算量（本机虚拟线程 100 万块 190–204 ms，比 12 块慢 50 倍）。块数为 1：没有并行，等同于顺序。合适的块数 ≈ 核数的几倍（让负载均衡又不过度拆分），ForkJoin 里用 `threshold`（本机 10⁵ 个元素）控制。
</details>

**题 6（实验）**：在你自己的机器上运行 `measureDepth(512 * 1024)` 两次（先冷启动、再预热 30 次之后），预测会看到什么？

<details><summary>答案</summary>

预热后的深度会比第一次大几倍（本机 6 161 → 25 228），因为 JIT 编译后的栈帧比解释执行的小。
</details>

---

## 10. 延伸阅读

* 《Structure and Interpretation of Computer Programs》第 1.2.1 节（线性递归与迭代）：为什么“递归的过程”和“递归的写法”是两回事，讲尾递归的经典来源。
* Java 语言规范（JLS）§4.2.2 / §15.18.2：整数运算与溢出规则——确认“Java 整数加法回绕且不抛异常”。
* Java 虚拟机规范（JVMS）§2.5.2「Java Virtual Machine Stacks」与 §6.3：栈、栈帧、`StackOverflowError` 的官方定义。
* `java.lang.Math` 的 Javadoc（`addExact`、`multiplyExact`、`ceilDiv`、`clamp`）：每个方法的溢出语义。
* `java.util.concurrent.ForkJoinPool` / `RecursiveTask` 的 Javadoc：“工作窃取”与阈值选择的官方指导。
* JEP 444（Virtual Threads）：虚拟线程的动机、调度与“不适合 CPU 密集”的官方说明。
* JEP 453（Structured Concurrency, Preview）：`StructuredTaskScope` 的设计。
* JEP 441（Pattern Matching for switch）、JEP 440（Record Patterns）、JEP 409（Sealed Classes）：本题数据建模的语言基础。
* Kotlin 文档「Tail recursive functions」：同一个问题在另一个 JVM 语言里怎么由编译器解决。
