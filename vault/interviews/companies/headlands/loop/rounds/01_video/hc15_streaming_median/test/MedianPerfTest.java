import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.management.ManagementFactory;
import java.time.Duration;
import java.util.Arrays;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：100 万次操作。每个结构的最终答案都和独立的结果交叉检查。 */
class MedianPerfTest {
    static final int N = 1_000_000;
    static final int BAND = 1 << 20;

    /** 以 BAND/2 为中心的钟形分布，落在 0..BAND-1。 */
    static long[] ticks(long seed) {
        var rnd = new Random(seed);
        long[] out = new long[N];
        for (int i = 0; i < N; i++) out[i] = Math.floorMod((long) (BAND / 2 + rnd.nextGaussian() * BAND / 8), BAND);
        return out;
    }

    static final long[] DATA = ticks(0);

    @Test @Tag("part4") @Tag("perf")
    void histogramMillionAddsAndQueriesWithoutAllocating() {
        var h = new TickHistogram(BAND);
        var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
        long[] allocated = new long[1];
        long sum = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            long tid = Thread.currentThread().threadId();
            for (int i = 0; i < 200_000; i++) h.add(DATA[i]);   // 预热
            long before = mx.getThreadAllocatedBytes(tid);
            long acc = 0;
            for (int i = 200_000; i < N; i++) {
                h.add(DATA[i]);
                acc += h.percentile(1 + i % 100);
            }
            allocated[0] = mx.getThreadAllocatedBytes(tid) - before;
            return acc;
        });
        assertTrue(sum > 0);
        assertEquals(N, h.count());
        long[] sorted = DATA.clone();
        Arrays.sort(sorted);
        assertEquals(sorted[N / 2 - 1], h.median());
        assertEquals(sorted[(int) (0.95 * N) - 1], h.percentile(95));
        assertTrue(allocated[0] < 256 * 1024, "allocated " + allocated[0] + " bytes for 800k operations");
    }

    @Test @Tag("part4") @Tag("perf")
    void twoHeapMedianMillionAdds() {
        var m = new StreamingMedian();
        long last = assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            long acc = 0;
            for (long x : DATA) {
                m.add(x);
                acc ^= m.median();
            }
            return acc;
        });
        assertTrue(last >= 0);
        long[] sorted = DATA.clone();
        Arrays.sort(sorted);
        assertEquals(sorted[N / 2 - 1], m.median());
        assertEquals(N, m.size());
    }

    @Test @Tag("part4") @Tag("perf")
    void windowMedianMillionAddsWithTenThousandWindow() {
        int k = 10_000;
        var w = new WindowMedian(k);
        assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            for (long x : DATA) {
                w.add(x);
                w.median();
            }
        });
        long[] tail = Arrays.copyOfRange(DATA, N - k, N);
        assertEquals(Oracle.lowerMedian(tail), w.median());
        assertEquals(k, w.size());
        assertTrue(w.retained() <= 4 * k, "retained " + w.retained());
    }

    @Test @Tag("part4") @Tag("perf")
    void fixedPercentileHeapsMillionAdds() {
        var h = new TwoHeapPercentile(95);
        assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            for (long x : DATA) {
                h.add(x);
                h.value();
            }
        });
        long[] sorted = DATA.clone();
        Arrays.sort(sorted);
        assertEquals(sorted[(int) (0.95 * N) - 1], h.value());
    }

    @Test @Tag("part4") @Tag("perf")
    void orderStatisticsTreeMillionAddsAndQueries() {
        var t = new OrderStatistics();
        assertTimeoutPreemptively(Duration.ofSeconds(4), () -> {
            long acc = 0;
            for (int i = 0; i < N; i++) {
                t.add(DATA[i]);
                acc += t.percentile(1 + i % 100);
            }
            assertTrue(acc > 0);
        });
        long[] sorted = DATA.clone();
        Arrays.sort(sorted);
        for (int p : new int[] {1, 50, 95, 100}) assertEquals(sorted[(int) Math.ceilDiv((long) p * N, 100L) - 1], t.percentile(p), "p " + p);
    }
}
