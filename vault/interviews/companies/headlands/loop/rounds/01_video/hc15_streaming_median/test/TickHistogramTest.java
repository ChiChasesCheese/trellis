import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：价格范围有界时的直方图（树状数组）——功能测试；性能在 MedianPerfTest。 */
class TickHistogramTest {
    @Test @Tag("part4")
    void nearestRankExample() {
        var h = new TickHistogram(100);
        for (long x : new long[] {35, 20, 50, 15, 40}) h.add(x);
        assertEquals(5, h.count());
        assertEquals(15, h.percentile(5));
        assertEquals(20, h.percentile(30));
        assertEquals(20, h.percentile(40));
        assertEquals(35, h.percentile(50));
        assertEquals(35, h.median());
        assertEquals(50, h.percentile(100));
    }

    @Test @Tag("part4")
    void kthAndCountAtMostWithDuplicates() {
        var h = new TickHistogram(10);
        for (long x : new long[] {5, 1, 5, 3, 5, 3, 9}) h.add(x);
        long[] sorted = {1, 3, 3, 5, 5, 5, 9};
        for (int r = 1; r <= 7; r++) assertEquals(sorted[r - 1], h.kth(r), "kth " + r);
        assertEquals(0, h.countAtMost(0));
        assertEquals(1, h.countAtMost(1));
        assertEquals(3, h.countAtMost(3));
        assertEquals(6, h.countAtMost(8));
        assertEquals(7, h.countAtMost(9));
    }

    @Test @Tag("part4") @Tag("edge")
    void countAtMostOutsideTheBand() {
        var h = new TickHistogram(10);
        h.add(0);
        h.add(9);
        assertEquals(0, h.countAtMost(-1));
        assertEquals(0, h.countAtMost(Long.MIN_VALUE));
        assertEquals(1, h.countAtMost(0));
        assertEquals(2, h.countAtMost(10));
        assertEquals(2, h.countAtMost(Long.MAX_VALUE));
    }

    @Test @Tag("part4") @Tag("edge")
    void argumentsAndEmpty() {
        assertThrows(IllegalArgumentException.class, () -> new TickHistogram(0));
        assertThrows(IllegalArgumentException.class, () -> new TickHistogram(-1));
        assertThrows(IllegalArgumentException.class, () -> new TickHistogram(TickHistogram.MAX_TICKS + 1));
        var h = new TickHistogram(8);
        assertEquals(0, h.count());
        assertThrows(NoSuchElementException.class, h::median);
        assertThrows(NoSuchElementException.class, () -> h.percentile(99));
        assertThrows(IllegalArgumentException.class, () -> h.percentile(0));
        assertThrows(IllegalArgumentException.class, () -> h.percentile(101));
        assertThrows(IllegalArgumentException.class, () -> h.add(-1));
        assertThrows(IllegalArgumentException.class, () -> h.add(8));
        assertThrows(IllegalArgumentException.class, () -> h.add(Long.MAX_VALUE));
        assertThrows(IllegalArgumentException.class, () -> h.add(Long.MIN_VALUE));
        assertEquals(0, h.count()); // 被拒绝的 add 没有计数
        assertThrows(IllegalArgumentException.class, () -> h.kth(1));
        h.add(7);
        assertThrows(IllegalArgumentException.class, () -> h.kth(0));
        assertThrows(IllegalArgumentException.class, () -> h.kth(2));
        assertEquals(7, h.kth(1));
    }

    @Test @Tag("part4") @Tag("edge")
    void singleTickBand() {
        var h = new TickHistogram(1);
        for (int i = 0; i < 5; i++) h.add(0);
        assertEquals(0, h.median());
        assertEquals(0, h.percentile(100));
        assertEquals(5, h.count());
        assertThrows(IllegalArgumentException.class, () -> h.add(1));
    }

    @Test @Tag("part4") @Tag("edge")
    void bandEdgesAndTheLargestSupportedBand() {
        var h = new TickHistogram(TickHistogram.MAX_TICKS);
        h.add(0);
        h.add(TickHistogram.MAX_TICKS - 1);
        assertEquals(0, h.kth(1));
        assertEquals(TickHistogram.MAX_TICKS - 1, h.kth(2));
        assertEquals(0, h.median());
        assertEquals(TickHistogram.MAX_TICKS - 1, h.percentile(51));
    }

    @Test @Tag("part4")
    void matchesTheSortingOracleForEveryBandSize() {
        for (int band : new int[] {1, 2, 3, 7, 8, 9, 100, 1000, 1024, 1025}) { // 包括非 2 的幂
            var rnd = new Random(band);
            var h = new TickHistogram(band);
            var seen = new ArrayList<Long>();
            for (int i = 0; i < 800; i++) {
                long x = rnd.nextInt(band);
                h.add(x);
                seen.add(x);
                long[] arr = seen.stream().mapToLong(Long::longValue).toArray();
                for (int p : new int[] {1, 25, 50, 75, 99, 100}) {
                    if (i % 13 == 0 || p == 50) assertEquals(Oracle.percentile(arr, p), h.percentile(p), "band " + band + " n " + (i + 1) + " p " + p);
                }
            }
        }
    }

    @Test @Tag("part4")
    void agreesWithTheOrderStatisticsTree() {
        var rnd = new Random(3);
        var h = new TickHistogram(5000);
        var t = new OrderStatistics();
        for (int i = 0; i < 20_000; i++) {
            long x = (long) Math.abs(rnd.nextGaussian() * 800) % 5000;
            h.add(x);
            t.add(x);
            if (i % 97 == 0) {
                for (int p : new int[] {1, 50, 95, 100}) assertEquals(t.percentile(p), h.percentile(p));
                assertEquals(t.countAtMost(x), h.countAtMost(x));
            }
        }
    }
}
