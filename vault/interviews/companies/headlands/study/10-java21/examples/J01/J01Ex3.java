import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/** J01 例 3（贴近真实）：成交回报 -> 按 (symbol, side) 聚合；record 当复合 key、实现接口、泛型 record、反射可见、浅不可变陷阱。 */
public class J01Ex3 {

    enum Side { BUY, SELL }

    record Fill(String symbol, Side side, long priceTicks, long qty) implements Comparable<Fill> {
        Fill {
            if (qty <= 0) throw new IllegalArgumentException("qty");
        }
        static Fill parse(String line) {
            String[] t = line.split(",");
            return new Fill(t[0], Side.valueOf(t[1]), Long.parseLong(t[2]), Long.parseLong(t[3]));
        }
        @Override public int compareTo(Fill o) {
            return Comparator.comparing(Fill::symbol).thenComparingLong(Fill::priceTicks).compare(this, o);
        }
    }

    /** 复合 key：以前要手写一个带 equals/hashCode 的类，或者拼字符串 symbol + "|" + side。 */
    record BookKey(String symbol, Side side) {}

    /** 泛型 record：一个「值 + 它是否通过校验」的小容器。 */
    record Tagged<T>(T value, boolean valid) {}

    /** 陷阱：数组字段是浅不可变的——record 只保证「引用不变」，不保证数组内容不变。 */
    record Leaky(int[] data) {}

    public static void main(String[] args) {
        List<String> lines = List.of(
                "AAPL,BUY,18950,100", "AAPL,BUY,18955,50", "AAPL,SELL,18960,30",
                "MSFT,BUY,41000,10", "AAPL,BUY,18950,25");

        Map<BookKey, Long> qtyByBook = new TreeMap<>(Comparator
                .comparing(BookKey::symbol).thenComparing(BookKey::side));
        for (String line : lines) {
            Fill f = Fill.parse(line);
            qtyByBook.merge(new BookKey(f.symbol(), f.side()), f.qty(), Long::sum);
        }
        qtyByBook.forEach((k, v) -> System.out.println(k + " -> " + v));

        // 反射看得到：record 是一种特殊的类
        System.out.println(Fill.class.isRecord());
        System.out.println(Arrays.stream(Fill.class.getRecordComponents())
                .map(c -> c.getType().getSimpleName() + " " + c.getName()).toList());

        Tagged<String> t = new Tagged<>("abc", true);
        System.out.println(t);

        Leaky l = new Leaky(new int[]{1, 2, 3});
        l.data()[0] = 99;                       // 合法！record 管不住数组内容
        System.out.println(Arrays.toString(l.data()));
        Leaky same = new Leaky(l.data());
        System.out.println(l.equals(new Leaky(new int[]{99, 2, 3})));  // false：数组用引用 equals
        System.out.println(l.equals(same));                            // true：同一个数组引用

        List<Fill> sorted = new ArrayList<>(lines.stream().map(Fill::parse).toList());
        sorted.sort(null);                      // 自然顺序 = compareTo
        System.out.println(sorted.get(0));
    }
}
