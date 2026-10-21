import java.util.concurrent.atomic.AtomicLongArray;

/**
 * J16 例 8：伪共享（false sharing）。两个线程各自只改"自己的"计数器，互不相干——
 * 但如果两个计数器在同一条 64 字节缓存行里，CPU 核之间会为这条行来回抢所有权，变慢。
 * 做法：同一个数组里，下标 0 和 1（相邻 8 字节） vs 下标 0 和 16（相距 128 字节）。
 * 粗糙计时，只看相对差异；不同机器差异很大（Apple Silicon 的缓存行是 128 字节）。
 */
public class J16Ex8FalseSharing {
    static long run(int idxA, int idxB, int iterations) throws Exception {
        AtomicLongArray arr = new AtomicLongArray(64);
        Thread a = new Thread(() -> { for (int i = 0; i < iterations; i++) arr.set(idxA, arr.get(idxA) + 1); });
        Thread b = new Thread(() -> { for (int i = 0; i < iterations; i++) arr.set(idxB, arr.get(idxB) + 1); });
        long t0 = System.nanoTime();
        a.start(); b.start(); a.join(); b.join();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    public static void main(String[] args) throws Exception {
        int n = 50_000_000;
        run(0, 1, 2_000_000); run(0, 32, 2_000_000);   // 预热
        for (int rep = 0; rep < 3; rep++) {
            long adjacent = run(0, 1, n);
            long apart = run(0, 32, n);                // 相距 32*8 = 256 字节
            System.out.println("第 " + (rep + 1) + " 轮：相邻(下标 0,1) " + adjacent + " ms  vs  分开(下标 0,32) " + apart + " ms");
        }
    }
}
