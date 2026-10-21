import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** J08 旧写法：类型在左右两边重复；复杂泛型类型占掉大半行；有些类型根本写不出名字。 */
public class J08Old {

    static final class Fill {
        final String symbol; final long qty;
        Fill(String symbol, long qty) { this.symbol = symbol; this.qty = qty; }
    }

    public static void main(String[] args) {
        List<Fill> fills = new ArrayList<Fill>();       // Java 7 之前还要把 <Fill> 写两遍；7 起可用 <>
        fills.add(new Fill("AAPL", 100));
        fills.add(new Fill("MSFT", 50));
        fills.add(new Fill("AAPL", 25));

        // 左边的类型和右边的 new 几乎一模一样
        Map<String, List<Fill>> bySymbol = new HashMap<String, List<Fill>>();
        for (Fill f : fills) {
            List<Fill> bucket = bySymbol.get(f.symbol);
            if (bucket == null) {
                bucket = new ArrayList<Fill>();
                bySymbol.put(f.symbol, bucket);
            }
            bucket.add(f);
        }

        // 遍历时又要把 Map.Entry<String, List<Fill>> 完整写一遍
        for (Map.Entry<String, List<Fill>> e : bySymbol.entrySet()) {
            long total = 0;
            for (Fill f : e.getValue()) total += f.qty;
            System.out.println(e.getKey() + " " + total);
        }
    }
}
