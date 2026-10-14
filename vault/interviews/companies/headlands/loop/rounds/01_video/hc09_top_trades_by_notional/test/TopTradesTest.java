import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** hc09 Part 1（top-k 事件）与 Part 2（top-k ticker）。 */
class TopTradesTest {
    // problem.md 的样例
    static final String[] T = {"AAPL", "MSFT", "AAPL", "GOOG", "MSFT", "TSLA"};
    static final long[] P = {18000, 40000, 18100, 14000, 40000, 25000};
    static final long[] V = {10, 3, 5, 9, 3, 8};
    // notional: 180000, 120000, 90500, 126000, 120000, 200000

    static TopTrades.Trade trade(int i) {
        return new TopTrades.Trade(i, T[i], P[i], V[i]);
    }

    /** 对拍用的朴素实现：下标排序，只用小数值（不会溢出）。 */
    static List<Integer> oracleEvents(String[] t, long[] p, long[] v, int k) {
        var idx = new ArrayList<Integer>();
        for (int i = 0; i < t.length; i++) idx.add(i);
        idx.sort(Comparator.<Integer>comparingLong(i -> p[i] * v[i]).reversed()
                .thenComparing(i -> t[i]).thenComparingInt(i -> i));
        return idx.subList(0, Math.min(k, idx.size()));
    }

    static List<TopTrades.TickerTotal> oracleTickers(String[] t, long[] p, long[] v, int k) {
        var m = new HashMap<String, Long>();
        for (int i = 0; i < t.length; i++) m.merge(t[i], p[i] * v[i], Long::sum);
        return m.entrySet().stream().map(e -> new TopTrades.TickerTotal(e.getKey(), e.getValue()))
                .sorted(TopTrades.BEST_TICKER_FIRST).limit(k).toList();
    }

    static List<Integer> indices(List<TopTrades.Trade> trades) {
        return trades.stream().map(TopTrades.Trade::index).toList();
    }

    // ============================================================ Part 1

    @Test @Tag("part1")
    void sampleTopThree() {
        var top = TopTrades.topEvents(T, P, V, 3);
        assertEquals(List.of(trade(5), trade(0), trade(3)), top);
        assertEquals(List.of(200_000L, 180_000L, 126_000L), top.stream().map(TopTrades.Trade::notional).toList());
    }

    @Test @Tag("part1")
    void tieOnNotionalAndTickerFallsBackToIndex() {
        // 第 4 名：下标 1 和下标 4 都是 (MSFT, 120000)，下标小的在前
        var top = TopTrades.topEvents(T, P, V, 4);
        assertEquals(List.of(5, 0, 3, 1), indices(top));
        assertEquals(List.of(5, 0, 3, 1, 4, 2), indices(TopTrades.topEvents(T, P, V, 6)));
    }

    @Test @Tag("part1") @Tag("edge")
    void tieOnNotionalFallsBackToTickerAscending() {
        var t = new String[]{"ZZZ", "AAA", "MMM", "AAA"};
        var p = new long[]{10, 10, 10, 10};
        var v = new long[]{5, 5, 5, 5};
        assertEquals(List.of(1, 3, 2, 0), indices(TopTrades.topEvents(t, p, v, 4)));
        assertEquals(List.of(1, 3), indices(TopTrades.topEvents(t, p, v, 2)));
    }

    @Test @Tag("part1") @Tag("edge")
    void kLargerThanNReturnsEverythingSorted() {
        var top = TopTrades.topEvents(T, P, V, 100);
        assertEquals(6, top.size());
        assertEquals(oracleEvents(T, P, V, 100), indices(top));
    }

    @Test @Tag("part1") @Tag("edge")
    void kZeroAndEmptyInput() {
        assertEquals(List.of(), TopTrades.topEvents(T, P, V, 0));
        assertEquals(List.of(), TopTrades.topEvents(new String[0], new long[0], new long[0], 5));
        assertEquals(List.of(), TopTrades.topEvents(new String[0], new long[0], new long[0], 0));
    }

    @Test @Tag("part1") @Tag("edge")
    void singleEvent() {
        var top = TopTrades.topEvents(new String[]{"X"}, new long[]{7}, new long[]{3}, 1);
        assertEquals(List.of(new TopTrades.Trade(0, "X", 7, 3)), top);
        assertEquals(21, top.getFirst().notional());
    }

    @Test @Tag("part1") @Tag("edge")
    void zeroVolumeAndZeroPriceAreLegalAndRankLast() {
        var t = new String[]{"A", "B", "C"};
        var top = TopTrades.topEvents(t, new long[]{0, 5, 9}, new long[]{100, 0, 1}, 3);
        assertEquals(List.of(2, 0, 1), indices(top)); // 9, 0(A), 0(B)
    }

    @Test @Tag("part1") @Tag("edge")
    void invalidInputs() {
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topEvents(T, P, V, -1));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topEvents(T, Arrays.copyOf(P, 5), V, 2));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topEvents(T, P, Arrays.copyOf(V, 7), 2));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topEvents(new String[]{"A"}, new long[]{-1}, new long[]{1}, 1));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topEvents(new String[]{"A"}, new long[]{1}, new long[]{-1}, 1));
        assertThrows(NullPointerException.class, () -> TopTrades.topEvents(null, P, V, 1));
        assertThrows(NullPointerException.class, () -> TopTrades.topEvents(new String[]{"A", null}, new long[]{1, 1}, new long[]{1, 1}, 1));
    }

    @Test @Tag("part1") @Tag("edge")
    void invalidEventIsRejectedEvenIfItCouldNeverMakeTheTopK() {
        // 校验对每个事件都做，不是只对进堆的事件做
        var t = new String[]{"A", "B", "C"};
        assertThrows(IllegalArgumentException.class,
                () -> TopTrades.topEvents(t, new long[]{1000, 5, -1}, new long[]{1000, 5, 1}, 1));
    }

    @Test @Tag("part1") @Tag("edge")
    void multiplicationOverflowIsDetectedNotWrapped() {
        var t = new String[]{"BIG", "SMALL"};
        // 第 1 个事件溢出，k=1 且它排在最后——溢出仍然要报
        assertThrows(ArithmeticException.class,
                () -> TopTrades.topEvents(t, new long[]{1, Long.MAX_VALUE}, new long[]{1, 2}, 1));
        // 如果错误地用 int 或不检查的 long 乘法，Long.MAX_VALUE * 2 会绕回 -2
        assertThrows(ArithmeticException.class,
                () -> TopTrades.topEvents(new String[]{"A"}, new long[]{Long.MAX_VALUE}, new long[]{2}, 1));
    }

    @Test @Tag("part1") @Tag("edge")
    void notionalExactlyLongMaxIsFineAndSquareRootBoundary() {
        var top = TopTrades.topEvents(new String[]{"A", "B"}, new long[]{Long.MAX_VALUE, 1}, new long[]{1, 1}, 2);
        assertEquals(Long.MAX_VALUE, top.getFirst().notional());
        // floor(sqrt(Long.MAX_VALUE)) = 3037000499
        var ok = TopTrades.topEvents(new String[]{"A"}, new long[]{3_037_000_499L}, new long[]{3_037_000_499L}, 1);
        assertEquals(3_037_000_499L * 3_037_000_499L, ok.getFirst().notional());
        assertThrows(ArithmeticException.class,
                () -> TopTrades.topEvents(new String[]{"A"}, new long[]{3_037_000_500L}, new long[]{3_037_000_500L}, 1));
    }

    @Test @Tag("part1") @Tag("edge")
    void inputArraysAreNotModified() {
        var t = T.clone();
        var p = P.clone();
        var v = V.clone();
        TopTrades.topEvents(t, p, v, 3);
        TopTrades.topTickers(t, p, v, 3);
        assertTrue(Arrays.equals(T, t) && Arrays.equals(P, p) && Arrays.equals(V, v));
    }

    @Test @Tag("part1") @Tag("edge")
    void returnedListIsImmutable() {
        var top = TopTrades.topEvents(T, P, V, 3);
        assertThrows(UnsupportedOperationException.class, () -> top.add(trade(1)));
    }

    @ParameterizedTest @Tag("part1")
    @ValueSource(longs = {1, 2, 3, 4, 5, 6, 7, 8})
    void randomAgainstOracleWithHeavyTies(long seed) {
        var rnd = new Random(seed);
        int n = 1 + rnd.nextInt(300);
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        for (int i = 0; i < n; i++) {
            t[i] = "S" + rnd.nextInt(6);
            p[i] = 1 + rnd.nextInt(4);   // 值域极小 → 大量 notional 相同
            v[i] = rnd.nextInt(4);
        }
        for (int k : new int[]{1, 2, 5, 17, n, n + 3}) {
            assertEquals(oracleEvents(t, p, v, k), indices(TopTrades.topEvents(t, p, v, k)), "seed " + seed + " k " + k);
            assertEquals(TopTrades.topEventsSorted(t, p, v, k), TopTrades.topEvents(t, p, v, k));
        }
    }

    @Test @Tag("part1") @Tag("fmt")
    void recordToStringIsTheDebugFormat() {
        assertEquals("Trade[index=5, ticker=TSLA, price=25000, volume=8]", trade(5).toString());
        assertEquals("TickerTotal[ticker=AAPL, notional=270500]", new TopTrades.TickerTotal("AAPL", 270_500).toString());
    }

    @Test @Tag("part1") @Tag("perf")
    void randomMillionEventsTop100UnderTwoSeconds() {
        int n = 1_000_000;
        var rnd = new Random(0);
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        var names = new String[5000];
        for (int i = 0; i < names.length; i++) names[i] = "T" + i;
        for (int i = 0; i < n; i++) {
            t[i] = names[rnd.nextInt(names.length)];
            p[i] = 1 + rnd.nextInt(1_000_000);
            v[i] = 1 + rnd.nextInt(10_000);
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var top = TopTrades.topEvents(t, p, v, 100);
            assertEquals(100, top.size());
            for (int i = 1; i < top.size(); i++) assertTrue(top.get(i - 1).notional() >= top.get(i).notional());
        });
    }

    @Test @Tag("part1") @Tag("perf")
    void adversarialAscendingOrderEveryEventEntersTheHeap() {
        // 每个新事件都比堆里所有都大：堆的最坏情况，O(n log k)
        int n = 1_000_000;
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        Arrays.fill(t, "X");
        for (int i = 0; i < n; i++) {
            p[i] = i + 1;
            v[i] = 1_000;
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var top = TopTrades.topEvents(t, p, v, 1_000);
            assertEquals(n - 1, top.getFirst().index());
            assertEquals(n - 1_000, top.getLast().index());
        });
    }

    // ============================================================ Part 2

    @Test @Tag("part2")
    void sampleTopTwoTickers() {
        // AAPL 270500, MSFT 240000, TSLA 200000, GOOG 126000
        assertEquals(List.of(new TopTrades.TickerTotal("AAPL", 270_500), new TopTrades.TickerTotal("MSFT", 240_000)),
                TopTrades.topTickers(T, P, V, 2));
        assertEquals(4, TopTrades.topTickers(T, P, V, 10).size());
    }

    @Test @Tag("part2")
    void topTickerCanDifferFromTheTopEvent() {
        assertEquals("TSLA", TopTrades.topEvents(T, P, V, 1).getFirst().ticker());
        assertEquals("AAPL", TopTrades.topTickers(T, P, V, 1).getFirst().ticker());
    }

    @Test @Tag("part2") @Tag("edge")
    void equalTotalsBreakTiesByTickerAscending() {
        var t = new String[]{"B", "A", "C", "A"};
        var p = new long[]{10, 4, 10, 6};
        var v = new long[]{1, 1, 1, 1};
        // A=10, B=10, C=10
        assertEquals(List.of("A", "B", "C"),
                TopTrades.topTickers(t, p, v, 3).stream().map(TopTrades.TickerTotal::ticker).toList());
        assertEquals(List.of("A"), TopTrades.topTickers(t, p, v, 1).stream().map(TopTrades.TickerTotal::ticker).toList());
    }

    @Test @Tag("part2") @Tag("edge")
    void zeroNotionalTickersStillExist() {
        var top = TopTrades.topTickers(new String[]{"A", "B"}, new long[]{0, 3}, new long[]{5, 1}, 5);
        assertEquals(List.of(new TopTrades.TickerTotal("B", 3), new TopTrades.TickerTotal("A", 0)), top);
    }

    @Test @Tag("part2") @Tag("edge")
    void emptyKZeroAndInvalid() {
        assertEquals(List.of(), TopTrades.topTickers(new String[0], new long[0], new long[0], 3));
        assertEquals(List.of(), TopTrades.topTickers(T, P, V, 0));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topTickers(T, P, V, -1));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topTickers(T, Arrays.copyOf(P, 2), V, 1));
        assertThrows(NullPointerException.class, () -> TopTrades.topTickers(new String[]{null}, new long[]{1}, new long[]{1}, 1));
    }

    @Test @Tag("part2") @Tag("edge")
    void aggregateOverflowIsDetectedEvenWhenEachEventFits() {
        long half = Long.MAX_VALUE / 2 + 1;   // 2 * half 溢出
        assertThrows(ArithmeticException.class,
                () -> TopTrades.topTickers(new String[]{"A", "A"}, new long[]{half, half}, new long[]{1, 1}, 1));
        assertThrows(ArithmeticException.class,
                () -> TopTrades.topTickersStream(new String[]{"A", "A"}, new long[]{half, half}, new long[]{1, 1}, 1));
        // 不同 ticker 不会合并 → 不溢出
        var ok = TopTrades.topTickers(new String[]{"A", "B"}, new long[]{half, half}, new long[]{1, 1}, 2);
        assertEquals(half, ok.getFirst().notional());
        // 恰好 Long.MAX_VALUE
        var exact = TopTrades.topTickers(new String[]{"A", "A"}, new long[]{Long.MAX_VALUE - 5, 5}, new long[]{1, 1}, 1);
        assertEquals(Long.MAX_VALUE, exact.getFirst().notional());
    }

    @ParameterizedTest @Tag("part2")
    @ValueSource(longs = {11, 12, 13, 14, 15, 16})
    void heapStreamAndOracleAgree(long seed) {
        var rnd = new Random(seed);
        int n = 1 + rnd.nextInt(400);
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        for (int i = 0; i < n; i++) {
            t[i] = "S" + rnd.nextInt(40);
            p[i] = rnd.nextInt(5);
            v[i] = rnd.nextInt(5);
        }
        for (int k : new int[]{0, 1, 3, 10, 40, 100}) {
            var expect = oracleTickers(t, p, v, k);
            assertEquals(expect, TopTrades.topTickers(t, p, v, k), "heap, seed " + seed + " k " + k);
            assertEquals(expect, TopTrades.topTickersStream(t, p, v, k), "stream, seed " + seed + " k " + k);
        }
    }

    @Test @Tag("part2")
    void topOfWorksOnAPrebuiltMap() {
        Map<String, Long> m = Map.of("A", 5L, "B", 9L, "C", 5L, "D", 1L);
        assertEquals(List.of("B", "A", "C"), TopTrades.topOf(m, 3).stream().map(TopTrades.TickerTotal::ticker).toList());
        assertEquals(List.of(), TopTrades.topOf(Map.of(), 3));
        assertThrows(IllegalArgumentException.class, () -> TopTrades.topOf(m, -1));
    }

    @Test @Tag("part2")
    void summarizeUsesTeeing() {
        var s = TopTrades.summarize(T, P, V);
        assertEquals(180_000 + 120_000 + 90_500 + 126_000 + 120_000 + 200_000, s.grandTotal());
        assertEquals(Optional.of(trade(5)), s.largest());
        var empty = TopTrades.summarize(new String[0], new long[0], new long[0]);
        assertEquals(0, empty.grandTotal());
        assertEquals(Optional.empty(), empty.largest());
        long half = Long.MAX_VALUE / 2 + 1;
        assertThrows(ArithmeticException.class,
                () -> TopTrades.summarize(new String[]{"A", "B"}, new long[]{half, half}, new long[]{1, 1}));
    }

    @Test @Tag("part2") @Tag("perf")
    void millionEventsHundredThousandTickersUnderTwoSeconds() {
        int n = 1_000_000;
        var rnd = new Random(0);
        var names = new String[100_000];
        for (int i = 0; i < names.length; i++) names[i] = "T" + i;
        var t = new String[n];
        var p = new long[n];
        var v = new long[n];
        for (int i = 0; i < n; i++) {
            t[i] = names[rnd.nextInt(names.length)];
            p[i] = 1 + rnd.nextInt(100_000);
            v[i] = 1 + rnd.nextInt(1_000);
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var top = TopTrades.topTickers(t, p, v, 50);
            assertEquals(50, top.size());
            for (int i = 1; i < top.size(); i++) assertTrue(top.get(i - 1).notional() >= top.get(i).notional());
        });
    }
}
