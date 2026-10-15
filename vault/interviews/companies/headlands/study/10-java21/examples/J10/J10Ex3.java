import java.util.*;
import java.util.concurrent.*;

/** J10 例 3（贴近真实）：给 500 个代码并发取行情，限制「同时在途请求」不超过 20 个——用 Semaphore，而不是靠线程池大小。 */
public class J10Ex3 {
    record Quote(String symbol, long bidTicks, long askTicks) {}

    static final Semaphore IN_FLIGHT = new Semaphore(20); // 下游行情网关最多接受 20 个并发
    static final ConcurrentHashMap<String, Integer> peak = new ConcurrentHashMap<>();
    static int concurrent = 0; // 仅用于演示，受 synchronized 保护
    static int maxConcurrent = 0;

    static Quote fetch(String sym) throws InterruptedException {
        IN_FLIGHT.acquire(); // 虚拟线程在这里阻塞是廉价的：它被卸载，不占 OS 线程
        try {
            synchronized (J10Ex3.class) { concurrent++; maxConcurrent = Math.max(maxConcurrent, concurrent); }
            Thread.sleep(50); // 模拟网络
            synchronized (J10Ex3.class) { concurrent--; }
            long h = sym.hashCode() & 0xFFFF;
            return new Quote(sym, 10_000 + h, 10_001 + h);
        } finally {
            IN_FLIGHT.release();
        }
    }

    public static void main(String[] args) throws Exception {
        List<String> symbols = new ArrayList<>();
        for (int i = 0; i < 500; i++) symbols.add("SYM" + i);

        long t0 = System.nanoTime();
        List<Quote> quotes;
        try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<Quote>> fs = symbols.stream().map(s -> ex.submit(() -> fetch(s))).toList();
            quotes = new ArrayList<>();
            for (var f : fs) quotes.add(f.get());
        }
        long ms = (System.nanoTime() - t0) / 1_000_000;
        System.out.println("取回 " + quotes.size() + " 个行情, 第一个 = " + quotes.get(0));
        System.out.println("最大同时在途 = " + maxConcurrent + " (上限 20), 总耗时约 " + ms + " ms");
        // 500 个 / 20 并发 = 25 批 * 50ms ≈ 1250ms
    }
}
