import java.util.*;

/** Memory layout: long[] vs Long[] in allocation order vs Long[] after shuffling (pointer chasing). */
public class K21Locality {
    static volatile long sink;
    public static void main(String[] a) {
        int n = 12_000_000;
        long[] prim = new long[n]; Long[] boxedSeq = new Long[n]; Long[] boxedShuf = new Long[n];
        for (int i = 0; i < n; i++) { prim[i] = i; boxedSeq[i] = (long) i + 1000; }
        // shuffle order of the reference array only: objects stay where they were allocated
        List<Long> tmp = new ArrayList<>(Arrays.asList(boxedSeq)); Collections.shuffle(tmp, new Random(1)); boxedShuf = tmp.toArray(new Long[0]);
        for (int r = 0; r < 5; r++) {
            long t0 = System.nanoTime(); long s = 0; for (long v : prim) s += v; long t1 = System.nanoTime();
            long s2 = 0; for (Long v : boxedSeq) s2 += v; long t2 = System.nanoTime();
            long s3 = 0; for (Long v : boxedShuf) s3 += v; long t3 = System.nanoTime();
            sink = s + s2 + s3;
            if (r >= 2) System.out.printf("sum of %,d: long[] %4d ms | Long[] (alloc order) %4d ms | Long[] (shuffled) %4d ms%n", n, (t1 - t0) / 1_000_000, (t2 - t1) / 1_000_000, (t3 - t2) / 1_000_000);
        }
    }
}
