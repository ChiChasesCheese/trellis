import java.util.*;
import java.util.stream.*;

/** J14 旧写法：Java 7/8 风格的聚合。循环 + 可变累加器；Java 8 的 Stream 要 collect(Collectors.toList())；一次遍历算两个值很别扭。 */
public class J14Old {
    record Trade(String symbol, long px, long qty) {}

    public static void main(String[] args) {
        List<Trade> trades = List.of(new Trade("AAPL", 18950, 100), new Trade("AAPL", 18960, 300), new Trade("MSFT", 41000, 50));

        // 痛点 1：一次遍历要算 "总名义金额" 和 "总数量"（为了 VWAP），只能手写可变累加器
        long notional = 0, qty = 0;
        for (Trade t : trades) { notional += t.px() * t.qty(); qty += t.qty(); }
        System.out.println("VWAP = " + (double) notional / qty);

        // 痛点 2：Stream 最后一步啰嗦 .collect(Collectors.toList())
        List<String> symbols = trades.stream().map(Trade::symbol).distinct().collect(Collectors.toList());
        System.out.println(symbols);

        // 痛点 3：Java 8 的 iterate 是无限的，要配 limit；条件终止没法直接写
        List<Integer> powers = Stream.iterate(1, x -> x * 2).limit(8).collect(Collectors.toList());
        System.out.println(powers);

        // 痛点 4：一个元素产出 0..n 个结果，要 flatMap 为每个元素建一个小 Stream（有分配开销）
        List<Long> bigQtys = trades.stream()
                .flatMap(t -> t.qty() >= 100 ? Stream.of(t.qty()) : Stream.empty())
                .collect(Collectors.toList());
        System.out.println(bigQtys);
    }
}
