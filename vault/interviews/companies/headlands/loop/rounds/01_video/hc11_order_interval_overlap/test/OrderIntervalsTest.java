import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** hc11 Part 1（扫描线）与 Part 2（买卖方向 + 撤单）。 */
class OrderIntervalsTest {
    static final OrderIntervals.Side BUY = OrderIntervals.Side.BUY;
    static final OrderIntervals.Side SELL = OrderIntervals.Side.SELL;

    static OrderIntervals.Peak pk(int c, long t) {
        return new OrderIntervals.Peak(c, t);
    }

    static OrderIntervals.Place place(long id, OrderIntervals.Side s, long a, long b) {
        return new OrderIntervals.Place(id, s, a, b);
    }

    static OrderIntervals.Cancel cancel(long id, long t) {
        return new OrderIntervals.Cancel(id, t);
    }

    /** 暴力对拍：逐个整数时刻数活跃订单。只适用于小坐标。 */
    static OrderIntervals.Peak brute(long[][] iv, int horizon) {
        int best = 0;
        long when = 0;
        for (int t = 0; t < horizon; t++) {
            int live = 0;
            for (long[] x : iv) if (x[0] <= t && t < x[1]) live++;
            if (live > best) {
                best = live;
                when = t;
            }
        }
        return pk(best, when);
    }

    // ============================================================ Part 1

    @Test @Tag("part1")
    void problemSamples() {
        assertEquals(3, OrderIntervals.maxOverlap(new long[][]{{1, 5}, {2, 6}, {4, 8}}));
        assertEquals(pk(3, 4), OrderIntervals.peak(new long[][]{{1, 5}, {2, 6}, {4, 8}}));
        assertEquals(pk(3, 2), OrderIntervals.peak(new long[][]{{0, 10}, {2, 3}, {2, 3}, {5, 7}}));
    }

    @Test @Tag("part1") @Tag("edge")
    void endBeforeStartTieRuleTouchingIntervalsDoNotOverlap() {
        var touching = new long[][]{{1, 3}, {3, 5}};
        assertEquals(1, OrderIntervals.maxOverlap(touching));
        assertEquals(pk(1, 1), OrderIntervals.peak(touching));
        // 同一数据按闭区间 [s, e] 就是 2 —— 约定不同，答案不同
        assertEquals(2, OrderIntervals.maxOverlapInclusive(touching));
        // 链式交接：永远只有一个
        assertEquals(1, OrderIntervals.maxOverlap(new long[][]{{0, 1}, {1, 2}, {2, 3}, {3, 4}}));
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyAndSingleAndIdentical() {
        assertEquals(0, OrderIntervals.maxOverlap(new long[0][]));
        assertEquals(pk(0, 0), OrderIntervals.peak(new long[0][]));
        assertEquals(pk(1, 7), OrderIntervals.peak(new long[][]{{7, 9}}));
        assertEquals(4, OrderIntervals.maxOverlap(new long[][]{{2, 5}, {2, 5}, {2, 5}, {2, 5}}));
    }

    @Test @Tag("part1") @Tag("edge")
    void zeroLengthIntervalsNeverLive() {
        assertEquals(0, OrderIntervals.maxOverlap(new long[][]{{5, 5}}));
        assertEquals(1, OrderIntervals.maxOverlap(new long[][]{{5, 5}, {0, 10}, {5, 5}}));
        // 闭区间下 [5,5] 是一个点，活在时刻 5
        assertEquals(2, OrderIntervals.maxOverlapInclusive(new long[][]{{5, 5}, {0, 10}}));
    }

    @Test @Tag("part1") @Tag("edge")
    void unsortedInputAndInputIsNotModified() {
        var iv = new long[][]{{8, 9}, {1, 4}, {3, 6}, {0, 2}, {5, 7}};
        var copy = new long[][]{{8, 9}, {1, 4}, {3, 6}, {0, 2}, {5, 7}};
        assertEquals(pk(2, 1), OrderIntervals.peak(iv));
        assertEquals(List.of(List.of(8L, 9L), List.of(1L, 4L), List.of(3L, 6L), List.of(0L, 2L), List.of(5L, 7L)),
                java.util.Arrays.stream(iv).map(a -> java.util.Arrays.stream(a).boxed().toList()).toList());
        assertEquals(copy.length, iv.length);
    }

    @Test @Tag("part1") @Tag("edge")
    void earliestTimeIsReportedWhenMaxRepeats() {
        // 在 t=1 和 t=10 都有 2 个活着：要最早的
        assertEquals(pk(2, 1), OrderIntervals.peak(new long[][]{{1, 3}, {1, 3}, {10, 12}, {10, 12}}));
    }

    @Test @Tag("part1") @Tag("edge")
    void invalidIntervals() {
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.maxOverlap(new long[][]{{5, 4}}));
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.maxOverlap(new long[][]{{-1, 4}}));
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.maxOverlap(new long[][]{{1, 2, 3}}));
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.maxOverlap(new long[][]{{1}}));
        assertThrows(NullPointerException.class, () -> OrderIntervals.maxOverlap(null));
        assertThrows(NullPointerException.class, () -> OrderIntervals.maxOverlap(new long[][]{null}));
    }

    @Test @Tag("part1") @Tag("edge")
    void hugeCoordinatesNeverOverflow() {
        long max = Long.MAX_VALUE;
        var iv = new long[][]{{0, max}, {max - 2, max}, {max - 1, max}, {max - 5, max - 1}};
        // t = max-1: {0,max}, {max-2,max}, {max-1,max} 活着 → 3；t = max-2: {0,max}, {max-2,max}, {max-5,max-1} → 3，更早
        assertEquals(pk(3, max - 2), OrderIntervals.peak(iv));
        // 如果实现里做了 end - start 或 (a + b) / 2，这里就会溢出
        assertEquals(1, OrderIntervals.maxOverlap(new long[][]{{0, max}}));
    }

    @ParameterizedTest @Tag("part1")
    @ValueSource(longs = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10})
    void randomAgainstBruteForce(long seed) {
        var rnd = new Random(seed);
        int n = rnd.nextInt(60);
        var iv = new long[n][];
        for (int i = 0; i < n; i++) {
            long a = rnd.nextInt(40);
            long b = a + rnd.nextInt(15);
            iv[i] = new long[]{a, b};
        }
        assertEquals(brute(iv, 60), OrderIntervals.peak(iv), "seed " + seed);
    }

    @Test @Tag("part1") @Tag("perf")
    void millionIntervalsUnderTwoSeconds() {
        int n = 1_000_000;
        var rnd = new Random(0);
        var iv = new long[n][];
        for (int i = 0; i < n; i++) {
            long a = rnd.nextInt(10_000_000);
            iv[i] = new long[]{a, a + 1 + rnd.nextInt(1_000)};
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var p = OrderIntervals.peak(iv);
            assertEquals(true, p.count() > 50);
        });
    }

    // ============================================================ Part 2

    static List<OrderIntervals.OrderEvent> sample() {
        return List.of(
                place(1, BUY, 0, 10), place(2, BUY, 2, 8), place(3, SELL, 3, 6), place(4, SELL, 4, 12), place(5, BUY, 5, 9),
                cancel(2, 6), cancel(4, 5));
    }

    @Test @Tag("part2")
    void problemSample() {
        // 有效区间：1 BUY [0,10)  2 BUY [2,6)  3 SELL [3,6)  4 SELL [4,5)  5 BUY [5,9)
        var r = OrderIntervals.analyze(sample());
        assertEquals(pk(3, 5), r.buy());    // t=5: 订单 1,2,5
        assertEquals(pk(2, 4), r.sell());   // t=4: 订单 3,4
        assertEquals(pk(4, 4), r.all());    // t=4: 1,2,3,4；t=5: 1,2,3,5 也是 4，取最早
    }

    @Test @Tag("part2")
    void cancellationsMatter() {
        // 没有撤单：全部在 t=5 一起活着 → 5
        var noCancel = OrderIntervals.analyze(sample().subList(0, 5));
        assertEquals(pk(5, 5), noCancel.all());
        assertEquals(pk(3, 5), noCancel.buy());
        assertEquals(pk(2, 4), noCancel.sell());
    }

    @Test @Tag("part2") @Tag("fmt")
    void recordsPrintInTheDebugFormat() {
        var r = OrderIntervals.analyze(sample());
        assertEquals("Report[buy=Peak[count=3, time=5], sell=Peak[count=2, time=4], all=Peak[count=4, time=4]]", r.toString());
        assertEquals("Place[id=1, side=BUY, start=0, end=10]", place(1, BUY, 0, 10).toString());
        assertEquals("Cancel[id=2, time=6]", cancel(2, 6).toString());
    }

    @Test @Tag("part2") @Tag("edge")
    void emptyInputAndOneSideOnly() {
        var empty = OrderIntervals.analyze(List.of());
        assertEquals(new OrderIntervals.Report(pk(0, 0), pk(0, 0), pk(0, 0)), empty);
        var r = OrderIntervals.analyze(List.of(place(1, SELL, 3, 9), place(2, SELL, 4, 5)));
        assertEquals(new OrderIntervals.Report(pk(0, 0), pk(2, 4), pk(2, 4)), r);
    }

    @Test @Tag("part2") @Tag("edge")
    void cancelTimingRelativeToTheInterval() {
        // 撤单在开始前 → 从没活过；恰好在开始 → 从没活过（[s, s) 为空）；在结束后 → 无影响；中间 → 截短
        for (var c : new long[]{0, 4, 5}) {
            var r = OrderIntervals.analyze(List.of(place(1, BUY, 5, 10), cancel(1, c)));
            assertEquals(pk(0, 0), r.all(), "cancel at " + c);
        }
        assertEquals(pk(1, 5), OrderIntervals.analyze(List.of(place(1, BUY, 5, 10), cancel(1, 10))).all());
        assertEquals(pk(1, 5), OrderIntervals.analyze(List.of(place(1, BUY, 5, 10), cancel(1, 99))).all());
        // 截短后让出位置：A [0,10) 被 5 截短，B [5,8) 正好接上 → 最大 1
        var r = OrderIntervals.analyze(List.of(place(1, BUY, 0, 10), place(2, BUY, 5, 8), cancel(1, 5)));
        assertEquals(pk(1, 0), r.buy());
    }

    @Test @Tag("part2") @Tag("edge")
    void duplicateCancelsEarliestWinsAndOrderInListDoesNotMatter() {
        var evs = new ArrayList<OrderIntervals.OrderEvent>(List.of(cancel(1, 7), cancel(1, 3), cancel(1, 9), place(1, BUY, 0, 10), place(2, BUY, 5, 6)));
        // 订单 1 实际是 [0,3)，与订单 2 [5,6) 不重叠
        assertEquals(pk(1, 0), OrderIntervals.analyze(evs).all());
    }

    @Test @Tag("part2") @Tag("edge")
    void zeroLengthPlaceIsLegalButNeverLive() {
        assertEquals(pk(0, 0), OrderIntervals.analyze(List.of(place(1, BUY, 4, 4))).all());
    }

    @Test @Tag("part2") @Tag("edge")
    void invalidEvents() {
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.analyze(List.of(place(1, BUY, 0, 5), place(1, SELL, 1, 2))));
        assertThrows(IllegalArgumentException.class, () -> OrderIntervals.analyze(List.of(cancel(9, 1))));
        assertThrows(IllegalArgumentException.class, () -> place(1, BUY, 5, 4));
        assertThrows(IllegalArgumentException.class, () -> place(1, BUY, -1, 4));
        assertThrows(IllegalArgumentException.class, () -> cancel(1, -1));
        assertThrows(NullPointerException.class, () -> place(1, null, 1, 2));
        assertThrows(NullPointerException.class, () -> OrderIntervals.analyze(null));
    }

    @Test @Tag("part2") @Tag("edge")
    void hugeTimesInTheBatchVersion() {
        long max = Long.MAX_VALUE;
        var r = OrderIntervals.analyze(List.of(place(1, BUY, 0, max), place(2, SELL, max - 1, max), cancel(1, max - 1)));
        assertEquals(pk(1, 0), r.buy());
        assertEquals(pk(1, max - 1), r.sell());
        assertEquals(pk(1, 0), r.all());   // 订单 1 在 max-1 被撤，订单 2 正好接上
    }

    @ParameterizedTest @Tag("part2")
    @ValueSource(longs = {51, 52, 53, 54, 55, 56, 57, 58})
    void randomAgainstBruteForcePerSide(long seed) {
        var rnd = new Random(seed);
        int n = rnd.nextInt(50);
        var events = new ArrayList<OrderIntervals.OrderEvent>();
        var eff = new HashMap<Long, long[]>();
        var sides = new HashMap<Long, OrderIntervals.Side>();
        for (long id = 0; id < n; id++) {
            var side = rnd.nextBoolean() ? BUY : SELL;
            long a = rnd.nextInt(30);
            long b = a + rnd.nextInt(12);
            events.add(place(id, side, a, b));
            eff.put(id, new long[]{a, b});
            sides.put(id, side);
        }
        for (int c = 0; c < n / 2; c++) {
            long id = rnd.nextInt(Math.max(1, n));
            if (!eff.containsKey(id)) continue;
            long t = rnd.nextInt(40);
            events.add(cancel(id, t));
            eff.get(id)[1] = Math.min(eff.get(id)[1], t);
        }
        java.util.Collections.shuffle(events, rnd);
        var buy = eff.entrySet().stream().filter(e -> sides.get(e.getKey()) == BUY).map(java.util.Map.Entry::getValue).toArray(long[][]::new);
        var sell = eff.entrySet().stream().filter(e -> sides.get(e.getKey()) == SELL).map(java.util.Map.Entry::getValue).toArray(long[][]::new);
        var all = eff.values().toArray(long[][]::new);
        var r = OrderIntervals.analyze(events);
        assertEquals(brute(buy, 50), r.buy(), "buy, seed " + seed);
        assertEquals(brute(sell, 50), r.sell(), "sell, seed " + seed);
        assertEquals(brute(all, 50), r.all(), "all, seed " + seed);
    }

    @Test @Tag("part2") @Tag("perf")
    void halfMillionOrdersWithCancellationsUnderTwoSeconds() {
        int n = 500_000;
        var rnd = new Random(0);
        var events = new ArrayList<OrderIntervals.OrderEvent>(n + n / 2);
        for (int i = 0; i < n; i++) {
            long a = rnd.nextInt(5_000_000);
            events.add(place(i, rnd.nextBoolean() ? BUY : SELL, a, a + 1 + rnd.nextInt(2_000)));
        }
        for (int i = 0; i < n / 2; i++) events.add(cancel(rnd.nextInt(n), rnd.nextInt(5_000_000)));
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var r = OrderIntervals.analyze(events);
            assertEquals(true, r.all().count() >= Math.max(r.buy().count(), r.sell().count()));
        });
    }
}
