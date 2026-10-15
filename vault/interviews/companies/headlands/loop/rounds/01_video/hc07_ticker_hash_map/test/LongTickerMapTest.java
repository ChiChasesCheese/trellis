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

class LongTickerMapTest {
    private static long k(String ticker) { return TickerCodec.pack(ticker); }

    @Test @Tag("part2")
    void basics() {
        var m = new LongTickerMap();
        assertEquals(-1, m.get(k("AAPL"), -1));
        assertFalse(m.containsKey(k("AAPL")));
        assertTrue(m.put(k("AAPL"), 10));
        assertFalse(m.put(k("AAPL"), 20));
        assertEquals(20, m.get(k("AAPL"), -1));
        assertEquals(25, m.add(k("AAPL"), 5));
        assertEquals(7, m.add(k("MSFT"), 7));       // 新 key 从 0 起
        assertEquals(2, m.size());
        assertTrue(m.remove(k("AAPL")));
        assertFalse(m.remove(k("AAPL")));
        assertEquals(1, m.size());
        assertEquals(0, m.get(k("AAPL"), 0));
    }

    @Test @Tag("part2") @Tag("edge")
    void keysMustBePositive() {
        var m = new LongTickerMap();
        for (long bad : new long[] {0, -1, Long.MIN_VALUE}) {
            assertThrows(IllegalArgumentException.class, () -> m.put(bad, 1));
            assertThrows(IllegalArgumentException.class, () -> m.get(bad, 0));
            assertThrows(IllegalArgumentException.class, () -> m.add(bad, 1));
            assertThrows(IllegalArgumentException.class, () -> m.remove(bad));
            assertThrows(IllegalArgumentException.class, () -> m.containsKey(bad));
        }
        assertThrows(IllegalArgumentException.class, () -> new LongTickerMap(-1));
        assertTrue(m.put(Long.MAX_VALUE, 1));
        assertEquals(1, m.get(Long.MAX_VALUE, 0));
    }

    @Test @Tag("part2") @Tag("edge")
    void zeroAndNegativeValuesAreRealValues() {
        var m = new LongTickerMap();
        m.put(k("Z"), 0);
        assertTrue(m.containsKey(k("Z")));
        assertEquals(0, m.get(k("Z"), 99));
        m.put(k("N"), Long.MIN_VALUE);
        assertEquals(Long.MIN_VALUE, m.get(k("N"), 0));
    }

    @Test @Tag("part2") @Tag("edge")
    void addOverflowLeavesTheValueAlone() {
        var m = new LongTickerMap();
        m.put(k("BIG"), Long.MAX_VALUE);
        assertThrows(ArithmeticException.class, () -> m.add(k("BIG"), 1));
        assertEquals(Long.MAX_VALUE, m.get(k("BIG"), 0));
        assertEquals(1, m.size());
    }

    @Test @Tag("part2") @Tag("edge")
    void growsAndKeepsEverything() {
        var m = new LongTickerMap();
        var tickers = Tickers.random(new Random(3), 100_000, 8);
        for (int i = 0; i < tickers.size(); i++) {
            m.put(k(tickers.get(i)), i);
            assertTrue((long) (m.size() + m.tombstones()) * 4 <= (long) m.capacity() * 3);
        }
        assertEquals(tickers.size(), m.size());
        for (int i = 0; i < tickers.size(); i++) assertEquals(i, m.get(k(tickers.get(i)), -1));
    }

    @Test @Tag("part2") @Tag("edge")
    void tombstoneChurnStaysBounded() {
        var m = new LongTickerMap();
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            for (long i = 1; i <= 400_000; i++) {
                m.put(i, i);
                if (i > 10) assertTrue(m.remove(i - 10));
                assertEquals(-5, m.get(Long.MAX_VALUE - 1, -5)); // 必须始终留有空格，否则这里死循环
            }
        });
        assertEquals(10, m.size());
        assertTrue(m.capacity() <= 1024, "capacity " + m.capacity());
    }

    @Test @Tag("part2") @Tag("edge")
    void deletingInTheMiddleOfAChainKeepsTheRest() {
        // 一批互相挤在一起的 key：先删一半再逐个查
        var m = new LongTickerMap(4);
        var tickers = Tickers.random(new Random(4), 3000, 3);
        for (String t : tickers) m.put(k(t), 1);
        for (int i = 0; i < tickers.size(); i += 2) assertTrue(m.remove(k(tickers.get(i))));
        for (int i = 0; i < tickers.size(); i++)
            assertEquals(i % 2 == 0 ? -1 : 1, m.get(k(tickers.get(i)), -1), tickers.get(i));
    }

    @Test @Tag("part2")
    void randomOperationsAgreeWithHashMap() {
        var r = new Random(0);
        var mine = new LongTickerMap();
        var ref = new HashMap<Long, Long>();
        long[] universe = Tickers.pack(Tickers.random(r, 800, 8));
        for (int step = 0; step < 300_000; step++) {
            long key = universe[r.nextInt(universe.length)];
            switch (r.nextInt(5)) {
                case 0 -> {
                    long v = r.nextInt(1000) - 500;
                    assertEquals(ref.put(key, v) == null, mine.put(key, v));
                }
                case 1 -> {
                    long d = r.nextInt(100) - 50;
                    assertEquals(ref.merge(key, d, Long::sum), mine.add(key, d));
                }
                case 2 -> assertEquals(ref.remove(key) != null, mine.remove(key));
                default -> {
                    Long v = ref.get(key);
                    assertEquals(v == null ? -777L : v, mine.get(key, -777L));
                    assertEquals(v != null, mine.containsKey(key));
                }
            }
            assertEquals(ref.size(), mine.size());
        }
        var copy = new HashMap<Long, Long>();
        mine.forEach(copy::put);
        assertEquals(ref, copy);
    }

    @Test @Tag("part2") @Tag("edge")
    void hashSpreadsPackedKeysWhoseLowBitsAreAllZero() {
        // 打包后短代码的低位全是补的 0：用 key & mask 当下标的实现，会让几乎所有 key 落在同一格
        var m = new LongTickerMap();
        for (String t : Tickers.allThreeLetters()) m.put(k(t), 1);
        assertEquals(17576, m.size());
        assertTrue(m.maxProbeLength() <= 64, "longest probe " + m.maxProbeLength());
        var m2 = new LongTickerMap();
        for (String t : Tickers.random(new Random(5), 8000, 8)) m2.put(k(t), 1);
        assertTrue(m2.maxProbeLength() <= 64, "longest probe " + m2.maxProbeLength());
    }

    @Test @Tag("part2")
    void agreesWithTickerMapOnTheSameFeed() {
        var r = new Random(6);
        var tickers = Tickers.random(r, 3000, 8);
        var strMap = new TickerMap();
        var longMap = new LongTickerMap();
        for (int i = 0; i < 200_000; i++) {
            String t = tickers.get(r.nextInt(tickers.size()));
            long q = 1 + r.nextInt(500);
            assertEquals(strMap.add(t, q), longMap.add(k(t), q));
        }
        strMap.forEach((t, v) -> assertEquals(v, longMap.get(k(t), -1)));
        assertEquals(strMap.size(), longMap.size());
    }

    @Test @Tag("part2") @Tag("perf")
    void fiveMillionAddsOnEightThousandTickers() {
        long[] keys = Tickers.pack(Tickers.random(new Random(0), 8000, 8));
        var r = new Random(1);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var m = new LongTickerMap();
            for (int i = 0; i < 5_000_000; i++) m.add(keys[r.nextInt(keys.length)], 1);
            long total = 0;
            for (long key : keys) total += m.get(key, 0);
            assertEquals(5_000_000, total);
        });
    }

    @Test @Tag("part2") @Tag("perf")
    void steadyStateAddsDoNotAllocate() {
        long[] keys = Tickers.pack(Tickers.random(new Random(0), 8000, 8));
        var m = new LongTickerMap(keys.length);
        for (long key : keys) m.put(key, 0);
        var r = new Random(2);
        int[] picks = new int[2_000_000];                 // 先抽好，测试自己的随机数不进分配统计
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(keys.length);
        long allocated = assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
            var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
            long tid = Thread.currentThread().threadId();
            for (int i = 0; i < 400_000; i++) m.add(keys[picks[i]], 1); // 预热
            long before = mx.getThreadAllocatedBytes(tid);
            for (int i = 400_000; i < picks.length; i++) m.add(keys[picks[i]], 1);
            return mx.getThreadAllocatedBytes(tid) - before;
        });
        assertTrue(allocated < 256 * 1024, "allocated " + allocated + " bytes for 1.6M adds");
    }

    @Test @Tag("part2") @Tag("perf")
    void boxedHashMapAllocatesOrdersOfMagnitudeMore() {
        // 对照组：同一个流，HashMap<String,Long>.merge 每次都要装箱一个 Long
        var tickers = Tickers.random(new Random(0), 8000, 8);
        var r = new Random(2);
        int[] picks = new int[2_000_000];
        for (int i = 0; i < picks.length; i++) picks[i] = r.nextInt(tickers.size());
        long[] keys = Tickers.pack(tickers);
        var boxed = new HashMap<String, Long>();
        var packed = new LongTickerMap(keys.length);
        tickers.forEach(t -> { boxed.put(t, 0L); packed.put(k(t), 0); });
        long[] bytes = assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
            var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
            long tid = Thread.currentThread().threadId();
            for (int i = 0; i < 400_000; i++) { boxed.merge(tickers.get(picks[i]), 1L, Long::sum); packed.add(keys[picks[i]], 1); }
            long b0 = mx.getThreadAllocatedBytes(tid);
            for (int i = 400_000; i < picks.length; i++) boxed.merge(tickers.get(picks[i]), 1L, Long::sum);
            long b1 = mx.getThreadAllocatedBytes(tid);
            for (int i = 400_000; i < picks.length; i++) packed.add(keys[picks[i]], 1);
            long b2 = mx.getThreadAllocatedBytes(tid);
            return new long[] {b1 - b0, b2 - b1};
        });
        assertTrue(bytes[0] > 8_000_000, "HashMap<String,Long> allocated only " + bytes[0]);
        assertTrue(bytes[1] < 256 * 1024, "LongTickerMap allocated " + bytes[1]);
    }
}
