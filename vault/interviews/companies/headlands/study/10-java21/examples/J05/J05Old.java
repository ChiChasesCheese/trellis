/** J05 旧写法：Java 8 的 switch 是「语句」，靠赋值外部变量产出结果；忘记 break 就 fall-through。 */
public class J05Old {

    enum Side { BUY, SELL, SHORT }

    /** 旧写法 1：用临时变量 + 每个分支 break。 */
    static int sign(Side s) {
        int result;
        switch (s) {
            case BUY:
                result = 1;
                break;
            case SELL:
            case SHORT:                 // 两个标签共用一个分支，靠「故意不写 break」
                result = -1;
                break;
            default:
                throw new IllegalArgumentException("unknown " + s);
        }
        return result;
    }

    /** 旧写法 2：忘记 break。编译器不报错，运行时悄悄多执行了下一个分支。 */
    static String buggy(Side s) {
        String label = "";
        switch (s) {
            case BUY:
                label += "buy";            // 本意只想到这里
            case SELL:
                label += "sell";           // 忘了 break：BUY 也会走到这里
                break;
            default:
                label += "other";
        }
        return label;
    }

    /** 旧写法 3：switch 内部所有 case 共享同一个作用域，变量名不能重复。 */
    static String scope(int n) {
        switch (n) {
            case 1:
                String a = "one";
                return a;
            case 2:
                // String a = "two";       // 编译错误：变量 a 已在 case 1 里定义（同一个花括号）
                a = "two";                // 反而能用，但没有初始化——危险
                return a;
            default:
                return "many";
        }
    }

    public static void main(String[] args) {
        System.out.println(sign(Side.BUY) + " " + sign(Side.SELL) + " " + sign(Side.SHORT));
        System.out.println(buggy(Side.BUY));    // 期望 "buy"，实际 "buysell"
        System.out.println(buggy(Side.SELL));
        System.out.println(scope(2));
    }
}
