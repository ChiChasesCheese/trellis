import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;

/** J06 例 3（贴近真实）：手写 equals；弱类型配置读取；对事件流做「只挑某一种」的过滤。 */
public class J06Ex3 {

    // ---- 1. 非 record 类的 equals：这是 instanceof 模式最常见的用法 ----
    static final class Instrument {
        final String ticker;
        final String exchange;
        Instrument(String ticker, String exchange) { this.ticker = ticker; this.exchange = exchange; }

        @Override public boolean equals(Object o) {
            return o instanceof Instrument other                   // 判断 + 转型 + 命名，一行
                    && ticker.equals(other.ticker)
                    && exchange.equals(other.exchange);
        }
        @Override public int hashCode() { return Objects.hash(ticker, exchange); }
    }

    // ---- 2. 配置值：来自 Map<String, Object>（比如解析 JSON 之后） ----
    static long readLong(Map<String, Object> cfg, String key, long dflt) {
        Object v = cfg.get(key);
        if (v instanceof Integer i) return i;
        if (v instanceof Long l) return l;
        if (v instanceof String s && !s.isBlank()) return Long.parseLong(s.trim());
        return dflt;
    }

    // ---- 3. 事件流里挑成交 ----
    sealed interface Event permits Trade, Rested, Rejected {}
    record Trade(long px, long qty) implements Event {}
    record Rested(long id) implements Event {}
    record Rejected(long id, String why) implements Event {}

    static long tradedQty(List<Event> events) {
        long total = 0;
        for (Event e : events) {
            if (e instanceof Trade t) total += t.qty();
        }
        return total;
    }

    /** 同样的过滤，带 record 模式（J04）：直接取出字段，再加条件。 */
    static List<String> bigTrades(List<Event> events, long minQty) {
        List<String> out = new ArrayList<>();
        for (Event e : events) {
            if (e instanceof Trade(var px, var qty) && qty >= minQty) out.add(qty + "@" + px);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(new Instrument("AAPL", "XNAS").equals(new Instrument("AAPL", "XNAS")));
        System.out.println(new Instrument("AAPL", "XNAS").equals(new Instrument("AAPL", "XNYS")));
        System.out.println(new Instrument("AAPL", "XNAS").equals("AAPL"));
        System.out.println(new Instrument("AAPL", "XNAS").equals(null));

        Map<String, Object> cfg = Map.of("a", 1, "b", 2L, "c", " 30 ");
        System.out.println(readLong(cfg, "a", -1) + " " + readLong(cfg, "b", -1) + " " + readLong(cfg, "c", -1) + " " + readLong(cfg, "z", -1));

        List<Event> evs = List.of(new Trade(100, 5), new Rested(1), new Trade(101, 12), new Rejected(2, "qty"));
        System.out.println(tradedQty(evs));
        System.out.println(bigTrades(evs, 10));
    }
}
