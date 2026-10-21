/** J07 旧写法：多行字符串只能 "\n" + 拼接 + 转义双引号。内容和结构被符号淹没。 */
public class J07Old {

    public static void main(String[] args) {
        // 一小段 JSON：每个双引号都要转义，每行都要 \n 和 +
        String json = "{\n" +
                "  \"symbol\": \"AAPL\",\n" +
                "  \"side\": \"BUY\",\n" +
                "  \"qty\": 100\n" +
                "}\n";
        System.out.print(json);

        // 多行输入（测试里的样例输入）
        String input = "# sample\n" +
                "LIMIT 1 SELL 101 5\n" +
                "LIMIT 2 BUY 101 3\n";
        System.out.println(input.split("\n").length + " lines");

        // 一个更长的 SQL：漏了一个空格，两行粘在一起
        String sql = "SELECT symbol, SUM(qty) " +
                "FROM fills" +                    // ← 这里少了一个空格
                "WHERE side = 'BUY' " +
                "GROUP BY symbol";
        System.out.println(sql);
    }
}
