/** J04 例 1（最简单）：在 instanceof 和 switch 里把 record 直接拆成变量。 */
public class J04Ex1 {

    record Point(long x, long y) {}

    public static void main(String[] args) {
        Object o = new Point(3, 4);

        // instanceof + 记录模式：判断类型 + 取出两个分量，一步完成
        if (o instanceof Point(long x, long y)) {
            System.out.println("distance^2 = " + (x * x + y * y));
        }

        // 组件类型可以写 var，让编译器推断
        if (o instanceof Point(var x, var y) && x < y) {
            System.out.println("x < y");
        }

        // switch 里同理
        String s = switch (o) {
            case Point(var x, var y) when x == 0 && y == 0 -> "origin";
            case Point(var x, var y) -> "point " + x + "," + y;
            default -> "not a point";
        };
        System.out.println(s);

        // 不匹配的情形：不是 Point -> 整个 if 为 false，x 和 y 也不存在
        Object other = "hello";
        System.out.println(other instanceof Point(var x, var y));
    }
}
