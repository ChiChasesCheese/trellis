/** J07 例 2（进阶）：转义序列；\<换行> 续行；\s 保留行尾空格；"""  自身的转义；stripIndent / translateEscapes / formatted。 */
public class J07Ex2 {

    public static void main(String[] args) {
        // 行尾的空格默认被删掉（编辑器常常自动加行尾空格，所以编译器帮你去掉）。
        // 注意 \u0020 是 Unicode 转义：编译最早阶段就被换成一个真正的空格，所以它和手敲的行尾空格一样会被删掉。
        String a = "x   \ny";                                  // 普通字符串：行内的空格都保留，长度 6
        String trimmed = """
                x   \u0020
                y""";                                          // x 后面的 4 个空格都被删，只剩 "x\ny"，长度 3
        System.out.println(a.length() + " " + trimmed.length());

        // \s 表示一个空格，且在「去除行尾空格」之后才被处理，所以能保住行尾的空格
        String keepTrailing = """
                x\s\s\s
                y""";
        System.out.println("[" + keepTrailing.replace("\n", "|") + "]");     // [x   |y]

        // \<换行>：把下一行接到本行，不产生换行。适合很长的一行
        String longLine = """
                SELECT symbol, SUM(qty) \
                FROM fills \
                WHERE side = 'BUY'""";
        System.out.println(longLine);

        // \n 、\t 、\\ 仍然可用；\""" 用来在内容里放三个连续引号
        String esc = """
                tab:\there
                quotes: \"""three\"""
                backslash: \\
                """;
        System.out.print(esc);

        // 方法：stripIndent 对一个普通字符串执行同样的「去公共缩进」；formatted 填充占位符
        String raw = "   a\n     b\n   c";
        System.out.println(raw.stripIndent().replace("\n", "|"));            // a|  b|c

        String report = """
                symbol=%s qty=%d
                """.formatted("AAPL", 100);
        System.out.print(report);

        // translateEscapes：把「文本里的反斜杠转义」变成真正的字符（用于从配置文件读出来的字符串）
        System.out.println("a\\tb".translateEscapes().equals("a\tb"));      // true
    }
}
