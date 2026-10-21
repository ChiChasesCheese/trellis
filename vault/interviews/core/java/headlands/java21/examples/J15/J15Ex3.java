/**
 * J15 例 3（贴近真实）：位操作——把 8 个字母的股票代码压成一个 long（每个字母 5 位），再解出来；
 * 以及 Integer.compress / expand 的小演示。思路与 kit 里 hc07 的 TickerCodec 一致。
 */
public class J15Ex3 {
    // 8 字节行情字段 "AAPL    "（右补空格）-> 每个字节只保留低 5 位 -> 拼成 40 位
    static final long KEEP_LOW5 = 0x1F1F1F1F1F1F1F1FL;

    static long pack(String ticker8) {
        long word = 0;
        for (int i = 0; i < 8; i++) word = (word << 8) | (byte) ticker8.charAt(i);   // 大端拼成一个 64 位字（和从报文里读 8 字节一样）
        return Long.compress(word, KEEP_LOW5);                                       // 一条指令把分散的 5 位拼到一起
    }

    static String unpack(long key) {
        long spread = Long.expand(key, KEEP_LOW5);          // compress 的逆：把 5 位一组撒回每个字节的低 5 位
        StringBuilder sb = new StringBuilder();
        for (int i = 7; i >= 0; i--) {
            int f = (int) (spread >>> (8 * i)) & 0x1F;
            if (f == 0) break;                               // 空格 0x20 的低 5 位是 0：遇到就结束
            sb.append((char) ('A' + f - 1));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        long k = pack("AAPL    ");
        System.out.println("key = 0x" + Long.toHexString(k) + " (" + Long.toBinaryString(k).length() + " 位有效), unpack = " + unpack(k));
        System.out.println("MSFT -> " + unpack(pack("MSFT    ")));

        // compress / expand 的最小演示：mask 里为 1 的位被"抽出来并靠右排好"
        int v = 0b1011_0110, mask = 0b1111_0000;
        System.out.println("compress(" + Integer.toBinaryString(v) + ", " + Integer.toBinaryString(mask) + ") = "
                + Integer.toBinaryString(Integer.compress(v, mask)));
        System.out.println("expand(1011, 11110000) = " + Integer.toBinaryString(Integer.expand(0b1011, mask)));

        // 其他常用位工具
        System.out.println("bitCount(0b10110110) = " + Integer.bitCount(0b10110110));
        System.out.println("numberOfTrailingZeros(0) = " + Integer.numberOfTrailingZeros(0) + "   <- 约定：0 返回 32，不是 -1");
        System.out.println("highestOneBit(100) = " + Integer.highestOneBit(100));
        System.out.println("rotateLeft(0x80000001, 1) = 0x" + Integer.toHexString(Integer.rotateLeft(0x80000001, 1)));
        System.out.println("reverseBytes(0x01020304) = 0x" + Integer.toHexString(Integer.reverseBytes(0x01020304)));
    }
}
