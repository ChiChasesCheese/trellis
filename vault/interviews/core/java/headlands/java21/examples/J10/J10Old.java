import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/** J10 旧写法（Java 8 风格）：每个阻塞任务占一个平台线程，所以必须用「线程池」限流。 */
public class J10Old {
    static String fetchQuote(String symbol) throws InterruptedException {
        Thread.sleep(100); // 假装一次 100ms 的网络往返
        return symbol + ":100.25";
    }

    public static void main(String[] args) throws Exception {
        // 痛点 1：不敢开太多线程，只好开一个固定大小的池（这里 50 个）
        ExecutorService pool = Executors.newFixedThreadPool(50);
        List<Future<String>> futures = new ArrayList<>();
        long t0 = System.nanoTime();
        for (int i = 0; i < 1_000; i++) {
            final String sym = "SYM" + i;
            futures.add(pool.submit(() -> fetchQuote(sym)));
        }
        for (Future<String> f : futures) f.get();
        pool.shutdown();
        long ms = (System.nanoTime() - t0) / 1_000_000;
        // 1000 个任务 / 50 个线程 = 20 批，每批 100ms ≈ 2000ms
        System.out.println("fixed pool(50): 1000 个 100ms 任务耗时约 " + ms + " ms");
    }
}
