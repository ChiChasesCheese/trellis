import java.time.Duration;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

public class K09VirtualThreads {
    public static void main(String[] a) throws Exception {
        Thread.ofVirtual().name("v1").start(() -> System.out.println("inside: " + Thread.currentThread())).join();
        System.out.println("isVirtual=" + Thread.ofVirtual().unstarted(() -> {}).isVirtual());
        for (int n : new int[]{10_000, 100_000}) {
            AtomicInteger done = new AtomicInteger();
            long t0 = System.nanoTime();
            try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
                for (int i = 0; i < n; i++) ex.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return done.incrementAndGet(); });
            }
            System.out.printf("%,d virtual threads each blocking 1 s: finished=%d in %d ms%n", n, done.get(), (System.nanoTime() - t0) / 1_000_000);
        }
        long t0 = System.nanoTime();
        try (var ex = Executors.newFixedThreadPool(200)) {
            for (int i = 0; i < 2_000; i++) ex.submit(() -> { Thread.sleep(Duration.ofSeconds(1)); return 1; });
        }
        System.out.printf("2,000 tasks on a 200-thread platform pool: %d ms (= 2000/200 * 1 s)%n", (System.nanoTime() - t0) / 1_000_000);
        // CPU-bound gets nothing from virtual threads
        System.out.println("availableProcessors=" + Runtime.getRuntime().availableProcessors());
    }
}
