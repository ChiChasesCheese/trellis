import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 1：两个堆，数据流中位数（偶数个取下中位数）。 */
class StreamingMedianTest {
    static long[] mediansOf(long... prices) {
        var m = new StreamingMedian();
        long[] out = new long[prices.length];
        for (int i = 0; i < prices.length; i++) {
            m.add(prices[i]);
            out[i] = m.median();
        }
        return out;
    }

    @Test @Tag("part1")
    void sample() {
        // 5 → 5；{5,15} 下中位数 5；{1,5,15} → 5；{1,3,5,15} → 下中位数 3（上中位数是 5）
        assertEquals(java.util.Arrays.toString(new long[] {5, 5, 5, 3}), java.util.Arrays.toString(mediansOf(5, 15, 1, 3)));
    }

    @Test @Tag("part1")
    void singleAndPair() {
        var m = new StreamingMedian();
        m.add(42);
        assertEquals(42, m.median());
        assertEquals(1, m.size());
        m.add(10);
        assertEquals(10, m.median()); // {10, 42}：下中位数
        m.add(50);
        assertEquals(42, m.median());
        assertEquals(3, m.size());
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyThrows() {
        var m = new StreamingMedian();
        assertEquals(0, m.size());
        assertThrows(NoSuchElementException.class, m::median);
        assertThrows(NoSuchElementException.class, m::doubledMedian);
    }

    @Test @Tag("part1") @Tag("edge")
    void ascendingDescendingAndConstant() {
        var asc = new long[10];
        var desc = new long[10];
        var same = new long[7];
        for (int i = 0; i < 10; i++) {
            asc[i] = i + 1;
            desc[i] = 10 - i;
        }
        java.util.Arrays.fill(same, 9);
        // 升序 1..n 的下中位数 = ceil(n/2)
        assertEquals("[1, 1, 2, 2, 3, 3, 4, 4, 5, 5]", java.util.Arrays.toString(mediansOf(asc)));
        // 10, 9, 8, ...: n 个数是 10-n+1..10，下中位数 = 10-n+ceil(n/2)
        assertEquals("[10, 9, 9, 8, 8, 7, 7, 6, 6, 5]", java.util.Arrays.toString(mediansOf(desc)));
        assertEquals("[9, 9, 9, 9, 9, 9, 9]", java.util.Arrays.toString(mediansOf(same)));
    }

    @Test @Tag("part1") @Tag("edge")
    void negativesAndExtremes() {
        assertEquals("[-5, -5, -1]", java.util.Arrays.toString(mediansOf(-5, -1, 3)));
        assertEquals(Long.MIN_VALUE, mediansOf(Long.MIN_VALUE, Long.MAX_VALUE)[1]);
        assertEquals(Long.MAX_VALUE, mediansOf(Long.MAX_VALUE, Long.MAX_VALUE)[1]);
        assertEquals(Long.MIN_VALUE, mediansOf(Long.MIN_VALUE, Long.MIN_VALUE, Long.MAX_VALUE)[2]);
        assertEquals(0, mediansOf(Long.MIN_VALUE, 0, Long.MAX_VALUE)[2]);
    }

    @Test @Tag("part1") @Tag("edge")
    void duplicatesOnBothSidesOfTheMiddle() {
        assertEquals("[2, 2, 2, 2, 2, 2]", java.util.Arrays.toString(mediansOf(2, 2, 2, 2, 2, 2)));
        // {3}→3  {1,3}→1  {1,3,3}→3  {1,1,3,3}→1  {1,1,3,3,3}→3
        assertEquals("[3, 1, 3, 1, 3]", java.util.Arrays.toString(mediansOf(3, 1, 3, 1, 3)));
    }

    @Test @Tag("part1")
    void doubledMedianIsTheExactMedianTimesTwo() {
        var m = new StreamingMedian();
        m.add(1);
        assertEquals(2, m.doubledMedian());
        m.add(2);
        assertEquals(3, m.doubledMedian()); // (1 + 2) / 2 = 1.5 → 3
        m.add(10);
        assertEquals(4, m.doubledMedian()); // 中位数 2
        m.add(20);
        assertEquals(12, m.doubledMedian()); // (2 + 10) / 2 = 6 → 12
        assertEquals(2, m.median()); // median() 还是下中位数
    }

    @Test @Tag("part1") @Tag("edge")
    void doubledMedianOverflows() {
        var one = new StreamingMedian();
        one.add(Long.MAX_VALUE);
        assertThrows(ArithmeticException.class, one::doubledMedian);
        var neg = new StreamingMedian();
        neg.add(Long.MIN_VALUE);
        assertThrows(ArithmeticException.class, neg::doubledMedian);
        var two = new StreamingMedian();
        two.add(Long.MAX_VALUE);
        two.add(Long.MIN_VALUE);
        assertEquals(-1, two.doubledMedian()); // MIN + MAX = -1，不溢出
        two.add(5);
        assertEquals(10, two.doubledMedian());
        var big = new StreamingMedian();
        big.add(Long.MAX_VALUE);
        big.add(Long.MAX_VALUE);
        assertThrows(ArithmeticException.class, big::doubledMedian);
        assertEquals(Long.MAX_VALUE, big.median()); // 查询失败不影响状态
    }

    @Test @Tag("part1")
    void randomStreamsMatchTheSortingOracle() {
        for (long bound : new long[] {3, 10, 1_000_000, Long.MAX_VALUE}) {
            var rnd = new Random(bound);
            var m = new StreamingMedian();
            var seen = new java.util.ArrayList<Long>();
            for (int i = 0; i < 3000; i++) {
                long x = rnd.nextLong(bound) - bound / 2;
                m.add(x);
                seen.add(x);
                assertEquals(Oracle.lowerMedian(seen.stream().mapToLong(Long::longValue).toArray()), m.median(), "bound " + bound + " step " + i);
                assertEquals(i + 1, m.size());
            }
        }
    }

    @Test @Tag("part1") @Tag("edge")
    void queryingDoesNotChangeState() {
        var m = new StreamingMedian();
        for (long x : new long[] {4, 8, 15, 16, 23, 42}) m.add(x);
        long first = m.median();
        for (int i = 0; i < 5; i++) assertEquals(first, m.median());
        assertEquals(15, first);
        assertEquals(6, m.size());
    }
}
