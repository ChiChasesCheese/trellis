import java.util.Arrays;
import java.util.Random;

/**
 * ld02 讲义配套实验：TradingDesk 的事件处理速度（单线程，JIT 预热后）。本机数字只说明量级，不是低延迟系统的指标——
 * reference 为了清晰用了 HashMap<Long,…> / 装箱 / record 分配，没有为零分配优化。
 *
 * 编译 / 运行（在 kit 根目录）：
 *   javac --release 21 --enable-preview -d /tmp/ld02bench loop/rounds/03_lld/ld02_trading_ood/reference/*.java study/30-articles/examples/ld02/DeskBench.java
 *   java --enable-preview -cp /tmp/ld02bench DeskBench
 */
public class DeskBench {
    public static void main(String[] args) {
        System.out.println("java " + System.getProperty("java.version") + ", " + System.getProperty("os.name"));
        RiskLimits big = new RiskLimits(1_000, Long.MAX_VALUE, 1_000_000_000L, 10_000_000, 10_000);
        int orders = 100_000;                         // 每张单 4 个事件：Submit, Ack, Fill, Fill
        long[] liveNs = new long[5], replayNs = new long[5];
        long events = 4L * orders;
        for (int run = 0; run < 5; run++) {
            TradingDesk d = new TradingDesk(big);
            d.setReferencePrice("A", 100);
            long t0 = System.nanoTime();
            long exec = 1;
            for (long id = 1; id <= orders; id++) {
                d.submit(new Order(id, "A", id % 2 == 0 ? Side.BUY : Side.SELL, 10, 100));
                d.onExec(new ExecEvent.Ack(id));
                d.onExec(new ExecEvent.Fill(id, exec++, 4, 100));
                d.onExec(new ExecEvent.Fill(id, exec++, 6, 100));
            }
            liveNs[run] = System.nanoTime() - t0;
            var journal = d.journal();
            t0 = System.nanoTime();
            TradingDesk copy = TradingDesk.replay(big, journal);
            replayNs[run] = System.nanoTime() - t0;
            if (!copy.position("A").equals(d.position("A"))) throw new AssertionError();
        }
        Arrays.sort(liveNs); Arrays.sort(replayNs);
        System.out.printf("live  : %,d events in %.1f ms (median of 5) => %.2f M events/s, %.0f ns/event%n", events, liveNs[2] / 1e6, events / (liveNs[2] / 1e9) / 1e6, (double) liveNs[2] / events);
        System.out.printf("replay: %,d events in %.1f ms (median of 5) => %.2f M events/s, %.0f ns/event%n", events, replayNs[2] / 1e6, events / (replayNs[2] / 1e9) / 1e6, (double) replayNs[2] / events);

        // PositionBook 单独：随机多空，最坏情况是长队列
        PositionBook pb = new PositionBook();
        Random rnd = new Random(0);
        int n = 3_000_000;
        long t0 = System.nanoTime();
        for (int i = 0; i < n; i++) pb.onFill("S" + (i & 63), rnd.nextBoolean() ? Side.BUY : Side.SELL, 1 + rnd.nextInt(5), 100 + rnd.nextInt(10));
        long ns = System.nanoTime() - t0;
        System.out.printf("PositionBook.onFill: %,d fills in %.1f ms => %.2f M fills/s (含 \"S\"+i 字符串拼接的分配)%n", n, ns / 1e6, n / (ns / 1e9) / 1e6);
    }
}
