import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicLongArray;

/**
 * Micro-benchmarks that show the memory hierarchy at work.
 * NOT a rigorous benchmark (use JMH for that): warm-up + best-of-N, single JVM, no pinning.
 * Run:  javac --release 21 --enable-preview CacheDemo.java && java --enable-preview CacheDemo
 */
public class CacheDemo {
    static volatile long sink; // defeats dead-code elimination

    static long usedHeap() {
        System.gc();
        return Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
    }

    static double bestMs(int reps, Runnable r) {
        double best = Double.MAX_VALUE;
        for (int i = 0; i < reps; i++) {
            long t0 = System.nanoTime();
            r.run();
            best = Math.min(best, (System.nanoTime() - t0) / 1e6);
        }
        return best;
    }

    public static void main(String[] args) throws Exception {
        System.out.println("JVM " + System.getProperty("java.version") + " on " + System.getProperty("os.name")
                + " " + System.getProperty("os.arch") + ", cpus=" + Runtime.getRuntime().availableProcessors());
        sumArrays();
        stride();
        matrix();
        latencyByWorkingSet();
        branchPrediction();
        aosVsSoa();
        falseSharing();
    }

    // 1. long[] vs ArrayList<Long> ------------------------------------------------------------
    static void sumArrays() {
        System.out.println("\n== 1. sum of 10M longs ==");
        int n = 10_000_000;
        long m0 = usedHeap();
        long[] prim = new long[n];
        for (int i = 0; i < n; i++) prim[i] = i;
        long m1 = usedHeap();
        List<Long> boxed = new ArrayList<>(n);
        for (int i = 0; i < n; i++) boxed.add((long) i + 1000);   // objects allocated back to back (+1000: skip the Long cache)
        long m2 = usedHeap();
        System.out.printf("heap per element: long[] %.1f B, ArrayList<Long> %.1f B%n", (m1 - m0) / (double) n, (m2 - m1) / (double) n);
        List<Long> shuffled = new ArrayList<>(boxed);
        Collections.shuffle(shuffled, new Random(1));              // same objects, random visiting order

        double a = bestMs(7, () -> { long s = 0; for (long v : prim) s += v; sink = s; });
        double b = bestMs(7, () -> { long s = 0; for (long v : boxed) s += v; sink = s; });
        double c = bestMs(7, () -> { long s = 0; for (long v : shuffled) s += v; sink = s; });
        System.out.printf("long[]                         : %7.2f ms  (%.2f ns/elem)%n", a, a * 1e6 / n);
        System.out.printf("ArrayList<Long> (allocation order): %7.2f ms  (%.2f ns/elem)%n", b, b * 1e6 / n);
        System.out.printf("ArrayList<Long> (shuffled)     : %7.2f ms  (%.2f ns/elem)%n", c, c * 1e6 / n);
    }

    // 2. stride: touching one int per k ints ----------------------------------------------------
    static void stride() {
        System.out.println("\n== 2. stride over a 256 MB int[] (same total bytes read per pass, fewer elements as stride grows) ==");
        int n = 64 * 1024 * 1024;
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = i;
        for (int k : new int[]{1, 2, 4, 8, 16, 32, 64, 128}) {
            final int stride = k;
            double ms = bestMs(5, () -> { long s = 0; for (int i = 0; i < n; i += stride) s += a[i]; sink = s; });
            System.out.printf("stride %3d ints (%4d B): %7.2f ms for %9d elements -> %.2f ns/elem%n",
                    k, k * 4, ms, n / k, ms * 1e6 / (n / k));
        }
    }

    // 3. row-major vs column-major ------------------------------------------------------------
    static void matrix() {
        System.out.println("\n== 3. 4096x4096 int matrix, row-major vs column-major ==");
        int n = 4096;
        int[][] m = new int[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) m[i][j] = i ^ j;
        double row = bestMs(5, () -> { long s = 0; for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) s += m[i][j]; sink = s; });
        double col = bestMs(5, () -> { long s = 0; for (int j = 0; j < n; j++) for (int i = 0; i < n; i++) s += m[i][j]; sink = s; });
        System.out.printf("row-major   : %7.2f ms%n", row);
        System.out.printf("column-major: %7.2f ms  (%.1fx slower)%n", col, col / row);
    }

    // 4. dependent-load latency by working-set size ------------------------------------------------
    static void latencyByWorkingSet() {
        System.out.println("\n== 4. pointer chasing (each load depends on previous): ns per load ==");
        Random rnd = new Random(42);
        for (int kb = 4; kb <= 256 * 1024; kb *= 4) {
            int n = kb * 1024 / 4;                 // number of ints
            int[] next = new int[n];
            // build a random single cycle (Sattolo) so the CPU cannot guess the next address
            int[] perm = new int[n];
            for (int i = 0; i < n; i++) perm[i] = i;
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i); int t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
            for (int i = 0; i < n; i++) next[perm[i]] = perm[(i + 1) % n];
            int steps = 20_000_000;
            double ms = bestMs(4, () -> { int p = 0; for (int i = 0; i < steps; i++) p = next[p]; sink = p; });
            System.out.printf("working set %8d KB: %6.2f ns/load%n", kb, ms * 1e6 / steps);
        }
    }

    // 5. branch prediction -------------------------------------------------------------------------
    static void branchPrediction() {
        System.out.println("\n== 5. branch prediction: same data, sorted vs random order ==");
        int n = 1 << 22;
        int[] data = new Random(7).ints(n, 0, 256).toArray();
        int[] sorted = data.clone();
        java.util.Arrays.sort(sorted);
        int[] out = new int[n];
        for (int[] arr : new int[][]{data, sorted}) {
            double ms = bestMs(15, () -> {
                int k = 0;
                for (int rep = 0; rep < 20; rep++)
                    for (int i = 0; i < n; i++) {
                        int v = arr[i];
                        if (v >= 128) out[k++ & (n - 1)] = v;   // data-dependent branch with a side effect
                    }
                sink = k;
            });
            System.out.printf("%-8s: %7.2f ms%n", arr == data ? "random" : "sorted", ms);
        }
    }

    // 5b. array of structs vs struct of arrays ------------------------------------------------------
    static final class Order { long id; long price; int qty; boolean buy; }

    static void aosVsSoa() {
        System.out.println("\n== 5b. 5M orders: total qty of orders with price >= 500 (reads 2 of 4 fields) ==");
        int n = 5_000_000;
        Random rnd = new Random(11);
        Order[] aos = new Order[n];
        long[] id = new long[n]; long[] price = new long[n]; int[] qty = new int[n];
        for (int i = 0; i < n; i++) {
            Order o = new Order();
            o.id = i; o.price = rnd.nextInt(1000); o.qty = rnd.nextInt(100); o.buy = (i & 1) == 0;
            aos[i] = o; id[i] = o.id; price[i] = o.price; qty[i] = o.qty;
        }
        double a = bestMs(7, () -> { long s = 0; for (Order o : aos) if (o.price >= 500) s += o.qty; sink = s; });
        // same objects, but the array is visited in random order (what a long-lived, churned heap looks like)
        Order[] shuffled = aos.clone();
        List<Order> tmp = new ArrayList<>(List.of(shuffled));
        Collections.shuffle(tmp, new Random(3));
        tmp.toArray(shuffled);
        double b = bestMs(7, () -> { long s = 0; for (Order o : shuffled) if (o.price >= 500) s += o.qty; sink = s; });
        double c = bestMs(7, () -> { long s = 0; for (int i = 0; i < n; i++) if (price[i] >= 500) s += qty[i]; sink = s; });
        System.out.printf("array of objects (allocation order): %7.2f ms%n", a);
        System.out.printf("array of objects (shuffled)        : %7.2f ms%n", b);
        System.out.printf("parallel arrays (struct of arrays) : %7.2f ms%n", c);
    }

    // 6. false sharing -----------------------------------------------------------------------------
    static void falseSharing() throws Exception {
        System.out.println("\n== 6. false sharing: two threads each atomically increment their OWN counter, 50M times ==");
        int iters = 50_000_000;
        for (int gap : new int[]{1, 16, 64}) {   // distance in longs between the two counters (8, 128, 512 bytes)
            AtomicLongArray arr = new AtomicLongArray(gap + 1);
            double best = Double.MAX_VALUE;
            for (int rep = 0; rep < 4; rep++) {
                Thread t0 = new Thread(() -> { for (int i = 0; i < iters; i++) arr.incrementAndGet(0); });
                Thread t1 = new Thread(() -> { for (int i = 0; i < iters; i++) arr.incrementAndGet(gap); });
                long s = System.nanoTime();
                t0.start(); t1.start(); t0.join(); t1.join();
                best = Math.min(best, (System.nanoTime() - s) / 1e6);
            }
            System.out.printf("counters %3d bytes apart: %7.1f ms%n", gap * 8, best);
        }
    }
}
