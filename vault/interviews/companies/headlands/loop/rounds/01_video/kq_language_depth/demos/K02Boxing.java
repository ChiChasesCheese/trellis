import java.lang.management.ManagementFactory;
import java.util.*;

/** Boxing: the == trap, the cache, and what it costs in allocation and time. */
public class K02Boxing {
    static final com.sun.management.ThreadMXBean TM =
        (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    static long alloc() { return TM.getThreadAllocatedBytes(Thread.currentThread().threadId()); }

    public static void main(String[] a) {
        Integer a1 = 127, a2 = 127, b1 = 128, b2 = 128;
        System.out.println("127 == 127 (boxed): " + (a1 == a2));
        System.out.println("128 == 128 (boxed): " + (b1 == b2) + "   equals: " + b1.equals(b2));
        Integer n = null;
        try { int x = n; } catch (NullPointerException e) { System.out.println("unboxing null -> NPE"); }

        int N = 20_000_000;
        for (int round = 0; round < 3; round++) {
            long a0 = alloc(), t0 = System.nanoTime();
            long s = 0; for (int i = 0; i < N; i++) s += i;
            long t1 = System.nanoTime(), a1b = alloc();
            Long boxed = 0L; for (int i = 0; i < N; i++) boxed += i;     // boxed += : unbox, add, box
            long t2 = System.nanoTime(), a2b = alloc();
            System.out.printf("round %d: long sum %4d ms, alloc %,12d B | Long sum %4d ms, alloc %,12d B%n",
                round, (t1 - t0) / 1_000_000, a1b - a0, (t2 - t1) / 1_000_000, a2b - a1b);
            if (s != boxed) throw new AssertionError();
        }
        // memory per element
        long m0 = alloc(); int[] p = new int[1_000_000]; long m1 = alloc();
        List<Integer> l = new ArrayList<>(1_000_000);
        for (int i = 0; i < 1_000_000; i++) l.add(i + 1000);                  // beyond the cache
        long m2 = alloc();
        System.out.printf("int[1M]: %,d B   ArrayList<Integer>(1M): %,d B (incl. 1M Integer objects)%n", m1 - m0, m2 - m1);
    }
}
