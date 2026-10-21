import java.util.Arrays;

/** J02 例 1（最简单）：sealed interface + permits + record，加一个反射看 PermittedSubclasses。 */
public class J02Ex1 {

    sealed interface Result permits Ok, Err {}
    record Ok(long value) implements Result {}
    record Err(String message) implements Result {}

    static String show(Result r) {
        return switch (r) {              // 没有 default：编译器知道只有 Ok 和 Err
            case Ok ok -> "ok " + ok.value();
            case Err err -> "err " + err.message();
        };
    }

    public static void main(String[] args) {
        System.out.println(show(new Ok(42)));
        System.out.println(show(new Err("boom")));

        System.out.println(Result.class.isSealed());
        System.out.println(Arrays.stream(Result.class.getPermittedSubclasses())
                .map(Class::getSimpleName).toList());
        System.out.println(Ok.class.isSealed());   // record 是隐式 final，不是 sealed
    }
}
