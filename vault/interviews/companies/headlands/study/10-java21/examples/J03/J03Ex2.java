/** J03 例 2（进阶）：when 守卫、case 顺序（支配）、case null, default、sealed 穷尽、enum 常量作 case。 */
public class J03Ex2 {

    sealed interface Signal permits Level, Tick {}
    enum Level implements Signal { LOW, MID, HIGH }          // enum 实现 sealed 接口
    record Tick(long px, long qty) implements Signal {}

    static String classify(Signal s) {
        return switch (s) {
            case Level.LOW -> "low level";                   // Java 21: 限定名的 enum 常量可以直接当 case
            case Level.MID -> "mid level";
            case Level.HIGH -> "high level";
            case Tick t when t.qty() == 0 -> "empty tick";   // 守卫：同一个类型的分支，靠 when 细分
            case Tick t when t.px() > 100_000 -> "expensive tick";
            case Tick t -> "tick " + t.px() + "x" + t.qty();  // 兜底分支：不带 when
        };
    }

    static String sizeBucket(Object o) {
        return switch (o) {
            case Integer i when i < 0 -> "negative";
            case Integer i when i < 10 -> "small";
            case Integer i -> "big";
            case String s when s.isEmpty() -> "empty string";
            case String s -> "string";
            case null, default -> "other/null";              // null 和 default 可以合并写
        };
    }

    public static void main(String[] args) {
        for (Signal s : new Signal[]{Level.MID, new Tick(1, 0), new Tick(200_000, 5), new Tick(100, 3)}) {
            System.out.println(classify(s));
        }
        for (Object o : new Object[]{-5, 3, 99, "", "x", null, 2.5}) {
            System.out.println(sizeBucket(o));
        }
    }
}
