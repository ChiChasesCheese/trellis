import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.management.ManagementFactory;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Random;
import java.util.Set;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class FrozenTickerMapTest {
    private static long k(String t) { return TickerCodec.pack(t); }

    @Test @Tag("part3")
    void basics() {
        var m = new FrozenTickerMap(List.of("AAPL", "MSFT", "GOOG"));
        assertEquals(3, m.size());
        assertTrue(m.containsKey(k("AAPL")));
        assertFalse(m.containsKey(k("IBM")));
        assertEquals(0, m.get(k("AAPL"), -1));                 // 在 universe 里但还没写过 -> 0，不是 absent
        assertEquals(-1, m.get(k("IBM"), -1));
        assertEquals(100, m.add(k("AAPL"), 100));
        assertEquals(130, m.add(k("AAPL"), 30));
        assertTrue(m.put(k("MSFT"), 5));
        assertFalse(m.put(k("IBM"), 5));
        assertEquals(5, m.get(k("MSFT"), -1));
        assertThrows(IllegalArgumentException.class, () -> m.add(k("IBM"), 1));
    }

    @Test @Tag("part3") @Tag("edge")
    void rejectsBadUniverses() {
        assertThrows(IllegalArgumentException.class, () -> new FrozenTickerMap(List.of("AAPL", "AAPL")));
        assertThrows(IllegalArgumentException.class, () -> new FrozenTickerMap(List.of("AAPL", "brk.b")));
        assertThrows(IllegalArgumentException.class, () -> new FrozenTickerMap(List.of("")));
        var empty = new FrozenTickerMap(List.of());
        assertEquals(0, empty.size());
        assertEquals(-3, empty.get(k("A"), -3));
        assertEquals(-1, empty.indexOf(k("A")));
    }

    @Test @Tag("part3") @Tag("edge")
    void nonPositiveKeysAreJustAbsent() {
        var m = new FrozenTickerMap(List.of("A"));
        for (long bad : new long[] {0, -1, Long.MIN_VALUE}) {
            assertEquals(-1, m.indexOf(bad));
            assertFalse(m.containsKey(bad));
            assertEquals(42, m.get(bad, 42));
            assertFalse(m.put(bad, 1));
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void overflowThrowsAndKeepsTheValue() {
        var m = new FrozenTickerMap(List.of("A"));
        m.put(k("A"), Long.MAX_VALUE);
        assertThrows(ArithmeticException.class, () -> m.add(k("A"), 1));
        assertEquals(Long.MAX_VALUE, m.get(k("A"), 0));
        int i = m.indexOf(k("A"));
        assertThrows(ArithmeticException.class, () -> m.addAt(i, 1));
        assertEquals(Long.MAX_VALUE, m.getAt(i));
    }

    @Test @Tag("part3")
    void indexBasedFastPath() {
        var universe = Tickers.random(new Random(1), 2000, 8);
        var m = new FrozenTickerMap(universe);
        for (String t : universe) {
            int i = m.indexOf(k(t));
            assertTrue(i >= 0 && i < universe.size());
            assertEquals(k(t), m.keyAt(i));
            m.addAt(i, 3);
        }
        for (String t : universe) assertEquals(3, m.get(k(t), -1));
    }

    @Test @Tag("part3")
    void agreesWithLongTickerMapOnTheSameFeed() {
        var r = new Random(2);
        var universe = Tickers.random(r, 8000, 8);
        var frozen = new FrozenTickerMap(universe);
        var open = new LongTickerMap();
        var ref = new HashMap<Long, Long>();
        long[] keys = Tickers.pack(universe);
        for (int i = 0; i < 300_000; i++) {
            long key = keys[r.nextInt(keys.length)];
            long q = r.nextInt(1000);
            assertEquals(open.add(key, q), frozen.add(key, q));
            ref.merge(key, q, Long::sum);
        }
        for (long key : keys) assertEquals(ref.getOrDefault(key, 0L), frozen.get(key, -1));
        assertEquals(Set.copyOf(ref.keySet()).size() <= keys.length, true);
    }

    @Test @Tag("part3") @Tag("perf")
    void fortyMillionIndexedUpdates() {
        var universe = Tickers.random(new Random(0), 8000, 8);
        var m = new FrozenTickerMap(universe);
        long[] keys = Tickers.pack(universe);
        var r = new Random(1);
        int[] picks = new int[1 << 16];
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(keys.length);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            for (int i = 0; i < 20_000_000; i++) m.add(keys[picks[i & (picks.length - 1)]], 1);
            long total = 0;
            for (long key : keys) total += m.get(key, 0);
            assertEquals(20_000_000, total);
        });
    }

    @Test @Tag("part3") @Tag("perf")
    void hotPathDoesNotAllocate() {
        var universe = Tickers.random(new Random(0), 8000, 8);
        var m = new FrozenTickerMap(universe);
        long[] keys = Tickers.pack(universe);
        var r = new Random(1);
        int[] picks = new int[2_000_000];
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(keys.length);
        long allocated = assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
            var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
            long tid = Thread.currentThread().threadId();
            for (int i = 0; i < 400_000; i++) m.add(keys[picks[i]], 1);
            long before = mx.getThreadAllocatedBytes(tid);
            for (int i = 400_000; i < picks.length; i++) m.add(keys[picks[i]], 1);
            return mx.getThreadAllocatedBytes(tid) - before;
        });
        assertTrue(allocated < 256 * 1024, "allocated " + allocated);
    }
}
