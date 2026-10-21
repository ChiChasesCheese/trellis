import java.util.List;

/** J04 例 2（进阶）：嵌套模式；泛型 record 的类型推断；子模式「全覆盖」时 null 也能匹配；子模式不全覆盖时 null 不匹配。 */
public class J04Ex2 {

    record Mean(long numerator, long denominator) {}
    sealed interface Answer permits Value, Empty {}
    record Value(Mean mean) implements Answer {}
    record Empty() implements Answer {}

    // 嵌套：Value(Mean(var n, var d)) 一次拆两层
    static String render(Answer a) {
        return switch (a) {
            case Value(Mean(var n, var d)) when d == 1 -> Long.toString(n);
            case Value(Mean(var n, var d)) -> n + "/" + d;
            case Empty() -> "empty";           // 零组件 record 的模式：Empty()
        };
    }

    // 泛型 record：Box<T> 的 T 从选择器类型推断
    record Box<T>(T content) {}
    static String unbox(Box<String> b) {
        return switch (b) {
            case Box<String>(var s) -> "string box: " + s.toUpperCase();   // s 的类型是 String
        };
    }
    static String unboxAny(Box<?> b) {
        return switch (b) {
            case Box<?>(String s) -> "string " + s;
            case Box<?>(Integer i) -> "int " + (i + 1);
            case Box<?>(var other) -> "other " + other;
        };
    }

    // null 的规则
    record Holder(Object value) {}
    static String nullRules(Holder h) {
        return switch (h) {
            case Holder(String s) -> "string " + s;        // 子模式 String 不是「对 Object 全覆盖」：null 不会匹配它
            case Holder(Object o) -> "object " + o;        // 子模式 Object 对 Object 全覆盖：null 也匹配
        };
    }

    // 访问器抛异常：模式匹配会把它包成 MatchException（原异常放在 cause 里）
    record Bad(int x) {
        public int x() { throw new IllegalStateException("accessor failed"); }
    }
    static String useBad(Object o) {
        return switch (o) {
            case Bad(var x) -> "x=" + x;
            default -> "d";
        };
    }

    // 穷尽性会「相乘」：Pair 的两个组件各有 2 种，一共要覆盖 2 x 2 = 4 种组合
    sealed interface Bit permits Zero, One {}
    record Zero() implements Bit {}
    record One() implements Bit {}
    record Pair(Bit a, Bit b) {}
    static String xor(Pair p) {
        return switch (p) {
            case Pair(Zero a, Zero b) -> "0";
            case Pair(Zero a, One b) -> "1";
            case Pair(One a, Zero b) -> "1";
            case Pair(One a, One b) -> "0";
        };
    }

    public static void main(String[] args) {
        System.out.println(render(new Value(new Mean(7, 1))));
        System.out.println(render(new Value(new Mean(-7, 2))));
        System.out.println(render(new Empty()));
        System.out.println(unbox(new Box<>("abc")));
        System.out.println(unboxAny(new Box<>(41)));
        System.out.println(unboxAny(new Box<>(2.5)));
        System.out.println(nullRules(new Holder("x")));
        System.out.println(nullRules(new Holder(null)));      // 落到第二个分支，不抛 NPE
        try {
            nullRules(null);                                    // 外层 record 本身是 null：NPE
        } catch (NullPointerException e) {
            System.out.println("Holder 本身为 null -> NPE");
        }
        System.out.println(List.of(new Holder(1)).get(0));
        System.out.println(xor(new Pair(new Zero(), new One())) + xor(new Pair(new One(), new One())));
        try {
            useBad(new Bad(1));
        } catch (MatchException e) {
            System.out.println("MatchException, cause = " + e.getCause());
        }
    }
}
