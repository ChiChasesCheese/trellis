import java.lang.management.*;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

/**
 * J19 例 4：GC 对延迟尾部的影响。"hiccup meter"（jHiccup 的做法）：一个线程每 1ms 睡一次，
 * 记录实际醒来比预期晚了多少。如果 JVM 全局停顿了（stop-the-world），这个线程也会晚醒。
 * 另一组线程制造 GC 压力：维持一个较大的存活集（live set），同时大量分配短命对象。
 * 分别用 G1 和 Generational ZGC 跑，比较 p99 / max 延迟。
 *   java --enable-preview -Xmx2g -Xms2g -XX:+UseG1GC                   J19Ex4Hiccup
 *   java --enable-preview -Xmx2g -Xms2g -XX:+UseZGC -XX:+ZGenerational J19Ex4Hiccup
 * 加参数 idle 则不制造分配压力，用来测本机 sleep(1) 自身的基线误差（macOS 上 sleep 通常会晚醒几毫秒）。
 */
public class J19Ex4Hiccup {
    static volatile boolean stop;

    public static void main(String[] args) throws Exception {
        // 存活集：约 600MB 的长寿对象，GC 每次需要处理它
        int liveCount = 6_000_000;
        List<byte[]> live = new ArrayList<>(liveCount);
        for (int i = 0; i < liveCount; i++) live.add(new byte[100]);

        long[] hic = new long[40_000];
        int[] n = {0};
        Thread meter = new Thread(() -> {
            while (!stop && n[0] < hic.length) {
                long t0 = System.nanoTime();
                try { Thread.sleep(1); } catch (InterruptedException e) { return; }
                long late = System.nanoTime() - t0 - 1_000_000;
                hic[n[0]++] = Math.max(0, late);
            }
        }, "meter");
        meter.setDaemon(true);

        boolean idle = args.length > 0 && args[0].equals("idle");   // idle：不制造 GC 压力，只测本机的"基线噪声"
        int allocThreads = idle ? 0 : 4;
        Thread[] alloc = new Thread[allocThreads];
        for (int t = 0; t < allocThreads; t++) {
            alloc[t] = new Thread(() -> {
                var rnd = ThreadLocalRandom.current();
                while (!stop) {
                    for (int i = 0; i < 1000; i++) {
                        byte[] garbage = new byte[200];                                // 短命对象
                        garbage[0] = 1;
                        if ((i & 255) == 0) live.set(rnd.nextInt(liveCount), garbage); // 偶尔替换存活集里的一个，制造跨代引用
                    }
                }
            });
            alloc[t].setDaemon(true);
            alloc[t].start();
        }
        meter.start();
        meter.join(30_000);
        stop = true;

        long[] a = Arrays.copyOf(hic, n[0]);
        Arrays.sort(a);
        var gcs = new StringBuilder();
        long totalCount = 0, totalMs = 0;
        for (GarbageCollectorMXBean gc : ManagementFactory.getGarbageCollectorMXBeans()) {
            gcs.append(gc.getName()).append("(").append(gc.getCollectionCount()).append("次) ");
            totalCount += gc.getCollectionCount();
        }
        System.out.printf("GC: %s%n", gcs);
        System.out.printf("采样 %d 次: 晚醒 p50=%.2f ms  p99=%.2f ms  p99.9=%.2f ms  max=%.2f ms%n",
                a.length, a[a.length / 2] / 1e6, a[(int) (a.length * 0.99)] / 1e6, a[(int) (a.length * 0.999)] / 1e6, a[a.length - 1] / 1e6);
    }
}
