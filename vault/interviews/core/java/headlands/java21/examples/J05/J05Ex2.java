/** J05 例 2（进阶）：yield、分支里抛异常、结果类型的统一、冒号形式的 yield、switch 当方法参数。 */
public class J05Ex2 {

    enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

    /** 分支需要多条语句 -> 用 {} 块，用 yield 给出这个分支的值。 */
    static int tradingHours(Day d) {
        return switch (d) {
            case MON, TUE, WED, THU, FRI -> {
                int open = 9, close = 16;                 // 块内可以声明局部变量，作用域只在这个分支
                yield close - open;
            }
            case SAT, SUN -> 0;
        };
    }

    /** 分支里可以直接 throw：这个分支就「不产出值」，也合法。 */
    static long parsePositive(String s) {
        return switch (s.isEmpty() ? 0 : 1) {
            case 0 -> throw new IllegalArgumentException("empty");
            default -> {
                long v = Long.parseLong(s);
                if (v <= 0) throw new IllegalArgumentException("not positive: " + v);
                yield v;
            }
        };
    }

    /** 冒号形式的 switch 表达式：不用箭头，改用 yield 给值（仍可 fall-through，不推荐）。 */
    static String oldStyleExpr(int n) {
        return switch (n) {
            case 1:
                yield "one";
            case 2:
            case 3:
                yield "two or three";
            default:
                yield "many";
        };
    }

    /** 各分支类型不同时，整个表达式的类型是它们的「共同类型」。 */
    static double mixedTypes(int k) {
        var x = switch (k) {
            case 0 -> 1;          // int
            case 1 -> 2.5;        // double
            default -> 3L;        // long
        };                          // x 的类型是 double（数值提升）
        return x;
    }

    public static void main(String[] args) {
        for (Day d : new Day[]{Day.MON, Day.SAT}) System.out.println(d + " " + tradingHours(d));
        System.out.println(parsePositive("42"));
        for (String bad : new String[]{"", "-3"}) {
            try {
                parsePositive(bad);
            } catch (IllegalArgumentException e) {
                System.out.println("rejected: " + e.getMessage());
            }
        }
        System.out.println(oldStyleExpr(1) + " | " + oldStyleExpr(3) + " | " + oldStyleExpr(9));
        System.out.println(mixedTypes(0) + " " + mixedTypes(1) + " " + mixedTypes(2));

        // switch 表达式可以直接作为方法参数、字符串拼接的一部分
        int level = 3;
        System.out.println("level is " + switch (level) { case 1 -> "low"; case 2 -> "mid"; default -> "high"; });
    }
}
