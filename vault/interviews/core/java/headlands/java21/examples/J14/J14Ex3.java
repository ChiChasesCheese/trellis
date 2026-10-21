import java.util.*;
import java.util.stream.*;

/** J14 例 3（贴近真实）：一次遍历算多个指标——teeing、groupingBy + summarizing、filtering/flatMapping、收集器组合。 */
public class J14Ex3 {
    record Trade(String symbol, long pxTicks, long qty) {}
    record Vwap(long qty, long notional) {
        double value() { return qty == 0 ? Double.NaN : (double) notional / qty; }
    }

    public static void main(String[] args) {
        List<Trade> trades = List.of(
                new Trade("AAPL", 18950, 100), new Trade("AAPL", 18960, 300),
                new Trade("MSFT", 41000, 50), new Trade("MSFT", 41010, 150), new Trade("AAPL", 18940, 10));

        // 1. teeing：同一个流，两个收集器并行，最后合并两个结果。一次遍历得到 VWAP。
        Vwap all = trades.stream().collect(Collectors.teeing(
                Collectors.summingLong(Trade::qty),
                Collectors.summingLong(t -> Math.multiplyExact(t.pxTicks(), t.qty())),
                Vwap::new));
        System.out.printf("总体 VWAP = %.3f (qty=%d)%n", all.value(), all.qty());

        // 2. teeing 求 min/max 价差
        var range = trades.stream().map(Trade::pxTicks).collect(Collectors.teeing(
                Collectors.minBy(Comparator.<Long>naturalOrder()),
                Collectors.maxBy(Comparator.<Long>naturalOrder()),
                (lo, hi) -> lo.orElseThrow() + ".." + hi.orElseThrow()));
        System.out.println("价格范围(全部) = " + range);

        // 3. groupingBy + 下游 teeing：按代码分组，每组一个 VWAP
        Map<String, Vwap> bySymbol = trades.stream().collect(Collectors.groupingBy(
                Trade::symbol, TreeMap::new,
                Collectors.teeing(
                        Collectors.summingLong(Trade::qty),
                        Collectors.summingLong(t -> t.pxTicks() * t.qty()),
                        Vwap::new)));
        bySymbol.forEach((s, v) -> System.out.printf("  %s VWAP=%.3f qty=%d%n", s, v.value(), v.qty()));

        // 4. summarizingLong：count/sum/min/max/average 一次拿全
        LongSummaryStatistics st = trades.stream().collect(Collectors.summarizingLong(Trade::qty));
        System.out.println("qty 统计: " + st);

        // 5. filtering（Java 9）：分组后在每组内部过滤，空组仍然保留（与先 filter 再分组不同）
        Map<String, List<Long>> bigBySymbol = trades.stream().collect(Collectors.groupingBy(
                Trade::symbol, TreeMap::new,
                Collectors.filtering(t -> t.qty() >= 200, Collectors.mapping(Trade::qty, Collectors.toList()))));
        System.out.println("每个代码的大单(qty>=200): " + bigBySymbol);
        Map<String, List<Long>> filterFirst = trades.stream().filter(t -> t.qty() >= 200).collect(
                Collectors.groupingBy(Trade::symbol, TreeMap::new, Collectors.mapping(Trade::qty, Collectors.toList())));
        System.out.println("先 filter 再分组        : " + filterFirst);
    }
}
