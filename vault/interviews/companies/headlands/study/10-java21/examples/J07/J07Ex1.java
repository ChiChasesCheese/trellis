/** J07 例 1（最简单）：三个引号开头，换行后写内容；缩进由「最左的内容 / 结束符」决定；是否带结尾换行取决于结束符的位置。 */
public class J07Ex1 {

    public static void main(String[] args) {
        // 1. 基本形式：开头 """ 后面必须立刻换行；内容里可以直接写双引号
        String json = """
                {
                  "symbol": "AAPL",
                  "qty": 100
                }
                """;
        System.out.print(json);

        // 2. 和旧写法得到的字符串完全相同
        String old = "{\n  \"symbol\": \"AAPL\",\n  \"qty\": 100\n}\n";
        System.out.println(json.equals(old));                    // true
        System.out.println(json == old);                         // 也是 true：两者都是编译期常量，指向常量池里同一个 String

        // 3. 结束符 """ 的位置决定「要不要结尾的换行」
        String withNl = """
                hello
                """;
        String withoutNl = """
                hello""";
        System.out.println(withNl.length() + " " + withoutNl.length());   // 6 5

        // 4. 结束符的缩进比内容更靠左 -> 内容保留多出来的缩进
        String indented = """
                    four more spaces
                """;
        System.out.println("[" + indented + "]");

        // 5. 它就是普通的 String，可以直接调用 String 的所有方法
        System.out.println(json.lines().count() + " lines");
    }
}
