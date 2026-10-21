/** J03 例 1（最简单）：对 Object 做类型模式 switch；null 分支；default。 */
public class J03Ex1 {

    static String describe(Object o) {
        return switch (o) {
            case null -> "null!";                       // Java 21 起 switch 可以显式处理 null
            case Integer i -> "int " + (i + 1);         // i 是 Integer，已经自动转型，不用强转
            case Long l -> "long " + l;
            case String s -> "string of length " + s.length();
            case int[] a -> "int array of " + a.length;
            default -> "something else: " + o.getClass().getSimpleName();
        };
    }

    public static void main(String[] args) {
        Object[] samples = {null, 41, 7L, "hello", new int[]{1, 2, 3}, 3.14};
        for (Object o : samples) System.out.println(describe(o));

        // 没有 case null 时，null 会抛 NPE（和老 switch 一致）
        try {
            String r = switch ((Object) null) {
                case String s -> s;
                default -> "d";
            };
            System.out.println(r);
        } catch (NullPointerException e) {
            System.out.println("没有 case null -> NPE");
        }
    }
}
