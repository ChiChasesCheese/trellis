import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.concurrent.locks.*;

/** Lock vs CAS vs striped counter under contention (rough timing, JMH it is not). */
public class K08Counters {
    static long plain; static final Object L = new Object();
    static final AtomicLong AL = new AtomicLong(); static final LongAdder LA = new LongAdder();
    static final ReentrantLock RL = new ReentrantLock(); static long guarded;

    interface Body { void run(int n); }
    static long time(int threads, int per, Body b) throws Exception {
        ExecutorService ex = Executors.newFixedThreadPool(threads);
        CountDownLatch go = new CountDownLatch(1); var fs = new java.util.ArrayList<Future<?>>();
        for (int t = 0; t < threads; t++) fs.add(ex.submit(() -> { go.await(); b.run(per); return null; }));
        long t0 = System.nanoTime(); go.countDown(); for (var f : fs) f.get(); long ns = System.nanoTime() - t0; ex.shutdown(); return ns / 1_000_000;
    }
    public static void main(String[] x) throws Exception {
        int per = 5_000_000;
        for (int threads : new int[]{1, 4, 8}) {
            for (int rep = 0; rep < 2; rep++) {
                long sync = time(threads, per, n -> { for (int i = 0; i < n; i++) synchronized (L) { guarded++; } });
                long rl = time(threads, per, n -> { for (int i = 0; i < n; i++) { RL.lock(); try { guarded++; } finally { RL.unlock(); } } });
                long at = time(threads, per, n -> { for (int i = 0; i < n; i++) AL.incrementAndGet(); });
                long ad = time(threads, per, n -> { for (int i = 0; i < n; i++) LA.increment(); });
                if (rep == 1) System.out.printf("threads=%d  synchronized %5d ms | ReentrantLock %5d ms | AtomicLong %5d ms | LongAdder %5d ms%n", threads, sync, rl, at, ad);
            }
        }
        System.out.println("AtomicLong total " + AL.get() + " LongAdder total " + LA.sum() + " (each = threads*per summed over reps)");
    }
}
