import java.time.Duration;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;

/** JDK 21: a virtual thread blocking inside synchronized pins its carrier; ReentrantLock does not.  Run with -Djdk.virtualThreadScheduler.parallelism=1 -Djdk.virtualThreadScheduler.maxPoolSize=1 */
public class K09Pinning {
    static final Object MON = new Object(); static final ReentrantLock RL = new ReentrantLock();
    static long run(boolean useSync) throws Exception {
        long t0 = System.nanoTime();
        try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 8; i++) ex.submit(() -> {
                if (useSync) { synchronized (new Object()) { Thread.sleep(Duration.ofMillis(200)); } }  // pins (blocks carrier)
                else { RL.lock(); RL.unlock(); Thread.sleep(Duration.ofMillis(200)); }                   // unmounts
                return null; });
        }
        return (System.nanoTime() - t0) / 1_000_000;
    }
    public static void main(String[] a) throws Exception {
        System.out.println("1 carrier, 8 tasks each sleeping 200 ms");
        run(true); run(false);                                  // warm-up
        System.out.println("sleep inside synchronized : " + run(true) + " ms  (serialised: ~8 x 200)");
        System.out.println("sleep outside synchronized: " + run(false) + " ms (overlapped: ~200)");
    }
}
