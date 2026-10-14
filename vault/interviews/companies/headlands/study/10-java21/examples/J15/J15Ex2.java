import java.util.HexFormat;

/** J15 例 2：字符串小工具——formatted、StringBuilder.repeat、String.repeat/strip/isBlank/lines、HexFormat。 */
public class J15Ex2 {
    public static void main(String[] args) {
        // 1. String.formatted（Java 15）：实例方法版的 String.format，可以接在文本块后面
        String line = "TRADE taker=%d maker=%d px=%d qty=%d".formatted(3, 1, 18950, 100);
        System.out.println(line);
        String report = """
                symbol: %s
                vwap  : %.2f
                """.formatted("AAPL", 189.5731);
        System.out.print(report);

        // 2. StringBuilder.repeat（Java 21）：两个重载：repeat(int codePoint, int count) 和 repeat(CharSequence, int count)
        String bin = Integer.toBinaryString(5);                        // "101" —— 不补前导零
        String padded = new StringBuilder(32).repeat('0', 32 - bin.length()).append(bin).toString();
        System.out.println(padded);
        System.out.println(new StringBuilder().repeat("ab", 3).append('|').repeat("-", 5));
        //    注意：repeat('0', n) 的第一个参数是 int 型的码点。写成 repeat("0", n) 也行，但走的是 CharSequence 重载。

        // 3. String.repeat（Java 11）、strip / isBlank / lines（Java 11）
        System.out.println("=".repeat(10));
        System.out.println("[" + "  　hi  ".strip() + "]  <- strip 会去掉 Unicode 空白；trim 不会去全角空格: [" + "  　hi  ".trim() + "]");
        System.out.println("isBlank: " + "   ".isBlank() + " / isEmpty: " + "   ".isEmpty());
        System.out.println("lines: " + "a\nb\r\nc".lines().toList());

        // 4. HexFormat（Java 17）：十六进制的官方工具
        byte[] bs = {10, 27, (byte) 255};
        HexFormat hf = HexFormat.of();
        System.out.println("formatHex           = " + hf.formatHex(bs));
        System.out.println("withUpperCase       = " + hf.withUpperCase().formatHex(bs));
        System.out.println("delimiter+prefix    = " + HexFormat.ofDelimiter(":").withPrefix("0x").formatHex(bs));
        System.out.println("parseHex(\"0a1bff\")  = " + java.util.Arrays.toString(hf.parseHex("0a1bff")));
        System.out.println("toHexDigits(int)    = " + hf.withUpperCase().toHexDigits(48879) + "  (固定 8 位，自动补零)");
        System.out.println("toHexDigits(long)   = " + hf.toHexDigits(255L));
        System.out.println("fromHexDigits(\"ff\") = " + HexFormat.fromHexDigits("ff"));
    }
}
