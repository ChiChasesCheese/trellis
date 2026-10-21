import java.util.Map;
import java.util.Objects;

/** J06 旧写法：instanceof 之后必须再强转一次——同一个类型写两遍。 */
public class J06Old {

    static final class Price {
        final String symbol;
        final long ticks;
        Price(String symbol, long ticks) { this.symbol = symbol; this.ticks = ticks; }

        @Override public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Price)) return false;
            Price other = (Price) o;                         // ← 第二次写 Price
            return ticks == other.ticks && Objects.equals(symbol, other.symbol);
        }
        @Override public int hashCode() { return Objects.hash(symbol, ticks); }
    }

    /** 配置值：来自 Map<String, Object>，类型要自己判断。 */
    static long readLong(Map<String, Object> cfg, String key, long dflt) {
        Object v = cfg.get(key);
        if (v instanceof Integer) {
            return ((Integer) v).longValue();                // 又是判断 + 强转
        } else if (v instanceof Long) {
            return (Long) v;
        } else if (v instanceof String) {
            return Long.parseLong(((String) v).trim());
        }
        return dflt;
    }

    public static void main(String[] args) {
        System.out.println(new Price("AAPL", 5).equals(new Price("AAPL", 5)));
        Map<String, Object> cfg = Map.of("a", 1, "b", 2L, "c", " 30 ");
        System.out.println(readLong(cfg, "a", -1) + " " + readLong(cfg, "b", -1) + " " + readLong(cfg, "c", -1) + " " + readLong(cfg, "z", -1));
    }
}
