/** J05 例 1（最简单）：箭头形式 + 多标签 + 直接产出值；字符串、枚举。 */
public class J05Ex1 {

    enum Side { BUY, SELL, SHORT }

    static int sign(Side s) {
        return switch (s) {
            case BUY -> 1;
            case SELL, SHORT -> -1;        // 多个标签，逗号分隔，不再靠 fall-through
        };                                  // 枚举全部列出：不需要 default，编译器检查穷尽
    }

    static String describe(String cmd) {
        return switch (cmd) {
            case "LIMIT", "limit" -> "limit order";
            case "MARKET" -> "market order";
            case "CANCEL" -> "cancel";
            default -> "unknown: " + cmd;   // String 是开放集合，必须有 default
        };
    }

    public static void main(String[] args) {
        for (Side s : Side.values()) System.out.println(s + " -> " + sign(s));
        System.out.println(describe("limit"));
        System.out.println(describe("CANCEL"));
        System.out.println(describe("foo"));

        // 箭头形式也可以当语句用：不产出值，也没有 fall-through
        int n = 2;
        switch (n) {
            case 1 -> System.out.println("one");
            case 2 -> System.out.println("two");
            default -> System.out.println("many");
        }
    }
}
