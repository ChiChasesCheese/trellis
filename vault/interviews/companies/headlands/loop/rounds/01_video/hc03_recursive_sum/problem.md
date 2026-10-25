# hc03 · 递归求和 1..n（面试官一路追问）

## 读题前你需要知道

这组题把几个“看起来是语言细节、其实是 JVM / 计算机原理”的概念串在一起：**调用栈与栈帧**（递归为什么会爆栈）、**补码与整数溢出**（`int`/`long` 为什么会“绕回去”）、
**尾调用与 trampoline**（为什么 Java 不能把递归自动变循环）、**线程与并行**（`ForkJoin`、虚拟线程各适合什么）。
你只需要会写基本的 Java（类、方法、递归、循环、数组）。

## 背景

面试官让你「写个函数，递归求 1 到 n 的和」。这不是考算法，是一个**脚手架**：他每问一句，就看你对 Java 的一个层面懂不懂——
返回类型怎么设计、溢出、JVM 的栈、JIT、闭式公式的数值陷阱、并行。每个 Part 对应一轮追问。

## 公共类型（starter 已给出）

```java
public sealed interface SumResult permits Ok, Overflow {}
public record Ok(long value) implements SumResult {}
public record Overflow(BigInteger exact) implements SumResult {}   // 带数学上的精确值
public enum Width { INT, LONG }   // 累加器位宽；INT 让溢出在 n = 65536 就发生
```

所有「溢出」的语义统一：**数学上的真实和放不进该位宽 ⇒ `Overflow(exact)`**，`exact` 是精确值；绝不返回回绕后的错误数。

## Part 1 · 朴素递归 + checked overflow

| 签名                                                        | 内容                                                                                                                                                                      |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `static SumResult sumToRecursive(long n, Width w)`          | `sum(n) = n + sum(n-1)`；`n < 0` → `IllegalArgumentException`；加法用 `Math.addExact`，`ArithmeticException` 转成 `Overflow(exactTo(n))`；**`StackOverflowError` 不要吞** |
| `Width.add(long, long)` · `static BigInteger exactTo(long)` | 检查加法（INT 位宽额外 `Math.toIntExact`）· 精确值                                                                                                                        |

- `INT`：`n = 65535` → `Ok(2147450880)`；`n = 65536` → `Overflow(2147516416)`。
- 测试在 512 MiB 栈的线程里跑 `n = 65536`——默认 1 MiB 栈上 `sumToRecursive(65536)` 先抛 `StackOverflowError`（`n = 40000` 还行），
  **栈比 int 先“溢出”**，这是 Part 2 的伏笔。

## Part 2 · 栈深：为什么没有 TCO，怎么办

| 签名                                                                                    | 内容                                                                                |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `static int measureDepth(long stackBytes)`                                              | 在指定栈大小的新线程里一路递归到 `StackOverflowError`，返回深度                     |
| `static SumResult sumToIterative(long n, Width w)`                                      | 迭代版，语义同 Part 1                                                               |
| `sealed interface Trampoline<T> permits Done, More` + `static <T> T run(Trampoline<T>)` | `Done(value)` / `More(Supplier<Trampoline<T>>)`；`run` 是 `while` + 模式匹配 switch |
| `static SumResult sumToTrampoline(long n, Width w)`                                     | 尾递归形式（累加器参数）+ trampoline                                                |
| `static boolean isEven(long n)`                                                         | 互递归 `even/odd`，trampoline 跑到 2 000 000                                        |

- 在 512 KiB 栈上：`sumToRecursive(1_000_000)` 必须抛 `StackOverflowError`；`sumToTrampoline` / `sumToIterative` 必须返回 `Ok(500000500000)`。
- `measureDepth(64 MiB)` 必须远深于 `measureDepth(512 KiB)`（> 4 倍）。

## Part 3 · 区间 [a, b]：负数、long / BigInteger、闭式

| 签名                                              | 内容                                                    |
| ------------------------------------------------- | ------------------------------------------------------- |
| `static BigInteger rangeSumExact(long a, long b)` | 精确值；`a > b` → `IllegalArgumentException`            |
| `static SumResult rangeSum(long a, long b)`       | long 装得下 `Ok`，否则 `Overflow(exact)`；`a > b` → IAE |
| `static long naiveClosedForm(long n)`             | **已给出**的错误写法 `n*(n+1)/2`，测试拿它对比          |

要点：`(a+b)` 与 `(b-a+1)` **奇偶相反**，把偶的那个先除 2 再 `multiplyExact`；`a+b`、`b-a+1` 自己也可能溢出，
但**中间量溢出 ≠ 结果溢出**（`rangeSum(Long.MIN_VALUE, Long.MAX_VALUE)` 是 `Ok(Long.MIN_VALUE)`），所以快路径失败后退到 BigInteger 再判断是否装得下。

## Part 4 · 并行求和（对象：`long[] data`）

| 签名                                                          | 内容                                                                                   |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `record Wide(long hi, long lo)`                               | 128 位补码累加器：`plus(long)` · `merge(Wide)` · `fitsLong()` · `toBigInteger()`       |
| `static SumResult checkedSum(long[])`                         | 顺序基线；**只有真实总和放不进 long 才 `Overflow`**（`[MAX, 1, -1]` 是 `Ok(MAX)`）     |
| `static SumResult parallelSumForkJoin(long[], int threshold)` | `RecursiveTask`，≤ threshold 直接算，否则 fork 左 / 算右 / join；`threshold < 1` → IAE |
| `static SumResult parallelSumStream(long[])`                  | 按块下标并行的 parallel stream                                                         |
| `static SumResult sumVirtual(long[], int chunks)`             | 每块一个虚拟线程（`StructuredTaskScope`，预览 API）；`chunks < 1` → IAE                |

为什么要 `Wide`：逐步 `addExact` 的结果**取决于求和顺序**（`[MAX, 1, -1]`），并行时每块的顺序更是任意；128 位累加满足结合律，
块怎么切都得到同一个答案，最后只判一次「放不放得进 long」。三种并行实现对同一输入必须与 `checkedSum` 逐字相等（含 `Overflow.exact`）。

## 边界清单

- `n = 0`、`n = 1`、`n < 0`；`Long.MAX_VALUE` 附近的 `n`（只能走闭式，迭代要 40 亿步）
- INT 位宽 `65535 / 65536`；LONG 位宽 `4294967295 / 4294967296`
- 区间：单点、`a == b == 0`、全负、跨 0、`MIN..MAX`、`MAX-1..MAX`、`MIN..0`、`a > b`
- 数组：空、单元素、块数 > 元素数、`threshold = 1`、块内溢出但总和不溢出（`MAX × 2000 + MIN × 2000`）
- 栈：512 KiB / 64 MiB 的线程栈；100 万层 `More` 链；200 万层互递归

## 相关变体

- 「不用公式」→「那现在用公式」→「n 很大怎么办」：Part 1 → Part 3。
- 「改成 `int`」「改成 `double`」（浮点累加不满足结合律，并行结果会抖）。
- 「求 1..n 的平方和 / 立方和」：闭式 `n(n+1)(2n+1)/6` 需要先除 2 再除 3，数值顺序同样重要。
- C++ 版的对应问题：`-O2` 会不会把尾递归变成循环（会，Java 不会）。

## 考什么

不是算法，是**看你被追问时的反应链**：定义结果类型而不是抛异常/回绕 → 知道 JVM 为什么没有 TCO 并能量出阈值 → 用 trampoline 把栈换成堆
→ 知道闭式的数值陷阱 → 知道 CPU 密集并行该用 ForkJoin/parallel stream，而虚拟线程是给阻塞 I/O 用的。
