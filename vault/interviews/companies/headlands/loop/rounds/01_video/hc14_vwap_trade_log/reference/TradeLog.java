import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalLong;
import java.util.TreeMap;

/**
 * hc14 Part 1：成交日志 → 每个 symbol 的 VWAP / 成交量 / 笔数 / 最低价 / 最高价。
 * 一行 = {@code ts_ms,symbol,price,qty}；价格是十进制字符串（最多 4 位小数），内部用 long 定点数（1 单位 = 0.0001）。
 */
public final class TradeLog {
    private TradeLog() {}

    /** 定点数的放大倍数：价格 187.25 存成 1_872_500。 */
    public static final long SCALE = 10_000;
    public static final int MAX_SYMBOL_LEN = 10;

    /** 一笔合法成交。构造器校验，所以手里有 Trade 就说明 price × qty 一定装得进 long。 */
    public record Trade(long tsMs, String symbol, long price, long qty) {
        public Trade {
            Objects.requireNonNull(symbol, "symbol");
            if (tsMs < 0) throw new IllegalArgumentException("negative timestamp: " + tsMs);
            if (!validSymbol(symbol)) throw new IllegalArgumentException("invalid symbol: " + symbol);
            if (price <= 0) throw new IllegalArgumentException("non-positive price: " + price);
            if (qty <= 0) throw new IllegalArgumentException("non-positive quantity: " + qty);
            Math.multiplyExact(price, qty);
        }

        /** price × qty，单位 0.0001。 */
        public long notional() {
            return price * qty;
        }
    }

    /** 某个 symbol 的统计。notional = Σ price × qty；vwap = notional / volume 四舍五入（半数向上）。 */
    public record SymbolStats(String symbol, long count, long volume, long notional, long vwap, long minPrice, long maxPrice) {}

    /** symbols 按 symbol 升序；accepted + malformed = 非空行数。 */
    public record Report(List<SymbolStats> symbols, long accepted, long malformed) {}

    public static boolean validSymbol(String s) {
        int n = s.length();
        if (n == 0 || n > MAX_SYMBOL_LEN) return false;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (!((c >= 'A' && c <= 'Z') || isDigit(c) || c == '.')) return false;
        }
        return true;
    }

    private static boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    /** 价格字符串 → 定点 long；不合法（语法见 problem.md）返回 empty。 */
    public static OptionalLong parsePrice(String s) {
        int n = s.length(), i = 0, intDigits = 0;
        long whole = 0;
        while (i < n && isDigit(s.charAt(i))) {
            whole = whole * 10 + (s.charAt(i) - '0');
            i++;
            if (++intDigits > 9) return OptionalLong.empty();
        }
        if (intDigits == 0) return OptionalLong.empty();
        long frac = 0;
        int fracDigits = 0;
        if (i < n && s.charAt(i) == '.') {
            i++;
            while (i < n && isDigit(s.charAt(i))) {
                frac = frac * 10 + (s.charAt(i) - '0');
                i++;
                if (++fracDigits > 4) return OptionalLong.empty();
            }
            if (fracDigits == 0) return OptionalLong.empty();
        }
        if (i != n) return OptionalLong.empty();
        for (int d = fracDigits; d < 4; d++) frac *= 10;
        long price = whole * SCALE + frac;
        return price > 0 ? OptionalLong.of(price) : OptionalLong.empty();
    }

    /** 只含数字、长度 1..maxDigits 的 [from, to) → 值；否则 -1。 */
    private static long digits(String s, int from, int to, int maxDigits) {
        int len = to - from;
        if (len < 1 || len > maxDigits) return -1;
        long v = 0;
        for (int i = from; i < to; i++) {
            char c = s.charAt(i);
            if (!isDigit(c)) return -1;
            v = v * 10 + (c - '0');
        }
        return v;
    }

    /** 一行 → Trade；任何一条规则不满足（见 problem.md）返回 empty。 */
    public static Optional<Trade> parseLine(String line) {
        int c1 = line.indexOf(',');
        if (c1 < 0) return Optional.empty();
        int c2 = line.indexOf(',', c1 + 1);
        if (c2 < 0) return Optional.empty();
        int c3 = line.indexOf(',', c2 + 1);
        if (c3 < 0 || line.indexOf(',', c3 + 1) >= 0) return Optional.empty();
        long ts = digits(line, 0, c1, 18);
        long qty = digits(line, c3 + 1, line.length(), 12);
        if (ts < 0 || qty <= 0) return Optional.empty();
        var price = parsePrice(line.substring(c2 + 1, c3));
        if (price.isEmpty()) return Optional.empty();
        try {
            return Optional.of(new Trade(ts, line.substring(c1 + 1, c2), price.getAsLong(), qty));
        } catch (IllegalArgumentException | ArithmeticException e) {
            return Optional.empty(); // 非法 symbol，或 price × qty 溢出 long
        }
    }

    /** notional / volume 四舍五入，半数向上；整个过程不会溢出。volume ≤ 0 或 notional < 0 → IAE。 */
    public static long vwap(long notional, long volume) {
        if (volume <= 0 || notional < 0) throw new IllegalArgumentException("volume must be positive, notional non-negative");
        long q = notional / volume, r = notional % volume;
        return r >= volume - r ? q + 1 : q;
    }

    private static final class Acc {
        long count, volume, notional, min = Long.MAX_VALUE, max;
    }

    /** 逐行解析并汇总。空串（长度 0）的行直接跳过，不计数；null 元素 → NPE。累加溢出 → ArithmeticException。 */
    public static Report analyze(List<String> lines) {
        var by = new TreeMap<String, Acc>();
        long accepted = 0, malformed = 0;
        for (String line : lines) {
            if (line.isEmpty()) continue;
            var parsed = parseLine(line);
            if (parsed.isEmpty()) {
                malformed++;
                continue;
            }
            var t = parsed.get();
            var a = by.computeIfAbsent(t.symbol(), _ -> new Acc());
            a.volume = Math.addExact(a.volume, t.qty());
            a.notional = Math.addExact(a.notional, t.notional());
            a.count++;
            a.min = Math.min(a.min, t.price());
            a.max = Math.max(a.max, t.price());
            accepted++;
        }
        var out = new ArrayList<SymbolStats>(by.size());
        by.forEach((sym, a) -> out.add(new SymbolStats(sym, a.count, a.volume, a.notional, vwap(a.notional, a.volume), a.min, a.max)));
        return new Report(List.copyOf(out), accepted, malformed);
    }

    /** 定点数 → "整数部分.四位小数"，如 1872500 → "187.2500"。负数 → IAE。 */
    public static String formatPrice(long units) {
        if (units < 0) throw new IllegalArgumentException("negative: " + units);
        return "%d.%04d".formatted(units / SCALE, units % SCALE);
    }

    /** 每个 symbol 一行，最后一行汇总。 */
    public static List<String> render(Report r) {
        var out = new ArrayList<String>();
        for (var s : r.symbols()) {
            out.add("%s count=%d volume=%d notional=%s vwap=%s min=%s max=%s".formatted(s.symbol(), s.count(), s.volume(),
                    formatPrice(s.notional()), formatPrice(s.vwap()), formatPrice(s.minPrice()), formatPrice(s.maxPrice())));
        }
        out.add("accepted=%d malformed=%d".formatted(r.accepted(), r.malformed()));
        return List.copyOf(out);
    }
}
