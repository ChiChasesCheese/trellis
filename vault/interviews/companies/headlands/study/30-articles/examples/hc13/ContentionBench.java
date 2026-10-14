import java.util.concurrent.CountDownLatch;
import java.util.concurrent.locks.ReentrantLock;

/**
 * 讲义 hc13 §4.4 的实验：同一个池，三种并发写法，线程数 1 / 2 / 4 / 8 下每秒能做多少次 分配+归还。
 *   locked  ：ReentrantLock 包住单线程的 GenPool
 *   treiber ：ConcurrentPool（无锁 Treiber 栈 + tagged head）
 *   cached  ：每线程一个小缓存（栈），批量从 treiber 池补货 / 退货，大部分操作根本不碰共享的 head
 *
 * 编译 / 运行（在 kit 根目录）：
 *   javac --release 21 --enable-preview -d /tmp/hc13 loop/rounds/01_video/hc13_fixed_memory_pool/reference/*.java study/30-articles/examples/hc13/ContentionBench.java
 *   java --enable-preview -cp /tmp/hc13 ContentionBench
 */
public class ContentionBench {
    interface Pool { long allocate(); void free(long h); }

    static final class Locked implements Pool {
        final GenPool p = new GenPool(1 << 16);
        final ReentrantLock lock = new ReentrantLock();
        public long allocate() { lock.lock(); try { return p.allocate(); } finally { lock.unlock(); } }
        public void free(long h) { lock.lock(); try { p.free(h); } finally { lock.unlock(); } }
    }

    static final class Treiber implements Pool {
        final ConcurrentPool p = new ConcurrentPool(1 << 16);
        public long allocate() { return p.allocate(); }
        public void free(long h) { p.free(h); }
    }

    /** 每线程缓存。注意：缓存里的 handle 在共享池眼里仍是「在用」，所以对缓存内的重复 free 它看不见——这是缓存换速度的代价。 */
    static final class Cached implements Pool {
        static final int BATCH = 32, MAX = 64;
        final ConcurrentPool shared = new ConcurrentPool(1 << 16);
        final ThreadLocal<long[]> cache = ThreadLocal.withInitial(() -> new long[MAX + 1]);   // [0] 存个数
        public long allocate() {
            long[] c = cache.get();
            if (c[0] == 0) {
                for (int i = 0; i < BATCH; i++) {
                    long h = shared.allocate();
                    if (h == ConcurrentPool.NONE) break;
                    c[(int) ++c[0]] = h;
                }
                if (c[0] == 0) return ConcurrentPool.NONE;
            }
            return c[(int) c[0]--];
        }
        public void free(long h) {
            long[] c = cache.get();
            if (c[0] == MAX) {
                for (int i = 0; i < BATCH; i++) shared.free(c[(int) c[0]--]);
            }
            c[(int) ++c[0]] = h;
        }
    }

    static double run(Pool pool, int threads, int opsPerThread) throws Exception {
        var gate = new CountDownLatch(1);
        var ts = new Thread[threads];
        for (int t = 0; t < threads; t++) {
            ts[t] = new Thread(() -> {
                try { gate.await(); } catch (InterruptedException e) { return; }
                long[] mine = new long[16];
                for (int i = 0; i < opsPerThread / 16; i++) {
                    int k = 0;
                    for (; k < 16; k++) { long h = pool.allocate(); if (h == ConcurrentPool.NONE) break; mine[k] = h; }
                    for (int j = 0; j < k; j++) pool.free(mine[j]);
                }
            });
            ts[t].start();
        }
        long t0 = System.nanoTime();
        gate.countDown();
        for (var t : ts) t.join();
        double sec = (System.nanoTime() - t0) / 1e9;
        return (double) threads * opsPerThread / sec / 1e6;     // 百万次 (alloc 或 free) 每秒
    }

    public static void main(String[] a) throws Exception {
        int ops = 4_000_000;
        System.out.println("单位：百万次操作/秒（alloc 和 free 各算一次），越大越好");
        System.out.printf("%-8s %10s %10s %10s%n", "线程数", "locked", "treiber", "cached");
        for (int threads : new int[] {1, 2, 4, 8}) {
            double best[] = new double[3];
            for (int rep = 0; rep < 5; rep++) {                  // 前几轮预热，取最好一轮
                best[0] = Math.max(best[0], run(new Locked(), threads, ops));
                best[1] = Math.max(best[1], run(new Treiber(), threads, ops));
                best[2] = Math.max(best[2], run(new Cached(), threads, ops));
            }
            System.out.printf("%-8d %10.1f %10.1f %10.1f%n", threads, best[0], best[1], best[2]);
        }
    }
}
