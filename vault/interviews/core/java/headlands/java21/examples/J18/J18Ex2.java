import java.util.*;

/** J18 例 2：接口的 default / static / private 方法；多继承冲突怎么解；函数式接口 + default 组合。 */
public class J18Ex2 {
    // ---- 1. default：给接口"加功能"而不破坏已有实现 ----
    interface Validator<T> {
        boolean test(T t);                                   // 唯一的抽象方法 -> 可以当 lambda 用

        default Validator<T> and(Validator<? super T> other) { return t -> test(t) && other.test(t); }
        default Validator<T> negate() { return t -> !test(t); }

        static <T> Validator<T> not(Validator<T> v) { return v.negate(); }   // static：接口自己的工具方法
        static <T> Validator<T> all(List<Validator<T>> vs) {
            return t -> check(vs, t);
        }
        private static <T> boolean check(List<Validator<T>> vs, T t) {       // Java 9：private 方法，复用但不暴露
            for (var v : vs) if (!v.test(t)) return false;
            return true;
        }
    }

    // ---- 2. 钻石冲突：两个接口都给同名 default，实现类必须自己裁决 ----
    interface Maker { default String describe() { return "maker"; } }
    interface Taker { default String describe() { return "taker"; } }
    static class Both implements Maker, Taker {
        @Override public String describe() { return Maker.super.describe() + "+" + Taker.super.describe(); }   // 用 X.super.m() 指名
    }

    // ---- 3. 类优先于接口：类（含父类）的方法永远胜过接口的 default ----
    static class Base { public String describe() { return "base"; } }
    static class Derived extends Base implements Maker { }

    // ---- 4. 贴近真实：下单校验链（default 方法组合）----
    record Order(String symbol, long qty, long px) {}

    public static void main(String[] args) {
        Validator<Order> positiveQty = o -> o.qty() > 0;
        Validator<Order> priceInBand = o -> o.px() >= 18_000 && o.px() <= 19_000;
        Validator<Order> aapl = o -> o.symbol().equals("AAPL");

        var ok = positiveQty.and(priceInBand).and(aapl);
        System.out.println("合法单: " + ok.test(new Order("AAPL", 100, 18_950)));
        System.out.println("价格越界: " + ok.test(new Order("AAPL", 100, 25_000)));
        System.out.println("not(positiveQty): " + Validator.not(positiveQty).test(new Order("X", 0, 1)));
        System.out.println("all(...): " + Validator.all(List.of(positiveQty, priceInBand)).test(new Order("X", 5, 18_500)));

        System.out.println("Both.describe = " + new Both().describe());
        System.out.println("Derived.describe = " + new Derived().describe() + "  (类 Base 胜过接口 Maker)");
    }
}
