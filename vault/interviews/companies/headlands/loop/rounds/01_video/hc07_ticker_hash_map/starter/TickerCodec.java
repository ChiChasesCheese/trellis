/**
 * Part 2：把 1..8 个大写 ASCII 字母的股票代码压进一个 long，不分配、不用 String 哈希。
 *
 * 约定的编码（测试会检查 "AAPL" 的具体值）：'A'..'Z' -> 1..26，每个字符 5 比特；
 * 第 i 个字符（i 从 0 起）放在第 [35-5i, 39-5i] 比特；不足 8 个字符的尾部补 0。结果总是 > 0 且 < 2^40。
 */
public final class TickerCodec {
    private TickerCodec() {}

    public static final int MAX_LEN = 8;

    public sealed interface Parsed permits Ticker, Invalid {}
    public record Ticker(long key) implements Parsed {}
    public record Invalid(String reason) implements Parsed {}

    /** null、空、超过 8 个字符、含非 A-Z 字符 -> Invalid；否则 Ticker。 */
    public static Parsed parse(CharSequence s) { throw new UnsupportedOperationException("TODO"); }

    /** 同 parse，非法时抛 IllegalArgumentException。提示：对 parse 的结果写一个模式匹配 switch。 */
    public static long pack(CharSequence s) { throw new UnsupportedOperationException("TODO"); }

    /** key 是不是一个合法的打包结果（> 0，< 2^40，字段 <= 26，第一个 0 字段之后全是 0）。 */
    public static boolean isValidKey(long key) { throw new UnsupportedOperationException("TODO"); }

    /** pack 的反函数；非法 key 抛 IllegalArgumentException。 */
    public static String unpack(long key) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 行情报文里的代码字段：8 个字节，大写字母 + 右侧补空格 (0x20)，例如 "AAPL    "，从 buf[off] 开始。
     * 提示：VarHandle（MethodHandles.byteArrayViewVarHandle）一次读 8 字节；Long.compress 拼比特。
     * 不是「若干字母 + 若干尾部空格」（含全空格、前导空格、中间空格、小写）-> IllegalArgumentException；
     * off+8 > buf.length -> IndexOutOfBoundsException。
     */
    public static long packWire(byte[] buf, int off) { throw new UnsupportedOperationException("TODO"); }
}
