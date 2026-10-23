---
id: hl-j18-validator-example
node: java21.j18-comparators-interfaces
type: qa
step: 17
---
## Q
用接口的 `default`/`static`/`private` 方法写一个可组合的订单校验器 `Validator<T>`，并展示链式组合与取反。

## A
```java
interface Validator<T> {
    boolean test(T t);
    default Validator<T> and(Validator<? super T> other) { return t -> test(t) && other.test(t); }
    default Validator<T> negate() { return t -> !test(t); }
    static <T> Validator<T> not(Validator<T> v) { return v.negate(); }
    static <T> Validator<T> all(List<Validator<T>> vs) { return t -> check(vs, t); }
    private static <T> boolean check(List<Validator<T>> vs, T t) { /* 逐个 test */ }
}
var ok = positiveQty.and(priceInBand).and(aapl);
```
结果：合法单 `true`；价格越界 `false`；`Validator.not(positiveQty)` 测数量为 0 的单得 `true`（`not(v)` 就是 `v.negate()`）；`all(List.of(positiveQty, priceInBand))` 测数量 5、价格在带内的单得 `true`（列表里每个校验器都通过才为真）。只有一个抽象方法 + 若干 default = **可组合的函数式接口**，`java.util.function.Predicate` 就是这样设计的。
