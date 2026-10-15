import java.util.*;

/** J15 旧写法（Java 8 风格）：溢出悄悄回绕；手写溢出检测；手写补零、手写 hex。 */
public class J15Old {
    // 手写 clamp：嵌套 Math.max/min，顺序一不小心就写反
    static int clamp(int v, int lo, int hi) { return Math.max(lo, Math.min(hi, v)); }

    // 手写 hex（byte[] -> "0a1b"）
    static String hex(byte[] bs) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bs) sb.append(String.format("%02x", b));
        return sb.toString();
    }

    public static void main(String[] args) {
        // 痛点 1：int 溢出不报错
        int px = 2_000_000_000, q = 2;
        int notional = px * q;
        System.out.println("px*q = " + notional + "   <- 悄悄变成负数，没有任何异常");

        // 痛点 2：手写溢出检测又长又容易错
        long a = Long.MAX_VALUE, b = 1;
        long sum = a + b;
        boolean overflow = ((a ^ sum) & (b ^ sum)) < 0;    // 符号位技巧，没人看得懂
        System.out.println("long 相加溢出? " + overflow + ", sum = " + sum);

        // 痛点 3：补零、重复字符
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.append('0');       // 手写循环拼 5 个 0
        System.out.println(sb + " " + String.format("%08d", 42) + " " + hex(new byte[]{10, 27, (byte) 255}));
        System.out.println(clamp(150, 0, 100) + " " + String.format("id=%d px=%d", 7, 18950));
    }
}
