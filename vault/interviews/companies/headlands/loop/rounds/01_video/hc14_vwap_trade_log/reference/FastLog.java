import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * hc14 Part 4：热路径版本。输入是整块 byte[]（整个日志文件读进内存），一遍扫完：
 * 不建 String、不用正则、不装箱；symbol（最长 10 个字符，每个 6 位）打包成一个 long 当哈希键，
 * 每个 symbol 的累计值放在并行的 long[] 里（开放寻址）。结果和 {@link TradeLog#analyze} 逐字段一致。
 */
public final class FastLog {
    private static final byte[] CODE = new byte[256]; // symbol 字符 → 1..37，0 = 非法
    private static final long GOLDEN = 0x9E3779B97F4A7C15L;

    static {
        for (int c = 'A'; c <= 'Z'; c++) CODE[c] = (byte) (1 + c - 'A');
        for (int c = '0'; c <= '9'; c++) CODE[c] = (byte) (27 + c - '0');
        CODE['.'] = 37;
    }

    private int bits = 10;
    private long[] keys = new long[1 << bits]; // 0 = 空槽（合法键一定非 0）
    private long[] count = new long[1 << bits], volume = new long[1 << bits], notional = new long[1 << bits];
    private long[] min = new long[1 << bits], max = new long[1 << bits];
    private int used;

    private FastLog() {}

    public static TradeLog.Report analyze(byte[] data) {
        return new FastLog().run(data);
    }

    private TradeLog.Report run(byte[] data) {
        int n = data.length, pos = 0;
        long accepted = 0, malformed = 0;
        while (pos < n) {
            int end = pos;
            while (end < n && data[end] != '\n') end++;
            if (end > pos) {
                if (line(data, pos, end)) accepted++;
                else malformed++;
            }
            pos = end + 1;
        }
        var out = new ArrayList<TradeLog.SymbolStats>(used);
        for (int i = 0; i < keys.length; i++) {
            if (keys[i] == 0) continue;
            out.add(new TradeLog.SymbolStats(decode(keys[i]), count[i], volume[i], notional[i],
                    TradeLog.vwap(notional[i], volume[i]), min[i], max[i]));
        }
        out.sort(Comparator.comparing(TradeLog.SymbolStats::symbol));
        return new TradeLog.Report(List.copyOf(out), accepted, malformed);
    }

    private static boolean digit(byte b) {
        return b >= '0' && b <= '9';
    }

    private boolean line(byte[] b, int s, int e) {
        int p = s, d = 0;
        while (p < e && digit(b[p])) { // ts：1..18 位数字
            p++;
            if (++d > 18) return false;
        }
        if (d == 0 || p >= e || b[p] != ',') return false;
        p++;
        long key = 0;
        int len = 0;
        while (p < e && b[p] != ',') { // symbol：1..10 个合法字符，打包
            int code = CODE[b[p] & 0xFF];
            if (code == 0 || ++len > TradeLog.MAX_SYMBOL_LEN) return false;
            key = (key << 6) | code;
            p++;
        }
        if (len == 0 || p >= e) return false;
        p++;
        long whole = 0, frac = 0;
        int wd = 0, fd = 0;
        while (p < e && digit(b[p])) {
            whole = whole * 10 + (b[p++] - '0');
            if (++wd > 9) return false;
        }
        if (wd == 0) return false;
        if (p < e && b[p] == '.') {
            p++;
            while (p < e && digit(b[p])) {
                frac = frac * 10 + (b[p++] - '0');
                if (++fd > 4) return false;
            }
            if (fd == 0) return false;
        }
        if (p >= e || b[p] != ',') return false;
        p++;
        for (int i = fd; i < 4; i++) frac *= 10;
        long price = whole * TradeLog.SCALE + frac;
        if (price <= 0) return false;
        long qty = 0;
        int qd = 0;
        while (p < e && digit(b[p])) {
            qty = qty * 10 + (b[p++] - '0');
            if (++qd > 12) return false;
        }
        if (qd == 0 || p != e || qty == 0) return false;
        long hi = Math.multiplyHigh(price, qty), lo = price * qty;
        if (hi != 0 || lo < 0) return false; // price × qty 装不进 long：这一行算坏行
        add(key, price, qty, lo);
        return true;
    }

    private void add(long key, long price, long qty, long value) {
        int mask = keys.length - 1;
        int i = (int) ((key * GOLDEN) >>> (64 - bits));
        while (keys[i] != 0 && keys[i] != key) i = (i + 1) & mask;
        if (keys[i] == 0) {
            keys[i] = key;
            count[i] = 1;
            volume[i] = qty;
            notional[i] = value;
            min[i] = max[i] = price;
            if (++used * 2 > keys.length) grow();
            return;
        }
        volume[i] = Math.addExact(volume[i], qty);
        notional[i] = Math.addExact(notional[i], value);
        count[i]++;
        if (price < min[i]) min[i] = price;
        if (price > max[i]) max[i] = price;
    }

    private void grow() {
        long[] k = keys, c = count, v = volume, nt = notional, mn = min, mx = max;
        bits++;
        int cap = 1 << bits, mask = cap - 1;
        keys = new long[cap];
        count = new long[cap];
        volume = new long[cap];
        notional = new long[cap];
        min = new long[cap];
        max = new long[cap];
        for (int j = 0; j < k.length; j++) {
            if (k[j] == 0) continue;
            int i = (int) ((k[j] * GOLDEN) >>> (64 - bits));
            while (keys[i] != 0) i = (i + 1) & mask;
            keys[i] = k[j];
            count[i] = c[j];
            volume[i] = v[j];
            notional[i] = nt[j];
            min[i] = mn[j];
            max[i] = mx[j];
        }
    }

    private static String decode(long key) {
        var sb = new StringBuilder(TradeLog.MAX_SYMBOL_LEN);
        while (key != 0) {
            int code = (int) (key & 63);
            sb.append(code <= 26 ? (char) ('A' + code - 1) : code <= 36 ? (char) ('0' + code - 27) : '.');
            key >>>= 6;
        }
        return sb.reverse().toString();
    }
}
