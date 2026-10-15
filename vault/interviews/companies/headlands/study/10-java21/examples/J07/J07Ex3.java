import java.util.ArrayList;
import java.util.List;

/**
 * J07 例 3（贴近真实）：测试里「多行输入 -> 多行期望输出」。这是本 kit 的 test/*.java 里最常用的写法：
 * 把样例原封不动地粘进文本块，再用 lines() 拆成行。
 */
public class J07Ex3 {

    /** 被测函数：每个 LIMIT 命令累加数量，每个 BUY 单报一行；忽略空行和 # 注释。 */
    static List<String> summarize(List<String> lines) {
        List<String> out = new ArrayList<>();
        long total = 0;
        for (String raw : lines) {
            String line = raw.strip();
            if (line.isEmpty() || line.startsWith("#")) continue;
            String[] t = line.split("\\s+");
            long qty = Long.parseLong(t[4]);
            total += qty;
            if (t[2].equals("BUY")) out.add("BUY id=" + t[1] + " qty=" + qty);
        }
        out.add("total=" + total);
        return out;
    }

    /** 测试辅助：文本块 -> 行列表。 */
    static List<String> lines(String block) {
        return block.lines().toList();
    }

    public static void main(String[] args) {
        var input = lines("""
                # 样例
                LIMIT 1 SELL 101 5
                LIMIT 2 BUY 101 3

                """);                                           // 中间的空行、末尾的空行都是内容的一部分

        var expected = lines("""
                BUY id=2 qty=3
                total=8
                """);

        var actual = summarize(input);
        System.out.println(actual.equals(expected) ? "PASS" : "FAIL " + actual);

        // JSON 和 SQL 也是文本块最常见的用途
        String sql = """
                SELECT symbol, SUM(qty) AS total
                FROM fills
                WHERE side = 'BUY'
                GROUP BY symbol
                """;
        System.out.print(sql);
    }
}
