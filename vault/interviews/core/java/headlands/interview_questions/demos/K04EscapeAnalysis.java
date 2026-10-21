import java.lang.management.ManagementFactory;

/** Escape analysis: same code, allocation on/off. Run twice: default, and -XX:-DoEscapeAnalysis. */
public class K04EscapeAnalysis {
    static final com.sun.management.ThreadMXBean TM =
        (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    static long alloc() { return TM.getThreadAllocatedBytes(Thread.currentThread().threadId()); }
    record Point(long x, long y) { Point plus(Point o) { return new Point(x + o.x, y + o.y); } }
    static long dist(long i) {                       // Points never leave this method (or the inlined call chain)
        Point p = new Point(i, i + 1).plus(new Point(2, 3));
        return p.x() + p.y();
    }
    public static void main(String[] a) {
        long s = 0;
        for (int w = 0; w < 5; w++) {
            long a0 = alloc(), t0 = System.nanoTime();
            for (long i = 0; i < 50_000_000L; i++) s += dist(i);
            long t1 = System.nanoTime(), a1 = alloc();
            System.out.printf("round %d: %4d ms, allocated %,15d bytes%n", w, (t1 - t0) / 1_000_000, a1 - a0);
        }
        System.out.println("(checksum " + s + ")");
    }
}
