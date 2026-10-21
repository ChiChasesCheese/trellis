import java.util.*;
import java.util.function.Supplier;

/**
 * J18 例 3（贴近真实）：Objects 工具做 API 卫语句；订单簿"价格-时间优先"的 Comparator（带完整 tie-break）。
 */
public class J18Ex3 {
    enum Side { BUY, SELL }

    record Order(long id, Side side, long px, long ts, long qty) {
        Order {                                                          // 紧凑构造器（J01）里用 requireNonNull 卫语句
            Objects.requireNonNull(side, "side");
            if (qty <= 0) throw new IllegalArgumentException("qty must be > 0: " + qty);
        }
    }

    static final Comparator<Order> BUY_PRIORITY = Comparator
            .comparingLong(Order::px).reversed()                          // 价高者优先
            .thenComparingLong(Order::ts)                                 // 同价，先到者优先
            .thenComparingLong(Order::id);                                // 再相同按 id，保证"全序"，输出确定

    static final Comparator<Order> SELL_PRIORITY = Comparator
            .comparingLong(Order::px)                                     // 价低者优先
            .thenComparingLong(Order::ts)
            .thenComparingLong(Order::id);

    static String describe(String[] names, int index) {
        Objects.checkIndex(index, names.length);                          // 越界抛 IndexOutOfBoundsException，信息含 index 和 length
        return names[index];
    }

    public static void main(String[] args) {
        // ---- Objects 工具 ----
        try { new Order(1, null, 100, 1, 10); } catch (NullPointerException e) { System.out.println("requireNonNull(side) -> NPE: " + e.getMessage()); }

        Supplier<String> lazyMsg = () -> "expensive message " + System.nanoTime();   // 只有真的为 null 才构造消息
        try { Objects.requireNonNull(null, lazyMsg); } catch (NullPointerException e) { System.out.println("Supplier 版本 -> NPE: " + e.getMessage().startsWith("expensive")); }

        String cfg = null;
        System.out.println("requireNonNullElse = " + Objects.requireNonNullElse(cfg, "default"));
        System.out.println("requireNonNullElseGet = " + Objects.requireNonNullElseGet(cfg, () -> "computed"));
        System.out.println("Objects.toString(null, \"-\") = " + Objects.toString(cfg, "-"));
        System.out.println("Objects.equals(null, null) = " + Objects.equals(null, null) + ", hash(1,2,3) = " + Objects.hash(1, 2, 3));
        try { describe(new String[]{"a", "b"}, 5); } catch (IndexOutOfBoundsException e) { System.out.println("checkIndex -> " + e.getMessage()); }

        // ---- 价格-时间优先 ----
        List<Order> buys = new ArrayList<>(List.of(
                new Order(1, Side.BUY, 100, 5, 10), new Order(2, Side.BUY, 101, 3, 10),
                new Order(3, Side.BUY, 101, 1, 10), new Order(4, Side.BUY, 99, 2, 10), new Order(5, Side.BUY, 101, 1, 10)));
        buys.sort(BUY_PRIORITY);
        System.out.println("买盘优先级: " + buys.stream().map(o -> "#" + o.id() + "(" + o.px() + "@t" + o.ts() + ")").toList());

        // 用 TreeSet 保存订单簿：比较器必须是全序；若比较器对不同订单返回 0，TreeSet 会把它们当成同一个而丢掉
        var bad = new TreeSet<Order>(Comparator.comparingLong(Order::px).reversed());       // 缺 tie-break！
        var good = new TreeSet<Order>(BUY_PRIORITY);
        bad.addAll(buys); good.addAll(buys);
        System.out.println("缺 tie-break 的 TreeSet 里剩 " + bad.size() + " 个订单；完整 tie-break 的剩 " + good.size() + " 个");
    }
}
