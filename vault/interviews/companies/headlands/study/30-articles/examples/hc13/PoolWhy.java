import java.lang.management.GarbageCollectorMXBean;
import java.lang.management.ManagementFactory;
import java.util.Arrays;

/**
 * 为什么 Java 程序要「池化」？—— 讲义 hc13 §2.1 的实验。
 *
 * 场景：行情网关。每秒来很多订单消息，每条消息要在内存里活一小会儿（窗口里最近 W 条都还在用），然后被新的顶掉。
 * A 组：每条消息 new 一个 Order 对象（堆上）。
 * B 组：不 new，用 OffHeapOrderPool 复用堆外的槽位。
 * 测：总耗时、GC 次数与 GC 总时间、单次操作的最长耗时、超过 1 ms 的操作个数。
 *
 * 编译 / 运行（在 kit 根目录）：
 *   javac --release 21 --enable-preview -d /tmp/hc13 loop/rounds/01_video/hc13_fixed_memory_pool/reference/*.java study/30-articles/examples/hc13/PoolWhy.java
 *   java --enable-preview -Xmx256m -XX:+UseG1GC -cp /tmp/hc13 PoolWhy
 */
public class PoolWhy {
    static final int WINDOW = 1_000_000;          // 同时「在飞」的订单个数
    static final int MESSAGES = 30_000_000;

    public static void main(String[] args) {
        for (int round = 0; round < 3; round++) {
            System.out.println("=== 第 " + (round + 1) + " 轮 ===");
            heapRun();
            pooledRun();
        }
    }

    static void heapRun() {
        Order[] window = new Order[WINDOW];
        long gc0 = gcCount(), gcT0 = gcMillis();
        long maxNs = 0, slow = 0, sink = 0;
        long t0 = System.nanoTime();
        for (int i = 0; i < MESSAGES; i++) {
            long a = System.nanoTime();
            window[i % WINDOW] = new Order(i, 18_950 + (i & 63), 100 + (i & 7), i & 1);
            long d = System.nanoTime() - a;
            if (d > maxNs) maxNs = d;
            if (d > 1_000_000) slow++;
        }
        long total = System.nanoTime() - t0;
        for (Order o : window) sink += o.qty();
        report("堆上 new Order ", total, gc0, gcT0, maxNs, slow, sink);
    }

    static void pooledRun() {
        long[] window = new long[WINDOW];
        try (var pool = new OffHeapOrderPool(WINDOW)) {
            for (int i = 0; i < WINDOW; i++) window[i] = pool.allocate();    // 预热：窗口先填满
            long gc0 = gcCount(), gcT0 = gcMillis();
            long maxNs = 0, slow = 0, sink = 0;
            long t0 = System.nanoTime();
            for (int i = 0; i < MESSAGES; i++) {
                long a = System.nanoTime();
                int k = i % WINDOW;
                pool.free(window[k]);
                long h = pool.allocate();
                pool.put(h, i, 18_950 + (i & 63), 100 + (i & 7), i & 1);              // 零分配：直接写字段
                window[k] = h;
                long d = System.nanoTime() - a;
                if (d > maxNs) maxNs = d;
                if (d > 1_000_000) slow++;
            }
            long total = System.nanoTime() - t0;
            for (long h : window) sink += pool.qty(h);
            report("堆外池 复用槽位", total, gc0, gcT0, maxNs, slow, sink);
        }
    }

    static void report(String name, long totalNs, long gc0, long gcT0, long maxNs, long slow, long sink) {
        System.out.printf("%s  总耗时 %5d ms | GC %3d 次 / %4d ms | 单次最慢 %8.2f ms | >1ms 的操作 %d 个 (sink=%d)%n",
                name, totalNs / 1_000_000, gcCount() - gc0, gcMillis() - gcT0, maxNs / 1e6, slow, sink);
    }

    static long gcCount() {
        return ManagementFactory.getGarbageCollectorMXBeans().stream().mapToLong(GarbageCollectorMXBean::getCollectionCount).sum();
    }
    static long gcMillis() {
        return ManagementFactory.getGarbageCollectorMXBeans().stream().mapToLong(GarbageCollectorMXBean::getCollectionTime).sum();
    }
}
