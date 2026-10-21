import java.util.*;

/** J18 旧写法（Java 7）：匿名 Comparator 类；比较里手写 null 与 tie-break；接口加方法会破坏所有实现者。 */
public class J18Old {
    static final class Order {
        final long id; final String side; final long px; final long ts;
        Order(long id, String side, long px, long ts) { this.id = id; this.side = side; this.px = px; this.ts = ts; }
        public String toString() { return "Order#" + id + "(" + px + "@" + ts + ")"; }
    }

    public static void main(String[] args) {
        List<Order> orders = new ArrayList<>(List.of(
                new Order(1, "BUY", 100, 5), new Order(2, "BUY", 101, 3), new Order(3, "BUY", 101, 1), new Order(4, "BUY", 99, 2)));

        // 买盘优先级：价格高优先；价格相同，时间早优先；再相同按 id
        Collections.sort(orders, new Comparator<Order>() {
            @Override public int compare(Order a, Order b) {
                int c = Long.compare(b.px, a.px);              // 降序：把 a、b 对调
                if (c != 0) return c;
                c = Long.compare(a.ts, b.ts);
                if (c != 0) return c;
                return Long.compare(a.id, b.id);
            }
        });
        System.out.println(orders);

        // 经典 bug：用减法比较
        int a = Integer.MAX_VALUE, b = -1;
        System.out.println("a - b = " + (a - b) + "  (溢出成负数，说明 a<b？)  Integer.compare(a, b) = " + Integer.compare(a, b));
    }
}
