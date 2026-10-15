import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class SymbolIndexTest {

    /** 断言 idx 是 universe 上的最小完美哈希：下标恰好是 0..n-1 的一个排列，keyAt 是它的反函数。 */
    private static void assertMinimalPerfect(long[] universe, SymbolIndex idx) {
        int n = universe.length;
        assertEquals(n, idx.size());
        boolean[] hit = new boolean[n];
        for (long key : universe) {
            int i = idx.indexOf(key);
            assertTrue(i >= 0 && i < n, "index out of range for " + key + ": " + i);
            assertFalse(hit[i], "two keys share index " + i);
            hit[i] = true;
            assertEquals(key, idx.keyAt(i));
        }
    }

    @Test @Tag("part3")
    void smallUniverse() {
        long[] u = Tickers.pack(List.of("AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "META"));
        var idx = SymbolIndex.build(u);
        assertMinimalPerfect(u, idx);
        assertEquals(-1, idx.indexOf(TickerCodec.pack("IBM")));
    }

    @Test @Tag("part3") @Tag("edge")
    void degenerateUniverses() {
        var empty = SymbolIndex.build(new long[0]);
        assertEquals(0, empty.size());
        assertEquals(-1, empty.indexOf(TickerCodec.pack("A")));
        var one = SymbolIndex.build(new long[] {TickerCodec.pack("X")});
        assertEquals(0, one.indexOf(TickerCodec.pack("X")));
        assertEquals(-1, one.indexOf(TickerCodec.pack("Y")));
        long[] two = Tickers.pack(List.of("A", "B"));
        assertMinimalPerfect(two, SymbolIndex.build(two));
        for (int n = 1; n <= 40; n++) {
            long[] u = Tickers.pack(Tickers.random(new Random(n), n, 6));
            assertMinimalPerfect(u, SymbolIndex.build(u));
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void rejectsBadUniverses() {
        long a = TickerCodec.pack("A");
        assertThrows(IllegalArgumentException.class, () -> SymbolIndex.build(new long[] {a, a}));
        assertThrows(IllegalArgumentException.class, () -> SymbolIndex.build(new long[] {a, 0}));
        assertThrows(IllegalArgumentException.class, () -> SymbolIndex.build(new long[] {a, -3}));
    }

    @Test @Tag("part3")
    void keysOutsideTheUniverseAreRecognised() {
        var r = new Random(7);
        var inside = Tickers.random(r, 8000, 6);
        var all = new HashSet<>(inside);
        long[] u = Tickers.pack(inside);
        var idx = SymbolIndex.build(u);
        int tested = 0;
        for (String t : Tickers.random(r, 60_000, 8)) {
            if (all.contains(t)) continue;
            assertEquals(-1, idx.indexOf(TickerCodec.pack(t)), t);
            tested++;
        }
        assertTrue(tested > 50_000);
        for (long odd : new long[] {0, -1, Long.MIN_VALUE, Long.MAX_VALUE, 1}) assertEquals(-1, idx.indexOf(odd));
    }

    @Test @Tag("part3") @Tag("edge")
    void denseStructuredUniverse() {
        long[] u = Tickers.pack(Tickers.allThreeLetters());   // AAA..ZZZ，key 的低 25 位全是 0
        assertMinimalPerfect(u, SymbolIndex.build(u));
    }

    @Test @Tag("part3") @Tag("edge")
    void buildOrderDoesNotMatter() {
        var tickers = new ArrayList<>(Tickers.random(new Random(8), 5000, 8));
        long[] u = Tickers.pack(tickers);
        java.util.Collections.shuffle(tickers, new Random(9));
        long[] shuffled = Tickers.pack(tickers);
        assertMinimalPerfect(u, SymbolIndex.build(u));
        assertMinimalPerfect(shuffled, SymbolIndex.build(shuffled));
        assertTrue(u != shuffled);
    }

    @Test @Tag("part3") @Tag("perf")
    void buildsOneHundredThousandSymbolsQuickly() {
        long[] u = Tickers.pack(Tickers.random(new Random(0), 100_000, 8));
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> assertMinimalPerfect(u, SymbolIndex.build(u)));
    }

    @Test @Tag("part3") @Tag("perf")
    void twentyMillionLookups() {
        long[] u = Tickers.pack(Tickers.random(new Random(0), 8000, 8));
        var idx = SymbolIndex.build(u);
        var r = new Random(1);
        int[] picks = new int[1 << 16];
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(u.length);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            long sum = 0;
            for (int i = 0; i < 20_000_000; i++) sum += idx.indexOf(u[picks[i & (picks.length - 1)]]);
            assertTrue(sum > 0);
        });
    }
}
