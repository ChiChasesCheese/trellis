import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** J08 例 3（贴近真实）：流水线的中间结果、分组聚合、什么时候该写显式类型。 */
public class J08Ex3 {

    enum Side { BUY, SELL }
    record Fill(String symbol, Side side, long px, long qty) {}

    public static void main(String[] args) {
        var fills = List.of(
                new Fill("AAPL", Side.BUY, 18_950, 100), new Fill("AAPL", Side.SELL, 18_960, 30),
                new Fill("MSFT", Side.BUY, 41_000, 10), new Fill("AAPL", Side.BUY, 18_955, 50));

        // 分组聚合的结果类型是 Map<String, Long>，右边一长串里没有写出来；var 让左边也不用重复
        var qtyBySymbol = fills.stream().collect(
                Collectors.groupingBy(Fill::symbol, TreeMap::new, Collectors.summingLong(Fill::qty)));
        System.out.println(qtyBySymbol);

        // 嵌套分组：Map<String, Map<Side, Long>> 写出来很长，var 省掉
        var nested = fills.stream().collect(Collectors.groupingBy(Fill::symbol, TreeMap::new,
                Collectors.groupingBy(Fill::side, () -> new TreeMap<>(Comparator.naturalOrder()),
                        Collectors.summingLong(Fill::qty))));
        System.out.println(nested);

        for (var e : nested.entrySet()) {
            for (var inner : e.getValue().entrySet()) {
                System.out.println(e.getKey() + " " + inner.getKey() + " " + inner.getValue());
            }
        }

        // 什么时候【不】用 var：右边看不出类型 + 类型本身是关键信息
        long notional = compute(fills.get(0));            // 显式写 long：读者一眼知道是 long，不是 int
        Map<String, Long> declared = qtyBySymbol;         // 想把变量的类型限制成接口时，显式写接口
        System.out.println(notional + " " + declared.size());
    }

    static long compute(Fill f) { return Math.multiplyExact(f.px(), f.qty()); }
}
