/** volatile gives visibility, not atomicity: count++ on a volatile loses updates; synchronized / Atomic don't. */
public class K22VolatileCounter {
    static volatile int vol;
    static int guarded; static final Object L = new Object();
    static final java.util.concurrent.atomic.AtomicInteger AT = new java.util.concurrent.atomic.AtomicInteger();

    static void run(String name, Runnable body) throws Exception {
        Thread[] ts = new Thread[4];
        for (int i = 0; i < ts.length; i++) { ts[i] = new Thread(body); ts[i].start(); }
        for (Thread t : ts) t.join();
    }
    public static void main(String[] a) throws Exception {
        int per = 1_000_000;
        run("volatile++", () -> { for (int i = 0; i < per; i++) vol++; });
        run("synchronized", () -> { for (int i = 0; i < per; i++) synchronized (L) { guarded++; } });
        run("AtomicInteger", () -> { for (int i = 0; i < per; i++) AT.incrementAndGet(); });
        System.out.printf("expected 4,000,000 | volatile++ %,d | synchronized %,d | AtomicInteger %,d%n", vol, guarded, AT.get());
    }
}
