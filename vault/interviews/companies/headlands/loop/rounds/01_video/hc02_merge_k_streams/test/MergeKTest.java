import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import java.util.Random;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class MergeKTest {

    // ---------------------------------------------------------------- helpers

    /** 比较时只看 key：用来检查「相等元素按序列编号稳定输出」。 */
    record Rec(int key, String tag) implements Comparable<Rec> {
        @Override public int compareTo(Rec o) { return Integer.compare(key, o.key); }
    }

    /** 显然正确的参照：按序列顺序拼接，再做稳定排序（List.sort 是稳定的）。 */
    private static <T extends Comparable<? super T>> List<T> oracle(List<? extends List<? extends T>> lists) {
        var all = new ArrayList<T>();
        lists.forEach(all::addAll);
        all.sort(null);
        return all;
    }

    private static List<List<Integer>> randomSortedLists(Random rnd, int k, int maxLen, int bound) {
        var lists = new ArrayList<List<Integer>>();
        for (int i = 0; i < k; i++) {
            var l = new ArrayList<Integer>();
            int n = rnd.nextInt(maxLen + 1);
            for (int j = 0; j < n; j++) l.add(rnd.nextInt(bound));
            Collections.sort(l);
            lists.add(l);
        }
        return lists;
    }

    /** 记录 next() 被调用了多少次的迭代器。 */
    static final class Counting<T> implements Iterator<T> {
        private final Iterator<T> inner;
        final AtomicInteger pulls = new AtomicInteger();

        Counting(List<T> data) { inner = data.iterator(); }

        @Override public boolean hasNext() { return inner.hasNext(); }

        @Override public T next() {
            pulls.incrementAndGet();
            return inner.next();
        }
    }

    /** 由测试线程手动喂数据的「慢」source：hasNext 阻塞直到有数据或结束。 */
    static final class Gated implements Iterator<Integer> {
        private static final Optional<Integer> END = Optional.empty();
        final BlockingQueue<Optional<Integer>> feed = new LinkedBlockingQueue<>();
        final CountDownLatch interrupted = new CountDownLatch(1);
        private Integer buffered;
        private boolean ended;

        void give(int v) { feed.add(Optional.of(v)); }

        void end() { feed.add(END); }

        @Override public boolean hasNext() {
            if (buffered != null) return true;
            if (ended) return false;
            try {
                var o = feed.take();
                if (o.isEmpty()) { ended = true; return false; }
                buffered = o.get();
                return true;
            } catch (InterruptedException e) {
                interrupted.countDown();
                Thread.currentThread().interrupt();
                throw new IllegalStateException("interrupted while waiting for data", e);
            }
        }

        @Override public Integer next() {
            if (!hasNext()) throw new NoSuchElementException();
            var v = buffered;
            buffered = null;
            return v;
        }
    }

    /** 第一次 hasNext 前等发令枪；每次取元素前随机 yield，把线程交错打乱。 */
    static final class Jittery implements Iterator<Integer> {
        private final Iterator<Integer> inner;
        private final CountDownLatch gate;
        private final Random rnd;
        private boolean passed;

        Jittery(List<Integer> data, CountDownLatch gate, long seed) {
            this.inner = data.iterator();
            this.gate = gate;
            this.rnd = new Random(seed);
        }

        @Override public boolean hasNext() {
            if (!passed) {
                try { gate.await(); } catch (InterruptedException e) { throw new IllegalStateException(e); }
                passed = true;
            }
            if (rnd.nextInt(4) == 0) Thread.yield();
            return inner.hasNext();
        }

        @Override public Integer next() { return inner.next(); }
    }

    // ================= Part 1: 合并 k 个列表 =================

    @Test @Tag("part1")
    void sampleFromProblemStatement() {
        assertEquals(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9),
                MergeK.merge(List.of(List.of(1, 4, 7), List.of(2, 5, 8), List.of(3, 6, 9))));
        assertEquals(List.of(1, 1, 2, 3, 4, 4, 5, 6),
                MergeK.merge(List.of(List.of(1, 4, 5), List.of(1, 3, 4), List.of(2, 6))));
    }

    @Test @Tag("part1") @Tag("edge")
    void degenerateShapes() {
        assertEquals(List.of(), MergeK.<Integer>merge(List.of()));                       // k = 0
        assertEquals(List.of(), MergeK.<Integer>merge(List.of(List.of(), List.of())));   // 全是空序列
        assertEquals(List.of(3), MergeK.merge(List.of(List.<Integer>of(), List.of(3), List.of())));
        assertEquals(List.of(1, 2, 3), MergeK.merge(List.of(List.of(1, 2, 3))));         // k = 1
        assertEquals(List.of(-5, -5, 0, 7, 7, 7), MergeK.merge(List.of(List.of(-5, 7, 7), List.of(-5, 0, 7))));
    }

    @Test @Tag("part1") @Tag("edge")
    void extremesDoNotOverflowComparisons() {
        // 用 a - b 比较大小会在这里溢出
        assertEquals(List.of(Long.MIN_VALUE, -1L, Long.MAX_VALUE, Long.MAX_VALUE),
                MergeK.merge(List.of(List.of(Long.MIN_VALUE, Long.MAX_VALUE), List.of(-1L, Long.MAX_VALUE))));
        assertArrayEquals(new long[]{Long.MIN_VALUE, 0, Long.MAX_VALUE},
                MergeK.mergeLongs(new long[][]{{Long.MIN_VALUE, Long.MAX_VALUE}, {0}}));
    }

    private static void assertArrayEquals(long[] expected, long[] actual) {
        org.junit.jupiter.api.Assertions.assertArrayEquals(expected, actual);
    }

    @Test @Tag("part1") @Tag("edge")
    void equalElementsComeOutInStreamOrder() {
        var a = List.of(new Rec(1, "a1"), new Rec(2, "a2"), new Rec(2, "a3"));
        var b = List.of(new Rec(1, "b1"), new Rec(2, "b2"));
        var c = List.of(new Rec(2, "c1"));
        var tags = MergeK.merge(List.of(a, b, c)).stream().map(Rec::tag).toList();
        assertEquals(List.of("a1", "b1", "a2", "a3", "b2", "c1"), tags);
        var swapped = MergeK.merge(List.of(c, b, a)).stream().map(Rec::tag).toList();
        assertEquals(List.of("b1", "a1", "c1", "b2", "a2", "a3"), swapped);
    }

    @Test @Tag("part1") @Tag("edge")
    void unsortedInputIsReportedWithLocation() {
        var ex = assertThrows(MergeK.UnsortedInputException.class,
                () -> MergeK.merge(List.of(List.of(1, 2, 3), List.of(5, 9, 4, 10))));
        assertEquals(1, ex.stream());
        assertEquals(2, ex.position());
        var ex2 = assertThrows(MergeK.UnsortedInputException.class,
                () -> MergeK.mergeLongs(new long[][]{{1, 2}, {3, 2}}));
        assertEquals(1, ex2.stream());
        assertEquals(1, ex2.position());
    }

    @Test @Tag("part1") @Tag("edge")
    void nullElementsAreRejected() {
        var withNull = new ArrayList<Integer>();
        withNull.add(1);
        withNull.add(null);
        assertThrows(NullPointerException.class, () -> MergeK.merge(List.of(withNull, List.of(2))));
    }

    @Test @Tag("part1") @Tag("edge")
    void inputsAreNotModified() {
        var a = new ArrayList<>(List.of(1, 3));
        var b = new ArrayList<>(List.of(2));
        MergeK.merge(List.of(a, b));
        assertEquals(List.of(1, 3), a);
        assertEquals(List.of(2), b);
    }

    @Test @Tag("part1") @Tag("edge")
    void randomMatchesStableSortOracleAndPrimitiveVersion() {
        var rnd = new Random(11);
        for (int round = 0; round < 300; round++) {
            var lists = randomSortedLists(rnd, rnd.nextInt(12), 30, 15);
            assertEquals(oracle(lists), MergeK.merge(lists));
            long[][] arrays = lists.stream().map(l -> l.stream().mapToLong(Integer::longValue).toArray()).toArray(long[][]::new);
            long[] expected = oracle(lists).stream().mapToLong(Integer::longValue).toArray();
            assertArrayEquals(expected, MergeK.mergeLongs(arrays));
        }
    }

    @Test @Tag("part1") @Tag("perf")
    void millionElementsInThousandListsUnderTwoSeconds() {
        var rnd = new Random(0);
        int k = 1000, per = 1000;
        var lists = new ArrayList<List<Integer>>();
        long[][] arrays = new long[k][];
        for (int i = 0; i < k; i++) {
            long[] a = rnd.longs(per, 0, 1_000_000).sorted().toArray();
            arrays[i] = a;
            lists.add(Arrays.stream(a).mapToObj(x -> (int) x).toList());
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var merged = MergeK.merge(lists);
            assertEquals(k * per, merged.size());
            assertTrue(merged.get(0) <= merged.get(merged.size() - 1));
        });
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            long[] merged = MergeK.mergeLongs(arrays);
            assertEquals(k * per, merged.length);
            for (int i = 1; i < merged.length; i++) if (merged[i - 1] > merged[i]) throw new AssertionError("not sorted at " + i);
        });
    }

    // ================= Part 2: 惰性迭代器 / Stream =================

    @Test @Tag("part2")
    void constructionPullsNothingAndPullsAreMinimal() {
        var a = new Counting<>(List.of(1, 4, 7));
        var b = new Counting<>(List.of(2, 5, 8));
        var c = new Counting<>(List.<Integer>of());
        var it = MergeK.mergeIterators(List.of(a, b, c));
        assertEquals(0, a.pulls.get() + b.pulls.get());               // 构造时一个都不取
        assertEquals(1, it.next());
        assertEquals(1, a.pulls.get());                                // 每个非空 source 各取一个队首
        assertEquals(1, b.pulls.get());
        assertEquals(2, it.next());                                    // 这时才给 a 补位
        assertEquals(2, a.pulls.get());
        assertEquals(1, b.pulls.get());                            // b 刚输出，补位推迟到下一次调用
        assertTrue(it.hasNext());
        assertEquals(2, b.pulls.get());
    }

    @Test @Tag("part2")
    void totalPullsNeverExceedKPlusConsumed() {
        var rnd = new Random(5);
        var data = randomSortedLists(rnd, 7, 40, 100);
        var srcs = data.stream().map(Counting::new).toList();
        var it = MergeK.mergeIterators(srcs);
        int consumed = 0;
        while (consumed < 50 && it.hasNext()) {
            it.next();
            consumed++;
            int pulls = srcs.stream().mapToInt(s -> s.pulls.get()).sum();
            assertTrue(pulls <= srcs.size() + consumed - 1, "pulls=" + pulls + " consumed=" + consumed);
        }
    }

    @Test @Tag("part2")
    void worksOnInfiniteStreams() {
        var evens = Stream.iterate(0, x -> x + 2).iterator();
        var threes = Stream.iterate(0, x -> x + 3).iterator();
        var it = MergeK.mergeIterators(List.of(evens, threes));
        var firstTen = new ArrayList<Integer>();
        for (int i = 0; i < 10; i++) firstTen.add(it.next());
        assertEquals(List.of(0, 0, 2, 3, 4, 6, 6, 8, 9, 10), firstTen);
    }

    @Test @Tag("part2") @Tag("edge")
    void hasNextIsIdempotentAndEndIsSticky() {
        var it = MergeK.mergeIterators(List.of(List.of(1).iterator(), List.<Integer>of().iterator()));
        assertTrue(it.hasNext());
        assertTrue(it.hasNext());
        assertEquals(1, it.next());
        assertFalse(it.hasNext());
        assertFalse(it.hasNext());
        assertThrows(NoSuchElementException.class, it::next);
        assertFalse(MergeK.mergeIterators(List.<Iterator<Integer>>of()).hasNext());
    }

    @Test @Tag("part2") @Tag("edge")
    void streamTiesGoToLowerStreamIndex() {
        var a = List.of(new Rec(1, "a1"), new Rec(1, "a2")).iterator();
        var b = List.of(new Rec(1, "b1")).iterator();
        var tags = new ArrayList<String>();
        MergeK.mergeIterators(List.of(a, b)).forEachRemaining(r -> tags.add(r.tag()));
        assertEquals(List.of("a1", "a2", "b1"), tags);
    }

    @Test @Tag("part2") @Tag("edge")
    void unsortedIsDetectedOnlyWhenReached() {
        var it = MergeK.mergeIterators(List.of(List.of(1, 5, 3).iterator(), List.of(2, 4).iterator()));
        assertEquals(1, it.next());
        assertEquals(2, it.next());
        assertEquals(4, it.next());
        assertEquals(5, it.next());                                    // 5 之后的 3 此刻还没被读到
        var ex = assertThrows(MergeK.UnsortedInputException.class, it::hasNext);
        assertEquals(0, ex.stream());
        assertEquals(2, ex.position());
    }

    @Test @Tag("part2") @Tag("edge")
    void nullFromASourceIsRejected() {
        var src = new ArrayList<Integer>();
        src.add(null);
        var it = MergeK.mergeIterators(List.of(src.iterator()));
        assertThrows(NullPointerException.class, it::hasNext);
    }

    @Test @Tag("part2")
    void streamVersionIsLazyAndClosesSources() {
        var closed = new AtomicInteger();
        var pulled = new AtomicInteger();
        Stream<Integer> a = Stream.iterate(0, x -> x + 2).peek(x -> pulled.incrementAndGet()).onClose(closed::incrementAndGet);
        Stream<Integer> b = Stream.iterate(1, x -> x + 2).peek(x -> pulled.incrementAndGet()).onClose(closed::incrementAndGet);
        List<Integer> firstFive;
        try (var merged = MergeK.mergeStreams(List.of(a, b))) {
            firstFive = merged.limit(5).toList();
        }
        assertEquals(List.of(0, 1, 2, 3, 4), firstFive);
        assertEquals(2, closed.get());
        assertTrue(pulled.get() <= 8, "pulled " + pulled.get());      // 惰性：只比需要的多一点点
    }

    @Test @Tag("part2") @Tag("edge")
    void streamVersionMatchesOracle() {
        var rnd = new Random(3);
        for (int round = 0; round < 100; round++) {
            var lists = randomSortedLists(rnd, rnd.nextInt(8), 20, 10);
            var merged = MergeK.mergeStreams(lists.stream().map(List::stream).toList()).toList();
            assertEquals(oracle(lists), merged);
        }
    }

    @Test @Tag("part2") @Tag("perf")
    void millionElementsThroughIteratorUnderTwoSeconds() {
        var rnd = new Random(0);
        var lists = new ArrayList<List<Integer>>();
        for (int i = 0; i < 100; i++) {
            lists.add(IntStream.generate(() -> rnd.nextInt(1_000_000)).limit(10_000).sorted().boxed().toList());
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var it = MergeK.mergeIterators(lists.stream().map(List::iterator).toList());
            long n = 0;
            int prev = Integer.MIN_VALUE;
            while (it.hasNext()) {
                int v = it.next();
                if (v < prev) throw new AssertionError("not sorted");
                prev = v;
                n++;
            }
            assertEquals(1_000_000, n);
        });
    }

    // ================= Part 3: 生产者线程 + 有界队列 + 非阻塞 =================

    private static <T extends Comparable<? super T>> List<T> drainBlocking(ConcurrentMerge<T> m) throws InterruptedException {
        var out = new ArrayList<T>();
        while (true) {
            switch (m.next()) {
                case ConcurrentMerge.Ready<T>(var v, _) -> out.add(v);
                case ConcurrentMerge.Done<T> _ -> { return out; }
                case ConcurrentMerge.Pending<T> _ -> throw new AssertionError("next() must not return Pending");
            }
        }
    }

    @Test @Tag("part3")
    void blockingNextProducesTheMergedSequence() throws Exception {
        var lists = List.of(List.of(1, 4, 7), List.of(2, 5, 8), List.of(3, 6, 9));
        try (var m = ConcurrentMerge.start(lists.stream().map(List::iterator).toList(), 2)) {
            assertEquals(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9), drainBlocking(m));
            assertInstanceOf(ConcurrentMerge.Done.class, m.next());     // Done 之后仍是 Done
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void emptyAndZeroSourcesAndBadCapacity() throws Exception {
        try (var m = ConcurrentMerge.<Integer>start(List.of(), 1)) {
            assertEquals(List.of(), drainBlocking(m));
        }
        try (var m = ConcurrentMerge.start(List.of(List.<Integer>of().iterator(), List.<Integer>of().iterator()), 1)) {
            assertEquals(List.of(), drainBlocking(m));
        }
        assertThrows(IllegalArgumentException.class, () -> ConcurrentMerge.start(List.of(List.of(1).iterator()), 0));
    }

    @Test @Tag("part3") @Tag("edge")
    void tryNextIsPendingUntilEveryLiveStreamHasAHead() throws Exception {
        var fast = new Gated();
        var slow = new Gated();
        fast.give(1);
        fast.give(3);
        fast.end();
        try (var m = ConcurrentMerge.<Integer>start(List.of(fast, slow), 4)) {
            // slow 还没给出任何东西：fast 里的 1 也不能输出——slow 可能马上给 0
            for (int i = 0; i < 2000; i++) assertInstanceOf(ConcurrentMerge.Pending.class, m.tryNext());
            slow.give(2);
            slow.end();
            var got = new ArrayList<Integer>();
            assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
                while (true) {
                    var p = m.tryNext();
                    if (p instanceof ConcurrentMerge.Ready<Integer>(var v, _)) got.add(v);
                    else if (p instanceof ConcurrentMerge.Done<Integer>) return;
                    else Thread.yield(); // Pending：让生产者线程跑
                }
            });
            assertEquals(List.of(1, 2, 3), got);
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void readyCarriesTheStreamIndex() throws Exception {
        try (var m = ConcurrentMerge.start(List.of(List.of(5).iterator(), List.of(5).iterator()), 1)) {
            var first = (ConcurrentMerge.Ready<Integer>) m.next();
            var second = (ConcurrentMerge.Ready<Integer>) m.next();
            assertEquals(0, first.stream());                           // 相等时编号小的先出
            assertEquals(1, second.stream());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void backpressureBoundsReadAhead() throws Exception {
        var data = IntStream.range(0, 1000).boxed().toList();
        var src = new Counting<>(data);
        int capacity = 4;
        try (var m = ConcurrentMerge.start(List.of(src), capacity)) {
            assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
                while (src.pulls.get() < capacity + 1) Thread.yield();  // 队列满 + 手里再拿着一个，卡在 put
            });
            for (int i = 0; i < 2000; i++) Thread.yield();
            assertEquals(capacity + 1, src.pulls.get());               // 消费者不动，生产者就停在 capacity+1
            assertEquals(0, ((ConcurrentMerge.Ready<Integer>) m.next()).value());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void failingSourceSurfacesAsMergeExceptionAfterItsEarlierItems() throws Exception {
        Iterator<Integer> boom = new Iterator<>() {
            int i;
            @Override public boolean hasNext() { return true; }
            @Override public Integer next() {
                if (i++ == 2) throw new IllegalStateException("disk on fire");
                return 10 * i;
            }
        };
        var other = new Gated();                                        // 永远不给数据：只能靠终止标记/关闭退出
        try (var m = ConcurrentMerge.<Integer>start(List.of(boom, other), 4)) {
            var ex = assertThrows(ConcurrentMerge.MergeException.class, () -> {
                other.give(100);                                         // 让 other 有队首，这样合并器会读到 boom 的消息
                for (int i = 0; i < 10; i++) m.next();
            });
            assertEquals(0, ex.stream());
            assertEquals("disk on fire", ex.getCause().getMessage());
            assertTimeoutPreemptively(Duration.ofSeconds(5), () -> other.interrupted.await()); // 失败后其余生产者被中断
            assertThrows(IllegalStateException.class, m::tryNext);      // 已关闭
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void unsortedSourceFailsWithUnsortedCause() throws Exception {
        try (var m = ConcurrentMerge.start(List.of(List.of(1, 3, 2).iterator()), 2)) {
            var ex = assertThrows(ConcurrentMerge.MergeException.class, () -> drainBlocking(m));
            var cause = assertInstanceOf(MergeK.UnsortedInputException.class, ex.getCause());
            assertEquals(2, cause.position());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void closeInterruptsBlockedProducersAndIsIdempotent() throws Exception {
        var stuck = new Gated();
        var m = ConcurrentMerge.<Integer>start(List.of(stuck), 1);
        assertInstanceOf(ConcurrentMerge.Pending.class, m.tryNext());
        assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
            m.close();
            m.close();
            stuck.interrupted.await();
        });
        assertThrows(IllegalStateException.class, m::next);
    }

    @RepeatedTest(25) @Tag("part3") @Tag("conc")
    void randomInterleavingsGiveTheDeterministicStableMerge(org.junit.jupiter.api.RepetitionInfo info) throws Exception {
        long seed = info.getCurrentRepetition();
        var rnd = new Random(seed);
        var lists = randomSortedLists(rnd, 2 + rnd.nextInt(8), 400, 50);   // 值域小 → 大量相等元素
        var gate = new CountDownLatch(1);
        var sources = new ArrayList<Iterator<Integer>>();
        for (int i = 0; i < lists.size(); i++) sources.add(new Jittery(lists.get(i), gate, seed * 100 + i));
        // 编码 (key, stream) 以验证稳定性：相等 key 必须按流编号输出
        var m = ConcurrentMerge.start(sources, 1 + rnd.nextInt(6));
        try (m) {
            gate.countDown();
            var out = new ArrayList<Integer>();
            var streams = new ArrayList<Integer>();
            while (true) {
                var p = m.next();
                if (p instanceof ConcurrentMerge.Ready<Integer>(var v, var s)) { out.add(v); streams.add(s); }
                else break;
            }
            assertEquals(oracle(lists), out);
            for (int i = 1; i < out.size(); i++) {
                if (out.get(i).equals(out.get(i - 1))) assertTrue(streams.get(i) >= streams.get(i - 1), "tie order at " + i);
            }
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void eightStreamsOfFiftyThousandUnderTwoSeconds() {
        var rnd = new Random(0);
        var lists = new ArrayList<List<Integer>>();
        for (int i = 0; i < 8; i++) lists.add(IntStream.generate(() -> rnd.nextInt(1_000_000)).limit(50_000).sorted().boxed().toList());
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            try (var m = ConcurrentMerge.start(lists.stream().map(List::iterator).toList(), 1024)) {
                var out = drainBlocking(m);
                assertEquals(400_000, out.size());
                for (int i = 1; i < out.size(); i++) if (out.get(i - 1) > out.get(i)) throw new AssertionError("not sorted");
            }
        });
    }

    // ================= Part 4: StructuredTaskScope =================

    @Test @Tag("part4")
    void mergeAllReturnsTheMergedList() throws Exception {
        var lists = List.of(List.of(1, 4, 7), List.<Integer>of(), List.of(2, 5, 8), List.of(3, 6, 9));
        assertEquals(List.of(1, 2, 3, 4, 5, 6, 7, 8, 9), ConcurrentMerge.mergeAll(lists.stream().map(List::iterator).toList(), 2));
        assertEquals(List.of(), ConcurrentMerge.<Integer>mergeAll(List.of(), 1));
        assertThrows(IllegalArgumentException.class, () -> ConcurrentMerge.mergeAll(List.of(List.of(1).iterator()), 0));
    }

    @Test @Tag("part4") @Tag("edge")
    void oneFailingProducerCancelsTheOthers() {
        var stuck = new Gated();                                        // 永远等不到数据
        var stuck2 = new Gated();
        Iterator<Integer> boom = new Iterator<>() {
            @Override public boolean hasNext() { return true; }
            @Override public Integer next() { throw new IllegalArgumentException("bad record"); }
        };
        var ex = assertTimeoutPreemptively(Duration.ofSeconds(5), () ->
                assertThrows(ConcurrentMerge.MergeException.class,
                        () -> ConcurrentMerge.mergeAll(List.of(stuck, boom, stuck2), 2)));
        assertEquals(1, ex.stream());
        assertEquals("bad record", ex.getCause().getMessage());
        // 走出 mergeAll 时，另外两个生产者必须已经被中断并结束（StructuredTaskScope 的承诺）
        assertEquals(0, stuck.interrupted.getCount());
        assertEquals(0, stuck2.interrupted.getCount());
    }

    @Test @Tag("part4") @Tag("edge")
    void unsortedInputFailsMergeAll() {
        var ex = assertThrows(ConcurrentMerge.MergeException.class,
                () -> ConcurrentMerge.mergeAll(List.of(List.of(1, 2).iterator(), List.of(5, 4).iterator()), 2));
        assertEquals(1, ex.stream());
        assertInstanceOf(MergeK.UnsortedInputException.class, ex.getCause());
    }

    @RepeatedTest(25) @Tag("part4") @Tag("conc")
    void mergeAllMatchesOracleUnderRandomInterleavings(org.junit.jupiter.api.RepetitionInfo info) throws Exception {
        long seed = 1000 + info.getCurrentRepetition();
        var rnd = new Random(seed);
        var lists = randomSortedLists(rnd, 1 + rnd.nextInt(9), 300, 40);
        var gate = new CountDownLatch(1);
        var sources = new ArrayList<Iterator<Integer>>();
        for (int i = 0; i < lists.size(); i++) sources.add(new Jittery(lists.get(i), gate, seed * 100 + i));
        gate.countDown();
        assertEquals(oracle(lists), ConcurrentMerge.mergeAll(sources, 1 + rnd.nextInt(5)));
    }

    @Test @Tag("part4") @Tag("perf")
    void mergeAllEightByFiftyThousandUnderTwoSeconds() {
        var rnd = new Random(0);
        var lists = new ArrayList<List<Integer>>();
        for (int i = 0; i < 8; i++) lists.add(IntStream.generate(() -> rnd.nextInt(1_000_000)).limit(50_000).sorted().boxed().toList());
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var out = ConcurrentMerge.mergeAll(lists.stream().map(List::iterator).toList(), 1024);
            assertEquals(400_000, out.size());
        });
    }
}
