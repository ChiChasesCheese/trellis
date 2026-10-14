import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.PriorityQueue;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * hc09 Part 1 + Part 2：成交事件按 notional（价格 × 数量）取 top-k，以及按 ticker 汇总后取 top-k。
 *
 * <p>输入是三个平行数组（parallel arrays）：第 i 个事件是 (tickers[i], prices[i], volumes[i])。
 * 价格用整数 tick（比如 1 tick = 1 美分），数量用整数股数，所以 notional 是精确的 long，
 * 没有浮点误差；乘法和累加都用 {@code Math.xxxExact}，溢出就抛 {@link ArithmeticException}，绝不静默回绕。
 */
public final class TopTrades {
    private TopTrades() {}

    // ---------------------------------------------------------------- 数据类型

    /**
     * 一个成交事件。index 是它在输入数组里的下标——它既是「事件身份」，也是排序的最后一道 tie-break，
     * 所以任意两个事件之间都有严格先后，top-k 的结果是唯一的（确定性输出）。
     */
    public record Trade(int index, String ticker, long price, long volume) {
        public Trade {
            Objects.requireNonNull(ticker, "ticker");
            if (index < 0) throw new IllegalArgumentException("index must be >= 0: " + index);
            if (price < 0) throw new IllegalArgumentException("negative price: " + price);
            if (volume < 0) throw new IllegalArgumentException("negative volume: " + volume);
            // 构造时就检查一次乘法：对象一旦存在，notional() 就一定不会溢出。
            Math.multiplyExact(price, volume);
        }

        public long notional() {
            return price * volume; // 构造器已经证明不会溢出
        }
    }

    /** 一个 ticker 的累计 notional。 */
    public record TickerTotal(String ticker, long notional) {
        public TickerTotal {
            Objects.requireNonNull(ticker, "ticker");
            if (notional < 0) throw new IllegalArgumentException("negative notional: " + notional);
        }
    }

    /** 整体汇总：所有事件的 notional 之和，以及最大的那一个事件（空输入时为 empty）。 */
    public record Summary(long grandTotal, Optional<Trade> largest) {}

    // ---------------------------------------------------------------- 排序规则（全序，写全 tie-break）

    /** 「更好」排前面：notional 大的在前；相同按 ticker 字典序升序；再相同按 index 升序。 */
    public static final Comparator<Trade> BEST_FIRST =
            Comparator.comparingLong(Trade::notional).reversed()
                    .thenComparing(Trade::ticker)
                    .thenComparingInt(Trade::index);

    /** ticker 排名：总 notional 大的在前；相同按 ticker 字典序升序。ticker 在一张表里唯一，所以是全序。 */
    public static final Comparator<TickerTotal> BEST_TICKER_FIRST =
            Comparator.comparingLong(TickerTotal::notional).reversed()
                    .thenComparing(TickerTotal::ticker);

    // ---------------------------------------------------------------- Part 1

    /**
     * 前 k 个 notional 最大的事件，最好的在前。k 比事件数大就返回全部。
     *
     * <p>做法：大小为 k 的<b>最小堆</b>（min-heap，堆顶是目前保留的 k 个里「最差」的）。
     * 新事件如果比堆顶好，就顶替堆顶。每个事件至多 O(log k)，总共 O(n log k)；
     * 随机顺序下绝大多数事件连堆都进不去，只花一次 long 比较。
     *
     * <p>所有事件都会被校验并计算 notional（即使它进不了 top-k），所以乘法溢出一定会被发现。
     */
    public static List<Trade> topEvents(String[] tickers, long[] prices, long[] volumes, int k) {
        int n = checkInputs(tickers, prices, volumes, k);
        // 堆顶 = 保留集合里最差的 → 比较器取 BEST_FIRST 的反方向。
        var heap = new PriorityQueue<Trade>(Math.max(1, Math.min(k, n)), BEST_FIRST.reversed());
        for (int i = 0; i < n; i++) {
            long notional = notionalAt(tickers, prices, volumes, i);
            if (k == 0) continue;
            // 快速拒绝：堆满了且 notional 严格小于堆顶 → 不可能进 top-k，连 Trade 对象都不用建（零分配）。
            if (heap.size() == k && notional < heap.peek().notional()) continue;
            var t = new Trade(i, tickers[i], prices[i], volumes[i]);
            if (heap.size() < k) {
                heap.add(t);
            } else if (BEST_FIRST.compare(t, heap.peek()) < 0) { // t 比堆顶「更好」
                heap.poll();
                heap.add(t);
            }
        }
        // 堆按「最差先出」，所以 poll 出来是 worst → best；reversed() 是 Java 21 的 Sequenced Collections。
        var worstFirst = new ArrayList<Trade>(heap.size());
        while (!heap.isEmpty()) worstFirst.add(heap.poll());
        return List.copyOf(worstFirst.reversed());
    }

    /** 基线：全部建对象再整体排序，O(n log n) 时间 + O(n) 空间。用来对拍，也是「最笨的解法」。 */
    public static List<Trade> topEventsSorted(String[] tickers, long[] prices, long[] volumes, int k) {
        int n = checkInputs(tickers, prices, volumes, k);
        var all = new ArrayList<Trade>(n);
        for (int i = 0; i < n; i++) {
            notionalAt(tickers, prices, volumes, i);
            all.add(new Trade(i, tickers[i], prices[i], volumes[i]));
        }
        all.sort(BEST_FIRST);
        return List.copyOf(all.subList(0, Math.min(k, n)));
    }

    // ---------------------------------------------------------------- Part 2

    /** 按 ticker 汇总 notional 后取 top-k：HashMap 聚合 O(n)，再对 m 个不同 ticker 做大小 k 的堆 O(m log k)。 */
    public static List<TickerTotal> topTickers(String[] tickers, long[] prices, long[] volumes, int k) {
        int n = checkInputs(tickers, prices, volumes, k);
        var totals = new HashMap<String, Long>();
        for (int i = 0; i < n; i++) {
            totals.merge(tickers[i], notionalAt(tickers, prices, volumes, i), Math::addExact);
        }
        return topOf(totals, k);
    }

    /** 从「ticker → 总 notional」表里取 top-k（堆版本）。Part 4 合并分块结果后也走这里。 */
    public static List<TickerTotal> topOf(Map<String, Long> totals, int k) {
        if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
        if (k == 0) return List.of();
        var heap = new PriorityQueue<TickerTotal>(Math.min(k, Math.max(1, totals.size())), BEST_TICKER_FIRST.reversed());
        for (var e : totals.entrySet()) {
            var cand = new TickerTotal(e.getKey(), e.getValue());
            if (heap.size() < k) {
                heap.add(cand);
            } else if (BEST_TICKER_FIRST.compare(cand, heap.peek()) < 0) {
                heap.poll();
                heap.add(cand);
            }
        }
        var worstFirst = new ArrayList<TickerTotal>(heap.size());
        while (!heap.isEmpty()) worstFirst.add(heap.poll());
        return List.copyOf(worstFirst.reversed());
    }

    /** 同一件事的 Stream 写法：groupingBy + reducing(addExact)，再整体排序截断。O(n + m log m)，更短但常数更大。 */
    public static List<TickerTotal> topTickersStream(String[] tickers, long[] prices, long[] volumes, int k) {
        int n = checkInputs(tickers, prices, volumes, k);
        Map<String, Long> totals = IntStream.range(0, n).boxed().collect(
                Collectors.groupingBy(
                        i -> tickers[i],
                        Collectors.reducing(0L, i -> notionalAt(tickers, prices, volumes, i), Math::addExact)));
        return totals.entrySet().stream()
                .map(e -> new TickerTotal(e.getKey(), e.getValue()))
                .sorted(BEST_TICKER_FIRST)
                .limit(k)
                .toList();
    }

    /** teeing：一趟遍历同时得到「总额」和「最大事件」两个互不相关的聚合，最后合成一个 Summary。 */
    public static Summary summarize(String[] tickers, long[] prices, long[] volumes) {
        int n = checkInputs(tickers, prices, volumes, 0);
        return IntStream.range(0, n)
                .mapToObj(i -> {
                    notionalAt(tickers, prices, volumes, i);
                    return new Trade(i, tickers[i], prices[i], volumes[i]);
                })
                .collect(Collectors.teeing(
                        Collectors.reducing(0L, Trade::notional, Math::addExact),
                        Collectors.minBy(BEST_FIRST), // BEST_FIRST 下「最小」就是「最好」
                        Summary::new));
    }

    // ---------------------------------------------------------------- 共用校验（包可见，供 Part 3/4 复用）

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
