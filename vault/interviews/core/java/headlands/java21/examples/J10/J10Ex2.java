import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/** J10 例 2：同一份「1000 个 100ms 阻塞任务」，固定池 50 线程 vs 每任务一个虚拟线程。再加到 10000 个。 */
public class J10Ex2 {
    static String fetchQuote(String symbol) throws InterruptedException {
        Thread.sleep(100);
        return symbol;
    }

    static long run(ExecutorService ex, int n) throws Exception {
        List<Future<String>> fs = new ArrayList<>();
        long t0 = System.nanoTime();
        for (int i = 0; i < n; i++) {
            final String s = "S" + i;
            fs.add(ex.submit(() -> fetchQuote(s)));
        }
        for (var f : fs) f.get();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    public static void main(String[] args) throws Exception {
        try (var pool = Executors.newFixedThreadPool(50)) {
            System.out.println("固定池 50 线程, 1000 任务: " + run(pool, 1_000) + " ms");
        }
        // newVirtualThreadPerTaskExecutor：每个任务一个新虚拟线程；不是「池」，不复用线程。
        // ExecutorService 在 Java 19 起实现了 AutoCloseable，try-with-resources 结束时 close() = shutdown + 等全部任务结束
        try (var vex = Executors.newVirtualThreadPerTaskExecutor()) {
            System.out.println("虚拟线程每任务一个, 1000 任务: " + run(vex, 1_000) + " ms");
        }
        try (var vex = Executors.newVirtualThreadPerTaskExecutor()) {
            System.out.println("虚拟线程每任务一个, 10000 任务: " + run(vex, 10_000) + " ms");
        }
    }
}
