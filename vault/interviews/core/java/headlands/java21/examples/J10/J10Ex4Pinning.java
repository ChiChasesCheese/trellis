import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.ReentrantLock;

/**
 * J10 例 4：pinning（钉住）。JDK 21 里，虚拟线程在 synchronized 块里阻塞，会把 carrier 线程一起占住。
 * 为了让现象明显，运行时把 carrier 数限制为 2：
 *   java --enable-preview -Djdk.virtualThreadScheduler.parallelism=2 -Djdk.virtualThreadScheduler.maxPoolSize=2 J10Ex4Pinning
 * 8 个虚拟线程各自「持锁 sleep 200ms」。每个线程用【自己独立的】锁，所以不存在锁竞争，只比较 pin 与否：
 *   * ReentrantLock 内 sleep：虚拟线程被卸载，2 个 carrier 可以轮流服务 8 个线程 -> 约 200ms
 *   * synchronized 内 sleep ：每个线程占住一个 carrier 整整 200ms -> 8 个线程 / 2 个 carrier = 4 批 -> 约 800ms
 */
public class J10Ex4Pinning {
    static final int N = 8;

    static long timeIt(boolean useSynchronized) throws Exception {
        List<Thread> ts = new ArrayList<>();
        long t0 = System.nanoTime();
        for (int i = 0; i < N; i++) {
            final Object mon = new Object();                 // 各自独立的锁：不存在锁竞争，只有 pin 的影响
            final ReentrantLock lock = new ReentrantLock();
            ts.add(Thread.ofVirtual().start(() -> {
                if (useSynchronized) {
                    synchronized (mon) { sleep200(); }       // JDK 21：持有 monitor 时阻塞 -> carrier 被钉住
                } else {
                    lock.lock();
                    try { sleep200(); } finally { lock.unlock(); } // 持有 ReentrantLock 时阻塞 -> 正常卸载
                }
            }));
        }
        for (Thread t : ts) t.join();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    static void sleep200() {
        try { Thread.sleep(200); } catch (InterruptedException e) { throw new RuntimeException(e); }
    }

    public static void main(String[] args) throws Exception {
        System.out.println("carrier 并行度 = " + System.getProperty("jdk.virtualThreadScheduler.parallelism"));
        timeIt(false); // 预热
        System.out.println("ReentrantLock 内 sleep: " + timeIt(false) + " ms");
        System.out.println("synchronized 内 sleep : " + timeIt(true) + " ms");
    }
}
