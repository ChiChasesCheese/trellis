import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.math.MathContext;
import java.time.Duration;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import java.util.Random;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class QueueMeanTest {

    private static QueueMean.Mean frac(long n, long d) { return new QueueMean.Mean(BigInteger.valueOf(n), d); }

    private static List<String> lines(String block) { return block.lines().toList(); }

    /** 慢但显然正确的参照：BigInteger 重新求和。 */
    private static QueueMean.Mean oracle(ArrayDeque<Long> q) {
        BigInteger s = BigInteger.ZERO;
        for (long x : q) s = s.add(BigInteger.valueOf(x));
        return new QueueMean.Mean(s, q.size());
    }

    // ================= Part 1: push / pop / get_mean =================

    @Test @Tag("part1")
    void sampleFromProblemStatement() {
        var q = new QueueMean();
        q.push(1); q.push(2); q.push(3);
        assertEquals(2.0, q.getMean());
        q.push(4);
        assertEquals(2.5, q.getMean());
        assertEquals(1, q.pop());              // FIFO：先弹出最早的
        assertEquals(3.0, q.getMean());
        assertEquals(3, q.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyQueueRejectsPopAndMean() {
        var q = new QueueMean();
        assertTrue(q.isEmpty());
        assertThrows(NoSuchElementException.class, q::pop);
        assertThrows(NoSuchElementException.class, q::getMean);
        assertThrows(NoSuchElementException.class, q::mean);
        q.push(5);
        q.pop();
        assertThrows(NoSuchElementException.class, q::mean); // 弹空之后同样
    }

    @Test @Tag("part1") @Tag("edge")
    void meanIsReducedFractionWithPositiveDenominator() {
        var q = new QueueMean();
        q.push(2); q.push(4);
        assertEquals(frac(3, 1), q.mean());
        assertEquals(frac(6, 4), new QueueMean.Mean(BigInteger.valueOf(3), 2)); // 构造时约分，record equals 才可比
        q.pop(); q.pop();
        q.push(1); q.push(2);
        assertEquals(frac(3, 2), q.mean());
        q.pop(); q.pop();
        q.push(-1); q.push(-2);
        assertEquals(frac(-3, 2), q.mean());           // 符号只在分子
        assertEquals(-1.5, q.getMean());
        assertThrows(IllegalArgumentException.class, () -> new QueueMean.Mean(BigInteger.ONE, 0));
        assertThrows(IllegalArgumentException.class, () -> new QueueMean.Mean(BigInteger.ONE, -2));
    }

    @Test @Tag("part1") @Tag("edge")
    void zeroAndNegativeValues() {
        var q = new QueueMean();
        q.push(-3); q.push(3);
        assertEquals(frac(0, 1), q.mean());
        assertEquals(0.0, q.getMean());
        q.push(0);
        assertEquals(frac(0, 1), q.mean());
    }

    @Test @Tag("part1") @Tag("edge")
    void noFloatDriftFromARunningDoubleSum() {
        // 用 double 维护 running sum：1e16 + 1 + 1 = 1e16（每次加 1 都被舍掉），弹出 1e16 后和变成 0 而不是 2。
        var q = new QueueMean();
        q.push(10_000_000_000_000_000L);
        q.push(1);
        q.push(1);
        q.pop();
        assertEquals(frac(1, 1), q.mean());
        assertEquals(1.0, q.getMean());
    }

    @Test @Tag("part1") @Tag("edge")
    void sumOverflowingLongIsExact() {
        var q = new QueueMean();
        q.push(Long.MAX_VALUE);
        q.push(Long.MAX_VALUE);
        assertEquals(frac(Long.MAX_VALUE, 1), q.mean());   // 和 = 2^64 - 2，已经溢出 long
        q.push(Long.MAX_VALUE);
        assertEquals(frac(Long.MAX_VALUE, 1), q.mean());
        q.pop(); q.pop(); q.pop();
        q.push(5);
        assertEquals(frac(5, 1), q.mean());                 // 从「很大的和」退回小数，没有残留
        var neg = new QueueMean();
        neg.push(Long.MIN_VALUE);
        neg.push(Long.MIN_VALUE);
        assertEquals(frac(Long.MIN_VALUE, 1), neg.mean());
        neg.push(Long.MAX_VALUE);                           // MIN + MIN + MAX = -2^63 - 1
        assertEquals(new QueueMean.Mean(BigInteger.valueOf(Long.MIN_VALUE).subtract(BigInteger.ONE), 3), neg.mean());
    }

    @Test @Tag("part1") @Tag("edge")
    void getMeanIsTheNearestDouble() {
        var q = new QueueMean();
        q.push(Long.MAX_VALUE);
        q.push(Long.MAX_VALUE - 1);                          // 精确均值 MAX - 0.5，最近的 double 是 2^63
        assertEquals(0x1p63, q.getMean());
        var r = new QueueMean();
        r.push(1); r.push(2);
        assertEquals(1.5, r.getMean());
        var s = new QueueMean();
        s.push(1); s.push(1); s.push(2);                     // 4/3：一次除法即正确舍入
        assertEquals(4.0 / 3.0, s.getMean());
    }

    @Test @Tag("part1") @Tag("edge")
    void ringBufferWrapsAndGrowsInFifoOrder() {
        var q = new QueueMean();
        for (int i = 0; i < 1000; i++) q.push(i);
        for (int i = 0; i < 1000; i++) assertEquals(i, q.pop());
        assertTrue(q.isEmpty());
        // 让 head 停在缓冲中间再触发扩容，扩容必须按逻辑顺序拷贝
        for (int i = 0; i < 12; i++) q.push(i);
        for (int i = 0; i < 10; i++) q.pop();
        for (int i = 100; i < 140; i++) q.push(i);
        assertEquals(10, q.pop());
        assertEquals(11, q.pop());
        assertEquals(100, q.pop());
    }

    @Test @Tag("part1") @Tag("edge")
    void randomOpsMatchBigIntegerOracle() {
        var rnd = new Random(1);
        var q = new QueueMean();
        var ref = new ArrayDeque<Long>();
        for (int i = 0; i < 20_000; i++) {
            if (ref.isEmpty() || rnd.nextInt(100) < 55) {
                long x = switch (rnd.nextInt(4)) {
                    case 0 -> rnd.nextLong();
                    case 1 -> Long.MAX_VALUE - rnd.nextInt(3);
                    case 2 -> Long.MIN_VALUE + rnd.nextInt(3);
                    default -> rnd.nextInt(21) - 10;
                };
                q.push(x);
                ref.addLast(x);
            } else {
                assertEquals(ref.pollFirst(), q.pop());
            }
            if (i % 97 == 0 && !ref.isEmpty()) {
                var expected = oracle(ref);
                assertEquals(expected, q.mean());
                var bd = new BigDecimal(expected.numerator()).divide(new BigDecimal(expected.denominator()), MathContext.DECIMAL128);
                assertEquals(bd.doubleValue(), q.getMean());
            }
        }
    }

    @Test @Tag("part1") @Tag("perf")
    void millionOperationsUnderTwoSeconds() {
        var rnd = new Random(0);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var q = new QueueMean();
            double acc = 0;
            for (int i = 0; i < 1_000_000; i++) {
                if (q.isEmpty() || rnd.nextInt(100) < 52) q.push(rnd.nextLong() >> rnd.nextInt(40));
                else q.pop();
                if ((i & 7) == 0 && !q.isEmpty()) acc += q.getMean();
            }
            assertFalse(Double.isNaN(acc));
        });
    }

    // ================= Part 2: 修正快照事件流 =================

    @Test @Tag("part2") @Tag("fmt")
    void sampleSessionExactOutput() {
        var out = QueueEvents.solve(lines("""
                push 1
                push 2
                mean
                pop
                mean
                snapshot 10 20 30
                mean
                pop
                mean
                pop
                pop
                mean
                """));
        assertEquals(List.of("3/2", "2", "20", "25", "empty"), out);
    }

    @Test @Tag("part2")
    void snapshotReplacesTheWholeLogicalHistory() {
        var answers = QueueEvents.run(List.of(
                new QueueEvents.Push(1), new QueueEvents.Push(2), new QueueEvents.Query(),
                new QueueEvents.Correct(List.of(10L)), new QueueEvents.Query(),
                new QueueEvents.Pop(), new QueueEvents.Query()));
        assertEquals(List.of(new QueueEvents.Value(frac(3, 2)), new QueueEvents.Value(frac(10, 1)), new QueueEvents.Empty()), answers);
    }

    @Test @Tag("part2") @Tag("edge")
    void snapshotKeepsFifoOrderAndCanBeEmpty() {
        assertEquals(List.of("13/2", "empty"), QueueEvents.solve(lines("""
                snapshot 5 6 7
                pop
                mean
                snapshot
                mean
                """)));
    }

    @Test @Tag("part2") @Tag("edge")
    void snapshotWithOverflowingSum() {
        var big = Long.MAX_VALUE;
        assertEquals(List.of(Long.toString(big)), QueueEvents.solve(List.of("snapshot %d %d %d".formatted(big, big, big), "mean")));
    }

    @Test @Tag("part2") @Tag("edge")
    void correctEventCopiesItsContents() {
        var src = new ArrayList<>(List.of(1L, 2L));
        var event = new QueueEvents.Correct(src);
        src.add(99L);
        assertEquals(List.of(1L, 2L), event.contents());
        var withNull = new ArrayList<Long>();
        withNull.add(null);
        assertThrows(NullPointerException.class, () -> new QueueEvents.Correct(withNull));
    }

    @Test @Tag("part2") @Tag("edge")
    void popOnEmptyIsAnError() {
        assertThrows(NoSuchElementException.class, () -> QueueEvents.run(List.of(new QueueEvents.Pop())));
        assertThrows(NoSuchElementException.class, () -> QueueEvents.solve(List.of("snapshot 1", "pop", "pop")));
    }

    @Test @Tag("part2") @Tag("edge")
    void noQueriesNoAnswers() {
        assertEquals(List.of(), QueueEvents.run(List.of()));
        assertEquals(List.of(), QueueEvents.solve(List.of("push 1", "", "pop")));
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(strings = {"push", "push x", "push 1 2", "push 99999999999999999999", "pop 3", "mean 1", "snapshot a", "PUSH 1", "peek"})
    void parseRejectsMalformedLinesWithTheLineNumber(String bad) {
        var ex = assertThrows(IllegalArgumentException.class, () -> QueueEvents.parse(List.of("push 1", bad)));
        assertTrue(ex.getMessage().startsWith("line 2:"), ex.getMessage());
    }

    @Test @Tag("part2") @Tag("fmt")
    void renderFormats() {
        assertEquals("7", QueueEvents.render(new QueueEvents.Value(frac(7, 1))));
        assertEquals("-7/2", QueueEvents.render(new QueueEvents.Value(frac(-7, 2))));
        assertEquals("0", QueueEvents.render(new QueueEvents.Value(frac(0, 5))));
        assertEquals("empty", QueueEvents.render(new QueueEvents.Empty()));
    }

    @Test @Tag("part2") @Tag("perf")
    void millionEventsWithSnapshotsUnderTwoSeconds() {
        var rnd = new Random(0);
        var events = new ArrayList<QueueEvents.Event>();
        int size = 0;
        for (int i = 0; i < 1_000_000; i++) {
            int r = rnd.nextInt(100);
            if (r < 45 || size == 0) { events.add(new QueueEvents.Push(rnd.nextLong())); size++; }
            else if (r < 85) { events.add(new QueueEvents.Pop()); size--; }
            else if (r < 99) events.add(new QueueEvents.Query());
            else {
                int m = rnd.nextInt(5);
                var c = new ArrayList<Long>();
                for (int j = 0; j < m; j++) c.add(rnd.nextLong());
                events.add(new QueueEvents.Correct(c));
                size = m;
            }
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> QueueEvents.run(events));
    }

    // ================= Part 3: 持久化 / 版本化 =================

    @Test @Tag("part3")
    void oldVersionsStayUsable() {
        var vq = new VersionedQueue();
        int v1 = vq.push(VersionedQueue.EMPTY, 1);
        int v2 = vq.push(v1, 2);
        int v3 = vq.pop(v2);
        assertEquals(List.of(2L), vq.contents(v3));
        assertEquals(frac(3, 2), vq.mean(v2));          // 旧版本不被后面的 pop 改动
        assertEquals(2, vq.size(v2));
        assertEquals(0, vq.size(VersionedQueue.EMPTY));
        int branchA = vq.push(v2, 10);                    // 从同一个旧版本分叉
        int branchB = vq.push(v2, 20);
        assertEquals(List.of(1L, 2L, 10L), vq.contents(branchA));
        assertEquals(List.of(1L, 2L, 20L), vq.contents(branchB));
        assertEquals(frac(13, 3), vq.mean(branchA));
    }

    @Test @Tag("part3")
    void correctStartsAnIndependentHistory() {
        var vq = new VersionedQueue();
        int base = vq.push(VersionedQueue.EMPTY, 100);
        int fixed = vq.correct(List.of(1L, 2L, 3L));
        assertEquals(frac(2, 1), vq.mean(fixed));
        int popped = vq.pop(fixed);
        assertEquals(List.of(2L, 3L), vq.contents(popped));
        assertEquals(List.of(100L), vq.contents(base));   // 修正不影响原来的历史
        assertEquals(0, vq.size(vq.correct(List.of())));
    }

    @Test @Tag("part3") @Tag("edge")
    void emptyVersionAndUnknownVersionAreRejected() {
        var vq = new VersionedQueue();
        assertThrows(NoSuchElementException.class, () -> vq.pop(VersionedQueue.EMPTY));
        assertThrows(NoSuchElementException.class, () -> vq.mean(VersionedQueue.EMPTY));
        int v = vq.pop(vq.push(VersionedQueue.EMPTY, 7));
        assertThrows(NoSuchElementException.class, () -> vq.pop(v));
        assertThrows(IllegalArgumentException.class, () -> vq.push(-1, 1));
        assertThrows(IllegalArgumentException.class, () -> vq.size(99));
        assertThrows(IllegalArgumentException.class, () -> vq.mean(99));
    }

    @Test @Tag("part3") @Tag("edge")
    void exactSumsSurviveOverflowAcrossVersions() {
        var vq = new VersionedQueue();
        int v = VersionedQueue.EMPTY;
        for (int i = 0; i < 3; i++) v = vq.push(v, Long.MAX_VALUE);
        assertEquals(frac(Long.MAX_VALUE, 1), vq.mean(v));
        int w = vq.pop(vq.pop(v));
        assertEquals(frac(Long.MAX_VALUE, 1), vq.mean(w));
        int z = vq.push(w, Long.MIN_VALUE);                // [MAX, MIN]，和 = -1
        assertEquals(frac(-1, 2), vq.mean(z));
    }

    @Test @Tag("part3") @Tag("edge")
    void randomBranchingMatchesCopyingModel() {
        var rnd = new Random(7);
        var vq = new VersionedQueue();
        var model = new ArrayList<List<Long>>();
        model.add(List.of());
        for (int step = 0; step < 6000; step++) {
            int base = rnd.nextInt(model.size());
            var content = model.get(base);
            int r = rnd.nextInt(10);
            int got;
            List<Long> expected;
            if (r < 5 || content.isEmpty() && r < 9) {
                long x = rnd.nextInt(5) == 0 ? Long.MAX_VALUE : rnd.nextInt(2001) - 1000;
                got = vq.push(base, x);
                var tmp = new ArrayList<>(content);
                tmp.add(x);
                expected = tmp;
            } else if (r < 9) {
                got = vq.pop(base);
                expected = content.subList(1, content.size());
            } else {
                expected = List.of((long) rnd.nextInt(10), (long) rnd.nextInt(10));
                got = vq.correct(expected);
            }
            expected = List.copyOf(expected);
            assertEquals(model.size(), got, "version ids are dense and increasing");
            model.add(expected);
            assertEquals(expected, vq.contents(got));
            assertEquals(expected.size(), vq.size(got));
            if (!expected.isEmpty()) {
                BigInteger s = expected.stream().map(BigInteger::valueOf).reduce(BigInteger.ZERO, BigInteger::add);
                assertEquals(new QueueMean.Mean(s, expected.size()), vq.mean(got));
            }
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void deepChainsAndWideBranchingUnderTwoSeconds() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var rnd = new Random(0);
            var vq = new VersionedQueue();
            int n = 300_000;
            int v = VersionedQueue.EMPTY;
            for (int i = 0; i < n; i++) v = vq.push(v, i);
            int first = v;
            for (int i = 0; i < n; i++) v = vq.pop(v);        // 每次 pop 都要找深度 i+1 的祖先
            assertEquals(0, vq.size(v));
            assertEquals(new QueueMean.Mean(BigInteger.valueOf((long) n * (n - 1) / 2), n), vq.mean(first));
            // 随机选旧版本分叉：朴素的「每个版本拷贝一份数组」在这里是 O(n^2)
            var ids = new int[200_000];
            ids[0] = first;
            for (int i = 1; i < ids.length; i++) {
                int base = ids[rnd.nextInt(i)];
                ids[i] = vq.size(base) == 0 || rnd.nextBoolean() ? vq.push(base, rnd.nextLong()) : vq.pop(base);
            }
        });
    }

    // ================= Part 4: 单写者 + 多读者 =================

    @Test @Tag("part4")
    void singleThreadedBehaviour() {
        var sm = new SharedMean();
        assertEquals(0, sm.read().seq());
        assertTrue(sm.mean().isEmpty());
        sm.push(1); sm.push(2);
        assertEquals(Optional.of(frac(3, 2)), sm.mean());
        assertEquals(1, sm.pop());
        assertEquals(3, sm.read().seq());
        assertEquals(1, sm.read().size());
        sm.pop();
        assertTrue(sm.mean().isEmpty());
        assertThrows(NoSuchElementException.class, sm::pop);
    }

    @Test @Tag("part4") @Tag("edge")
    void secondWriterThreadIsRejected() throws Exception {
        var sm = new SharedMean();
        sm.push(1);
        var failure = new AtomicReference<Throwable>();
        var t = Thread.ofVirtual().start(() -> {
            try { sm.push(2); } catch (Throwable e) { failure.set(e); }
        });
        t.join();
        assertTrue(failure.get() instanceof IllegalStateException, String.valueOf(failure.get()));
        assertEquals(1, sm.read().size());
        sm.push(3);                                        // 原写者不受影响
        assertEquals(2, sm.read().size());
    }

    /** 不变量：队列里永远只有 7，所以任何一致的快照的均值恰好是 7/1（空则 Optional.empty）。撕裂读会得到 7k/(k±1)。 */
    @RepeatedTest(25) @Tag("part4") @Tag("conc")
    void readersAlwaysSeeAConsistentMean() throws Exception {
        final int readers = 4, ops = 3000;
        var sm = new SharedMean();
        var start = new CountDownLatch(1);
        var done = new AtomicBoolean();
        var problems = new ConcurrentLinkedQueue<String>();
        try (var pool = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = new ArrayList<Future<?>>();
            for (int r = 0; r < readers; r++) {
                futures.add(pool.submit(() -> {
                    start.await();
                    long lastSeq = -1;
                    long reads = 0;
                    while (!done.get() || reads < 1) {
                        var st = sm.read();
                        reads++;
                        Thread.yield(); // 虚拟线程是协作式调度：纯自旋的读者会占满所有 carrier，把写者饿死
                        if (st.seq() < lastSeq) problems.add("seq went backwards " + lastSeq + " -> " + st.seq());
                        lastSeq = st.seq();
                        var mean = st.mean();
                        if (st.size() == 0 ? mean.isPresent() : !mean.equals(Optional.of(frac(7, 1))))
                            problems.add("torn read: size=" + st.size() + " mean=" + mean);
                        if (!st.sum().toBigInteger().equals(BigInteger.valueOf(7L * st.size())))
                            problems.add("sum/size mismatch: " + st);
                    }
                    return null;
                }));
            }
            var writer = pool.submit(() -> {
                var rnd = new Random(42);
                start.await();
                int size = 0;
                try {
                    for (int i = 0; i < ops; i++) {
                        if (size == 0 || rnd.nextInt(100) < 55) { sm.push(7); size++; }
                        else { sm.pop(); size--; }
                    }
                } finally {
                    done.set(true); // 写者出错也要放读者走，否则读者自旋到永远
                }
                return size;
            });
            start.countDown();
            int finalSize = writer.get();
            for (var f : futures) f.get();
            assertEquals(finalSize, sm.read().size());
            assertEquals(ops, sm.read().seq());
        }
        assertTrue(problems.isEmpty(), () -> problems.stream().limit(5).toList().toString());
    }
}
