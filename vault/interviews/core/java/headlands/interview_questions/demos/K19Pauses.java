import java.util.*;

/**
 * Latency jitter probe: a thread does tiny steady work and records the largest gap between iterations
 * while a second thread allocates garbage and keeps a live set.  Run under different collectors:
 *   -XX:+UseG1GC / -XX:+UseParallelGC / -XX:+UseZGC -XX:+ZGenerational / -XX:+UseEpsilonGC (needs UnlockExperimental)
 */
public class K19Pauses {
    static volatile Object sink;
    public static void main(String[] a) throws Exception {
        int seconds = 8;
        Thread churn = new Thread(() -> {
            Map<Integer, byte[]> live = new HashMap<>();
            Random r = new Random(1); long end = System.nanoTime() + seconds * 1_000_000_000L;
            while (System.nanoTime() < end) {
                live.put(r.nextInt(300_000), new byte[200 + r.nextInt(300)]);   // ~100 MB live, constant churn
                sink = new byte[1024];
            }
        });
        churn.setDaemon(true); if (a.length == 0 || !a[0].equals("nochurn")) churn.start();   // "nochurn" = OS-noise control
        long end = System.nanoTime() + seconds * 1_000_000_000L, last = System.nanoTime(), max = 0; int over1ms = 0, over10ms = 0; long n = 0;
        long[] hist = new long[4];
        while (System.nanoTime() < end) {
            long now = System.nanoTime(); long gap = now - last; last = now; n++;
            if (gap > max) max = gap;
            if (gap > 1_000_000) over1ms++; if (gap > 10_000_000) over10ms++;
            for (int i = 0; i < 200; i++) Thread.onSpinWait();     // ~ a few hundred ns of "work"
        }
        System.out.printf("%-12s iterations=%,d  max gap=%.2f ms  gaps>1ms=%d  gaps>10ms=%d%n",
            java.lang.management.ManagementFactory.getGarbageCollectorMXBeans().get(0).getName(), n, max / 1e6, over1ms, over10ms);
    }
}
