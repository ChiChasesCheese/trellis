import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

/** 测试用的数据生成器（不属于被测 API）。 */
final class Tickers {
    private Tickers() {}

    /** n 个互不相同的随机代码，长度 1..maxLen 的大写字母。 */
    static List<String> random(Random r, int n, int maxLen) {
        Set<String> seen = new HashSet<>();
        var out = new ArrayList<String>(n);
        while (out.size() < n) {
            int len = 1 + r.nextInt(maxLen);
            var sb = new StringBuilder(len);
            for (int i = 0; i < len; i++) sb.append((char) ('A' + r.nextInt(26)));
            String s = sb.toString();
            if (seen.add(s)) out.add(s);
        }
        return out;
    }

    /** 全部 26^3 个三字母代码。 */
    static List<String> allThreeLetters() {
        var out = new ArrayList<String>(17576);
        for (char a = 'A'; a <= 'Z'; a++)
            for (char b = 'A'; b <= 'Z'; b++)
                for (char c = 'A'; c <= 'Z'; c++) out.add("" + a + b + c);
        return out;
    }

    /** 2^blocks 个字符串，String.hashCode() 全部相同（"Aa" 和 "BB" 的 hashCode 相等，拼接后仍相等）。 */
    static List<String> sameHashCode(int blocks) {
        var out = new ArrayList<String>(1 << blocks);
        for (int mask = 0; mask < (1 << blocks); mask++) {
            var sb = new StringBuilder();
            for (int b = 0; b < blocks; b++) sb.append(((mask >> b) & 1) == 0 ? "Aa" : "BB");
            out.add(sb.toString());
        }
        return out;
    }

    static long[] pack(List<String> tickers) {
        long[] keys = new long[tickers.size()];
        for (int i = 0; i < keys.length; i++) keys[i] = TickerCodec.pack(tickers.get(i));
        return keys;
    }
}
