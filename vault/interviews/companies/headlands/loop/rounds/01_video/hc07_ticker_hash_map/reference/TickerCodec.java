import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.nio.ByteOrder;

/**
 * Part 2：把股票代码压进一个 long。
 *
 * 前提（题面给的）：代码是 1..8 个大写 ASCII 字母。26 个字母只需要 5 个比特（2^5 = 32），8 个字母 = 40 比特，一个 long 绰绰有余。
 * 编码：'A'..'Z' -> 1..26（0 留给「没有字符」），第 i 个字符放在第 [35-5i, 39-5i] 比特；不足 8 个字符的尾部补 0。
 *
 *   "AAPL" -> 00001 00001 10000 01100 00000 00000 00000 00000   (从高位到低位)
 *
 * 性质：1) 不同代码 -> 不同的 long（单射）；2) 合法代码永远 > 0，所以 0 可以当哈希表里的「空格」标记；
 *       3) 比较两个代码 = 比较两个 long，不用 equals，不用分配任何对象。
 */
public final class TickerCodec {
    private TickerCodec() {}

    public static final int MAX_LEN = 8;
    private static final int BITS = 5;
    private static final long FIELD_MASK = 0x1F;
    /** 每个字节只留低 5 位：用于 Long.compress，把 8 个字节里各自的 5 个有效比特压成连续的 40 比特。 */
    private static final long COMPRESS_MASK = 0x1F1F1F1F1F1F1F1FL;
    private static final VarHandle BE_LONG = MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN);

    /** 解析结果：要么是一个合法的 key，要么是一个说明原因的 Invalid。不用异常是因为「非法输入」在行情流里是常态。 */
    public sealed interface Parsed permits Ticker, Invalid {}
    public record Ticker(long key) implements Parsed {}
    public record Invalid(String reason) implements Parsed {}

    public static Parsed parse(CharSequence s) {
        if (s == null) return new Invalid("null");
        int n = s.length();
        if (n == 0) return new Invalid("empty ticker");
        if (n > MAX_LEN) return new Invalid("ticker longer than " + MAX_LEN + ": " + s);
        long key = 0;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c < 'A' || c > 'Z') return new Invalid("not an uppercase ASCII letter at " + i + ": " + s);
            key |= (long) (c - 'A' + 1) << (BITS * (MAX_LEN - 1 - i));
        }
        return new Ticker(key);
    }

    /** 同 parse，但非法时抛 IllegalArgumentException。 */
    public static long pack(CharSequence s) {
        return switch (parse(s)) {
            case Ticker(var key) -> key;
            case Invalid(var reason) -> throw new IllegalArgumentException(reason);
        };
    }

    public static boolean isValidKey(long key) {
        if (key <= 0 || (key >>> (BITS * MAX_LEN)) != 0) return false;
        boolean ended = false;
        for (int i = 0; i < MAX_LEN; i++) {
            long f = (key >>> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
            if (f > 26) return false;
            if (f == 0) ended = true;
            else if (ended) return false;     // 0 之后不能再有字符
        }
        return true;
    }

    public static String unpack(long key) {
        if (!isValidKey(key)) throw new IllegalArgumentException("not a packed ticker: " + key);
        var sb = new StringBuilder(MAX_LEN);
        for (int i = 0; i < MAX_LEN; i++) {
            long f = (key >>> (BITS * (MAX_LEN - 1 - i))) & FIELD_MASK;
            if (f == 0) break;
            sb.append((char) ('A' + f - 1));
        }
        return sb.toString();
    }

    /**
     * 直接从行情报文里读：报文的代码字段是 8 个字节、右侧补空格 (0x20)，例如 "AAPL    "。
     * 一次 VarHandle 读出 8 字节（大端），校验，然后 Long.compress 把每个字节的低 5 位拼起来：
     * 字母 0x41..0x5A 的低 5 位恰好是 1..26，空格 0x20 的低 5 位恰好是 0 —— 和我们的编码天然吻合，不需要任何循环里的移位。
     * 非法（不是「字母+尾部空格」）-> IllegalArgumentException；off+8 > buf.length -> IndexOutOfBoundsException。
     */
    public static long packWire(byte[] buf, int off) {
        long word = (long) BE_LONG.get(buf, off);
        boolean seenSpace = false;
        for (int i = 0; i < MAX_LEN; i++) {
            int b = (int) (word >>> (8 * (MAX_LEN - 1 - i))) & 0xFF;
            if (b == ' ') seenSpace = true;
            else if (seenSpace || b < 'A' || b > 'Z') throw new IllegalArgumentException("bad ticker field at byte " + i);
        }
        if ((word >>> 56) == ' ') throw new IllegalArgumentException("empty ticker field");
        return Long.compress(word, COMPRESS_MASK);
    }
}
