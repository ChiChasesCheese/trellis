import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * hc09 Part 1 + Part 2（starter）：成交事件按 notional（价格 × 数量）取 top-k，以及按 ticker 汇总后取 top-k。
 *
 * <p>输入是三个平行数组：第 i 个事件是 (tickers[i], prices[i], volumes[i])。价格用整数 tick，数量用整数，
 * notional 是精确的 long；乘法和累加用 Math.xxxExact，溢出抛 ArithmeticException。
 * 已经给出：record、比较器、两个校验小工具。要你写的方法体都是 TODO。
 */
public final class TopTrades {
    private TopTrades() {}

    public record Trade(int index, String ticker, long price, long volume) {
        public Trade {
            Objects.requireNonNull(ticker, "ticker");
            if (index < 0) throw new IllegalArgumentException("index must be >= 0: " + index);
            if (price < 0) throw new IllegalArgumentException("negative price: " + price);
            if (volume < 0) throw new IllegalArgumentException("negative volume: " + volume);
            Math.multiplyExact(price, volume); // 构造时检查一次：对象存在就意味着 notional() 不会溢出
        }

        public long notional() {
            return price * volume;
        }
    }

    public record TickerTotal(String ticker, long notional) {
        public TickerTotal {
            Objects.requireNonNull(ticker, "ticker");
            if (notional < 0) throw new IllegalArgumentException("negative notional: " + notional);
        }
    }

    public record Summary(long grandTotal, Optional<Trade> largest) {}

    /** 「更好」排前面：notional 大的在前；相同按 ticker 升序；再相同按 index 升序。 */
    public static final Comparator<Trade> BEST_FIRST =
            Comparator.comparingLong(Trade::notional).reversed()
                    .thenComparing(Trade::ticker)
                    .thenComparingInt(Trade::index);

    /** ticker 排名：总 notional 大的在前；相同按 ticker 升序。 */
    public static final Comparator<TickerTotal> BEST_TICKER_FIRST =
            Comparator.comparingLong(TickerTotal::notional).reversed()
                    .thenComparing(TickerTotal::ticker);

    // ---------------------------------------------------------------- Part 1

    /**
     * 前 k 个 notional 最大的事件，最好的在前，k 比 n 大就返回全部。
     * 提示：大小为 k 的最小堆；堆满之后先用一次 long 比较快速拒绝；每个事件都要校验（溢出也要报）。
     */
    public static List<Trade> topEvents(String[] tickers, long[] prices, long[] volumes, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 基线：全部建对象再整体排序，O(n log n)。 */
    public static List<Trade> topEventsSorted(String[] tickers, long[] prices, long[] volumes, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---------------------------------------------------------------- Part 2

    /** 按 ticker 汇总 notional（累加用 Math::addExact），再取 top-k。 */
    public static List<TickerTotal> topTickers(String[] tickers, long[] prices, long[] volumes, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 从「ticker → 总 notional」表里取 top-k（堆版本）。k < 0 → IAE。 */
    public static List<TickerTotal> topOf(Map<String, Long> totals, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Stream 写法：groupingBy + reducing，再 sorted + limit。 */
    public static List<TickerTotal> topTickersStream(String[] tickers, long[] prices, long[] volumes, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 一趟遍历得到「总额」和「最大事件」：Collectors.teeing。空输入 → (0, empty)。 */
    public static Summary summarize(String[] tickers, long[] prices, long[] volumes) {
        throw new UnsupportedOperationException("TODO");
    }

    // ---------------------------------------------------------------- 共用校验（已给出）

    /** 检查数组与 k，返回事件数 n。 */
    static int checkInputs(String[] tickers, long[] prices, long[] volumes, int k) {
        Objects.requireNonNull(tickers, "tickers");
        Objects.requireNonNull(prices, "prices");
        Objects.requireNonNull(volumes, "volumes");
        if (tickers.length != prices.length || prices.length != volumes.length) {
            throw new IllegalArgumentException("length mismatch: %d tickers, %d prices, %d volumes"
                    .formatted(tickers.length, prices.length, volumes.length));
        }
        if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
        return tickers.length;
    }

    /** 第 i 个事件的 notional：校验非空、非负，乘法溢出抛 ArithmeticException。 */
    static long notionalAt(String[] tickers, long[] prices, long[] volumes, int i) {
        Objects.requireNonNull(tickers[i], () -> "ticker at " + i);
        long p = prices[i];
        long v = volumes[i];
        if (p < 0) throw new IllegalArgumentException("negative price at " + i + ": " + p);
        if (v < 0) throw new IllegalArgumentException("negative volume at " + i + ": " + v);
        return Math.multiplyExact(p, v);
    }
}
