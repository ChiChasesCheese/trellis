import java.util.HashMap;
import java.util.Map;

/** J01 例 1（最简单）：一行声明一个 record，免费得到构造器、访问器、equals、hashCode、toString。 */
public class J01Ex1 {

    record Fill(String symbol, long priceTicks, long qty) {}

    public static void main(String[] args) {
        Fill a = new Fill("AAPL", 18_950, 100);
        Fill b = new Fill("AAPL", 18_950, 100);

        System.out.println(a);                              // toString
        System.out.println(a.symbol() + " " + a.qty());     // 访问器：注意叫 symbol() 不是 getSymbol()
        System.out.println(a.equals(b));                    // 按内容比较 -> true
        System.out.println(a == b);                         // 引用比较 -> false
        System.out.println(a.hashCode() == b.hashCode());   // true

        // 因为 equals/hashCode 按内容算，record 天然能当 Map 的 key
        Map<Fill, String> notes = new HashMap<>();
        notes.put(a, "first");
        System.out.println(notes.get(b));                   // 用「内容相同的另一个对象」也查得到 -> first

        // record 不能改字段：没有 setter，字段是 private final
        // a.qty = 5;  // 编译错误
    }
}
