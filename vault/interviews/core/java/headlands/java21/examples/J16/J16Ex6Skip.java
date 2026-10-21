import java.util.*;
import java.util.concurrent.*;

/** J16 例 6：ConcurrentSkipListMap——并发的"有序 Map"。订单簿价位表：多线程挂单，另一个线程取最优价。 */
public class J16Ex6Skip {
    public static void main(String[] args) throws Exception {
        // 卖盘：价格升序，最优价 = 最小的 key。key=价格(tick)，value=该价位总量
        ConcurrentSkipListMap<Long, Long> asks = new ConcurrentSkipListMap<>();
        int threads = 4, per = 50_000;
        CountDownLatch go = new CountDownLatch(1);
        List<Thread> ts = new ArrayList<>();
        for (int t = 0; t < threads; t++) {
            final int id = t;
            ts.add(Thread.ofPlatform().start(() -> {
                try { go.await(); } catch (InterruptedException e) { return; }
                Random r = new Random(id);
                for (int i = 0; i < per; i++) asks.merge(18_950L + r.nextInt(100), 1L, Long::sum);   // 原子地"累加该价位数量"
            }));
        }
        go.countDown();
        for (Thread t : ts) t.join();

        long total = asks.values().stream().mapToLong(Long::longValue).sum();
        System.out.println("价位数 = " + asks.size() + ", 总量 = " + total + " (期望 " + (long) threads * per + ")");
        System.out.println("最优卖价 firstEntry = " + asks.firstEntry());
        System.out.println("最高卖价 lastEntry  = " + asks.lastEntry());
        System.out.println("价位 >= 19000 的前 3 个 = " + asks.tailMap(19_000L).entrySet().stream().limit(3).toList());
        System.out.println("pollFirstEntry(原子取走最优价位) = " + asks.pollFirstEntry() + "，之后最优 = " + asks.firstKey());
    }
}
