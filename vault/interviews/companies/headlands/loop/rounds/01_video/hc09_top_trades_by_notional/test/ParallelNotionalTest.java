import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.junit.jupiter.params.provider.ValueSource;

/** hc09 Part 4：分块并行聚合 + 合并。 */
class ParallelNotionalTest {

    /** 把四种并行实现统一成一个函数，参数化测试逐个跑。 */
    enum Impl {
        PARALLEL_STREAM {
            Map<String, Long> run(String[] t, long[] p, long[] v, int chunks) {
                return ParallelNotional.totalsParallelStream(t, p, v);
            }
        },
        FORK_JOIN {
            Map<String, Long> run(String[] t, long[] p, long[] v, int chunks) {
                return ParallelNotional.totalsForkJoin(t, p, v, Math.max(1, t.length / Math.max(1, chunks)));
            }
        },
        SCOPED {
            Map<String, Long> run(String[] t, long[] p, long[] v, int chunks) throws Exception {
                return ParallelNotional.totalsScoped(t, p, v, chunks);
            }
        },
        SHARED_MAP {
            Map<String, Long> run(String[] t, long[] p, long[] v, int chunks) throws Exception {
                return ParallelNotional.totalsSharedMap(t, p, v, chunks);
            }
        };

        abstract Map<String, Long> run(String[] t, long[] p, long[] v, int chunks) throws Exception;
    }

    record Data(String[] t, long[] p, long[] v) {
        static Data random(long seed, int n, int tickers, int maxPrice, int maxVol) {
            var rnd = new Random(seed);
            var names = new String[tickers];
            for (int i = 0; i < tickers; i++) names[i] = "T" + i;
            var t = new String[n];
            var p = new long[n];
            var v = new long[n];
            for (int i = 0; i < n; i++) {
                t[i] = names[rnd.nextInt(tickers)];
                p[i] = rnd.nextInt(maxPrice + 1);
                v[i] = rnd.nextInt(maxVol + 1);
            }
            return new Data(t, p, v);
        }
    }

    static final String[] T = TopTradesTest.T;
    static final long[] P = TopTradesTest.P;
    static final long[] V = TopTradesTest.V;

    // ============================================================ 正确性

    @ParameterizedTest @Tag("part4")
    @EnumSource(Impl.class)
    void sampleTotals(Impl impl) throws Exception {
        var expect = Map.of("AAPL", 270_500L, "MSFT", 240_000L, "TSLA", 200_000L, "GOOG", 126_000L);
        for (int chunks : new int[]{1, 2, 3, 6, 10}) {
            assertEquals(expect, impl.run(T, P, V, chunks), impl + " chunks=" + chunks);
        }
        assertEquals(expect, ParallelNotional.totalsSequential(T, P, V));
    }

    @ParameterizedTest @Tag("part4") @Tag("edge")
    @EnumSource(Impl.class)
    void emptyInputAndMoreChunksThanEvents(Impl impl) throws Exception {
        assertEquals(Map.of(), impl.run(new String[0], new long[0], new long[0], 4));
        assertEquals(Map.of("A", 6L), impl.run(new String[]{"A"}, new long[]{2}, new long[]{3}, 16));
    }

    @ParameterizedTest @Tag("part4") @Tag("edge")
    @EnumSource(Impl.class)
    void invalidEventsFailTheWholeCall(Impl impl) {
        var t = new String[]{"A", "B", "C", "D"};
        var ok = new long[]{1, 1, 1, 1};
        assertThrows(IllegalArgumentException.class, () -> impl.run(t, new long[]{1, 1, -1, 1}, ok, 2));
        assertThrows(IllegalArgumentException.class, () -> impl.run(t, ok, new long[]{1, 1, 1, -1}, 2));
        assertThrows(NullPointerException.class, () -> impl.run(new String[]{"A", null, "C", "D"}, ok, ok, 2));
        assertThrows(IllegalArgumentException.class, () -> impl.run(t, new long[]{1}, ok, 2));
    }

    @ParameterizedTest @Tag("part4") @Tag("edge")
    @EnumSource(Impl.class)
    void overflowInsideOneEventAndOnlyAtMergeTimeAreBothDetected(Impl impl) {
        long half = Long.MAX_VALUE / 2 + 1;
        // 单个事件乘法溢出
        assertThrows(ArithmeticException.class,
                () -> impl.run(new String[]{"A", "B"}, new long[]{Long.MAX_VALUE, 1}, new long[]{2, 1}, 2));
        // 每个事件、每块的部分和都不溢出，只有把两块合并时才溢出——分块边界正好把两个 A 分开
        assertThrows(ArithmeticException.class,
                () -> impl.run(new String[]{"A", "A"}, new long[]{half, half}, new long[]{1, 1}, 2));
        // 同样的数据换成不同 ticker：不应抛
        assertEquals(Map.of("A", half, "B", half), implRunUnchecked(impl, new String[]{"A", "B"}, new long[]{half, half}, new long[]{1, 1}, 2));
    }

    @ParameterizedTest @Tag("part4") @Tag("edge")
    @EnumSource(Impl.class)
    void totalExactlyLongMaxIsAcceptedWhateverTheSplit(Impl impl) throws Exception {
        var t = new String[]{"A", "A", "A", "A"};
        var p = new long[]{Long.MAX_VALUE - 6, 1, 2, 3};
        var v = new long[]{1, 1, 1, 1};
        for (int chunks : new int[]{1, 2, 3, 4}) {
            assertEquals(Map.of("A", Long.MAX_VALUE), impl.run(t, p, v, chunks), impl + " chunks=" + chunks);
        }
        // 再多 1 就必须报——不论怎么分块
        var p2 = new long[]{Long.MAX_VALUE - 6, 1, 2, 4};
        for (int chunks : new int[]{1, 2, 3, 4}) {
            assertThrows(ArithmeticException.class, () -> impl.run(t, p2, v, chunks), impl + " chunks=" + chunks);
        }
    }

    static Map<String, Long> implRunUnchecked(Impl impl, String[] t, long[] p, long[] v, int chunks) {
        try {
            return impl.run(t, p, v, chunks);
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new AssertionError(e);
        }
    }

    @ParameterizedTest @Tag("part4")
    @ValueSource(longs = {31, 32, 33, 34, 35})
    void shuffleAndChunkingNeverChangeTheAnswer(long seed) throws Exception {
        var d = Data.random(seed, 5_000, 50, 1_000, 100);
        var expect = ParallelNotional.totalsSequential(d.t(), d.p(), d.v());
        // 打乱事件顺序（保持三个数组对齐）
        var order = new ArrayList<Integer>();
        for (int i = 0; i < d.t().length; i++) order.add(i);
        Collections.shuffle(order, new Random(seed));
        var t = new String[order.size()];
        var p = new long[order.size()];
        var v = new long[order.size()];
        for (int i = 0; i < order.size(); i++) {
            t[i] = d.t()[order.get(i)];
            p[i] = d.p()[order.get(i)];
            v[i] = d.v()[order.get(i)];
        }
        for (var impl : Impl.values()) {
            for (int chunks : new int[]{1, 2, 7, 64}) {
                assertEquals(expect, impl.run(t, p, v, chunks), impl + " chunks=" + chunks);
            }
        }
    }

    @ParameterizedTest @Tag("part4")
    @ValueSource(longs = {41, 42, 43, 44})
    void parallelTopKEqualsSequentialTopKEvenWithManyTies(long seed) throws Exception {
        var d = Data.random(seed, 3_000, 200, 3, 3);   // 值域极小 → 大量 ticker 总额相同
        for (int k : new int[]{1, 5, 50, 500}) {
            assertEquals(TopTrades.topTickers(d.t(), d.p(), d.v(), k),
                    ParallelNotional.topTickersParallel(d.t(), d.p(), d.v(), k, 8), "k " + k);
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void argumentChecks() {
        assertThrows(IllegalArgumentException.class, () -> ParallelNotional.totalsScoped(T, P, V, 0));
        assertThrows(IllegalArgumentException.class, () -> ParallelNotional.totalsSharedMap(T, P, V, 0));
        assertThrows(IllegalArgumentException.class, () -> ParallelNotional.totalsForkJoin(T, P, V, 0));
        assertThrows(IllegalArgumentException.class, () -> ParallelNotional.topTickersParallel(T, P, V, -1, 2));
    }

    @Test @Tag("part4") @Tag("edge")
    void chunkBoundariesCoverEveryIndexExactlyOnce() {
        for (int n : new int[]{0, 1, 5, 10, 1_000_003}) {
            for (int chunks : new int[]{1, 2, 3, 7, 64}) {
                assertEquals(0, ParallelNotional.boundary(n, chunks, 0));
                assertEquals(n, ParallelNotional.boundary(n, chunks, chunks));
                for (int c = 0; c < chunks; c++) {
                    assertTrue(ParallelNotional.boundary(n, chunks, c) <= ParallelNotional.boundary(n, chunks, c + 1));
                }
            }
        }
        // n * c 超过 int 范围时也不能错
        assertEquals(1_500_000_000, ParallelNotional.boundary(2_000_000_000, 4, 3));
    }

    // ============================================================ 并发

    @RepeatedTest(20) @Tag("part4") @Tag("conc")
    void manyCallersAtOnceAllGetTheSequentialAnswer(org.junit.jupiter.api.RepetitionInfo info) throws Exception {
        var d = Data.random(info.getCurrentRepetition(), 20_000, 300, 5_000, 200);
        var expect = ParallelNotional.totalsSequential(d.t(), d.p(), d.v());
        int callers = 8;
        var gate = new CountDownLatch(1);
        var ready = new CountDownLatch(callers);
        var failures = new AtomicInteger();
        var threads = new ArrayList<Thread>();
        for (int c = 0; c < callers; c++) {
            final var impl = Impl.values()[c % Impl.values().length];
            threads.add(Thread.ofPlatform().start(() -> {
                ready.countDown();
                try {
                    gate.await();
                    for (int round = 0; round < 3; round++) {
                        if (!expect.equals(impl.run(d.t(), d.p(), d.v(), 4 + round))) failures.incrementAndGet();
                    }
                } catch (Throwable e) {
                    failures.incrementAndGet();
                }
            }));
        }
        ready.await();
        gate.countDown();
        for (var th : threads) th.join();
        assertEquals(0, failures.get());
    }

    @RepeatedTest(20) @Tag("part4") @Tag("conc")
    void failingCallsDoNotContaminateConcurrentGoodCalls(org.junit.jupiter.api.RepetitionInfo info) throws Exception {
        var good = Data.random(100 + info.getCurrentRepetition(), 10_000, 100, 1_000, 100);
        var expect = ParallelNotional.totalsSequential(good.t(), good.p(), good.v());
        var badP = good.p().clone();
        badP[good.p().length / 2] = Long.MAX_VALUE;
        var badV = good.v().clone();
        badV[good.p().length / 2] = 2;
        var gate = new CountDownLatch(1);
        var wrong = new AtomicInteger();
        var threads = new ArrayList<Thread>();
        for (int c = 0; c < 8; c++) {
            final boolean bad = c % 2 == 0;
            final var impl = Impl.values()[c % Impl.values().length];
            threads.add(Thread.ofPlatform().start(() -> {
                try {
                    gate.await();
                    if (bad) {
                        try {
                            impl.run(good.t(), badP, badV, 5);
                            wrong.incrementAndGet();   // 应该抛
                        } catch (ArithmeticException expected) {
                            // 正确
                        }
                    } else if (!expect.equals(impl.run(good.t(), good.p(), good.v(), 5))) {
                        wrong.incrementAndGet();
                    }
                } catch (Throwable e) {
                    wrong.incrementAndGet();
                }
            }));
        }
        gate.countDown();
        for (var th : threads) th.join();
        assertEquals(0, wrong.get());
    }

    @Test @Tag("part4") @Tag("conc")
    void aFailingChunkCancelsTheOthersPromptly() {
        // 第 0 块在第一个事件就溢出；其余块有 ~2M 事件要算，但 ShutdownOnFailure 会中断它们，
        // accumulate 每 4096 个事件检查一次中断标志，所以整个调用远快于算完。
        int n = 8_000_000;
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        java.util.Arrays.fill(t, "A");
        java.util.Arrays.fill(p, 1);
        java.util.Arrays.fill(v, 1);
        p[0] = Long.MAX_VALUE;
        v[0] = 2;
        assertTimeoutPreemptively(Duration.ofSeconds(2), () ->
                assertThrows(ArithmeticException.class, () -> ParallelNotional.totalsScoped(t, p, v, 4)));
    }

    // ============================================================ 性能

    @ParameterizedTest @Tag("part4") @Tag("perf")
    @EnumSource(Impl.class)
    void twoMillionEventsUnderTwoSeconds(Impl impl) {
        var d = Data.random(0, 2_000_000, 50_000, 100_000, 1_000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var m = impl.run(d.t(), d.p(), d.v(), 8);
            assertTrue(m.size() > 40_000);
        });
    }
}
