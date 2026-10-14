import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.OptionalLong;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class TickerMapTest {

    @Test @Tag("part1")
    void putGetRemoveBasics() {
        var m = new TickerMap();
        assertEquals(0, m.size());
        assertEquals(OptionalLong.empty(), m.get("AAPL"));
        assertFalse(m.containsKey("AAPL"));
        assertEquals(OptionalLong.empty(), m.put("AAPL", 100));
        assertEquals(OptionalLong.of(100), m.put("AAPL", 150));   // 返回旧值
        assertEquals(OptionalLong.of(150), m.get("AAPL"));
        assertEquals(1, m.size());
        assertEquals(OptionalLong.of(150), m.remove("AAPL"));
        assertEquals(OptionalLong.empty(), m.remove("AAPL"));
        assertEquals(0, m.size());
        assertEquals(OptionalLong.empty(), m.get("AAPL"));
    }

    @Test @Tag("part1") @Tag("edge")
    void zeroValueIsNotAbsent() {
        var m = new TickerMap();
        m.put("ZERO", 0);
        assertTrue(m.containsKey("ZERO"));
        assertEquals(OptionalLong.of(0), m.get("ZERO"));
        m.put("NEG", -5);
        assertEquals(OptionalLong.of(-5), m.get("NEG"));
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyStringIsAnOrdinaryKey() {
        var m = new TickerMap();
        m.put("", 7);
        assertEquals(OptionalLong.of(7), m.get(""));
        assertEquals(1, m.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void nullKeysAreRejected() {
        var m = new TickerMap();
        assertThrows(NullPointerException.class, () -> m.put(null, 1));
        assertThrows(NullPointerException.class, () -> m.get(null));
        assertThrows(NullPointerException.class, () -> m.containsKey(null));
        assertThrows(NullPointerException.class, () -> m.remove(null));
        assertThrows(NullPointerException.class, () -> m.add(null, 1));
        assertThrows(IllegalArgumentException.class, () -> new TickerMap(-1));
    }

    @Test @Tag("part1")
    void addAccumulates() {
        var m = new TickerMap();
        assertEquals(5, m.add("MSFT", 5));
        assertEquals(8, m.add("MSFT", 3));
        assertEquals(-2, m.add("MSFT", -10));
        assertEquals(OptionalLong.of(-2), m.get("MSFT"));
        assertEquals(1, m.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void addOverflowLeavesTheMapUntouched() {
        var m = new TickerMap();
        m.put("BIG", Long.MAX_VALUE);
        assertThrows(ArithmeticException.class, () -> m.add("BIG", 1));
        assertEquals(OptionalLong.of(Long.MAX_VALUE), m.get("BIG"));
        m.put("LOW", Long.MIN_VALUE);
        assertThrows(ArithmeticException.class, () -> m.add("LOW", -1));
        assertEquals(OptionalLong.of(Long.MIN_VALUE), m.get("LOW"));
        assertEquals(Long.MAX_VALUE, m.add("NEWKEY", Long.MAX_VALUE)); // 新 key 从 0 起，不溢出
        assertEquals(3, m.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void growsPastManyResizes() {
        var m = new TickerMap();
        for (int i = 0; i < 100_000; i++) {
            m.put("K" + i, i);
            assertTrue((long) (m.size() + m.tombstones()) * 4 <= (long) m.capacity() * 3, "load factor too high at " + i);
        }
        assertEquals(100_000, m.size());
        for (int i = 0; i < 100_000; i++) assertEquals(OptionalLong.of(i), m.get("K" + i));
        assertEquals(OptionalLong.empty(), m.get("K100000"));
    }

    @Test @Tag("part1") @Tag("edge")
    void expectedSizePreventsResizing() {
        var m = new TickerMap(10_000);
        int cap = m.capacity();
        for (int i = 0; i < 10_000; i++) m.put("S" + i, i);
        assertEquals(cap, m.capacity(), "a presized map must not need to grow");
    }

    @Test @Tag("part1") @Tag("edge")
    void everyKeyWithTheSameHashCodeStillWorks() {
        // 1024 个 hashCode 完全相同的字符串：所有 key 都想住在同一个「家」。
        var keys = Tickers.sameHashCode(10);
        assertEquals(1, keys.stream().mapToInt(String::hashCode).distinct().count()); // 前提自检
        var m = new TickerMap();
        for (int i = 0; i < keys.size(); i++) assertEquals(OptionalLong.empty(), m.put(keys.get(i), i));
        for (int i = 0; i < keys.size(); i++) assertEquals(OptionalLong.of(i), m.get(keys.get(i)));
        for (int i = 0; i < keys.size(); i += 2) assertEquals(OptionalLong.of(i), m.remove(keys.get(i)));
        for (int i = 0; i < keys.size(); i++)
            assertEquals(i % 2 == 0 ? OptionalLong.empty() : OptionalLong.of(i), m.get(keys.get(i)));
        assertEquals(512, m.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void deletingTheMiddleOfAProbeChainDoesNotHideLaterKeys() {
        // "Aa" 和 "BB" 的 hashCode 相同，所以这四个字符串的 hashCode 全相同：它们排成同一条探测链
        var m = new TickerMap();
        m.put("AaAa", 1);
        m.put("AaBB", 2);
        m.put("BBAa", 3);
        m.put("BBBB", 4);
        assertEquals(OptionalLong.of(1), m.remove("AaAa"));   // 链头
        assertEquals(OptionalLong.of(2), m.get("AaBB"));
        assertEquals(OptionalLong.of(3), m.get("BBAa"));
        assertEquals(OptionalLong.of(4), m.get("BBBB"));
        assertEquals(OptionalLong.of(2), m.remove("AaBB"));   // 链中间
        assertEquals(OptionalLong.of(3), m.get("BBAa"));
        assertEquals(OptionalLong.of(4), m.get("BBBB"));
        m.put("AaAa", 10);                                    // 重新插入：既不能丢也不能重复
        assertEquals(3, m.size());
        var seen = new HashSet<String>();
        m.forEach((k, v) -> assertTrue(seen.add(k), "duplicate key in forEach: " + k));
        assertEquals(java.util.Set.of("AaAa", "BBAa", "BBBB"), seen);
    }

    @Test @Tag("part1") @Tag("edge")
    void reinsertingADeletedKeyReusesTheTombstone() {
        var m = new TickerMap();
        for (int i = 0; i < 5; i++) m.put("Q" + i, i);
        int cap = m.capacity();
        for (int round = 0; round < 100_000; round++) {
            m.remove("Q3");
            m.put("Q3", round);
        }
        assertEquals(cap, m.capacity(), "remove+put of the same key must not grow the table");
        assertEquals(5, m.size());
        assertEquals(OptionalLong.of(99_999), m.get("Q3"));
    }

    @Test @Tag("part1") @Tag("edge")
    void tombstoneChurnDoesNotBloatTheTableOrLoopForever() {
        // 一直有新代码上市、旧代码退市：任何时刻只有 <= 10 个活 key，但累计经过 300k 个不同 key
        var m = new TickerMap();
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            for (int i = 0; i < 300_000; i++) {
                m.put("N" + i, i);
                if (i >= 10) m.remove("N" + (i - 10));
                assertEquals(OptionalLong.empty(), m.get("never-there")); // 表里必须始终留有空格，否则这里会死循环
            }
        });
        assertEquals(10, m.size());
        assertTrue(m.capacity() <= 1024, "capacity " + m.capacity() + " keeps growing because tombstones are never cleaned");
        assertTrue(m.tombstones() + m.size() <= m.capacity() * 3 / 4);
    }

    @Test @Tag("part1")
    void randomOperationsAgreeWithJavaUtilHashMap() {
        var r = new Random(0);
        var mine = new TickerMap();
        var ref = new HashMap<String, Long>();
        var universe = Tickers.random(r, 600, 6);
        for (int step = 0; step < 200_000; step++) {
            String k = universe.get(r.nextInt(universe.size()));
            switch (r.nextInt(5)) {
                case 0 -> {
                    long v = r.nextInt(1000) - 500;
                    Long old = ref.put(k, v);
                    assertEquals(old == null ? OptionalLong.empty() : OptionalLong.of(old), mine.put(k, v));
                }
                case 1 -> {
                    long d = r.nextInt(100) - 50;
                    assertEquals(ref.merge(k, d, Long::sum), mine.add(k, d));
                }
                case 2 -> {
                    Long old = ref.remove(k);
                    assertEquals(old == null ? OptionalLong.empty() : OptionalLong.of(old), mine.remove(k));
                }
                default -> {
                    Long v = ref.get(k);
                    assertEquals(v == null ? OptionalLong.empty() : OptionalLong.of(v), mine.get(k));
                    assertEquals(v != null, mine.containsKey(k));
                }
            }
            assertEquals(ref.size(), mine.size());
        }
        var copy = new HashMap<String, Long>();
        mine.forEach(copy::put);
        assertEquals(ref, copy);
    }

    @Test @Tag("part1")
    void probeLengthStaysShortOnRealisticTickers() {
        // 全部 17576 个三字母代码（AAA, AAB, AAC, ...）：String.hashCode 把它们排成几乎连续的整数，
        // 直接取低位当下标的实现会聚成一大片
        var m = new TickerMap();
        for (String t : Tickers.allThreeLetters()) m.put(t, 1);
        assertEquals(17576, m.size());
        assertTrue(m.maxProbeLength() <= 64, "longest probe " + m.maxProbeLength());
    }

    @Test @Tag("part1") @Tag("perf")
    void millionOperations() {
        var r = new Random(0);
        var tickers = Tickers.random(r, 200_000, 8).toArray(new String[0]);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var m = new TickerMap();
            for (int i = 0; i < 1_000_000; i++) m.add(tickers[r.nextInt(tickers.length)], 1);
            long total = 0;
            for (String t : tickers) total += m.get(t).orElse(0);
            assertEquals(1_000_000, total);
        });
    }
}
