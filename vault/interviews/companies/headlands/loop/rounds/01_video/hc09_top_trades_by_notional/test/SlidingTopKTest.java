import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** hc09 Part 3：滑动窗口 top-k。 */
class SlidingTopKTest {
    static TopTrades.TickerTotal tt(String t, long n) {
        return new TopTrades.TickerTotal(t, n);
    }

    static SlidingTopK.Fill fill(long time, String t, long p, long v) {
        return new SlidingTopK.Fill(time, t, p, v);
    }

    /** 文本块里一行一个 Feed：F time ticker price volume | T time | Q time。 */
    static List<SlidingTopK.Feed> parse(String script) {
        var out = new ArrayList<SlidingTopK.Feed>();
        for (var line : script.strip().lines().toList()) {
            var f = line.strip().split("\\s+");
            out.add(switch (f[0]) {
                case "F" -> new SlidingTopK.Fill(Long.parseLong(f[1]), f[2], Long.parseLong(f[3]), Long.parseLong(f[4]));
                case "T" -> new SlidingTopK.Tick(Long.parseLong(f[1]));
                case "Q" -> new SlidingTopK.Ask(Long.parseLong(f[1]));
                default -> throw new IllegalArgumentException(line);
            });
        }
        return out;
    }

    @Test @Tag("part3")
    void problemSampleReplay() {
        var feed = parse("""
                F 1 AAPL 100 2
                F 3 MSFT 50 10
                F 5 AAPL 100 3
                Q 5
                F 12 TSLA 10 10
                Q 12
                Q 15
                Q 40
                """);
        // 窗口 W=10，k=2。
        // t=5 : AAPL 200+300=500, MSFT 500 → 并列按 ticker 升序
        // t=12: 活跃区间 (2,12]：t=1 的 AAPL 200 过期 → MSFT 500, AAPL 300（TSLA 100 第三）
        // t=15: (5,15]：t=3 的 MSFT 和 t=5 的 AAPL 都过期（15-5=10>=W，边界算过期）→ 只剩 TSLA 100
        // t=40: 全部过期
        var answers = SlidingTopK.replay(10, 2, feed);
        assertEquals(List.of(
                new SlidingTopK.Answer(5, List.of(tt("AAPL", 500), tt("MSFT", 500))),
                new SlidingTopK.Answer(12, List.of(tt("MSFT", 500), tt("AAPL", 300))),
                new SlidingTopK.Answer(15, List.of(tt("TSLA", 100))),
                new SlidingTopK.Answer(40, List.of())), answers);
    }

    @Test @Tag("part3") @Tag("edge")
    void expiryBoundaryIsExactlyWindowLength() {
        var w = new SlidingTopK(10, 5);
        w.add(fill(100, "A", 1, 1));
        w.advanceTo(109);
        assertEquals(1, w.liveEvents());   // 109 - 100 = 9 < 10 → 还活着
        assertEquals(1, w.totalOf("A"));
        w.advanceTo(110);
        assertEquals(0, w.liveEvents());   // 110 - 100 = 10 >= 10 → 过期
        assertEquals(0, w.totalOf("A"));
        assertEquals(0, w.distinctTickers());
    }

    @Test @Tag("part3") @Tag("edge")
    void windowOfOneKeepsOnlyTheCurrentInstant() {
        var w = new SlidingTopK(1, 3);
        w.add(fill(5, "A", 2, 2));
        w.add(fill(5, "B", 1, 1));   // 同一时刻：都活着
        assertEquals(List.of(tt("A", 4), tt("B", 1)), w.top());
        w.advanceTo(6);
        assertEquals(List.of(), w.top());
    }

    @Test @Tag("part3") @Tag("edge")
    void sameTimestampIsAllowedAndTimeCannotGoBackwards() {
        var w = new SlidingTopK(10, 2);
        w.add(fill(7, "A", 1, 1));
        w.add(fill(7, "A", 1, 1));
        assertEquals(2, w.totalOf("A"));
        assertThrows(IllegalArgumentException.class, () -> w.add(fill(6, "A", 1, 1)));
        assertThrows(IllegalArgumentException.class, () -> w.advanceTo(6));
        assertEquals(2, w.totalOf("A"));   // 失败的调用没有改变状态
        assertEquals(7, w.now());
    }

    @Test @Tag("part3") @Tag("edge")
    void rankingChangesAsOldFillsExpire() {
        var w = new SlidingTopK(10, 2);
        w.add(fill(0, "BIG", 1000, 1));
        w.add(fill(4, "MID", 100, 1));
        w.add(fill(8, "SMALL", 10, 1));
        assertEquals(List.of(tt("BIG", 1000), tt("MID", 100)), w.top());
        w.advanceTo(10);                       // BIG 过期
        assertEquals(List.of(tt("MID", 100), tt("SMALL", 10)), w.top());
        w.add(fill(11, "BIG", 50, 1));         // BIG 以较小的总额回来
        assertEquals(List.of(tt("MID", 100), tt("BIG", 50)), w.top());
    }

    @Test @Tag("part3") @Tag("edge")
    void partialExpiryOfOneTickerLowersItsTotalButKeepsIt() {
        var w = new SlidingTopK(10, 3);
        w.add(fill(0, "A", 100, 1));
        w.add(fill(5, "A", 7, 1));
        w.advanceTo(10);
        assertEquals(7, w.totalOf("A"));
        assertEquals(List.of(tt("A", 7)), w.top());
        assertEquals(1, w.distinctTickers());
    }

    @Test @Tag("part3") @Tag("edge")
    void equalTotalsAreOrderedByTicker() {
        var w = new SlidingTopK(100, 3);
        w.add(fill(1, "C", 5, 1));
        w.add(fill(1, "A", 5, 1));
        w.add(fill(1, "B", 5, 1));
        assertEquals(List.of(tt("A", 5), tt("B", 5), tt("C", 5)), w.top());
    }

    @Test @Tag("part3") @Tag("edge")
    void zeroNotionalFillKeepsTheTickerAliveUntilItExpires() {
        var w = new SlidingTopK(10, 5);
        w.add(fill(0, "A", 0, 100));
        assertEquals(List.of(tt("A", 0)), w.top());
        assertEquals(1, w.distinctTickers());
        w.advanceTo(10);
        assertEquals(0, w.distinctTickers());
    }

    @Test @Tag("part3") @Tag("edge")
    void kZeroAndBadConstructorArguments() {
        var w = new SlidingTopK(10, 0);
        w.add(fill(1, "A", 1, 1));
        assertEquals(List.of(), w.top());
        assertThrows(IllegalArgumentException.class, () -> new SlidingTopK(0, 1));
        assertThrows(IllegalArgumentException.class, () -> new SlidingTopK(10, -1));
        assertThrows(IllegalArgumentException.class, () -> fill(-1, "A", 1, 1));
        assertThrows(IllegalArgumentException.class, () -> fill(1, "A", -1, 1));
        assertThrows(IllegalArgumentException.class, () -> fill(1, "A", 1, -1));
        assertThrows(NullPointerException.class, () -> fill(1, null, 1, 1));
        assertThrows(ArithmeticException.class, () -> fill(1, "A", Long.MAX_VALUE, 2));
    }

    @Test @Tag("part3") @Tag("edge")
    void totalOverflowInsideTheWindowIsAtomicAndRecoversAfterExpiry() {
        long half = Long.MAX_VALUE / 2 + 1;
        var w = new SlidingTopK(10, 3);
        w.add(fill(0, "A", half, 1));
        assertThrows(ArithmeticException.class, () -> w.add(fill(1, "A", half, 1)));
        // 状态没有被破坏：A 还是 half，只有一笔活跃成交，ranking 里只有一个 A
        assertEquals(half, w.totalOf("A"));
        assertEquals(1, w.liveEvents());
        assertEquals(List.of(tt("A", half)), w.top());
        w.add(fill(10, "A", half, 1));   // 第一笔在 t=10 过期，所以这笔可以加
        assertEquals(half, w.totalOf("A"));
        assertEquals(List.of(tt("A", half)), w.top());
    }

    @Test @Tag("part3") @Tag("edge")
    void replayTickGuardAndBackwardsTime() {
        var answers = SlidingTopK.replay(5, 1, parse("""
                T 0
                F 0 A 1 1
                T 0
                Q 0
                """));
        assertEquals(List.of(new SlidingTopK.Answer(0, List.of(tt("A", 1)))), answers);
        assertThrows(IllegalArgumentException.class, () -> SlidingTopK.replay(5, 1, parse("""
                T 9
                Q 3
                """)));
        assertEquals(List.of(), SlidingTopK.replay(5, 1, List.of()));
    }

    @ParameterizedTest @Tag("part3")
    @ValueSource(longs = {21, 22, 23, 24, 25, 26, 27, 28})
    void randomAgainstRecomputeFromScratch(long seed) {
        var rnd = new Random(seed);
        long window = 1 + rnd.nextInt(30);
        int k = rnd.nextInt(6);
        var w = new SlidingTopK(window, k);
        var fills = new ArrayList<SlidingTopK.Fill>();
        long time = 0;
        for (int step = 0; step < 1500; step++) {
            time += rnd.nextInt(4);   // 允许相同时间戳
            if (rnd.nextInt(4) == 0) {
                w.advanceTo(time);
            } else {
                var f = fill(time, "S" + rnd.nextInt(8), rnd.nextInt(4), rnd.nextInt(4));
                w.add(f);
                fills.add(f);
            }
            // 从头重算：活跃 = now - time < window
            var totals = new HashMap<String, Long>();
            int live = 0;
            for (var f : fills) {
                if (time - f.time() < window) {
                    totals.merge(f.ticker(), f.notional(), Long::sum);
                    live++;
                }
            }
            var expect = totals.entrySet().stream().map(e -> tt(e.getKey(), e.getValue()))
                    .sorted(TopTrades.BEST_TICKER_FIRST).limit(k).toList();
            assertEquals(expect, w.top(), "seed " + seed + " step " + step);
            assertEquals(live, w.liveEvents());
            assertEquals(totals.size(), w.distinctTickers());
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void millionFillsWithSlidingWindowUnderTwoSeconds() {
        int n = 1_000_000;
        var rnd = new Random(0);
        var names = new String[2_000];
        for (int i = 0; i < names.length; i++) names[i] = "T" + i;
        var feed = new ArrayList<SlidingTopK.Feed>(n + n / 100);
        long time = 0;
        for (int i = 0; i < n; i++) {
            time += rnd.nextInt(3);
            feed.add(fill(time, names[rnd.nextInt(names.length)], 1 + rnd.nextInt(1000), 1 + rnd.nextInt(100)));
            if (i % 100 == 99) feed.add(new SlidingTopK.Ask(time));
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var answers = SlidingTopK.replay(5_000, 10, feed);
            assertEquals(n / 100, answers.size());
            assertTrue(answers.getLast().top().size() <= 10);
        });
    }
}
