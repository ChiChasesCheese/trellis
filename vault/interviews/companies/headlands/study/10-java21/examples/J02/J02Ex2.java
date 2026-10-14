import java.util.List;

/** J02 例 2（进阶）：三种子类修饰符 final / sealed / non-sealed；省略 permits；sealed 抽象类；泛型。 */
public class J02Ex2 {

    // ---- (a) sealed 抽象类 + 三种修饰符 ----
    // permits 可以省略：子类和父类写在同一个编译单元（同一个 .java 文件）里时，编译器自己推出来。
    sealed static abstract class Instrument {
        abstract String ticker();
    }
    static final class Stock extends Instrument {            // final：到此为止
        public String ticker() { return "AAPL"; }
    }
    static sealed abstract class Option extends Instrument {  // sealed：继续封闭；abstract 是为了让 Option 自己不能被 new，switch 才不必为它单独写分支
        public String ticker() { return "AAPL240621C00200000"; }
    }
    static final class CallOption extends Option {}
    static final class PutOption extends Option {}
    static non-sealed class Custom extends Instrument {      // non-sealed：这里重新开放，任何人都能继承
        public String ticker() { return "CUSTOM"; }
    }
    static class UserDefined extends Custom {}               // 合法：因为 Custom 是 non-sealed

    static String kind(Instrument i) {
        return switch (i) {
            case Stock s -> "stock";
            case CallOption c -> "call";
            case PutOption p -> "put";
            case Custom c -> "custom";    // 覆盖 Custom 及其所有（无限多）后代
        };
    }

    // ---- (b) 泛型 sealed：Option<T> / Either ----
    sealed interface Either<L, R> permits Left, Right {}
    record Left<L, R>(L value) implements Either<L, R> {}
    record Right<L, R>(R value) implements Either<L, R> {}

    static <L, R> String fold(Either<L, R> e) {
        return switch (e) {
            case Left<L, R> l -> "left:" + l.value();
            case Right<L, R> r -> "right:" + r.value();
        };
    }

    // ---- (c) sealed 可以放 enum：enum 隐式 final，能当 permits 成员 ----
    sealed interface Signal permits Tick, Bar {}
    enum Tick implements Signal { UP, DOWN }
    record Bar(long open, long close) implements Signal {}

    public static void main(String[] args) {
        for (Instrument i : List.of(new Stock(), new CallOption(), new PutOption(), new UserDefined())) {
            System.out.println(i.ticker() + " -> " + kind(i));
        }
        System.out.println(fold(new Left<String, Integer>("bad")));
        System.out.println(fold(new Right<String, Integer>(7)));
        Signal s = Tick.UP;
        System.out.println(switch (s) {
            case Tick t -> "tick " + t;
            case Bar b -> "bar " + b.close();
        });
    }
}
