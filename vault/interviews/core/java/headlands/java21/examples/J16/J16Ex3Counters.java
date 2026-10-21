import java.util.concurrent.atomic.*;
import java.util.function.*;

/**
 * J16 例 3：四种计数器在不同线程数下的表现。
 *   int++ 不加保护（丢更新） / synchronized / AtomicLong(CAS) / LongAdder(分散热点)
 * 注意：这是粗糙的计时，不是 JMH 基准；只用来看趋势，不要当作性能数字引用。
 */
public class J16Ex3Counters {
    static int plain;
    static long locked;
    static final Object LOCK = new Object();
    static final AtomicLong atomic = new AtomicLong();
    static final LongAdder adder = new LongAdder();

    static long runThreads(int threads, int per, Runnable op) throws Exception {
        Thread[] ts = new Thread[threads];
        long t0 = System.nanoTime();
        for (int i = 0; i < threads; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < per; k++) op.run(); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    static void reset() { plain = 0; locked = 0; atomic.set(0); adder.reset(); }

    public static void main(String[] args) throws Exception {
        int per = 2_000_000;
        // 预热
        runThreads(2, 200_000, () -> atomic.incrementAndGet());
        runThreads(2, 200_000, adder::increment);
        System.out.printf("%-8s %-22s %-22s %-22s %-22s%n", "threads", "int++(丢更新)", "synchronized", "AtomicLong", "LongAdder");
        for (int threads : new int[]{1, 2, 4, 8}) {
            long expect = (long) threads * per;
            reset();
            long a = runThreads(threads, per, () -> plain++);
            long pa = plain;
            reset();
            long b = runThreads(threads, per, () -> { synchronized (LOCK) { locked++; } });
            reset();
            long c = runThreads(threads, per, () -> atomic.incrementAndGet());
            reset();
            long d = runThreads(threads, per, adder::increment);
            System.out.printf("%-8d %-22s %-22s %-22s %-22s%n", threads,
                    a + "ms 值=" + pa, b + "ms", c + "ms", d + "ms 值=" + adder.sum());
            if (pa != expect) System.out.println("         ^ int++ 期望 " + expect + "，实际 " + pa + "，丢了 " + (expect - pa));
        }
    }
}
