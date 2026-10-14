import java.math.BigInteger;
import java.util.function.Supplier;

/**
 * Headlands 视频面热身：递归求和 1..n，面试官一路追问。题面见 ../problem.md。
 * 把每个 TODO 换成实现；一次只做一个 Part，面试里也是这个节奏。
 */
public final class RecursiveSum {
    private RecursiveSum() {}

    // ------------------------------------------------------------------ 结果类型（已给出）

    /** 求和结果：要么装得下，要么溢出（带上数学上的精确值）。 */
    public sealed interface SumResult permits Ok, Overflow {}
    public record Ok(long value) implements SumResult {}
    public record Overflow(BigInteger exact) implements SumResult {}

    /** 累加器位宽。INT 让溢出在 n = 65536 就发生。 */
    public enum Width {
        INT, LONG;

        /** 检查加法：结果超出本位宽就抛 ArithmeticException。提示：Math.addExact / Math.toIntExact。 */
        long add(long a, long b) { throw new UnsupportedOperationException("TODO"); }
    }

    /** 数学上精确的 1+2+…+n（BigInteger）。Overflow 都带这个值。 */
    static BigInteger exactTo(long n) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 1：朴素递归 + checked

    /** sum(n) = n + sum(n-1)。n < 0 抛 IllegalArgumentException；溢出返回 Overflow；栈溢出不要吞。 */
    public static SumResult sumToRecursive(long n, Width w) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 2：栈深

    /** 在给定栈大小（字节）的新线程里一路递归到 StackOverflowError，返回到达的深度。提示：new Thread(null, r, name, stackSize)。 */
    public static int measureDepth(long stackBytes) { throw new UnsupportedOperationException("TODO"); }

    /** 迭代版，栈深 O(1)，语义与 sumToRecursive 完全一致。 */
    public static SumResult sumToIterative(long n, Width w) { throw new UnsupportedOperationException("TODO"); }

    /** Trampoline：算完了（Done）或还有下一步（More）。 */
    public sealed interface Trampoline<T> permits Done, More {}
    public record Done<T>(T value) implements Trampoline<T> {}
    public record More<T>(Supplier<Trampoline<T>> next) implements Trampoline<T> {}

    /** 跑 trampoline：while 循环 + 对 sealed 类型的模式匹配 switch，栈深恒定。 */
    public static <T> T run(Trampoline<T> start) { throw new UnsupportedOperationException("TODO"); }

    /** 尾递归形式（带累加器）+ trampoline。语义同 sumToRecursive。 */
    public static SumResult sumToTrampoline(long n, Width w) { throw new UnsupportedOperationException("TODO"); }

    /** 互递归 isEven/isOdd，用 trampoline 做到 n = 2_000_000 不爆栈。n < 0 抛 IllegalArgumentException。 */
    public static boolean isEven(long n) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 3：区间 [a,b] 与闭式

    /** 面试里最常见的错误写法（已给出，仅供对比，不要用）：n*(n+1) 先溢出，再除 2。 */
    public static long naiveClosedForm(long n) { return n * (n + 1) / 2; }

    /** a..b（含）之和的精确值；a > b 抛 IllegalArgumentException。 */
    public static BigInteger rangeSumExact(long a, long b) { throw new UnsupportedOperationException("TODO"); }

    /**
     * a..b 之和：long 装得下 Ok，否则 Overflow(exact)；a > b 抛 IllegalArgumentException。
     * 提示：(a+b) 与 (b-a+1) 奇偶相反；先除 2 再乘；中间量溢出时别急着报 Overflow（MIN..MAX 的和就是 Long.MIN_VALUE）。
     */
    public static SumResult rangeSum(long a, long b) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 4：并行求和

    /**
     * 128 位有符号累加器（hi:lo，补码），加法满足结合律，所以怎么切块、怎么合并都一样。
     * plus(x)：加一个 long（x 的符号扩展进 hi，lo 用无符号进位）；merge：两个累加器相加；
     * fitsLong：hi == (lo >> 63)；toBigInteger：精确值。
     */
    public record Wide(long hi, long lo) {
        public static final Wide ZERO = new Wide(0, 0);
        public Wide plus(long x) { throw new UnsupportedOperationException("TODO"); }
        public Wide merge(Wide o) { throw new UnsupportedOperationException("TODO"); }
        public boolean fitsLong() { throw new UnsupportedOperationException("TODO"); }
        public BigInteger toBigInteger() { throw new UnsupportedOperationException("TODO"); }
        public SumResult toResult() { return fitsLong() ? new Ok(lo) : new Overflow(toBigInteger()); }
    }

    /** 顺序基线：只有「真实总和」放不进 long 才 Overflow（[MAX,1,-1] 是 Ok(MAX)，不是 Overflow）。 */
    public static SumResult checkedSum(long[] data) { throw new UnsupportedOperationException("TODO"); }

    /** ForkJoin RecursiveTask：区间 ≤ threshold 直接算，否则一分为二（fork 左、算右、join）。threshold < 1 抛 IAE。 */
    public static SumResult parallelSumForkJoin(long[] data, int threshold) { throw new UnsupportedOperationException("TODO"); }

    /** parallel stream 版。提示：按「块下标」并行，不要对 5 千万个装箱 Long 并行。 */
    public static SumResult parallelSumStream(long[] data) { throw new UnsupportedOperationException("TODO"); }

    /** 每块一个虚拟线程（StructuredTaskScope，预览 API）。chunks < 1 抛 IAE。写完回答：为什么 CPU 密集任务不该这样做？ */
    public static SumResult sumVirtual(long[] data, int chunks) { throw new UnsupportedOperationException("TODO"); }
}
