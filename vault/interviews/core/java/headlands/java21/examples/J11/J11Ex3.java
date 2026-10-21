import java.time.Instant;
import java.time.Duration;
import java.util.concurrent.*;
import java.util.concurrent.StructuredTaskScope.Subtask;

/**
 * J11 例 3（贴近真实）：下单前检查——并行取 行情 / 风控额度 / 合约参考数据，任何一个失败立刻取消另外两个，
 * 并且整体最多等 deadline。演示三个场景：全成功、一个失败、整体超时。
 */
public class J11Ex3 {
    record Quote(long bid, long ask) {}
    record Limit(long maxQty) {}
    record Instrument(String symbol, long tickSize) {}
    record PreTrade(Quote q, Limit l, Instrument i) {}

    static <T> T slow(String name, long ms, T value, boolean fail) throws InterruptedException {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            System.out.println("    - " + name + " 被取消");
            throw e;
        }
        if (fail) throw new IllegalStateException(name + " unavailable");
        System.out.println("    - " + name + " 完成");
        return value;
    }

    static PreTrade check(long quoteMs, boolean riskFails, Duration deadline) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure("pretrade", Thread.ofVirtual().factory())) {
            Subtask<Quote> q = scope.fork(() -> slow("quote", quoteMs, new Quote(18950, 18951), false));
            Subtask<Limit> l = scope.fork(() -> slow("risk ", 100, new Limit(500), riskFails));
            Subtask<Instrument> i = scope.fork(() -> slow("refdata", 50, new Instrument("AAPL", 1), false));
            scope.joinUntil(Instant.now().plus(deadline)).throwIfFailed();
            return new PreTrade(q.get(), l.get(), i.get());
        }
    }

    static void run(String title, long quoteMs, boolean riskFails, Duration deadline) {
        System.out.println(title);
        try {
            System.out.println("  结果: " + check(quoteMs, riskFails, deadline));
        } catch (ExecutionException e) {
            System.out.println("  失败: " + e.getCause());
        } catch (TimeoutException e) {
            System.out.println("  超时: " + e.getClass().getSimpleName());
        } catch (Exception e) {
            System.out.println("  其他: " + e);
        }
    }

    public static void main(String[] args) {
        run("场景 1：全部成功", 150, false, Duration.ofSeconds(2));
        run("场景 2：风控失败(100ms)，行情要 1500ms -> 行情应被取消", 1500, true, Duration.ofSeconds(2));
        run("场景 3：行情太慢(3000ms)，deadline 400ms -> 超时并取消", 3000, false, Duration.ofMillis(400));
    }
}
