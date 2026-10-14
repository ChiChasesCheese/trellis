import java.math.BigInteger;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;
import java.util.concurrent.StructuredTaskScope;
import java.util.function.Supplier;
import java.util.stream.IntStream;

/** Headlands 视频面热身：递归求和 1..n，面试官一路追问。题面见 ../problem.md。 */
public final class RecursiveSum {
    private RecursiveSum() {}

    // ------------------------------------------------------------------ 结果类型
    // 为什么不直接返回 long？因为 long 装不下时只有三种坏选择：抛异常（调用方可能忘了 catch）、
    // 返回 -1（和合法结果混在一起，区间有负数时 -1 就是合法的和）、静默回绕（最糟，答案是错的却没人知道）。
    // sealed 的 Ok/Overflow 把「可能溢出」写进类型，调用方的 switch 不处理 Overflow 就编译不过。

    /** 求和结果：要么装得下，要么溢出（带上数学上的精确值，方便调用方报错或降级）。 */
    public sealed interface SumResult permits Ok, Overflow {}
    public record Ok(long value) implements SumResult {}
    public record Overflow(BigInteger exact) implements SumResult {}

    /**
     * 累加器的位宽。INT 让溢出在 n = 65536 就发生，测试不必跑 43 亿步。
     * 为什么要有这个枚举：long 的溢出点是 n = 4 294 967 296，朴素递归在到达之前早就栈溢出了，没法测。
     */
    public enum Width {
        INT, LONG;

        /** 检查加法：结果超出本位宽就抛 ArithmeticException。入参必须已在本位宽内。 */
        long add(long a, long b) {
            // 两个 int 范围内的数在 long 里相加绝不会溢出，所以先用 long 算，再检查结果是否还在 int 范围内。
            long s = Math.addExact(a, b);
            return switch (this) {
                case INT -> Math.toIntExact(s);
                case LONG -> s;
            };
        }
    }

    /** 数学上精确的 1+2+…+n（BigInteger，永不溢出）；各实现的 Overflow 都带这个值。 */
    static BigInteger exactTo(long n) {
        var bn = BigInteger.valueOf(n);
        return bn.multiply(bn.add(BigInteger.ONE)).shiftRight(1);
    }

    private static void requireNonNegative(long n) {
        if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
    }

    // ------------------------------------------------------------------ Part 1：朴素递归 + checked

    /**
     * sum(n) = n + sum(n-1)。栈深 = n；n 太大会抛 StackOverflowError（不要吞掉，Part 2 才处理）。
     * 为什么 try/catch 放在入口而不是递归内部：每层都包 try 没有任何好处，只会重复逻辑；
     * 内部只需要一个 long，异常一路向上抛，到边界再翻译成 Overflow，内部代码最简单。
     */
    public static SumResult sumToRecursive(long n, Width w) {
        requireNonNegative(n);
        try {
            return new Ok(addUp(n, w));
        } catch (ArithmeticException e) {
            return new Overflow(exactTo(n));
        }
    }

    private static long addUp(long n, Width w) {
        // 注意加法发生在「递归返回之后」：n + (子问题的结果)。所以每一层都必须等子调用回来，栈帧不能丢——
        // 这不是尾递归。尾递归要求递归调用是函数做的最后一件事（见 step()）。
        return n == 0 ? 0 : w.add(n, addUp(n - 1, w));
    }

    // ------------------------------------------------------------------ Part 2：栈深

    /**
     * 在给定线程栈大小（字节）的新线程里一路递归到 StackOverflowError，返回到达的深度。
     * 为什么要新线程：栈大小是「线程」的属性，Thread 构造器的第四个参数才能指定；主线程的栈改不了。
     * 为什么计数放在对象字段而不是返回值：栈溢出的那一刻没有机会返回任何东西，字段是唯一能带出结果的办法。
     */
    public static int measureDepth(long stackBytes) {
        var probe = new Probe();
        var t = new Thread(null, () -> {
            try {
                probe.dive();
            } catch (StackOverflowError _) {
                // 预期：深度就记在 probe.depth 里
            }
        }, "depth-probe", stackBytes);
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
        return probe.depth;
    }

    private static final class Probe {
        int depth;
        void dive() { depth++; dive(); }
    }

    /** 迭代版：栈深 O(1)。循环里没有「等待子调用返回」的状态，一个局部变量 acc 就是全部中间结果。 */
    public static SumResult sumToIterative(long n, Width w) {
        requireNonNegative(n);
        long acc = 0;
        try {
            for (long i = 1; i <= n; i++) acc = w.add(acc, i);
        } catch (ArithmeticException e) {
            return new Overflow(exactTo(n));
        }
        return new Ok(acc);
    }

    /**
     * Trampoline（蹦床）：要么算完了（Done），要么还有下一步（More）。把「递归调用」变成「返回一个待办」。
     * 为什么能省栈：每一步函数立刻 return（栈帧立即弹出），把「下一步该做什么」装进堆上的 More 对象，
     * 由 run() 里的循环取出来再执行。栈深永远是常数；代价是每步在堆上分配一个对象。
     */
    public sealed interface Trampoline<T> permits Done, More {}
    public record Done<T>(T value) implements Trampoline<T> {}
    public record More<T>(Supplier<Trampoline<T>> next) implements Trampoline<T> {}

    /**
     * 跑 trampoline：一个 while 循环 + 模式匹配 switch，栈深恒定。
     * 因为 Trampoline 是 sealed 的，switch 不需要 default：新增一种变体时这里会编译报错，提醒你补分支。
     */
    public static <T> T run(Trampoline<T> start) {
        var cur = start;
        while (true) {
            switch (cur) {
                case Done<T>(var v) -> { return v; }
                case More<T>(var next) -> cur = next.get();
            }
        }
    }

    /** 尾递归形式（累加器参数）+ trampoline。 */
    public static SumResult sumToTrampoline(long n, Width w) {
        requireNonNegative(n);
        try {
            return new Ok(run(step(n, 0, w)));
        } catch (ArithmeticException e) {
            return new Overflow(exactTo(n));
        }
    }

    // 尾递归形式：把「到目前为止的和」作为参数 acc 传下去，递归调用是最后一件事，返回的结果直接就是答案。
    // 懒求值很关键：w.add(acc, n) 写在 lambda 里，所以是在 run() 的循环里被调用的，而不是在本方法的栈帧里叠加。
    private static Trampoline<Long> step(long n, long acc, Width w) {
        return n == 0 ? new Done<>(acc) : new More<>(() -> step(n - 1, w.add(acc, n), w));
    }

    /** 互递归 isEven/isOdd：连「尾调用消除成循环」都不行的情形，trampoline 照样处理。 */
    public static boolean isEven(long n) {
        requireNonNegative(n);
        return run(even(n));
    }

    private static Trampoline<Boolean> even(long n) { return n == 0 ? new Done<>(true) : new More<>(() -> odd(n - 1)); }
    private static Trampoline<Boolean> odd(long n) { return n == 0 ? new Done<>(false) : new More<>(() -> even(n - 1)); }

    // ------------------------------------------------------------------ Part 3：区间 [a,b] 与闭式

    /**
     * 面试里最常见的错误写法：n*(n+1) 先溢出，再除 2。留在这里给测试对比，不要用。
     * 例：n = 2^32-1 时 n*(n+1) = 2^64 - 2^32，超出 long（补码回绕成 -2^32），除 2 得 -2^31，答案是负数却没有任何报错。
     */
    public static long naiveClosedForm(long n) { return n * (n + 1) / 2; }

    /** a..b（含）所有整数之和的精确值；a > b 抛 IllegalArgumentException。 */
    public static BigInteger rangeSumExact(long a, long b) {
        if (a > b) throw new IllegalArgumentException("a > b: " + a + " > " + b);
        return BigInteger.valueOf(a).add(BigInteger.valueOf(b))
                .multiply(BigInteger.valueOf(b).subtract(BigInteger.valueOf(a)).add(BigInteger.ONE))
                .shiftRight(1);
    }

    /**
     * a..b 之和，long 装得下返回 Ok，否则 Overflow(exact)。
     * 快路径：(a+b) 与 (b-a+1) 奇偶相反，先把偶的那个除 2，再 multiplyExact；
     * 任何中间量溢出就退到 BigInteger（中间量溢出 ≠ 结果溢出，例如 MIN..MAX 的和恰好是 Long.MIN_VALUE）。
     */
    public static SumResult rangeSum(long a, long b) {
        if (a > b) throw new IllegalArgumentException("a > b: " + a + " > " + b);
        try {
            // (a+b) 和 (b-a+1) 恰好一奇一偶：b-a+1 与 a+b 差 2a-1，是奇数。所以其中一个必为偶数，
            // 先把偶的那个除 2（整除，无余数），再相乘——乘积比「先乘再除」小一半，少一次溢出机会。
            long s = Math.addExact(a, b);
            long count = Math.addExact(Math.subtractExact(b, a), 1);
            long v = (count & 1) == 0 ? Math.multiplyExact(count / 2, s) : Math.multiplyExact(count, s / 2);
            return new Ok(v);
        } catch (ArithmeticException e) {
            // 中间量（a+b、b-a+1）溢出不代表结果溢出，例如 MIN..MAX 的和恰好是 Long.MIN_VALUE。
            // 所以不在这里下结论，退到 BigInteger 算精确值，再看它能不能装进 63 位 + 符号位。
            var exact = rangeSumExact(a, b);
            return exact.bitLength() <= 63 ? new Ok(exact.longValueExact()) : new Overflow(exact);
        }
    }

    // ------------------------------------------------------------------ Part 4：并行求和

    /**
     * 128 位有符号累加器（hi:lo，补码）。加法满足结合律，所以任意切块、任意合并顺序结果相同。
     * 为什么不用「每块 addExact 再合并」：addExact 会在中间步骤抛异常，而中间步骤取决于顺序（[MAX, 1, -1]），
     * 并行时每块的边界是任意的——同一份数据换个切法就可能抛或不抛。128 位累加永远不溢出，最后只判一次。
     * 进位怎么来的：lo 当作无符号数相加，结果比原来小说明回绕了一次（compareUnsigned），hi 就加 1；
     * 加数 x 是有符号的，它的「高 64 位」是符号扩展：非负为 0，负数为 -1（即 x >> 63）。
     */
    public record Wide(long hi, long lo) {
        public static final Wide ZERO = new Wide(0, 0);

        public Wide plus(long x) {
            long nlo = lo + x;
            long carry = Long.compareUnsigned(nlo, lo) < 0 ? 1 : 0;
            return new Wide(hi + (x >> 63) + carry, nlo);
        }

        public Wide merge(Wide o) {
            long nlo = lo + o.lo;
            long carry = Long.compareUnsigned(nlo, lo) < 0 ? 1 : 0;
            return new Wide(hi + o.hi + carry, nlo);
        }

        public boolean fitsLong() { return hi == (lo >> 63); }

        public BigInteger toBigInteger() {
            return BigInteger.valueOf(hi).shiftLeft(64).add(new BigInteger(Long.toUnsignedString(lo)));
        }

        public SumResult toResult() { return fitsLong() ? new Ok(lo) : new Overflow(toBigInteger()); }
    }

    /** [from,to) 一块的 128 位和。热循环里用局部变量（hi、lo 住在寄存器里），不分配对象——否则 GC 压力会盖过加法本身。 */
    static Wide sumChunk(long[] data, int from, int to) {
        long hi = 0, lo = 0;
        for (int i = from; i < to; i++) {
            long x = data[i];
            long nlo = lo + x;
            hi += (x >> 63) + (Long.compareUnsigned(nlo, lo) < 0 ? 1 : 0);
            lo = nlo;
        }
        return new Wide(hi, lo);
    }

    /** 顺序基线。结果与顺序无关：只有「真实总和」放不进 long 才 Overflow（[MAX,1,-1] 是 Ok(MAX)）。 */
    public static SumResult checkedSum(long[] data) { return sumChunk(data, 0, data.length).toResult(); }

    /** ForkJoin：区间 ≤ threshold 就直接算，否则一分为二，fork 左边、本线程算右边、join。 */
    public static SumResult parallelSumForkJoin(long[] data, int threshold) {
        if (threshold < 1) throw new IllegalArgumentException("threshold < 1");
        return ForkJoinPool.commonPool().invoke(new SumTask(data, 0, data.length, threshold)).toResult();
    }

    private static final class SumTask extends RecursiveTask<Wide> {
        private final long[] data;
        private final int from, to, threshold;

        SumTask(long[] data, int from, int to, int threshold) {
            this.data = data; this.from = from; this.to = to; this.threshold = threshold;
        }

        @Override protected Wide compute() {
            if (to - from <= threshold) return sumChunk(data, from, to);
            int mid = (from + to) >>> 1;   // 用 >>> 而不是 /2：from+to 溢出成负数时仍然正确（经典二分 bug）
            var left = new SumTask(data, from, mid, threshold);
            left.fork();   // 左半交给池里别的线程（可能被偷走）；右半本线程自己算，不空等
            var right = new SumTask(data, mid, to, threshold).compute();
            return left.join().merge(right);
        }
    }

    /** parallel stream：按块下标并行，每块用 sumChunk，最后 reduce。块数取并行度的 4 倍以平衡负载。 */
    public static SumResult parallelSumStream(long[] data) {
        int chunks = Math.max(1, ForkJoinPool.getCommonPoolParallelism() * 4);
        int size = (int) Math.ceilDiv((long) data.length, chunks);
        return IntStream.range(0, chunks).parallel()
                .mapToObj(i -> sumChunk(data, Math.min(data.length, i * size), Math.min(data.length, (i + 1) * size)))
                .reduce(Wide.ZERO, Wide::merge)
                .toResult();
    }

    /**
     * 每块一个虚拟线程（StructuredTaskScope，预览 API）。正确，但 CPU 密集任务并不该用它：
     * 虚拟线程只是多路复用在 carrier（= 核数个平台线程）上，不会多出并行度，也不会时间片抢占。
     */
    public static SumResult sumVirtual(long[] data, int chunks) {
        if (chunks < 1) throw new IllegalArgumentException("chunks < 1");
        int size = (int) Math.ceilDiv((long) data.length, chunks);
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            var parts = IntStream.range(0, chunks)
                    .mapToObj(i -> scope.fork(() -> sumChunk(data, Math.min(data.length, i * size),
                            Math.min(data.length, (i + 1) * size))))
                    .toList();
            scope.join().throwIfFailed();
            var total = Wide.ZERO;
            for (var p : parts) total = total.merge(p.get());
            return total.toResult();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        } catch (ExecutionException e) {
            throw new IllegalStateException(e.getCause());
        }
    }
}
