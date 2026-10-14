import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Random;

/**
 * Part 4 的「测量」：同一串更新（ticker 的累计成交量 += qty）喂给七种实现，打印 ns/op 和每条记录占多少字节。
 *   python3 tools/jtest.py main loop/rounds/01_video/hc07_ticker_hash_map --impl reference --cls Bench
 * 注意：这是 micro-benchmark，数字只在「同一台机器、同一次运行里互相比较」才有意义；
 * 想要可发表的数字请用 JMH。这里只做三件事：预热、取最好的一轮、避免死代码消除（结果累加进 sink 并打印）。
 */
public final class Bench {
    static long sink;

    /** 对照实验：和 LongTickerMap 同一算法，唯一区别是 key 和 value 放在两个数组里（分离布局）。 */
    static final class SplitLongMap {
        final long[] keys, vals;
        final int mask, shift;
        SplitLongMap(int capacity) {
            keys = new long[capacity];
            vals = new long[capacity];
            mask = capacity - 1;
            shift = 64 - Integer.numberOfTrailingZeros(capacity);
        }
        void add(long key, long delta) {
            int i = (int) ((key * 0x9E3779B97F4A7C15L) >>> shift);
            while (true) {
                long k = keys[i];
                if (k == key) { vals[i] += delta; return; }
                if (k == 0) { keys[i] = key; vals[i] = delta; return; }
                i = (i + 1) & mask;
            }
        }
    }

    interface Op { void run(int[] picks, int count); }

    static double nsPerOp(Op op, int[] picks, int count) {
        double best = Double.MAX_VALUE;
        for (int round = 0; round < 5; round++) {
            long t0 = System.nanoTime();
            op.run(picks, count);
            best = Math.min(best, (System.nanoTime() - t0) / (double) count);
        }
        return best;
    }

    static long usedHeap() {
        for (int i = 0; i < 4; i++) System.gc();
        var rt = Runtime.getRuntime();
        return rt.totalMemory() - rt.freeMemory();
    }

    public static void main(String[] args) {
        int[] sizes = {8_000, 2_000_000};
        int ops = 20_000_000;
        System.out.println("java " + System.getProperty("java.version") + ", " + Runtime.getRuntime().availableProcessors()
                + " cores, ops per run = " + ops);
        for (int n : sizes) {
            var r = new Random(0);
            var seen = new HashSet<String>();
            var tickers = new ArrayList<String>(n);
            while (tickers.size() < n) {
                int len = 4 + r.nextInt(5);
                var sb = new StringBuilder();
                for (int i = 0; i < len; i++) sb.append((char) ('A' + r.nextInt(26)));
                if (seen.add(sb.toString())) tickers.add(sb.toString());
            }
            String[] names = tickers.toArray(new String[0]);
            long[] keys = new long[n];
            for (int i = 0; i < n; i++) keys[i] = TickerCodec.pack(names[i]);

            for (String mode : List.of("uniform", "skewed")) {
                int[] picks = new int[1 << 20];
                for (int i = 0; i < picks.length; i++)
                    picks[i] = mode.equals("uniform") || r.nextInt(10) == 0 ? r.nextInt(n) : r.nextInt(Math.min(n, 64));
                int mask = picks.length - 1;

                var hm = new HashMap<String, Long>();
                var tm = new TickerMap();
                var lm = new LongTickerMap();
                var sm = new SplitLongMap(Integer.highestOneBit(n * 2 - 1) << 1);
                var fm = new FrozenTickerMap(tickers);
                int[] idx = new int[n];
                for (int i = 0; i < n; i++) idx[i] = fm.indexOf(keys[i]);
                try (var om = new OffHeapTickerMap(n)) {
                    for (int i = 0; i < n; i++) { hm.put(names[i], 0L); tm.put(names[i], 0); lm.put(keys[i], 0); om.put(keys[i], 0); sm.add(keys[i], 0); }
                    System.out.printf("%n== universe %,d symbols, %s access ==%n", n, mode);
                    System.out.printf("%-34s %8.1f ns/op%n", "HashMap<String,Long>.merge",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) hm.merge(names[p[i & mask]], 1L, Long::sum); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "TickerMap.add(String)",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) tm.add(names[p[i & mask]], 1); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "LongTickerMap.add(long)  [interleaved]",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) lm.add(keys[p[i & mask]], 1); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "SplitLongMap.add         [2 arrays]",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) sm.add(keys[p[i & mask]], 1); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "OffHeapTickerMap.add",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) om.add(keys[p[i & mask]], 1); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "FrozenTickerMap.add(long) [perfect]",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) fm.add(keys[p[i & mask]], 1); }, picks, ops));
                    System.out.printf("%-34s %8.1f ns/op%n", "FrozenTickerMap.addAt(idx)  [cached]",
                            nsPerOp((p, c) -> { for (int i = 0; i < c; i++) fm.addAt(idx[p[i & mask]], 1); }, picks, ops));
                    sink += hm.size() + tm.size() + lm.size() + om.size() + fm.getAt(0) + sm.vals[0];
                }
            }

            // 每条记录占多少内存：只在 universe = 2M 时测。用「线程分配字节数」而不是堆差值：
            // 两个 map 都按容量预留（不 resize），所以分配出来的字节 == 常驻字节，数字是精确的。
            if (n == 2_000_000) {
                var mx = (com.sun.management.ThreadMXBean) java.lang.management.ManagementFactory.getThreadMXBean();
                long tid = Thread.currentThread().threadId();
                long b0 = mx.getThreadAllocatedBytes(tid);
                var hm = new HashMap<String, Long>((int) (n / 0.75) + 1);
                for (int i = 0; i < n; i++) hm.put(names[i], (long) i + 1000);
                long hmBytes = mx.getThreadAllocatedBytes(tid) - b0;
                b0 = mx.getThreadAllocatedBytes(tid);
                var lm = new LongTickerMap(n);
                for (int i = 0; i < n; i++) lm.put(keys[i], (long) i + 1000);
                long lmBytes = mx.getThreadAllocatedBytes(tid) - b0;
                int buckets = (n + 3) / 4;
                double fmBytes = (8.0 * n + 8.0 * n + 4.0 * buckets) ;  // SymbolIndex.keys + FrozenTickerMap.values + disp
                System.out.printf("%n== memory at %,d entries (key objects NOT counted: the String[] is shared by all) ==%n", n);
                System.out.printf("HashMap<String,Long> table + Node + Long      : %6.1f B/entry  (allocated while building, presized)%n", hmBytes / (double) n);
                System.out.printf("LongTickerMap (presized, load<=1/2)           : %6.1f B/entry  (allocated while building, presized)%n", lmBytes / (double) n);
                System.out.printf("FrozenTickerMap (keys 8 + values 8 + disp 1)  : %6.1f B/entry  (array sizes; build temporaries are garbage)%n", fmBytes / n);
                sink += hm.size() + lm.size();
            }
        }
        System.out.println("\n(sink=" + sink + ")");
    }
}
