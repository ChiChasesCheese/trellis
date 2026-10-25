import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.OptionalLong;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2（滑动窗口 VWAP）与 Part 3（窗口内 top-k）。 */
class RollingVwapTest {
    static TradeLog.Trade t(long ts, String sym, long price, long qty) {
        return new TradeLog.Trade(ts, sym, price, qty);
    }

    static RollingVwap.SymbolNotional sn(String s, long n) {
        return new RollingVwap.SymbolNotional(s, n);
    }

    // price 的单位是 0.0001：100_000 = 10.0000
    static RollingVwap sample() {
        var r = new RollingVwap(1000);
        r.onTrade(t(0, "AAPL", 100_000, 10));
        r.onTrade(t(400, "AAPL", 120_000, 20));
        r.onTrade(t(900, "MSFT", 500_000, 5));
        return r;
    }

    // ---------------------------------------------------------------- Part 2
    @Test @Tag("part2")
    void sampleWalkthrough() {
        var r = sample();
        // (100000*10 + 120000*20) / 30 = 113333.33 → 113333
        assertEquals(OptionalLong.of(113_333), r.vwap("AAPL", 900));
        assertEquals(OptionalLong.of(500_000), r.vwap("MSFT", 900));
        assertEquals(OptionalLong.empty(), r.vwap("GOOG", 900));
        // now = 1000：ts 0 的那笔刚好过期（1000 - 0 >= 1000）
        r.onTrade(t(1000, "AAPL", 110_000, 10));
        assertEquals(2, r.liveSymbols());
        assertEquals(3, r.liveTrades());
        assertEquals(30, r.volume("AAPL"));
        assertEquals(3_500_000, r.notional("AAPL"));
        assertEquals(OptionalLong.of(116_667), r.vwap("AAPL", 1000)); // 3500000/30 = 116666.67
        // 1900：MSFT 在 900 的那笔过期（1900 - 900 = 1000），symbol 也要消失
        assertEquals(OptionalLong.empty(), r.vwap("MSFT", 1900));
        assertEquals(1, r.liveSymbols());
        assertEquals(1900, r.now());
    }

    @Test @Tag("part2") @Tag("edge")
    void expiryBoundaryIsHalfOpen() {
        var r = new RollingVwap(10);
        r.onTrade(t(5, "A", 10_000, 1));
        assertEquals(OptionalLong.of(10_000), r.vwap("A", 14)); // 14 - 5 = 9 < 10：活
        assertEquals(1, r.liveTrades());
        assertEquals(OptionalLong.empty(), r.vwap("A", 15));    // 15 - 5 = 10：过期
        assertEquals(0, r.liveTrades());
        assertEquals(0, r.liveSymbols());
    }

    @Test @Tag("part2") @Tag("edge")
    void windowOneKeepsOnlySameTimestamp() {
        var r = new RollingVwap(1);
        r.onTrade(t(5, "A", 10_000, 1));
        r.onTrade(t(5, "A", 30_000, 1));
        assertEquals(OptionalLong.of(20_000), r.vwap("A", 5));
        r.onTrade(t(6, "A", 50_000, 1));
        assertEquals(1, r.liveTrades());
        assertEquals(OptionalLong.of(50_000), r.vwap("A", 6));
    }

    @Test @Tag("part2") @Tag("edge")
    void sameTimestampTradesExpireTogether() {
        var r = new RollingVwap(100);
        for (int i = 0; i < 50; i++) r.onTrade(t(7, "A", 10_000 + i, 2));
        assertEquals(50, r.liveTrades());
        assertEquals(100, r.volume("A"));
        r.vwap("A", 106);
        assertEquals(50, r.liveTrades());
        r.vwap("A", 107);
        assertEquals(0, r.liveTrades());
        assertEquals(0, r.volume("A"));
    }

    @Test @Tag("part2") @Tag("edge")
    void timeNeverGoesBackwards() {
        var r = new RollingVwap(100);
        r.onTrade(t(50, "A", 10_000, 1));
        assertThrows(IllegalArgumentException.class, () -> r.onTrade(t(49, "A", 10_000, 1)));
        assertEquals(1, r.liveTrades());                   // 被拒绝的成交没有计入
        assertEquals(50, r.now());
        assertThrows(IllegalArgumentException.class, () -> r.vwap("A", 49));
        r.onTrade(t(50, "A", 10_000, 1));                  // 同一时刻可以
        assertEquals(OptionalLong.of(10_000), r.vwap("A", 60));
        assertEquals(60, r.now());
        assertThrows(IllegalArgumentException.class, () -> r.onTrade(t(55, "A", 10_000, 1))); // 查询已经把时钟推到 60
    }

    @Test @Tag("part2") @Tag("edge")
    void constructorAndNullArguments() {
        assertThrows(IllegalArgumentException.class, () -> new RollingVwap(0));
        assertThrows(IllegalArgumentException.class, () -> new RollingVwap(-5));
        var r = new RollingVwap(10);
        assertThrows(NullPointerException.class, () -> r.onTrade(null));
        assertThrows(NullPointerException.class, () -> r.vwap(null, 0));
        assertEquals(0, r.now());
        assertEquals(OptionalLong.empty(), r.vwap("A", 0));
        assertEquals(0, r.volume("A"));
        assertEquals(0, r.notional("A"));
    }

    @Test @Tag("part2") @Tag("edge")
    void symbolsAreIndependent() {
        var r = new RollingVwap(100);
        r.onTrade(t(0, "A", 10_000, 1));
        r.onTrade(t(60, "B", 20_000, 1));
        r.onTrade(t(120, "A", 30_000, 1));
        assertEquals(OptionalLong.of(30_000), r.vwap("A", 120)); // ts 0 的 A 已过期
        assertEquals(OptionalLong.of(20_000), r.vwap("B", 120));
        assertEquals(2, r.liveTrades());
    }

    @Test @Tag("part2") @Tag("edge")
    void overflowRejectsTheTradeAndKeepsState() {
        var r = new RollingVwap(1000);
        var big = t(0, "BIG", 1_000_000_000_000L, 9_000_000); // notional 9e18
        r.onTrade(big);
        assertThrows(ArithmeticException.class, () -> r.onTrade(t(1, "BIG", 1_000_000_000_000L, 9_000_000)));
        assertEquals(1, r.liveTrades());
        assertEquals(9_000_000_000_000_000_000L, r.notional("BIG"));
        assertEquals(9_000_000, r.volume("BIG"));
        assertEquals(OptionalLong.of(1_000_000_000_000L), r.vwap("BIG", 1));
        // 别的 symbol 不受影响
        r.onTrade(t(2, "OK", 10_000, 1));
        assertEquals(2, r.liveTrades());
        // 旧的那笔过期之后，同一 symbol 又能加了
        r.onTrade(t(1000, "BIG", 1_000_000_000_000L, 9_000_000));
        assertEquals(9_000_000_000_000_000_000L, r.notional("BIG"));
    }

    @Test @Tag("part2") @Tag("edge")
    void quantityOverflowAlsoRejects() {
        var r = new RollingVwap(1000);
        r.onTrade(t(0, "Q", 1, Long.MAX_VALUE - 1));
        assertThrows(ArithmeticException.class, () -> r.onTrade(t(1, "Q", 1, 2)));
        assertEquals(Long.MAX_VALUE - 1, r.volume("Q"));
        assertEquals(1, r.liveTrades());
        r.onTrade(t(2, "Q", 1, 1)); // 恰好到 Long.MAX_VALUE
        assertEquals(Long.MAX_VALUE, r.volume("Q"));
    }

    @Test @Tag("part2") @Tag("edge")
    void vwapRoundsHalfUp() {
        var r = new RollingVwap(1000);
        r.onTrade(t(0, "A", 1, 1));
        r.onTrade(t(1, "A", 2, 1)); // 1.5 → 2
        assertEquals(OptionalLong.of(2), r.vwap("A", 1));
        r.onTrade(t(2, "B", 1, 2));
        r.onTrade(t(2, "B", 2, 1)); // 4 / 3 = 1.33 → 1
        assertEquals(OptionalLong.of(1), r.vwap("B", 2));
    }

    /** 明显正确的慢实现：每次问都从头扫所有成交。 */
    static final class Model {
        final List<TradeLog.Trade> all = new ArrayList<>();
        final long window;
        Model(long w) { window = w; }
        OptionalLong vwap(String sym, long now) {
            long vol = 0, not = 0;
            for (var tr : all) if (tr.symbol().equals(sym) && now - tr.tsMs() < window) { vol += tr.qty(); not += tr.notional(); }
            return vol == 0 ? OptionalLong.empty() : OptionalLong.of(TradeLog.vwap(not, vol));
        }
        List<RollingVwap.SymbolNotional> top(int k, long now) {
            var m = new HashMap<String, Long>();
            for (var tr : all) if (now - tr.tsMs() < window) m.merge(tr.symbol(), tr.notional(), Long::sum);
            return m.entrySet().stream().map(e -> sn(e.getKey(), e.getValue()))
                    .sorted(Comparator.comparingLong(RollingVwap.SymbolNotional::notional).reversed().thenComparing(RollingVwap.SymbolNotional::symbol))
                    .limit(k).toList();
        }
    }

    @Test @Tag("part2")
    void randomVwapMatchesBruteForce() {
        var rnd = new Random(7);
        String[] syms = {"A", "B", "C", "D.E", "F1"};
        for (long window : new long[] {1, 3, 50, 1000}) {
            var fast = new RollingVwap(window);
            var slow = new Model(window);
            long now = 0;
            for (int i = 0; i < 3000; i++) {
                now += rnd.nextInt(4) == 0 ? rnd.nextInt(30) : 0;
                var tr = t(now, syms[rnd.nextInt(syms.length)], 1 + rnd.nextInt(2_000_000), 1 + rnd.nextInt(500));
                fast.onTrade(tr);
                slow.all.add(tr);
                if (i % 3 == 0) {
                    String q = syms[rnd.nextInt(syms.length)];
                    assertEquals(slow.vwap(q, now), fast.vwap(q, now), "window " + window + " step " + i);
                }
            }
        }
    }

    @Test @Tag("part2") @Tag("perf")
    void amortisedConstantTimePerTrade() {
        // 窗口里常驻 10 万笔成交；每笔都问一次 VWAP——每次都重扫窗口的写法要 10^11 次操作
        int n = 1_000_000;
        var rnd = new Random(0);
        var r = new RollingVwap(100_000);
        String[] syms = new String[500];
        for (int i = 0; i < syms.length; i++) syms[i] = "S" + i;
        long check = assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            long sum = 0;
            for (int i = 0; i < n; i++) {
                r.onTrade(t(i, syms[rnd.nextInt(syms.length)], 10_000 + rnd.nextInt(1_000_000), 1 + rnd.nextInt(1000)));
                sum += r.vwap(syms[i % syms.length], i).orElse(0);
            }
            return sum;
        });
        assertTrue(check > 0);
        assertEquals(100_000, r.liveTrades());
    }

    // ---------------------------------------------------------------- Part 3
    @Test @Tag("part3")
    void topKBasic() {
        var r = sample(); // AAPL 1000000+2400000 = 3400000，MSFT 2500000
        assertEquals(List.of(sn("AAPL", 3_400_000), sn("MSFT", 2_500_000)), r.topK(5, 900));
        assertEquals(List.of(sn("AAPL", 3_400_000)), r.topK(1, 900));
        assertEquals(List.of(), r.topK(0, 900));
        // 1000：AAPL 在 0 的那笔过期，AAPL 只剩 2400000 < MSFT 2500000
        assertEquals(List.of(sn("MSFT", 2_500_000), sn("AAPL", 2_400_000)), r.topK(2, 1000));
        assertEquals(1000, r.now());
        // 1400：AAPL 在 400 的那笔过期；1900：MSFT 在 900 的那笔过期
        assertEquals(List.of(sn("MSFT", 2_500_000)), r.topK(10, 1400));
        assertEquals(List.of(), r.topK(10, 1900));
    }

    @Test @Tag("part3") @Tag("edge")
    void topKTiesBreakBySymbolAscending() {
        var r = new RollingVwap(1000);
        for (String s : new String[] {"ZED", "ABC", "MID", "A.B"}) r.onTrade(t(0, s, 10_000, 3));
        r.onTrade(t(0, "TOP", 10_000, 4));
        assertEquals(List.of(sn("TOP", 40_000), sn("A.B", 30_000), sn("ABC", 30_000)), r.topK(3, 0));
        assertEquals(List.of(sn("TOP", 40_000), sn("A.B", 30_000), sn("ABC", 30_000), sn("MID", 30_000), sn("ZED", 30_000)), r.topK(99, 0));
    }

    @Test @Tag("part3") @Tag("edge")
    void topKArgumentsAndClock() {
        var r = new RollingVwap(10);
        assertEquals(List.of(), r.topK(3, 0));
        assertThrows(IllegalArgumentException.class, () -> r.topK(-1, 0));
        r.onTrade(t(5, "A", 10_000, 1));
        assertThrows(IllegalArgumentException.class, () -> r.topK(1, 4));  // 时间倒退
        assertThrows(IllegalArgumentException.class, () -> r.topK(-1, 4)); // k 的检查先于时钟
        assertEquals(List.of(), r.topK(0, 4 + 100)); // k = 0 也会推进时钟（并让 A 过期）
        assertEquals(0, r.liveTrades());
    }

    @Test @Tag("part3") @Tag("edge")
    void topKReturnsAnImmutableSnapshot() {
        var r = sample();
        var top = r.topK(2, 900);
        assertThrows(UnsupportedOperationException.class, () -> top.add(sn("X", 1)));
        r.onTrade(t(901, "MSFT", 500_000, 100));
        assertEquals(List.of(sn("AAPL", 3_400_000), sn("MSFT", 2_500_000)), top); // 旧结果不受后续成交影响
    }

    @Test @Tag("part3")
    void randomTopKMatchesBruteForce() {
        var rnd = new Random(11);
        var syms = new String[12];
        for (int i = 0; i < syms.length; i++) syms[i] = "S" + (char) ('A' + i);
        for (long window : new long[] {2, 40, 500}) {
            var fast = new RollingVwap(window);
            var slow = new Model(window);
            long now = 0;
            for (int i = 0; i < 2000; i++) {
                now += rnd.nextInt(3);
                var tr = t(now, syms[rnd.nextInt(syms.length)], 1 + rnd.nextInt(5), 1 + rnd.nextInt(4)); // 小数字：大量并列
                fast.onTrade(tr);
                slow.all.add(tr);
                if (i % 5 == 0) {
                    int k = rnd.nextInt(14);
                    assertEquals(slow.top(k, now), fast.topK(k, now), "window " + window + " step " + i + " k " + k);
                }
            }
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void topKOverManySymbols() {
        var rnd = new Random(1);
        var r = new RollingVwap(50_000);
        String[] syms = new String[5000];
        for (int i = 0; i < syms.length; i++) syms[i] = "T" + i;
        long total = assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            long sum = 0;
            for (int i = 0; i < 500_000; i++) {
                r.onTrade(t(i, syms[rnd.nextInt(syms.length)], 10_000 + rnd.nextInt(100_000), 1 + rnd.nextInt(100)));
                if (i % 500 == 0) sum += r.topK(10, i).size();
            }
            return sum;
        });
        assertTrue(total > 9_900 && total <= 10_000, "total " + total); // 前几次查询时窗口里不足 10 个 symbol
    }
}
