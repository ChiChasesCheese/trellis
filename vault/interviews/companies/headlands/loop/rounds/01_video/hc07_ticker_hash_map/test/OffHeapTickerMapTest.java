import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.management.ManagementFactory;
import java.time.Duration;
import java.util.HashMap;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class OffHeapTickerMapTest {
    private static long k(String t) { return TickerCodec.pack(t); }

    @Test @Tag("part4")
    void basics() {
        try (var m = new OffHeapTickerMap(100)) {
            assertEquals(0, m.size());
            assertEquals(-1, m.get(k("AAPL"), -1));
            assertFalse(m.containsKey(k("AAPL")));
            assertTrue(m.put(k("AAPL"), 10));
            assertFalse(m.put(k("AAPL"), 20));
            assertEquals(20, m.get(k("AAPL"), -1));
            assertEquals(25, m.add(k("AAPL"), 5));
            assertEquals(3, m.add(k("MSFT"), 3));
            assertEquals(2, m.size());
            assertTrue(m.containsKey(k("MSFT")));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void capacityIsAPowerOfTwoWithHeadroom() {
        for (int n : new int[] {1, 2, 3, 7, 8, 100, 1000, 4096, 5000}) {
            try (var m = new OffHeapTickerMap(n)) {
                assertEquals(n, m.maxEntries());
                assertTrue(Integer.bitCount(m.capacity()) == 1, "capacity " + m.capacity());
                assertTrue(m.capacity() >= 2 * n, "capacity " + m.capacity() + " for " + n);
            }
        }
        assertThrows(IllegalArgumentException.class, () -> new OffHeapTickerMap(0));
        assertThrows(IllegalArgumentException.class, () -> new OffHeapTickerMap(-5));
    }

    @Test @Tag("part4") @Tag("edge")
    void fullTableRejectsNewKeysButKeepsServingOldOnes() {
        try (var m = new OffHeapTickerMap(3)) {
            m.put(k("A"), 1);
            m.put(k("B"), 2);
            m.add(k("C"), 3);
            assertThrows(IllegalStateException.class, () -> m.put(k("D"), 4));
            assertThrows(IllegalStateException.class, () -> m.add(k("D"), 4));
            assertEquals(3, m.size());
            assertEquals(-1, m.get(k("D"), -1));
            assertEquals(5, m.add(k("B"), 3));          // 已有 key 仍可更新
            assertFalse(m.put(k("C"), 9));
            assertEquals(9, m.get(k("C"), -1));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void invalidKeysAndOverflow() {
        try (var m = new OffHeapTickerMap(10)) {
            for (long bad : new long[] {0, -1, Long.MIN_VALUE}) {
                assertThrows(IllegalArgumentException.class, () -> m.put(bad, 1));
                assertThrows(IllegalArgumentException.class, () -> m.get(bad, 0));
                assertThrows(IllegalArgumentException.class, () -> m.add(bad, 1));
                assertThrows(IllegalArgumentException.class, () -> m.containsKey(bad));
            }
            m.put(k("BIG"), Long.MAX_VALUE);
            assertThrows(ArithmeticException.class, () -> m.add(k("BIG"), 1));
            assertEquals(Long.MAX_VALUE, m.get(k("BIG"), 0));
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void accessAfterCloseFailsAndCloseIsIdempotent() {
        var m = new OffHeapTickerMap(10);
        m.put(k("A"), 1);
        m.close();
        m.close();
        assertThrows(IllegalStateException.class, () -> m.get(k("A"), 0));
        assertThrows(IllegalStateException.class, () -> m.put(k("B"), 1));
        assertThrows(IllegalStateException.class, () -> m.add(k("A"), 1));
    }

    @Test @Tag("part4")
    void randomOperationsAgreeWithHashMap() {
        var r = new Random(0);
        long[] keys = Tickers.pack(Tickers.random(r, 1000, 8));
        var ref = new HashMap<Long, Long>();
        try (var m = new OffHeapTickerMap(1000)) {
            for (int step = 0; step < 300_000; step++) {
                long key = keys[r.nextInt(keys.length)];
                if (r.nextInt(3) == 0) {
                    long v = r.nextInt(1000);
                    assertEquals(ref.put(key, v) == null, m.put(key, v));
                } else {
                    long d = r.nextInt(100);
                    assertEquals(ref.merge(key, d, Long::sum), m.add(key, d));
                }
                assertEquals(ref.size(), m.size());
            }
            for (long key : keys) assertEquals(ref.getOrDefault(key, -1L), m.get(key, -1));
        }
    }

    @Test @Tag("part4") @Tag("perf")
    void usableFromAnotherThread() {
        var m = new OffHeapTickerMap(10);
        try {
            assertTimeoutPreemptively(Duration.ofSeconds(2), () -> m.add(k("X"), 1)); // JUnit 在另一个线程里跑这个 lambda
            assertEquals(1, m.get(k("X"), 0));
        } finally {
            m.close();
        }
    }

    @Test @Tag("part4") @Tag("perf")
    void fiveMillionAddsAndNoHeapAllocation() {
        long[] keys = Tickers.pack(Tickers.random(new Random(0), 8000, 8));
        var r = new Random(1);
        int[] picks = new int[5_000_000];
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(keys.length);
        try (var m = new OffHeapTickerMap(8000)) {
            for (long key : keys) m.put(key, 0);
            long allocated = assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
                var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
                long tid = Thread.currentThread().threadId();
                for (int i = 0; i < 1_000_000; i++) m.add(keys[picks[i]], 1);
                long before = mx.getThreadAllocatedBytes(tid);
                for (int i = 1_000_000; i < picks.length; i++) m.add(keys[picks[i]], 1);
                return mx.getThreadAllocatedBytes(tid) - before;
            });
            assertTrue(allocated < 256 * 1024, "allocated " + allocated);
            long total = 0;
            for (long key : keys) total += m.get(key, 0);
            assertEquals(5_000_000, total);
        }
    }
}
