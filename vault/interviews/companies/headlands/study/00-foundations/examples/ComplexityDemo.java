import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

/**
 * Companion to complexity.md: counts steps instead of trusting formulas, then measures real time.
 * Run:  javac --release 21 --enable-preview ComplexityDemo.java && java --enable-preview ComplexityDemo
 */
public class ComplexityDemo {
    static volatile long sink;

    public static void main(String[] args) {
        searchSteps();
        growthCopies();
        throughput();
        quadratic();
    }

    // 1. Count comparisons: linear search vs binary search on a sorted array ---------------------
    static void searchSteps() {
        System.out.println("== 1. comparisons needed to find the LAST element (worst case) ==");
        System.out.printf("%12s %14s %14s%n", "n", "linear", "binary");
        for (int n : new int[]{10, 1_000, 1_000_000, 100_000_000}) {
            long lin = n;                                   // linear search must look at all n
            long bin = 0;
            int lo = 0, hi = n - 1, target = n - 1;         // binary search on virtual array [0..n-1], value == index
            while (lo <= hi) {
                bin++;
                int mid = (lo + hi) >>> 1;
                if (mid == target) break;
                if (mid < target) lo = mid + 1; else hi = mid - 1;
            }
            System.out.printf("%12d %14d %14d%n", n, lin, bin);
        }
    }

    // 2. Amortized analysis by experiment: total element copies while appending n items -----------
    static void growthCopies() {
        System.out.println("\n== 2. total elements copied while appending n = 1,000,000 items ==");
        int n = 1_000_000;
        System.out.printf("%-26s %14s %12s%n", "growth rule", "total copies", "copies / n");
        System.out.printf("%-26s %14d %12.2f%n", "x1.5 (java.util.ArrayList)", copies(n, 1.5, 0), copies(n, 1.5, 0) / (double) n);
        System.out.printf("%-26s %14d %12.2f%n", "x2.0", copies(n, 2.0, 0), copies(n, 2.0, 0) / (double) n);
        int small = 100_000;                                // additive growth is quadratic, so use smaller n
        System.out.printf("%-26s %14d %12.2f   (n = %d)%n", "+10 each time", copies(small, 0, 10), copies(small, 0, 10) / (double) small, small);
    }

    /** Simulate append-only array growth; return total number of elements copied during resizes. */
    static long copies(int n, double factor, int add) {
        long cap = 10, size = 0, copied = 0;
        for (int i = 0; i < n; i++) {
            if (size == cap) {                              // full: allocate a bigger array and copy `size` elements
                copied += size;
                cap = add > 0 ? cap + add : (long) (cap * factor);
                if (cap == size) cap++;
            }
            size++;
        }
        return copied;
    }

    // 3. How many "operations" per second is realistic? --------------------------------------------
    static void throughput() {
        System.out.println("\n== 3. measured cost per operation on this machine (after warm-up) ==");
        int n = 1_000_000;
        // (a) a loop whose iterations depend on each other: roughly "one simple op per cycle"
        for (int w = 0; w < 5; w++) dependentChain(100_000_000);
        long t0 = System.nanoTime();
        dependentChain(1_000_000_000);
        double sec = (System.nanoTime() - t0) / 1e9;
        System.out.printf("dependent multiply-add loop     : %.2f s for 1e9 iterations -> %.1e iters/s%n", sec, 1e9 / sec);

        // (b) HashMap and TreeMap: the O(1) / O(log n) in the textbook is not 1 ns
        Random rnd = new Random(1);
        int[] keys = new int[n];
        for (int i = 0; i < n; i++) keys[i] = rnd.nextInt();
        for (int rep = 0; rep < 3; rep++) {                 // repeat to let the JIT settle, print the last one
            Map<Integer, Integer> hm = new HashMap<>();
            long a = System.nanoTime();
            for (int k : keys) hm.put(k, k);
            long b = System.nanoTime();
            long s = 0;
            for (int k : keys) s += hm.get(k);
            long c = System.nanoTime();
            Map<Integer, Integer> tm = new TreeMap<>();
            for (int k : keys) tm.put(k, k);
            long d = System.nanoTime();
            for (int k : keys) s += tm.get(k);
            long e = System.nanoTime();
            sink = s;
            if (rep == 2) {
                System.out.printf("HashMap<Integer,Integer> put %.0f ns, get %.0f ns  (1e6 random keys)%n", (b - a) / (double) n, (c - b) / (double) n);
                System.out.printf("TreeMap<Integer,Integer> put %.0f ns, get %.0f ns  (1e6 random keys)%n", (d - c) / (double) n, (e - d) / (double) n);
            }
        }
    }

    static void dependentChain(int iters) {
        long x = 1;
        for (int i = 0; i < iters; i++) x = x * 31 + i;
        sink = x;
    }

    // 4. O(n^2) in practice -------------------------------------------------------------------------
    static void quadratic() {
        System.out.println("\n== 4. counting pairs (i<j) with a[i]+a[j] even: O(n^2) ==");
        Random rnd = new Random(2);
        for (int n : new int[]{2_000, 20_000, 100_000}) {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(1000);
            long t0 = System.nanoTime();
            long cnt = 0;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                    if (((a[i] + a[j]) & 1) == 0) cnt++;
            double sec = (System.nanoTime() - t0) / 1e9;
            double pairs = n * (n - 1.0) / 2;
            System.out.printf("n=%7d: %.2e pairs, %7.3f s -> %.2e pairs/s (cnt=%d)%n", n, pairs, sec, pairs / sec, cnt);
        }
    }
}
