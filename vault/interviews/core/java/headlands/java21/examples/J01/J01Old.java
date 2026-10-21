import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/** J01 旧写法：Java 8 风格的「一笔成交」值对象。光是装 3 个字段就要 40 多行。 */
public class J01Old {

    /** 手写版：每个字段 3 处样板（字段、构造器赋值、getter）+ equals/hashCode/toString。 */
    static final class Fill {
        private final String symbol;
        private final long priceTicks;
        private final long qty;

        Fill(String symbol, long priceTicks, long qty) {
            this.symbol = symbol;
            this.priceTicks = priceTicks;
            this.qty = qty;
        }

        String getSymbol() { return symbol; }
        long getPriceTicks() { return priceTicks; }
        long getQty() { return qty; }

        @Override public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Fill f = (Fill) o;
            return priceTicks == f.priceTicks && qty == f.qty && Objects.equals(symbol, f.symbol);
        }

        @Override public int hashCode() { return Objects.hash(symbol, priceTicks, qty); }

        @Override public String toString() {
            return "Fill{symbol=" + symbol + ", priceTicks=" + priceTicks + ", qty=" + qty + "}";
        }
    }

    /** 忘记写 equals/hashCode 的版本：看起来一样，放进 HashMap 却找不到。 */
    static final class ForgetfulFill {
        final String symbol;
        final long qty;
        ForgetfulFill(String symbol, long qty) { this.symbol = symbol; this.qty = qty; }
    }

    public static void main(String[] args) {
        Fill a = new Fill("AAPL", 18_950, 100);
        Fill b = new Fill("AAPL", 18_950, 100);
        System.out.println(a);
        System.out.println("a.equals(b) = " + a.equals(b));

        Map<ForgetfulFill, String> m = new HashMap<>();
        m.put(new ForgetfulFill("AAPL", 100), "first");
        System.out.println("忘记 equals 的版本，用「相同内容」的新对象去查 -> " + m.get(new ForgetfulFill("AAPL", 100)));
    }
}
