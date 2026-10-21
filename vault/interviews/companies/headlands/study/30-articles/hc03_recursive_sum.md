# hc03 · 递归求 1..n 之和 —— 讲义

> 读者：会写基本 Java（类、方法、循环、递归、数组），其余从零讲。

---

## 1. 这道题在问什么

面试官说：「写一个函数，用**递归**求 1 + 2 + … + n。」一分钟写完，但它是个**脚手架**：之后会不停问「那如果……呢？」，每个“如果”试探你对计算机一个层面是否真懂：

```
写完递归        →  「结果放 int 还是 long？溢出怎么办？」          （整数在计算机里怎么存）
                →  「n = 一百万会怎样？」                          （函数调用在内存里怎么排）
                →  「能不能不爆栈？尾递归呢？」                    （JVM 的限制、trampoline）
                →  「n 很大时有没有更快的办法？」                  （公式、数值陷阱）
                →  「如果是数组里一亿个数求和，怎么并行？」        （线程、ForkJoin、虚拟线程）
```

### 手算一遍

n = 4：`sum(4) = 4 + sum(3) = 4 + (3 + (2 + (1 + sum(0))))`，`sum(0) = 0`（递归的“出口”），回头一层层加：`1`、`3`、`6`、`10`。答案 10。

本题函数的返回类型不是裸 `long`，而是 `SumResult`：`Ok(value)`（装得下）或 `Overflow(exact)`（装不下）。原因见第 4 节。

---

## 2. 前置知识

> 复杂度速记：`O(n)` 线性增长；`O(log n)` n 翻倍只多一步；`O(n²)` 每对元素都处理；`O(1)` 与 n 无关。

### 2.1 递归（recursion）

**是什么**：函数在自己体内调用自己，每次处理更小的同类问题，直到小到能直接回答（**基线条件** base case）。

**为什么需要**：有些问题天然是“大问题 = 一点工作 + 小一点的同类问题”，求和就是 `sum(n) = n + sum(n-1)`。没有基线条件会永不返回。

**怎么工作**：每次调用是一次新的“函数执行”，有自己的参数和局部变量；外层必须**等**内层返回才能继续（这里做加法）。

```java
static long sum(long n) {
    if (n == 0) return 0;      // 基线条件：出口
    return n + sum(n - 1);     // 递归条件：n 加上“更小的问题”的答案
}
```

### 2.2 调用栈与栈帧（call stack, stack frame）

**是什么**：每个线程有一块专用内存叫**调用栈**。每次调用函数就在栈顶压入一个**栈帧**，存这次调用的参数、局部变量、“调用完回到哪一行”；返回时栈顶帧弹出。

**为什么需要**：调用会嵌套（A 调 B，B 调 C），C 返回后要回到 B 中间继续。“最后进来的最先出去”正是栈（后进先出，LIFO）。

用 `sum(3)` 演示（最上面是当前执行的）：

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

关键：**递归求和有 n+1 个栈帧同时存在**，栈深度 = n。每帧几十到上百字节，栈总大小有限。

栈满时 JVM 抛 `StackOverflowError`（是 `Error` 不是 `Exception`：JVM 自身资源耗尽，不是业务错）。默认每线程栈约 1 MiB（`-Xss` 可改，创建线程时也可单独指定），粗估一万到几万层，具体数字见第 4 节。栈帧由 JVM 自动管理，你能控制的是给新线程指定栈大小：

```java
Thread t = new Thread(null, runnable, "name", 64L * 1024 * 1024);   // 第四个参数：栈大小（字节），只是“提示”，OS 可能调整
```

### 2.3 整数、补码、溢出（two's complement, overflow）

计算机用固定个数的二进制位存整数：`int` 32 位，`long` 64 位，所以有上下限：

| 类型 | 位数 | 最小值 | 最大值 |
|---|---|---|---|
| `int` | 32 | −2 147 483 648（−2³¹） | 2 147 483 647（2³¹−1） |
| `long` | 64 | −9 223 372 036 854 775 808（−2⁶³） | 9 223 372 036 854 775 807（2⁶³−1） |

**负数用补码**（two's complement）存。以 8 位为例（32 位同理）：最高位的权重是**负的**。

```
位置:     7     6    5    4    3    2    1    0
权重:  −128   64   32   16    8    4    2    1

 5   = 0000 0101   =  4 + 1                        = 5
 127 = 0111 1111   =  64+32+16+8+4+2+1             = 127   ← 8 位能表示的最大正数
−1   = 1111 1111   = −128 + 64+32+16+8+4+2+1       = −1
−128 = 1000 0000   = −128                          ← 8 位能表示的最小数
```

**溢出**：结果超出范围时，硬件只保留低位，结果“绕回去”：

```
  0111 1111   (127)
+ 0000 0001   (  1)
-------------
  1000 0000   = −128       ← 127 + 1 变成了 −128！没有报错。
```

`int` 同理：`Integer.MAX_VALUE + 1 == Integer.MIN_VALUE`。**Java 整数加法不抛异常**——答案错了程序照常运行，最危险。

**对本题**：1 + … + n 约 n²/2 增长。`int` 在 **n = 65 536** 就装不下：1+…+65 535 = 2 147 450 880（刚好小于上限），再加 65 536 得 2 147 516 416，绕回成 **−2 147 450 880**。`long` 在 **n = 2³² = 4 294 967 296** 装不下。

用“精确”运算，溢出时抛 `ArithmeticException`：

```java
int a = Math.addExact(x, y);          // int 版本
long b = Math.addExact(p, q);         // long 版本
int c = Math.toIntExact(someLong);    // long → int，装不下就抛
// 还有 subtractExact / multiplyExact / negateExact / incrementExact
```

热点代码里 JIT 会把 `Math.addExact` 编译成“一条加法 + 检查溢出标志位”，开销很小。

### 2.4 尾调用与“JVM 为什么没有 TCO”（tail call, TCO）

**尾调用**：函数做的**最后一件事**是调用另一个函数，并直接把它的返回值当自己的返回值。

```java
return n + sum(n - 1);        // 不是尾调用：调用返回后还要做 “n +”
return step(n - 1, acc + n);  // 是尾调用：调用就是最后一件事（把 acc 传下去，答案在 acc 里）
```

尾调用返回后，当前栈帧里的东西**再也用不到**，聪明的编译器可**复用/丢掉当前帧**，让尾递归像循环一样只占常数个栈帧——**尾调用优化**（TCO）。Scheme、Haskell 保证 TCO，所以敢用递归当循环。

**Java 没有 TCO**：`javac` 不做，JIT 也不保证。常见理由是栈帧对语义可见：异常栈轨迹（stack trace）、`StackWalker`、调试器、历史上按调用栈判断权限的安全检查，都依赖“每次调用有一个帧”。Scala `@tailrec`、Kotlin `tailrec` 是**编译期把“自己调用自己”改写成循环**——只处理自递归，A 调 B、B 调 A 不行。所以 Java 想要深递归：改循环、用 trampoline（下节）、或加大栈。

### 2.5 Trampoline（蹦床）

**是什么**：“手动实现的尾调用优化”：函数不直接调用下一步，而是**返回一个描述‘下一步做什么’的对象**；外层循环不断取出并执行，直到拿到答案。

**为什么需要**：递归爆栈是因为每次调用叠一个栈帧。若每步**立刻返回**（帧立刻弹出），把“待办”放到**堆**（容量比栈大得多，由 GC 管理）上由循环驱动，栈深度就恒定。

```
普通递归：  step(3) → step(2) → step(1) → step(0)      栈帧叠 4 层
                                                        
trampoline： run 循环                                   栈永远只有 run 的 1 帧
   cur = step(3)      返回 More(下一步)   ← step(3) 的帧已弹出
   cur = cur.next()   返回 More(下一步)   ← step(2) 的帧已弹出
   cur = cur.next()   返回 More(下一步)
   cur = cur.next()   返回 Done(结果)     → 循环结束，返回结果
```

本题写法（用 sealed 接口表达“二选一”）：

```java
sealed interface Trampoline<T> permits Done, More {}
record Done<T>(T value) implements Trampoline<T> {}                       // 算完了
record More<T>(Supplier<Trampoline<T>> next) implements Trampoline<T> {}  // 还有下一步（Supplier = 一个“稍后再算”的函数）
```

代价：每步在堆上分配一个 `More` 和一个 lambda，比循环慢（数字见第 4 节）。**trampoline 解决“不爆栈”，不解决“更快”。**

### 2.6 求和公式与奇偶（closed form）

高斯：`1 + 2 + … + n = n(n+1)/2`（头尾配对，每对和为 `n+1`，共 `n/2` 对）。一般地 a 到 b（含）之和 `= (a + b) × (b − a + 1) / 2`：首项加末项，乘项数，除以 2。对负数也成立。

O(1) 时间、不爆栈，但有**数值陷阱**：先乘后除时，**乘积会先溢出**，即使最终答案装得下。

**避免**：`(a + b)` 与 `(b − a + 1)` 的差是 `2a − 1`（奇数），所以奇偶**相反**，**必有一个是偶数**。先把偶数那个除以 2（整除无余数）再相乘，乘积只有“先乘后除”的一半大。
例：n = 2³²−1 = 4 294 967 295：`n × (n+1) = 2⁶⁴ − 2³²` 超出 `long`；先除 2 得 `2 147 483 648 × 4 294 967 295 = 9 223 372 034 707 292 160`，装得下。

### 2.7 BigInteger

标准库里“位数不限”的整数类，无溢出，代价是慢（堆对象，运算是方法调用）。用作“慢但永远正确”的备选，也用来**验证**快速实现。

```java
BigInteger x = BigInteger.valueOf(a).add(BigInteger.valueOf(b));
x.multiply(y); x.shiftRight(1);   // 右移 1 位 = 除以 2（向负无穷取整；这里被除数是偶数，所以精确）
x.bitLength();                    // 表示这个数（不含符号位）需要的位数，≤ 63 说明 long 装得下
x.longValueExact();               // 装不下就抛 ArithmeticException
```

### 2.8 JIT 编译与内联（JIT, inlining）

JVM 先**解释**执行字节码；发现方法被频繁调用（“热点”）后，JIT 编译器（HotSpot 的 C1、C2）把它编译成机器码。**内联**（inlining）把被调方法的代码**直接贴到调用处**，省掉压栈、跳转、返回，并让编译器看到更大范围做优化。

**对本题**：循环能被大幅优化（展开、去重复检查）；**递归只能内联一两层**（HotSpot 默认 `MaxRecursiveInlineLevel=1`），每层仍是真函数调用。`-XX:+PrintInlining` 对递归方法输出 `recursive inlining too deep`。副作用：同一递归方法**解释执行**时的栈帧比**编译后**大几倍，“能递归多深”不是常数。

### 2.9 线程、并行、ForkJoin、虚拟线程（步骤 7、8 用到）

**线程**是一条独立执行流。**平台线程**就是操作系统线程，创建切换较贵，数量有限（几千个）。**CPU 核**是真正同时执行代码的硬件单元；线程数多于核数时 OS 轮流给时间片。

**并行**（parallelism）：多个任务**真的同时**在不同核上跑，为了更快。**并发**（concurrency）：多个任务**交替**推进（等 I/O 时让别的任务用 CPU），为了同时处理很多事，不一定更快。

**ForkJoinPool**：专为“大任务拆小任务再合并”设计的线程池。`RecursiveTask<T>.compute()` 里：小任务直接算；大任务拆两半，`fork()` 一半交给池（空闲线程可“偷”走）、自己算另一半、再 `join()`。**parallel stream** 把管道交给公共的 `ForkJoinPool.commonPool()`。

**虚拟线程**（Java 21 正式）：由 JVM 调度的轻量线程，可开几十万个。运行时挂在少量**载体线程**（carrier thread，一个 ForkJoinPool，默认大小 = 核数）上；只有**阻塞**（等网络、锁、`sleep`）时才摘下来让载体线程跑别的。**所以虚拟线程让“大量在等待的任务”很便宜，但不增加计算能力**；只算不阻塞的虚拟线程会一直霸占载体线程，无时间片抢占。

**内存带宽**：对 `long[]` 求和，瓶颈是把数据读进 CPU 的速度而非加法，所以核再多加速也有上限。5000 万个 long = 400 MB，顺序求和 17 ms ≈ 23 GB/s，并行只能再快 4–5 倍。

### 2.10 Java 21 语法速览

* `record`：自动生成构造器、访问器、`equals/hashCode/toString` 的不可变数据类。
* `sealed interface X permits A, B`：`X` 只能有 `A`、`B` 两种实现，编译器据此检查 `switch` 是否覆盖全。
* 模式匹配 `switch`：`case A(var f) -> …; case B b -> …`，一步判断类型并取字段。细节见第 6 节。

---

## 3. 从最笨的解法开始

```java
static int sum(int n) {
    if (n == 0) return 0;
    return n + sum(n - 1);
}
```

* **复杂度**：时间 O(n)；栈空间 O(n)。这里 n 是输入整数本身，不是输入“长度”。
* **错/慢在哪**：
  1. `sum(65536)` 应为 2 147 516 416，但 `int` 装不下，**静默**变成 −2 147 450 880。
  2. 改成 `long`，`sum(1_000_000)` 在默认栈上也 `StackOverflowError`。默认 1 MiB 栈下 `sumToRecursive(65536)` 就爆栈（`40000` 还行）——**栈比 `int` 先出问题**。
  3. `long` 溢出的 n = 4 294 967 296 需 43 亿次递归，栈撑不到，递归版**根本测不出 long 溢出**。

这三条是后面所有改进的动力。

---

## 4. 一步一步改进

### 步骤 1：让溢出“看得见”——checked 加法 + 结果类型

* **问题**：静默回绕是最坏的 bug。
* **想法**：`Math.addExact`，溢出抛 `ArithmeticException`。
* **但抛异常不够好**：调用方可能忘了 `catch`；且“溢出”在此是**可预期的业务结果**（n 太大），不是程序错误。返回特殊值（如 −1）也不行：区间求和（步骤 7）里负数是合法结果，魔法数会和合法结果混淆。
* **正确**：把“可能溢出”写进**返回类型**：

  ```java
  sealed interface SumResult permits Ok, Overflow {}
  record Ok(long value) implements SumResult {}
  record Overflow(BigInteger exact) implements SumResult {}   // 顺便带上数学上的精确值，方便调用方降级
  ```

  调用方用 `switch` 处理，**编译器强制处理 `Overflow`**。`ArithmeticException` 只在实现内部用，公共入口转成值。
* **便于验证**：加 `Width { INT, LONG }` 枚举，让累加器可用 `int` 宽度，`INT` 在 n = 65 536 就溢出，不需要 43 亿次递归。
* 复杂度不变：时间 O(n)，栈 O(n)。

### 步骤 2：测量栈深——`StackOverflowError` 发生在多深？

* “n = 100 万会怎样”要用数据回答。**做法**：新开线程、指定栈大小、递归到爆、数层数（`measureDepth`）。

  | 线程栈 | 冷启动第一次 | 预热之后 |
  |---|---|---|
  | 512 KiB | 6 161 | 25 228 |
  | 1 MiB | 17 258 | 57 996 |
  | 8 MiB | — | 516 748 |
  | 64 MiB | — | 4 186 764 |

  结论：①大致与栈大小成正比；②**同一 JVM 里预热前后差 3–4 倍**（解释执行的帧比 JIT 编译后的大）；③不能依赖固定数字。
* 这只量出了界限，还没解决。

### 步骤 3：最简单的解决——改成循环

* 递归求和不需要“回来之后继续”，循环里一个变量 `acc` 累加就够：

  ```java
  long acc = 0;
  for (long i = 1; i <= n; i++) acc = w.add(acc, i);
  ```

* 时间 O(n)，栈 O(1)。`n = 3×10⁸` 只需约 77 ms。
* **为什么比递归快这么多**：`n = 10 000` 重复 20 000 次（2×10⁸ 步），递归约 570–650 ms（≈ 3 ns/步），循环约 50 ms（≈ 0.25 ns/步）。递归每步是真函数调用（压栈帧、栈检查、返回），JIT 只能内联一层；循环能展开，`addExact` 变成一条加法加溢出检查。

若面试官说“必须用递归”，继续往下。

### 步骤 4：尾递归形式 + trampoline

* **问题**：想保留递归写法，又不要栈深度 O(n)。
* **想法 A：尾递归**——把“到目前为止的和”作为参数传下去，让递归调用成为最后一件事：

  ```java
  static long step(long n, long acc) { return n == 0 ? acc : step(n - 1, acc + n); }
  ```

  Scala/Kotlin（`tailrec`）会编译成循环，**Java 不会**（2.4）：仍叠 n 层栈帧。
* **想法 B：trampoline**（2.5）：`step` 不直接调用自己，返回“下一步”对象，`run` 里 `while` 驱动：

  ```java
  static Trampoline<Long> step(long n, long acc, Width w) {
      return n == 0 ? new Done<>(acc) : new More<>(() -> step(n - 1, w.add(acc, n), w));
  }
  ```

  注意 `w.add(acc, n)` 写在 **lambda 里面**，在 `run` 的循环里执行，而不是在 `step` 的帧里叠起来。
* **为什么行**：每个 `step` 立刻返回，栈深度恒为 1–2。
* 时间 O(n)，栈 O(1)，堆上每步一个短命对象（活跃对象 O(1)）。`n = 5×10⁶` 约 14 ms；每步约 2.5 ns（比循环慢 10 倍，与递归同量级）。
* **互递归**：`isEven(n) = n == 0 ? true : isOdd(n-1)`，`isOdd(n) = n == 0 ? false : isEven(n-1)`。连 `@tailrec` 都不处理，trampoline 可以：两个函数都写成返回 `Trampoline<Boolean>`。512 KiB 栈上也能跑到 n = 200 万。

### 步骤 5：闭式公式

* **问题**：循环仍 O(n)，n = 10¹⁸ 要几十年。**想法**：高斯公式 O(1)（2.6）。
* **数值陷阱**：`n * (n + 1) / 2` 先算乘积。n = 4 294 967 295 时乘积 2⁶⁴ − 2³²，`long` 装不下，补码绕回 −2³²，除 2 得 **−2 147 483 648**——无异常，答案却是负数。
* **改进**：先除后乘（2.6）：`(a+b)` 与 `(b−a+1)` 一奇一偶，偶的先除 2，再 `Math.multiplyExact`。

### 步骤 6：区间 [a, b]、负数、中间量溢出 ≠ 结果溢出

* **问题**：推广到 a..b（可负）时，`a + b` 和 `b − a + 1` **自己**会溢出：`a = MIN, b = MAX` 时 `b − a + 1` 是 2⁶⁴；`a = b = MAX` 时 `a + b` 溢出。
* **但**中间量溢出**不等于结果溢出**：`MIN..MAX` 的和，除 `MIN` 外两两抵消，剩 `MIN`，恰为 `Long.MIN_VALUE`，装得下！`MAX..MAX` 的和就是 `MAX`。
* **想法**：快路径用 `addExact/subtractExact/multiplyExact`；任何一步抛异常就**退到 `BigInteger`** 算精确值，再用 `bitLength() <= 63` 判断装不装得下 `long`。
* O(1)（快路径无分配；退路径 BigInteger 常数大）。

### 步骤 7：数组并行求和，“求和顺序”会影响溢出判断

* **场景**：`long[]` 里 5000 万个数求和，想用多核。**想法**：切块，每块算部分和再合并（ForkJoin：`fork` 左半、自己算右半、`join`）。
* **陷阱**：每块用 `Math.addExact` 累加再用 `addExact` 合并，结果**依赖顺序**。例 `[MAX, 1, -1]`：真实和 `MAX` 装得下，但从左到右 `MAX + 1` 就抛异常。并行时块边界任意，同一份数据换个切法会时而抛时而不抛。
* **想法**：用 **128 位累加器** `Wide(hi, lo)`：不溢出，加法满足结合律（先加谁后加谁结果一样），最后只判一次“`hi:lo` 是否在 `long` 范围内”。
  - 加有符号 `long x`：`lo` 当无符号数相加；结果比原 `lo` 小说明进位（回绕），`hi` 加 1；`x` 的“高 64 位”是符号扩展，`x ≥ 0` 为 0，`x < 0` 为 −1（`x >> 63`）。
  - 装得下：`hi == (lo >> 63)`（`hi` 必须等于 `lo` 符号位的扩展）。
* **三种并行实现**：`parallelSumForkJoin`（手写 `RecursiveTask`，区间 ≤ threshold 直接算）、`parallelSumStream`（对**块下标**做 parallel stream，别对装箱的 `Long` 流并行）、`sumVirtual`（下一步）。

### 步骤 8：虚拟线程——为什么不适合 CPU 密集

* “每块开一个虚拟线程”看着很现代。数据（12 核，5000 万 long）：

  | 实现 | 时间 |
  |---|---|
  | 顺序 128 位 | 16–18 ms |
  | ForkJoin（threshold = 10⁵） | 3–4 ms |
  | parallel stream（块下标） | 4 ms |
  | 虚拟线程，12 块 | 4–5 ms |
  | 虚拟线程，10 000 块 | 4–8 ms |
  | 虚拟线程，1 000 000 块 | 190–204 ms |
  | 虚拟线程，12 块，载体线程只有 1 个（`-Djdk.virtualThreadScheduler.parallelism=1`） | 17 ms |

* **解读**：12 块时与 ForkJoin 一样快，是因为载体线程恰有 12 个——**并行度来自载体线程，不是虚拟线程**。载体限为 1 个，12 个虚拟线程立刻退化成顺序（17 ms）。百万个虚拟线程只增加创建调度开销（慢 50 倍）。因此：**CPU 密集用 ForkJoin / parallel stream，线程数 ≈ 核数；虚拟线程用于大量阻塞 I/O。**

---

## 5. 逐段讲解法

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

* `sealed … permits`：结果只有两种，调用方 `switch` 漏一种就编译不过。
* `Width.add`：两个 `int` 范围内的数在 `long` 里相加**绝不溢出**，所以先用 `long` 算 `s`，`INT` 时再 `Math.toIntExact(s)` 检查是否还在 `int` 范围（不在抛 `ArithmeticException`）；`LONG` 时 `Math.addExact` 自己检查。
* 直接 `int` 相加再比较需要自己判回绕（`((a ^ s) & (b ^ s)) < 0` 这类位技巧），易写错。

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

* `try/catch` 在入口而非递归里：统一“内部用异常，边界转成值”的风格更清楚。
* **`StackOverflowError` 不捕获**，直接传给调用方；吞掉（返回 0 或 `Overflow`）会把“栈不够”误报成别的东西。
* `exactTo(n)`：`BigInteger` 版 `n(n+1)/2`，只在出错路径算一次。
* 加法发生在递归**返回之后**（`w.add(n, 子结果)`），所以**不是**尾递归。

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

* 计数放**对象字段**：栈溢出瞬间没法返回值，字段是唯一带出结果的办法。
* `catch (StackOverflowError _)`：`_` 是“不需要这个变量”的未命名变量（Java 21 预览）。
* 用新线程：栈大小是**线程**属性，只有构造 `Thread` 时能指定；也避免撑爆调用者线程的栈。

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

* `switch` 对 sealed 类型做**模式匹配**：`case Done<T>(var v)` 同时判断类型并取字段到 `v`；无 `default`，编译器知道只有两个实现。
* `cur = next.get()` 执行“下一步”得到新 `Trampoline`；栈帧在每次 `next.get()` 返回时已弹出，栈深恒定。

```java
private static Trampoline<Long> step(long n, long acc, Width w) {
    return n == 0 ? new Done<>(acc) : new More<>(() -> step(n - 1, w.add(acc, n), w));
}
```

* `w.add(acc, n)` 在 lambda 里，延迟到 `run` 循环才执行。写成 `new More<>(step(n - 1, w.add(acc, n), w))` 这种急切求值，就把递归又写回栈上。
* 溢出时 `w.add` 抛 `ArithmeticException`，从 `run` 一路抛到 `sumToTrampoline` 入口转成 `Overflow`。

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

* `(count & 1) == 0` 位与判偶（`count` 非负时等价 `count % 2 == 0`）。`count` 为偶则 `s` 必为奇，故除 `count`，反之除 `s`。`s / 2` 里 `s` 是偶数，负数也是精确除法，无“向零取整”问题。
* 快路径无分配；慢路径仅在中间量溢出时进入，用 `BigInteger` 保证正确。
* `bitLength() <= 63`：`bitLength()` 不含符号位，−2⁶³..2⁶³−1 都满足 ≤ 63（−2⁶³ 恰为 63）。

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

* `lo + x` 在 `long` 里按补码相加；把 `lo` 当**无符号**数比较，若 `nlo` 比 `lo` 小，说明越过 2⁶⁴ 丢了进位，补到 `hi`。
* `x >> 63` 算术右移：非负得 0，负得 −1（全 1）——`x` 符号扩展到高 64 位。
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

* `>>> 1` 而非 `/ 2`：`from + to` 溢出成负数时，`/ 2` 得负，`>>> 1`（无符号右移）仍得正确中点——经典二分 bug。
* 只 `fork` 左半，右半在**当前线程**算：避免两半都 fork、当前线程空等的一次调度。
* `sumChunk` 循环里用局部变量 `hi`、`lo`，不建 `Wide` 对象，否则 5000 万次分配压垮 GC。

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

* `StructuredTaskScope`（Java 21 预览）：一组子任务绑在一个“作用域”里，`try` 块退出前所有子任务必须结束；一个失败其余被取消。`scope.fork` 默认每个子任务一个虚拟线程。
* 旧写法 `new Thread` + `join`，或 `ExecutorService` + `Future.get`，要自己保证异常时关闭、取消其余。

---

## 6. Java 21 特性小课

### record 与 sealed

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

新写法：`public record Ok(long value) implements SumResult {}`。编译器生成构造器、访问器、`equals/hashCode/toString`，字段 `final`，结果可直接 `equals` 比较（`new Ok(55)`）。**不该用**：需要可变状态、需要继承时。

`sealed interface SumResult permits Ok, Overflow`：旧写法“结果有两种”只能靠约定（注释、`instanceof` 链加 `else throw`），现在编译器知道。

### 模式匹配 switch 与 record 解构

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

编译器检查所有 `permits` 类型都被覆盖（**穷尽性**），一步完成类型判断 + 取字段。加新结果类型而没改 `switch`，**编译失败**而非运行时崩。**别用 `default` 偷懒**：它会让编译器不再提醒你漏了新变体。

### switch 表达式

`Width.add` 里 `return switch (this) { case INT -> …; case LONG -> …; };`：每个分支是一个值，无 `break`、无 fallthrough，枚举常量必须覆盖。

### 虚拟线程 + StructuredTaskScope（预览）

见 5.6 与步骤 8。`StructuredTaskScope` 在 Java 21 是**预览特性**，编译和运行都要 `--enable-preview`。**不该用虚拟线程**：CPU 密集计算、长时间持有 `synchronized`（Java 21 会钉住载体线程）。

### 未命名变量 `_`（预览）

`catch (StackOverflowError _)`：声明“有异常对象但不用”。旧写法 `catch (StackOverflowError e)` 里 `e` 未使用，IDE 会警告。

### Stream API 与数学小工具

`IntStream.range(0, chunks).parallel().mapToObj(i -> sumChunk(...)).reduce(Wide.ZERO, Wide::merge)`：对“块下标”并行，而非对 5000 万个装箱的 `Long`。`Stream.toList()`（Java 16）返回不可变列表。`Math.addExact / subtractExact / multiplyExact / toIntExact`、`Math.ceilDiv`（向上取整除，代替有溢出风险的 `(a + b - 1) / b`）、`Long.compareUnsigned`。

### JIT 基础（口头）

能说出“为什么递归比循环慢”“为什么栈深不稳定”（2.8、步骤 3）就够了。

---

## 7. 追问预演

**Q1：为什么 Java 不做 TCO？Scala 和 Kotlin 怎么做到的？**

* 思考：区分“语言规范”和“编译器实现”。Java 规范没要求；字节码没有尾调用指令；栈帧对异常轨迹、调试、`StackWalker` 可见。
* 要点：Scala `@tailrec`、Kotlin `tailrec` 在**编译期**把自递归改写成循环（只限自递归）；互递归仍爆栈，需要 trampoline。
* 说出口：“JVM 没有尾调用优化，因为栈帧对异常轨迹和调试是可见语义。Scala 和 Kotlin 编译期把自递归变循环，互递归不行。在 Java 里我改循环，或用 trampoline 把栈换成堆。”

**Q2：你怎么知道会在多深爆栈？**

* 思考：能量出来，但不是常数，要诚实说。
* 要点：深度 ≈ 栈大小 ÷ 每帧大小；1 MiB 栈冷启动 17 258 层，预热后 57 996 层；受 JIT（解释帧大、编译帧小）、局部变量个数、`-Xss` 影响。
* 说出口：“大约每 MiB 栈几万层，但随 JIT 状态变 3–4 倍，我不依赖它。要深递归就迭代，或给线程大栈，或 trampoline。”

**Q3：溢出时返回什么？为什么不抛异常？**

* 思考：溢出在此是不是意外？输入 n 过大是调用方可能遇到的正常情况，所以是业务结果。
* 要点：sealed `Ok/Overflow` 迫使调用方处理；`Overflow` 带精确值（BigInteger）；内部用 `ArithmeticException`，入口转成值；异常有成本，但这里只抛一次。
* 说出口：“我把溢出定义成返回类型的一部分，编译器强制调用方处理。内部为简洁用 `addExact` 抛异常，入口统一转成 `Overflow`。”

**Q4：`n * (n + 1) / 2` 对大 n 有什么问题？**

* 要点：乘积先溢出（n = 2³²−1 时乘积 2⁶⁴−2³²，回绕成 −2³²，除 2 得 −2³¹）；解法：偶数因子先除 2 再乘、`multiplyExact`、中间量溢出退到 BigInteger。
* 说出口：“n 和 n+1 必有一个偶数，先除再乘，乘积只有原来一半，装得下的范围多一倍。”

**Q5：并行求和为什么不能每块 `addExact` 再合并？**

* 要点：`addExact` 结果依赖顺序（`[MAX, 1, -1]`），并行时顺序和块边界任意；用 128 位累加（结合律）或 BigInteger，最后判一次。

**Q6：为什么不用虚拟线程做并行求和？**

* 要点：虚拟线程跑在数量 = 核数的载体线程上，不抢占、不增加并行度；载体限为 1 时 12 个虚拟线程 = 顺序；百万个慢 50 倍。CPU 密集用 ForkJoin / parallel stream，I/O 密集才用虚拟线程。

**Q7：浮点数求和能并行吗？**

* 要点：`double` 加法不满足结合律（`(a+b)+c ≠ a+(b+c)`），并行结果与切块有关；Kahan 求和 / 成对求和降低误差但不消除顺序依赖。

---

## 8. 常见误区

1. **“`catch (StackOverflowError e) { return 0; }`”**——想让它别崩，但把“栈不够”伪装成合法答案，答案是错的。应让调用方知道，或从根本避免（迭代 / trampoline）。
2. **“`n * (n + 1) / 2` 就是正确的 O(1) 解”**——n 到 40 亿量级静默出负数。正确：先除偶数，再 `multiplyExact`，BigInteger 兜底。
3. **“中间量溢出就报 Overflow”**——`MIN..MAX` 的和是 `Long.MIN_VALUE`，装得下。用 BigInteger 复核，别看到异常就下结论。
4. **“`a > b` 时返回 0”**——可能是合理约定但必须明确；本题抛 `IllegalArgumentException`。面试要先问清楚。
5. **“并行就是每块各自 `addExact` 再合并”**——顺序相关（Q5）。例：`MAX × 2000 + MIN × 2000` 每块内溢出，总和 −2000 装得下。
6. **“虚拟线程是更快的线程，到处用”**——只对阻塞 I/O 有利，CPU 密集无益（步骤 8）。
7. **“`threshold` 写 0 或 1 都行”**——`threshold = 0` 时长度 1 的任务也要继续拆，`mid == from`，无限递归。
8. **“trampoline 能让程序变快”**——不能，每步多一次堆分配（约 2.5 ns/步，比循环慢 10 倍），只解决栈深。

---

## 9. 自测题

**题 1（概念）**：为什么 `sum(n) = n + sum(n-1)` 不是尾递归，而 `step(n, acc) = step(n-1, acc+n)` 是？

<details><summary>答案</summary>

尾递归要求递归调用是**最后一件事**，返回值直接作为自己的返回值。`n + sum(n-1)` 调用返回后还要做 `n +`，必须保留栈帧记住 `n`。`step` 把算好的部分（`acc`）作参数传下去，返回后无事可做，当前帧没用了。
</details>

**题 2（计算）**：`int` 里 `sum(65536)` 静默返回什么？为什么？

<details><summary>答案</summary>

真实值 2 147 516 416 超过 2 147 483 647，补码回绕：2 147 516 416 − 2³² = **−2 147 450 880**。
</details>

**题 3（概念）**：trampoline 为什么能避免 `StackOverflowError`？代价是什么？

<details><summary>答案</summary>

每步立即返回一个“待办”对象（栈帧立刻弹出），由外层 `while` 取出执行，栈深恒定。代价：每步堆上分配（`More` + lambda），时间常数约比循环大 10 倍，有 GC 压力。
</details>

**题 4（小编程）**：写 `static long sumTo(long n)`：返回 1..n 之和，O(1)，`n < 0` 抛 `IllegalArgumentException`，装不下 `long` 抛 `ArithmeticException`。不准用循环。

<details><summary>答案</summary>

```java
static long sumTo(long n) {
    if (n < 0) throw new IllegalArgumentException("n < 0");
    long b = Math.addExact(n, 1);                       // n = Long.MAX_VALUE 时抛：此时和也必然装不下
    return (n % 2 == 0) ? Math.multiplyExact(n / 2, b)  // n 为偶：先除 n
                        : Math.multiplyExact(n, b / 2); // n 为奇则 n+1 为偶：先除 n+1
}
```

检查：`sumTo(4_294_967_295L)`：n 为奇，`multiplyExact(4294967295, 2147483648) = 9223372034707292160`，装得下；`sumTo(4_294_967_296L)`：n 为偶，`multiplyExact(2147483648, 4294967297)` 超过 2⁶³−1，抛异常。先乘后除则前一个例子就错。
</details>

**题 5（设计）**：数组并行求和块数设成 1 000 000 会怎样？设成 1 呢？

<details><summary>答案</summary>

块数过多：任务创建、调度、合并开销超过每块计算量（虚拟线程 100 万块 190–204 ms，比 12 块慢 50 倍）。块数为 1：无并行，等同顺序。合适约核数的几倍（负载均衡又不过度拆分），ForkJoin 用 `threshold`（10⁵ 个元素）控制。
</details>

**题 6（实验）**：运行 `measureDepth(512 * 1024)` 两次（冷启动、再预热 30 次后），预测会看到什么？

<details><summary>答案</summary>

预热后深度比第一次大几倍（6 161 → 25 228），因为 JIT 编译后的栈帧比解释执行的小。
</details>

---

「延伸」SICP 第 1.2.1 节（线性递归与迭代）。
