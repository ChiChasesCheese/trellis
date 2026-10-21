import java.lang.management.ManagementFactory;

/** Exact bytes allocated per construct (HotSpot, 64-bit, compressed oops), measured, not remembered. */
public class K03ObjectSize {
    static final com.sun.management.ThreadMXBean TM =
        (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
    static long alloc() { return TM.getThreadAllocatedBytes(Thread.currentThread().threadId()); }
    static volatile Object sink;
    record P2(int x, int y) {}
    record P3(long a, long b, long c) {}
    static class Empty {}

    interface Make { Object get(); }
    static void m(String name, Make mk) {
        for (int i = 0; i < 20000; i++) sink = mk.get();   // warm
        long a = alloc();
        for (int i = 0; i < 1000; i++) sink = mk.get();
        long b = alloc();
        System.out.printf("%-34s %5d bytes%n", name, (b - a) / 1000);
    }
    public static void main(String[] x) {
        m("new Object()", Object::new);
        m("new Empty()", Empty::new);
        m("new P2(int,int)", () -> new P2(1, 2));
        m("new P3(long,long,long)", () -> new P3(1, 2, 3));
        m("Integer.valueOf(1000)  (boxed)", () -> Integer.valueOf(1000));
        m("new int[0]", () -> new int[0]);
        m("new int[10]", () -> new int[10]);
        m("new long[10]", () -> new long[10]);
        m("new Integer[10]  (refs only)", () -> new Integer[10]);
        m("\"中\".repeat(1000)  (UTF16)", () -> "中".repeat(1000));
        m("\"a\".repeat(1000)   (LATIN1)", () -> "a".repeat(1000));
    }
}
