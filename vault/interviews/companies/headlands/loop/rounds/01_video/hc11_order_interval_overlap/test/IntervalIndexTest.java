import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** hc11 Part 4：大坐标范围 —— 坐标压缩 + 懒标记线段树。 */
class IntervalIndexTest {

    static int bruteLive(long[][] iv, long t) {
        int c = 0;
        for (long[] x : iv) if (x[0] <= t && t < x[1]) c++;
        return c;
    }

    static int bruteMaxIn(long[][] iv, long from, long to) {
        int best = 0;
        for (long t = from; t < to; t++) best = Math.max(best, bruteLive(iv, t));
        return best;
    }

    @Test @Tag("part4")
    void problemSample() {
        // 坐标是 10^15 量级：数组下标开不出来，必须压缩
        long u = 1_000_000_000_000_000L;
        var iv = new long[][]{{1 * u, 5 * u}, {2 * u, 6 * u}, {4 * u, 8 * u}};
        var idx = IntervalIndex.of(iv);
        assertEquals(3, idx.max());
        assertEquals(6, idx.coordinateCount());
        assertEquals(5, idx.segmentCount());
        assertEquals(0, idx.liveAt(0));
        assertEquals(1, idx.liveAt(1 * u));
        assertEquals(2, idx.liveAt(2 * u + 12_345));
        assertEquals(3, idx.liveAt(4 * u));
        assertEquals(2, idx.liveAt(5 * u));    // [1,5) 在 5u 结束
        assertEquals(1, idx.liveAt(8 * u - 1));
        assertEquals(0, idx.liveAt(8 * u));
        assertEquals(2, idx.maxIn(5 * u, 100 * u));
        assertEquals(3, idx.maxIn(0, 5 * u));
        assertEquals(1, idx.maxIn(0, 2 * u));
    }

    @Test @Tag("part4") @Tag("edge")
    void maxIsTheSameAsTheSweepLine() {
        var iv = new long[][]{{0, 10}, {2, 3}, {2, 3}, {5, 7}};
        assertEquals(OrderIntervals.maxOverlap(iv), IntervalIndex.maxOverlap(iv));
        var touching = new long[][]{{1, 3}, {3, 5}};
        assertEquals(1, IntervalIndex.maxOverlap(touching));   // 半开：交接不重叠
    }

    @Test @Tag("part4") @Tag("edge")
    void degenerateIndexes() {
        var none = new IntervalIndex(new long[0]);
        assertEquals(0, none.max());
        assertEquals(0, none.liveAt(5));
        assertEquals(0, none.maxIn(0, 100));
        var one = new IntervalIndex(new long[]{7, 7, 7});
        assertEquals(1, one.coordinateCount());
        assertEquals(0, one.segmentCount());
        one.add(7, 7);   // 空区间
        assertEquals(0, one.max());
        assertEquals(0, IntervalIndex.maxOverlap(new long[0][]));
        assertEquals(0, IntervalIndex.maxOverlap(new long[][]{{4, 4}}));
    }

    @Test @Tag("part4") @Tag("edge")
    void coordinatesNearLongMaxValue() {
        long max = Long.MAX_VALUE;
        var iv = new long[][]{{0, max}, {max - 2, max}, {max - 1, max}, {max - 5, max - 1}};
        var idx = IntervalIndex.of(iv);
        assertEquals(3, idx.max());
        assertEquals(3, idx.liveAt(max - 2));
        assertEquals(3, idx.liveAt(max - 1));
        assertEquals(0, idx.liveAt(max));          // 右端不含
        assertEquals(2, idx.liveAt(max - 5));
        assertEquals(1, idx.liveAt(max - 6));
        assertEquals(3, idx.maxIn(max - 10, max));
        assertEquals(1, idx.maxIn(1, max - 5));   // to = max-5 不含
    }

    @Test @Tag("part4") @Tag("edge")
    void maxInRangeBoundaries() {
        var idx = IntervalIndex.of(new long[][]{{10, 20}, {15, 30}});
        assertEquals(0, idx.maxIn(0, 10));         // to 不含
        assertEquals(1, idx.maxIn(0, 11));
        assertEquals(2, idx.maxIn(19, 21));        // 19 在 [15,20) 里
        assertEquals(1, idx.maxIn(20, 21));        // 20 起 [10,20) 已结束
        assertEquals(0, idx.maxIn(30, 99));
        assertEquals(0, idx.maxIn(12, 12));        // 空范围
        assertEquals(2, idx.maxIn(0, 1_000));      // 范围伸出两端：外面是 0，最大值看里面
    }

    @Test @Tag("part4") @Tag("edge")
    void addAndRemoveAreInverse() {
        var idx = new IntervalIndex(new long[]{0, 5, 10, 20, 100});
        idx.add(0, 10);
        idx.add(5, 20);
        idx.add(5, 100);
        assertEquals(3, idx.max());
        assertEquals(3, idx.liveAt(7));
        idx.remove(5, 20);
        assertEquals(2, idx.max());
        assertEquals(2, idx.liveAt(7));
        assertEquals(1, idx.liveAt(30));
        idx.remove(0, 10);
        idx.remove(5, 100);
        assertEquals(0, idx.max());
        for (long t : new long[]{0, 5, 7, 10, 50, 100}) assertEquals(0, idx.liveAt(t));
    }

    @Test @Tag("part4") @Tag("edge")
    void invalidArguments() {
        var idx = new IntervalIndex(new long[]{1, 5, 9});
        assertThrows(IllegalArgumentException.class, () -> idx.add(1, 6));      // 6 不是已知端点
        assertThrows(IllegalArgumentException.class, () -> idx.add(2, 5));
        assertThrows(IllegalArgumentException.class, () -> idx.add(5, 1));      // end < start
        assertThrows(IllegalArgumentException.class, () -> idx.maxIn(9, 1));
        assertThrows(NullPointerException.class, () -> new IntervalIndex(null));
        assertThrows(IllegalArgumentException.class, () -> IntervalIndex.of(new long[][]{{1, 2, 3}}));
    }

    @ParameterizedTest @Tag("part4")
    @ValueSource(longs = {71, 72, 73, 74, 75, 76, 77, 78})
    void randomAgainstBruteForce(long seed) {
        var rnd = new Random(seed);
        int n = 1 + rnd.nextInt(40);
        var iv = new long[n][];
        for (int i = 0; i < n; i++) {
            long a = rnd.nextInt(50);
            iv[i] = new long[]{a, a + rnd.nextInt(20)};
        }
        var idx = IntervalIndex.of(iv);
        assertEquals(bruteMaxIn(iv, 0, 80), idx.max(), "max, seed " + seed);
        assertEquals(OrderIntervals.maxOverlap(iv), idx.max());
        for (long t = -2; t < 75; t++) assertEquals(bruteLive(iv, t), idx.liveAt(t), "liveAt " + t + ", seed " + seed);
        for (int q = 0; q < 300; q++) {
            long from = rnd.nextInt(80) - 5;
            long to = from + rnd.nextInt(30);
            assertEquals(bruteMaxIn(iv, from, to), idx.maxIn(from, to), "maxIn [" + from + "," + to + "), seed " + seed);
        }
    }

    @ParameterizedTest @Tag("part4")
    @ValueSource(longs = {81, 82, 83})
    void dynamicAddRemoveAgainstRecount(long seed) {
        var rnd = new Random(seed);
        long[] coords = new long[30];
        for (int i = 0; i < coords.length; i++) coords[i] = rnd.nextInt(60);
        var idx = new IntervalIndex(coords);
        var active = new ArrayList<long[]>();
        for (int step = 0; step < 400; step++) {
            if (active.isEmpty() || rnd.nextInt(3) != 0) {
                long a = coords[rnd.nextInt(coords.length)];
                long b = coords[rnd.nextInt(coords.length)];
                long[] iv = {Math.min(a, b), Math.max(a, b)};
                idx.add(iv[0], iv[1]);
                active.add(iv);
            } else {
                var iv = active.remove(rnd.nextInt(active.size()));
                idx.remove(iv[0], iv[1]);
            }
            var arr = active.toArray(long[][]::new);
            assertEquals(bruteMaxIn(arr, 0, 61), idx.max(), "step " + step);
            long t = rnd.nextInt(61);
            assertEquals(bruteLive(arr, t), idx.liveAt(t), "step " + step + " t " + t);
        }
    }

    @Test @Tag("part4") @Tag("perf")
    void threeHundredThousandHugeIntervalsAndQueriesUnderTwoSeconds() {
        int n = 300_000;
        var rnd = new Random(0);
        long range = 1_000_000_000_000_000_000L;   // 10^18
        var iv = new long[n][];
        for (int i = 0; i < n; i++) {
            long a = (rnd.nextLong() >>> 1) % range;
            long len = 1 + (rnd.nextLong() >>> 1) % (range / 1_000);
            iv[i] = new long[]{a, a + len};
        }
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var idx = IntervalIndex.of(iv);
            assertEquals(OrderIntervals.maxOverlap(iv), idx.max());
            int best = 0;
            for (int q = 0; q < 100_000; q++) {
                long from = (rnd.nextLong() >>> 1) % range;
                best = Math.max(best, idx.maxIn(from, from + range / 100));
            }
            assertTrue(best >= 1);
        });
    }
}
