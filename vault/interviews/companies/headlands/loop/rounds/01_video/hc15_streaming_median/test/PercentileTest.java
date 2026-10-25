import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import java.time.Duration;
import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 3：任意百分位（最近秩法）——固定 p 的两堆 vs 任意 p 的顺序统计树。 */
class PercentileTest {
    // ---------------------------------------------------------------- 最近秩
    @Test @Tag("part3")
    void rankTable() {
        long[][] cases = {
                // n, p, rank
                {0, 50, 0}, {1, 1, 1}, {1, 100, 1}, {2, 50, 1}, {3, 50, 2}, {4, 50, 2}, {5, 50, 3}, {7, 50, 4}, {10, 50, 5},
                {5, 30, 2}, {5, 40, 2}, {5, 100, 5}, {5, 1, 1}, {100, 99, 99}, {101, 99, 100}, {100, 1, 1}, {101, 1, 2},
                {10, 95, 10}, {20, 95, 19}, {200, 95, 190}, {199, 95, 190}};
        for (long[] c : cases) assertEquals(c[2], OrderStatistics.rank(c[0], (int) c[1]), "rank(" + c[0] + "," + c[1] + ")");
    }

    @Test @Tag("part3") @Tag("edge")
    void rankDoesNotOverflow() {
        assertEquals(Long.MAX_VALUE, OrderStatistics.rank(Long.MAX_VALUE, 100));
        assertEquals(4_611_686_018_427_387_904L, OrderStatistics.rank(Long.MAX_VALUE, 50)); // ceil(MAX / 2)
        assertEquals(92_233_720_368_547_759L, OrderStatistics.rank(Long.MAX_VALUE, 1));      // ceil(MAX / 100)
        assertThrows(IllegalArgumentException.class, () -> OrderStatistics.rank(10, 0));
        assertThrows(IllegalArgumentException.class, () -> OrderStatistics.rank(10, 101));
        assertThrows(IllegalArgumentException.class, () -> OrderStatistics.rank(10, -5));
        assertThrows(IllegalArgumentException.class, () -> OrderStatistics.rank(-1, 50));
    }

    // ---------------------------------------------------------------- 顺序统计结构
    static OrderStatistics tree(long... xs) {
        var t = new OrderStatistics();
        for (long x : xs) t.add(x);
        return t;
    }

    @Test @Tag("part3")
    void nearestRankExample() {
        var t = tree(35, 20, 50, 15, 40); // 乱序到达：排序后 15 20 35 40 50
        assertEquals(15, t.percentile(5));
        assertEquals(20, t.percentile(30));
        assertEquals(20, t.percentile(40));
        assertEquals(35, t.percentile(50));
        assertEquals(50, t.percentile(100));
        assertEquals(5, t.size());
    }

    @Test @Tag("part3")
    void kthAndCountAtMostWithDuplicates() {
        var t = tree(5, 1, 5, 3, 5, 3, 9);
        long[] sorted = {1, 3, 3, 5, 5, 5, 9};
        for (int r = 1; r <= 7; r++) assertEquals(sorted[r - 1], t.kth(r), "kth " + r);
        assertEquals(0, t.countAtMost(0));
        assertEquals(1, t.countAtMost(1));
        assertEquals(1, t.countAtMost(2));
        assertEquals(3, t.countAtMost(3));
        assertEquals(6, t.countAtMost(5));
        assertEquals(6, t.countAtMost(8));
        assertEquals(7, t.countAtMost(9));
        assertEquals(7, t.countAtMost(Long.MAX_VALUE));
        assertEquals(0, t.countAtMost(Long.MIN_VALUE));
    }

    @Test @Tag("part3") @Tag("edge")
    void orderStatisticsEmptyAndErrors() {
        var t = new OrderStatistics();
        assertEquals(0, t.size());
        assertThrows(NoSuchElementException.class, () -> t.percentile(50));
        assertThrows(IllegalArgumentException.class, () -> t.percentile(0));   // p 先检查，即使是空的
        assertThrows(IllegalArgumentException.class, () -> t.percentile(101));
        assertThrows(IllegalArgumentException.class, () -> t.kth(1));
        assertEquals(0, t.countAtMost(5));
        t.add(7);
        assertThrows(IllegalArgumentException.class, () -> t.kth(0));
        assertThrows(IllegalArgumentException.class, () -> t.kth(2));
        assertEquals(7, t.kth(1));
        assertEquals(7, t.percentile(1));
        assertEquals(7, t.percentile(100));
    }

    @Test @Tag("part3") @Tag("edge")
    void orderStatisticsExtremesAndNegatives() {
        var t = tree(Long.MAX_VALUE, Long.MIN_VALUE, 0, -1, 1, Long.MIN_VALUE);
        assertEquals(Long.MIN_VALUE, t.kth(1));
        assertEquals(Long.MIN_VALUE, t.kth(2));
        assertEquals(-1, t.kth(3));
        assertEquals(0, t.kth(4));
        assertEquals(1, t.kth(5));
        assertEquals(Long.MAX_VALUE, t.kth(6));
        assertEquals(-1, t.percentile(50)); // n = 6：第 3 小
    }

    @Test @Tag("part3")
    void orderStatisticsMatchTheSortingOracle() {
        for (long bound : new long[] {4, 50, 100_000}) {
            var rnd = new Random(bound);
            var t = new OrderStatistics();
            var seen = new ArrayList<Long>();
            for (int i = 0; i < 1500; i++) {
                long x = rnd.nextLong(bound) - bound / 3;
                t.add(x);
                seen.add(x);
                long[] arr = seen.stream().mapToLong(Long::longValue).toArray();
                for (int p : new int[] {1, 10, 25, 50, 75, 90, 99, 100}) {
                    if (i % 37 == 0 || p == 50) assertEquals(Oracle.percentile(arr, p), t.percentile(p), "bound " + bound + " n " + (i + 1) + " p " + p);
                }
                long probe = rnd.nextLong(bound) - bound / 3;
                if (i % 11 == 0) assertEquals(seen.stream().filter(v -> v <= probe).count(), t.countAtMost(probe));
            }
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void sortedInputDoesNotDegenerate() {
        // 升序插入 20 万个：不平衡的二叉搜索树会退化成链表（O(n²) 或栈溢出）
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var t = new OrderStatistics();
            for (int i = 0; i < 200_000; i++) t.add(i);
            assertEquals(99_999, t.percentile(50));
            assertEquals(199_999, t.percentile(100));
            for (int i = 1; i <= 200_000; i++) t.add(-i); // 再来一段降序
            assertEquals(400_000, t.size());
            assertEquals(-200_000, t.kth(1));
            assertEquals(199_999, t.kth(400_000));
        });
    }

    // ---------------------------------------------------------------- 固定 p 的两堆
    @Test @Tag("part3")
    void twoHeapNearestRankExample() {
        long[] stream = {35, 20, 50, 15, 40};
        int[] ps = {5, 30, 40, 50, 100};
        long[] want = {15, 20, 20, 35, 50};
        for (int j = 0; j < ps.length; j++) {
            var h = new TwoHeapPercentile(ps[j]);
            for (long x : stream) h.add(x);
            assertEquals(want[j], h.value(), "p " + ps[j]);
            assertEquals(5, h.size());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void twoHeapEmptyAndArguments() {
        assertThrows(IllegalArgumentException.class, () -> new TwoHeapPercentile(0));
        assertThrows(IllegalArgumentException.class, () -> new TwoHeapPercentile(101));
        var h = new TwoHeapPercentile(90);
        assertThrows(NoSuchElementException.class, h::value);
        h.add(Long.MIN_VALUE);
        assertEquals(Long.MIN_VALUE, h.value());
        h.add(Long.MAX_VALUE);
        assertEquals(Long.MAX_VALUE, h.value()); // n = 2，p = 90：rank = ceil(1.8) = 2
        assertEquals(2, h.size());
    }

    @Test @Tag("part3")
    void p50IsPart1Median() {
        var rnd = new Random(5);
        var h = new TwoHeapPercentile(50);
        var m = new StreamingMedian();
        for (int i = 0; i < 2000; i++) {
            long x = rnd.nextLong(100) - 50;
            h.add(x);
            m.add(x);
            assertEquals(m.median(), h.value());
        }
    }

    @Test @Tag("part3")
    void twoHeapMatchesTheSortingOracleForEveryP() {
        for (int p : new int[] {1, 2, 10, 25, 50, 66, 75, 90, 95, 99, 100}) {
            var rnd = new Random(p);
            var h = new TwoHeapPercentile(p);
            var seen = new ArrayList<Long>();
            for (int i = 0; i < 1200; i++) {
                long x = rnd.nextLong(i % 3 == 0 ? 6 : 100_000) - 3;
                h.add(x);
                seen.add(x);
                assertEquals(Oracle.percentile(seen.stream().mapToLong(Long::longValue).toArray(), p), h.value(), "p " + p + " n " + (i + 1));
            }
        }
    }

    @Test @Tag("part3")
    void bothStructuresAgreeOnTheSameStream() {
        var rnd = new Random(99);
        var tree = new OrderStatistics();
        var h95 = new TwoHeapPercentile(95);
        var h5 = new TwoHeapPercentile(5);
        for (int i = 0; i < 20_000; i++) {
            long x = rnd.nextLong(1000);
            tree.add(x);
            h95.add(x);
            h5.add(x);
            if (i % 101 == 0) {
                assertEquals(tree.percentile(95), h95.value());
                assertEquals(tree.percentile(5), h5.value());
            }
        }
    }
}
