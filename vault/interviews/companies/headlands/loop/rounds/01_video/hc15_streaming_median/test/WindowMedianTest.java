import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2：最近 k 笔成交价的滑动窗口中位数（惰性删除）。 */
class WindowMedianTest {
    @Test @Tag("part2")
    void slideSample() {
        // 窗口 3：{1}→1  {1,3}→1  {1,3,-1}→1  {3,-1,-3}→-1  {-1,-3,5}→-1  {-3,5,3}→3  {5,3,6}→5  {3,6,7}→6
        assertArrayEquals(new long[] {1, 1, 1, -1, -1, 3, 5, 6}, WindowMedian.slide(new long[] {1, 3, -1, -3, 5, 3, 6, 7}, 3));
    }

    @Test @Tag("part2")
    void sizeGrowsToKThenStays() {
        var w = new WindowMedian(3);
        assertEquals(0, w.size());
        w.add(10);
        w.add(20);
        assertEquals(2, w.size());
        assertEquals(10, w.median()); // {10,20} 下中位数
        w.add(30);
        w.add(40);
        w.add(50);
        assertEquals(3, w.size());
        assertEquals(40, w.median()); // {30,40,50}
    }

    @Test @Tag("part2") @Tag("edge")
    void windowOneIsTheLastPrice() {
        assertArrayEquals(new long[] {7, -2, 9, 9, 0}, WindowMedian.slide(new long[] {7, -2, 9, 9, 0}, 1));
    }

    @Test @Tag("part2") @Tag("edge")
    void windowTwoIsTheSmallerOfTheLastTwo() {
        assertArrayEquals(new long[] {5, 5, 1, 1, 3}, WindowMedian.slide(new long[] {5, 9, 1, 4, 3}, 2));
    }

    @Test @Tag("part2") @Tag("edge")
    void windowLargerThanTheStreamEqualsPart1() {
        long[] prices = {5, 15, 1, 3};
        assertArrayEquals(new long[] {5, 5, 5, 3}, WindowMedian.slide(prices, 100));
    }

    @Test @Tag("part2") @Tag("edge")
    void emptyAndArguments() {
        var w = new WindowMedian(4);
        assertThrows(NoSuchElementException.class, w::median);
        assertThrows(IllegalArgumentException.class, () -> new WindowMedian(0));
        assertThrows(IllegalArgumentException.class, () -> new WindowMedian(-3));
        assertThrows(IllegalArgumentException.class, () -> WindowMedian.slide(new long[] {1}, 0));
        assertThrows(NullPointerException.class, () -> WindowMedian.slide(null, 3));
        assertArrayEquals(new long[0], WindowMedian.slide(new long[0], 3));
    }

    @Test @Tag("part2") @Tag("edge")
    void duplicatesEqualToBothHeapTops() {
        // 旧值等于 lo 顶、同时 hi 里也有同样的值——惰性删除必须记在正确的堆上
        long[] p = {5, 5, 5, 1, 1, 1, 9, 9, 9, 9, 9, 5, 5, 1, 1, 9};
        for (int k : new int[] {2, 3, 4, 5}) assertArrayEquals(expected(p, k), WindowMedian.slide(p, k), "k " + k);
    }

    /** 用排序算 oracle。 */
    static long[] expected(long[] prices, int k) {
        var seen = new ArrayList<Long>();
        long[] out = new long[prices.length];
        for (int i = 0; i < prices.length; i++) {
            seen.add(prices[i]);
            out[i] = Oracle.lowerMedian(Oracle.lastK(seen, k));
        }
        return out;
    }

    @Test @Tag("part2") @Tag("edge")
    void extremeValuesInTheWindow() {
        long[] p = {Long.MAX_VALUE, Long.MIN_VALUE, 0, Long.MAX_VALUE, Long.MAX_VALUE, Long.MIN_VALUE, Long.MIN_VALUE, 7};
        for (int k : new int[] {1, 2, 3, 4}) assertArrayEquals(expected(p, k), WindowMedian.slide(p, k), "k " + k);
    }

    @Test @Tag("part2")
    void randomStreamsMatchTheSortingOracle() {
        for (int k : new int[] {1, 2, 3, 4, 5, 10, 50}) {
            for (long bound : new long[] {2, 5, 1000, Long.MAX_VALUE}) { // 小范围 = 大量重复
                var rnd = new Random(k * 31L + bound);
                long[] prices = new long[2500];
                for (int i = 0; i < prices.length; i++) prices[i] = bound == Long.MAX_VALUE ? rnd.nextLong() : rnd.nextLong(bound) - bound / 2;
                assertArrayEquals(expected(prices, k), WindowMedian.slide(prices, k), "k " + k + " bound " + bound);
            }
        }
    }

    @Test @Tag("part2")
    void orderedStreamsMatchTheSortingOracle() {
        long[] up = new long[600], down = new long[600], zigzag = new long[600];
        for (int i = 0; i < 600; i++) {
            up[i] = i;
            down[i] = 600 - i;
            zigzag[i] = i % 2 == 0 ? i : -i;
        }
        for (int k : new int[] {2, 3, 8, 99}) {
            assertArrayEquals(expected(up, k), WindowMedian.slide(up, k), "up k " + k);
            assertArrayEquals(expected(down, k), WindowMedian.slide(down, k), "down k " + k);
            assertArrayEquals(expected(zigzag, k), WindowMedian.slide(zigzag, k), "zigzag k " + k);
        }
    }

    @Test @Tag("part2") @Tag("edge")
    void lazyDeletionKeepsMemoryBoundedOnAnAscendingStream() {
        // 升序流：失效元素永远沉在 lo 的堆底。不整理的话，堆里会堆到 O(n) 个
        int k = 100;
        var w = new WindowMedian(k);
        int worst = 0;
        for (int i = 0; i < 100_000; i++) {
            w.add(i);
            worst = Math.max(worst, w.retained());
        }
        assertTrue(worst <= 4 * k, "retained up to " + worst + " entries for k = " + k);
        assertEquals(99_949, w.median()); // 窗口 99900..99999，第 50 小
    }
}
