import java.util.ArrayList;
import java.util.List;

/** J01 例 2（进阶）：紧凑构造器做校验和规范化；防御性拷贝；额外方法；静态工厂；非规范构造器。 */
public class J01Ex2 {

    enum Side { BUY, SELL }

    /** 紧凑构造器 compact canonical constructor：没有参数括号，末尾自动把参数赋给字段。 */
    record Order(long id, String symbol, Side side, long priceTicks, long qty) {
        Order {
            if (id <= 0) throw new IllegalArgumentException("id must be positive: " + id);
            if (priceTicks <= 0) throw new IllegalArgumentException("price must be positive: " + priceTicks);
            if (qty <= 0) throw new IllegalArgumentException("qty must be positive: " + qty);
            if (side == null) throw new NullPointerException("side");
            symbol = symbol.strip().toUpperCase();   // 规范化：给「参数」重新赋值，末尾才写进字段
        }

        /** 自定义方法：和普通类一样。 */
        long notionalTicks() { return Math.multiplyExact(priceTicks, qty); }

        /** 非规范构造器：必须第一句 this(...) 调用规范构造器。 */
        Order(long id, String symbol, Side side, long priceTicks) {
            this(id, symbol, side, priceTicks, 1);
        }

        /** 静态工厂：从一行文本解析。 */
        static Order parse(String line) {
            String[] t = line.split(",");
            return new Order(Long.parseLong(t[0].strip()), t[1], Side.valueOf(t[2].strip()),
                    Long.parseLong(t[3].strip()), Long.parseLong(t[4].strip()));
        }
    }

    /** 带集合字段的 record：用防御性拷贝，否则调用方还能从外面改你的内部状态。 */
    record Basket(String name, List<Order> orders) {
        Basket {
            orders = List.copyOf(orders);   // 不可修改的副本；顺便拒绝 null 元素
        }
    }

    public static void main(String[] args) {
        Order o = Order.parse(" 7 , aapl ,BUY, 18950, 100");
        System.out.println(o);                       // symbol 已被规范化成大写
        System.out.println(o.notionalTicks());
        System.out.println(new Order(8, "msft", Side.SELL, 41_000));  // qty 默认 1

        try {
            new Order(0, "X", Side.BUY, 1, 1);
        } catch (IllegalArgumentException e) {
            System.out.println("拒绝: " + e.getMessage());
        }

        List<Order> src = new ArrayList<>(List.of(o));
        Basket b = new Basket("morning", src);
        src.add(Order.parse("9,tsla,SELL,25000,5"));  // 改外面的列表
        System.out.println("basket 里还是 " + b.orders().size() + " 单");  // 1：因为拷贝过了
        try {
            b.orders().add(o);
        } catch (UnsupportedOperationException e) {
            System.out.println("basket.orders() 不可修改");
        }
    }
}
