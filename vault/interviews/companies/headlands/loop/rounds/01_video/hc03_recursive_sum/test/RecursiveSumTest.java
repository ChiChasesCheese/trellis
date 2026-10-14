import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigInteger;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.junit.jupiter.params.provider.ValueSource;

class RecursiveSumTest {

    private static final long MAX = Long.MAX_VALUE;
    private static final long MIN = Long.MIN_VALUE;

    private static RecursiveSum.SumResult ok(long v) { return new RecursiveSum.Ok(v); }
    private static RecursiveSum.SumResult overflow(String exact) { return new RecursiveSum.Overflow(new BigInteger(exact)); }

    /** 在指定栈大小的线程里跑；Error / 异常原样抛回测试线程。 */
    private static <T> T onStack(long bytes, Callable<T> body) throws Throwable {
        var result = new AtomicReference<T>();
        var failure = new AtomicReference<Throwable>();
        var t = new Thread(null, () -> {
            try { result.set(body.call()); } catch (Throwable e) { failure.set(e); }
        }, "sized-stack", bytes);
        t.start();
        t.join();
        if (failure.get() != null) throw failure.get();
        return result.get();
    }

    private static final long BIG = 1L << 29; // 512 MiB：足够 65536 层，且线程栈是按需提交的

    // ---------- Part 1：朴素递归 + checked ----------

    @ParameterizedTest @Tag("part1")
    @EnumSource(RecursiveSum.Width.class)
    void smallValues(RecursiveSum.Width w) {
        assertEquals(ok(0), RecursiveSum.sumToRecursive(0, w));
        assertEquals(ok(1), RecursiveSum.sumToRecursive(1, w));
        assertEquals(ok(55), RecursiveSum.sumToRecursive(10, w));
        assertEquals(ok(5050), RecursiveSum.sumToRecursive(100, w));
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @EnumSource(RecursiveSum.Width.class)
    void negativeNIsRejected(RecursiveSum.Width w) {
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.sumToRecursive(-1, w));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.sumToRecursive(Long.MIN_VALUE, w));
    }

    @Test @Tag("part1") @Tag("edge")
    void intWidthOverflowsExactlyAt65536() throws Throwable {
        // 1+…+65535 = 2147450880 ≤ Integer.MAX_VALUE；再加 65536 就是 2147516416
        assertEquals(ok(2_147_450_880L), onStack(BIG, () -> RecursiveSum.sumToRecursive(65_535, RecursiveSum.Width.INT)));
        assertEquals(overflow("2147516416"), onStack(BIG, () -> RecursiveSum.sumToRecursive(65_536, RecursiveSum.Width.INT)));
    }

    @Test @Tag("part1") @Tag("edge")
    void longWidthHoldsWhatIntCannot() throws Throwable {
        assertEquals(ok(2_147_516_416L), onStack(BIG, () -> RecursiveSum.sumToRecursive(65_536, RecursiveSum.Width.LONG)));
        assertEquals(ok(5_000_050_000L), onStack(BIG, () -> RecursiveSum.sumToRecursive(100_000, RecursiveSum.Width.LONG)));
    }

    @Test @Tag("part1")
    void resultTypeIsASealedAlgebra() {
        // 用 switch 穷尽两种结果；这个测试同时检查你的类型层次没有第三种实现
        RecursiveSum.SumResult r = RecursiveSum.sumToRecursive(10, RecursiveSum.Width.LONG);
        String text = switch (r) {
            case RecursiveSum.Ok(var v) -> "ok " + v;
            case RecursiveSum.Overflow(var exact) -> "overflow " + exact;
        };
        assertEquals("ok 55", text);
    }

    // ---------- Part 2：栈深、迭代、trampoline ----------

    @Test @Tag("part2")
    void measuredDepthGrowsWithStackSize() {
        int small = RecursiveSum.measureDepth(512 * 1024);
        int large = RecursiveSum.measureDepth(64L * 1024 * 1024);
        assertTrue(small > 1_000, "512 KiB 栈至少能递归上千层，实际 " + small);
        assertTrue(large > 4L * small, "64 MiB 栈应该远深于 512 KiB：" + large + " vs " + small);
    }

    @Test @Tag("part2") @Tag("edge")
    void naiveRecursionBlowsTheStackButTrampolineDoesNot() throws Throwable {
        long small = 512 * 1024;
        assertThrows(StackOverflowError.class,
                () -> onStack(small, () -> RecursiveSum.sumToRecursive(1_000_000, RecursiveSum.Width.LONG)));
        assertEquals(ok(500_000_500_000L),
                onStack(small, () -> RecursiveSum.sumToTrampoline(1_000_000, RecursiveSum.Width.LONG)));
        assertEquals(ok(500_000_500_000L),
                onStack(small, () -> RecursiveSum.sumToIterative(1_000_000, RecursiveSum.Width.LONG)));
    }

    @ParameterizedTest @Tag("part2")
    @EnumSource(RecursiveSum.Width.class)
    void iterativeAndTrampolineAgreeWithRecursion(RecursiveSum.Width w) {
        for (long n : new long[] {0, 1, 2, 10, 999}) {
            var expected = RecursiveSum.sumToRecursive(n, w);
            assertEquals(expected, RecursiveSum.sumToIterative(n, w), "iterative n=" + n);
            assertEquals(expected, RecursiveSum.sumToTrampoline(n, w), "trampoline n=" + n);
        }
    }

    @Test @Tag("part2") @Tag("edge")
    void stackSafeVersionsDetectOverflowAndRejectNegatives() {
        for (long n : new long[] {65_536, 70_000, 1_000_000}) {
            var expected = new RecursiveSum.Overflow(BigInteger.valueOf(n).multiply(BigInteger.valueOf(n + 1)).shiftRight(1));
            assertEquals(expected, RecursiveSum.sumToIterative(n, RecursiveSum.Width.INT), "iterative " + n);
            assertEquals(expected, RecursiveSum.sumToTrampoline(n, RecursiveSum.Width.INT), "trampoline " + n);
        }
        assertEquals(ok(2_147_450_880L), RecursiveSum.sumToIterative(65_535, RecursiveSum.Width.INT));
        assertEquals(ok(2_147_450_880L), RecursiveSum.sumToTrampoline(65_535, RecursiveSum.Width.INT));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.sumToIterative(-1, RecursiveSum.Width.LONG));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.sumToTrampoline(-1, RecursiveSum.Width.LONG));
    }

    @Test @Tag("part2")
    void trampolineRunLoop() throws Throwable {
        assertEquals(5, RecursiveSum.run(new RecursiveSum.Done<>(5)));
        assertEquals("x", RecursiveSum.run(new RecursiveSum.More<>(() -> new RecursiveSum.Done<>("x"))));
        // 一百万个 More 串成链，在 512 KiB 栈上跑完
        assertEquals(1_000_000, onStack(512 * 1024, () -> RecursiveSum.run(count(0, 1_000_000))));
    }

    private static RecursiveSum.Trampoline<Integer> count(int i, int limit) {
        return i == limit ? new RecursiveSum.Done<>(i) : new RecursiveSum.More<>(() -> count(i + 1, limit));
    }

    @Test @Tag("part2")
    void mutualRecursionIsEven() throws Throwable {
        assertTrue(RecursiveSum.isEven(0));
        assertFalse(RecursiveSum.isEven(1));
        assertTrue(RecursiveSum.isEven(10));
        assertFalse(RecursiveSum.isEven(7));
        assertTrue(onStack(512 * 1024, () -> RecursiveSum.isEven(2_000_000)));
        assertFalse(onStack(512 * 1024, () -> RecursiveSum.isEven(2_000_001)));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.isEven(-2));
    }

    @Test @Tag("part2") @Tag("perf")
    void perfStackSafeSums() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            assertEquals(ok(45_000_000_150_000_000L), RecursiveSum.sumToIterative(300_000_000, RecursiveSum.Width.LONG));
        });
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            assertEquals(ok(12_500_002_500_000L), RecursiveSum.sumToTrampoline(5_000_000, RecursiveSum.Width.LONG));
        });
    }

    // ---------- Part 3：区间 [a,b]、负数、闭式 ----------

    @Test @Tag("part3")
    void rangeSumExamples() {
        assertEquals(ok(5050), RecursiveSum.rangeSum(1, 100));
        assertEquals(ok(0), RecursiveSum.rangeSum(-5, 5));
        assertEquals(ok(-55), RecursiveSum.rangeSum(-10, -1));
        assertEquals(ok(4), RecursiveSum.rangeSum(-3, 4));
        assertEquals(ok(7), RecursiveSum.rangeSum(7, 7));
        assertEquals(ok(0), RecursiveSum.rangeSum(0, 0));
        assertEquals(ok(-7), RecursiveSum.rangeSum(-7, -7));
        assertEquals(BigInteger.valueOf(5050), RecursiveSum.rangeSumExact(1, 100));
    }

    @Test @Tag("part3") @Tag("edge")
    void emptyRangeIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.rangeSum(2, 1));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.rangeSumExact(MAX, MIN));
    }

    @Test @Tag("part3") @Tag("edge")
    void divideBeforeMultiply() {
        // n*(n+1) = 2^64 - 2^32 在 long 里已经溢出；先除 2 再乘就装得下
        long n = 4_294_967_295L;
        assertEquals(-2_147_483_648L, RecursiveSum.naiveClosedForm(n), "朴素写法静默给出错误答案");
        assertEquals(ok(9_223_372_034_707_292_160L), RecursiveSum.rangeSum(1, n));
        // 再大一个就真的装不下了
        assertEquals(overflow("9223372039002259456"), RecursiveSum.rangeSum(1, n + 1));
    }

    @Test @Tag("part3") @Tag("edge")
    void intermediateOverflowIsNotResultOverflow() {
        // MIN..MAX：count = 2^64 溢出，a+b = -1；真实和恰好是 Long.MIN_VALUE，仍然装得下
        assertEquals(ok(MIN), RecursiveSum.rangeSum(MIN, MAX));
        assertEquals(ok(0), RecursiveSum.rangeSum(-MAX, MAX));
        // 单点区间：a+b 溢出，但和就是 a 本身
        assertEquals(ok(MAX), RecursiveSum.rangeSum(MAX, MAX));
        assertEquals(ok(MIN), RecursiveSum.rangeSum(MIN, MIN));
        // [MAX-1, MAX] 的和是 2^64-3，真的装不下
        assertEquals(overflow("18446744073709551613"), RecursiveSum.rangeSum(MAX - 1, MAX));
    }

    @Test @Tag("part3") @Tag("edge")
    void hugeRangeCarriesExactValue() {
        var r = assertInstanceOf(RecursiveSum.Overflow.class, RecursiveSum.rangeSum(MIN, 0));
        assertEquals(new BigInteger("-42535295865117307937533511947398414336"), r.exact());
    }

    @Test @Tag("part3") @Tag("edge")
    void smallRangesMatchBruteForce() {
        for (long a = -40; a <= 40; a++)
            for (long b = a; b <= 40; b++) {
                long expected = 0;
                for (long i = a; i <= b; i++) expected += i;
                assertEquals(ok(expected), RecursiveSum.rangeSum(a, b), a + ".." + b);
            }
    }

    @Test @Tag("part3") @Tag("edge")
    void randomRangesAcrossTheWholeLongRange() {
        var rnd = new Random(0);
        int overflows = 0, oks = 0;
        for (int i = 0; i < 20_000; i++) {
            long a = rnd.nextLong() >> rnd.nextInt(64);
            long b = rnd.nextLong() >> rnd.nextInt(64);
            if (a > b) { long t = a; a = b; b = t; }
            // 独立算法：等差数列 n*a + n(n-1)/2
            var n = BigInteger.valueOf(b).subtract(BigInteger.valueOf(a)).add(BigInteger.ONE);
            var expected = n.multiply(BigInteger.valueOf(a)).add(n.multiply(n.subtract(BigInteger.ONE)).shiftRight(1));
            RecursiveSum.SumResult got = RecursiveSum.rangeSum(a, b);
            if (expected.bitLength() <= 63) {
                oks++;
                assertEquals(ok(expected.longValueExact()), got, a + ".." + b);
            } else {
                overflows++;
                assertEquals(new RecursiveSum.Overflow(expected), got, a + ".." + b);
            }
        }
        assertTrue(oks > 1_000 && overflows > 1_000, "随机用例应该两种结果都覆盖：" + oks + "/" + overflows);
    }

    // ---------- Part 4：并行求和 ----------

    private static long[] randomData(int n, long bound) {
        var rnd = new Random(0);
        long[] d = new long[n];
        for (int i = 0; i < n; i++) d[i] = rnd.nextLong(-bound, bound);
        return d;
    }

    private static long plainSum(long[] d) { long s = 0; for (long x : d) s += x; return s; }

    @Test @Tag("part4")
    void wideAccumulatorBasics() {
        var w = RecursiveSum.Wide.ZERO.plus(MAX).plus(MAX);
        assertFalse(w.fitsLong());
        assertEquals(BigInteger.valueOf(MAX).multiply(BigInteger.TWO), w.toBigInteger());
        assertTrue(w.plus(MIN).fitsLong());
        assertEquals(BigInteger.valueOf(-1), RecursiveSum.Wide.ZERO.plus(-1).toBigInteger());
        var merged = RecursiveSum.Wide.ZERO.plus(MIN).merge(RecursiveSum.Wide.ZERO.plus(MIN));
        assertEquals(BigInteger.valueOf(MIN).multiply(BigInteger.TWO), merged.toBigInteger());
        assertFalse(merged.fitsLong());
    }

    @Test @Tag("part4") @Tag("edge")
    void checkedSumDependsOnTheTrueTotalNotOnTheOrder() {
        assertEquals(ok(0), RecursiveSum.checkedSum(new long[] {}));
        assertEquals(ok(MAX), RecursiveSum.checkedSum(new long[] {MAX, 1, -1}));   // 逐步 addExact 会在第二步抛
        assertEquals(ok(MAX), RecursiveSum.checkedSum(new long[] {1, MAX, -1}));
        assertEquals(ok(-1), RecursiveSum.checkedSum(new long[] {MIN, MAX}));
        assertEquals(overflow("9223372036854775808"), RecursiveSum.checkedSum(new long[] {MAX, 1}));
        assertEquals(overflow("-9223372036854775809"), RecursiveSum.checkedSum(new long[] {MIN, -1}));
        assertEquals(ok(-2), RecursiveSum.checkedSum(new long[] {MAX, MAX, MIN, MIN, 1, -1}));
    }

    private static List<java.util.function.Function<long[], RecursiveSum.SumResult>> parallelImpls() {
        return List.of(
                d -> RecursiveSum.parallelSumForkJoin(d, 1_000),
                d -> RecursiveSum.parallelSumForkJoin(d, 1),
                RecursiveSum::parallelSumStream,
                d -> RecursiveSum.sumVirtual(d, 7),
                d -> RecursiveSum.sumVirtual(d, 1));
    }

    @Test @Tag("part4")
    void parallelImplementationsMatchSequential() {
        long[] data = randomData(100_003, 1_000_000);
        var expected = ok(plainSum(data));
        assertEquals(expected, RecursiveSum.checkedSum(data));
        for (var impl : parallelImpls()) assertEquals(expected, impl.apply(data));
    }

    @Test @Tag("part4") @Tag("edge")
    void parallelEdgeShapes() {
        for (long[] data : new long[][] {{}, {42}, {-1, 1}, {MAX}, {MIN}, new long[3]}) {
            var expected = RecursiveSum.checkedSum(data);
            for (var impl : parallelImpls()) assertEquals(expected, impl.apply(data), java.util.Arrays.toString(data));
        }
        assertEquals(ok(0), RecursiveSum.sumVirtual(new long[] {}, 16));        // 块数 > 元素数
        assertEquals(ok(6), RecursiveSum.sumVirtual(new long[] {1, 2, 3}, 100));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.parallelSumForkJoin(new long[1], 0));
        assertThrows(IllegalArgumentException.class, () -> RecursiveSum.sumVirtual(new long[1], 0));
    }

    @Test @Tag("part4") @Tag("edge")
    void parallelOverflowIsDecidedByTheTrueTotal() {
        // 每个块单独看都可能溢出，合起来不溢出：块边界不能影响答案
        long[] cancel = new long[4_000];
        for (int i = 0; i < cancel.length; i++) cancel[i] = i < 2_000 ? MAX : MIN;
        long[] over = new long[4_000];
        java.util.Arrays.fill(over, MAX);
        var bigOver = RecursiveSum.checkedSum(over);
        var cancelExpected = RecursiveSum.checkedSum(cancel);
        assertEquals(ok(-2_000), cancelExpected);
        assertInstanceOf(RecursiveSum.Overflow.class, bigOver);
        for (var impl : parallelImpls()) {
            assertEquals(cancelExpected, impl.apply(cancel));
            assertEquals(bigOver, impl.apply(over));
        }
    }

    @Test @Tag("part4") @Tag("conc")
    void concurrentCallersAllGetTheSameAnswer() throws Exception {
        long[] data = randomData(200_001, 1L << 40);
        var expected = ok(plainSum(data));
        int callers = 6;
        for (int round = 0; round < 20; round++) {
            var gate = new CountDownLatch(1);
            var results = new RecursiveSum.SumResult[callers * 3];
            var threads = new ArrayList<Thread>();
            for (int c = 0; c < callers; c++) {
                final int slot = c * 3;
                threads.add(Thread.ofPlatform().start(() -> {
                    await(gate);
                    results[slot] = RecursiveSum.parallelSumForkJoin(data, 5_000);
                    results[slot + 1] = RecursiveSum.parallelSumStream(data);
                    results[slot + 2] = RecursiveSum.sumVirtual(data, 16);
                }));
            }
            gate.countDown();
            for (var t : threads) t.join();
            for (int i = 0; i < results.length; i++) assertEquals(expected, results[i], "round " + round + " slot " + i);
        }
    }

    private static void await(CountDownLatch l) {
        try { l.await(); } catch (InterruptedException e) { throw new IllegalStateException(e); }
    }

    @Test @Tag("part4") @Tag("perf")
    void perfTenMillionElements() {
        long[] data = randomData(10_000_000, 1L << 30);
        var expected = ok(plainSum(data));
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            assertEquals(expected, RecursiveSum.checkedSum(data));
            assertEquals(expected, RecursiveSum.parallelSumForkJoin(data, 100_000));
            assertEquals(expected, RecursiveSum.parallelSumStream(data));
        });
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            // 一万个虚拟线程各算一小块：正确，只是比 ForkJoin 多出调度开销
            assertEquals(expected, RecursiveSum.sumVirtual(data, 10_000));
        });
    }
}
