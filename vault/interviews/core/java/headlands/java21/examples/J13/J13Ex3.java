import java.util.*;

/**
 * J13 例 3（贴近真实）：对一批消息分类计数，演示嵌套 record 模式里的 _、带 when 守卫的 case，
 * 以及 _ 不能当普通变量用（注释里的写法会编译失败）。
 */
public class J13Ex3 {
    enum Side { BUY, SELL }
    record Px(long ticks) {}
    record Order(long id, Side side, Px px, long qty) {}

    sealed interface Msg permits Placed, Cancelled {}
    record Placed(Order order) implements Msg {}
    record Cancelled(long id) implements Msg {}

    static String classify(Msg m) {
        return switch (m) {
            case Placed(Order(_, Side s, _, var q)) when q >= 1000 -> "BIG " + s;   // 嵌套解构，跳过 id 和 px
            case Placed(Order(_, Side s, _, _)) -> "SMALL " + s;
            case Cancelled _ -> "CANCEL";                                           // 仍然穷尽：没有 default
        };
    }

    public static void main(String[] args) {
        List<Msg> msgs = List.of(
                new Placed(new Order(1, Side.BUY, new Px(18950), 500)),
                new Placed(new Order(2, Side.SELL, new Px(18951), 2000)),
                new Placed(new Order(3, Side.BUY, new Px(18949), 1000)),
                new Cancelled(1));
        var counts = new TreeMap<String, Integer>();
        for (var m : msgs) counts.merge(classify(m), 1, Integer::sum);
        System.out.println(counts);

        // 以下三行如果取消注释，都会编译失败（_ 不是变量名，不能读）：
        // int x = _ + 1;
        // Object o = _;
        // System.out.println(_);
    }
}
