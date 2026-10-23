---
id: hl-j18-interface-members
node: java21.j18-comparators-interfaces
type: qa
step: 9
---
## Q
Java 9 起接口里能有哪五类成员？各自怎么调用、有什么限制？

## A
```java
interface Validator<T> {
    boolean test(T t);                        // 抽象：实现者必须提供；只有一个 -> 函数式接口
    default Validator<T> negate() { return t -> !test(t); }   // default：有实现，可被覆盖，通过实例调用
    static <T> Validator<T> not(Validator<T> v) { return v.negate(); } // static：通过 Validator.not(...) 调用，不会被继承
    private static <T> boolean check(List<Validator<T>> vs, T t) {...} // private static（Java 9）
    private boolean helper() {...}            // private 实例方法（Java 9）
}
```
- `private` 方法只能被接口内部方法调用，实现类看不到，也不能覆盖；
- 接口**不能有实例字段**，`default` 只能通过抽象方法和别的 `default` 方法工作；
- `default` **不能**覆盖 `Object` 的方法（`equals`、`hashCode`、`toString`）；
- 只有一个抽象方法 + 若干 default = **可组合的函数式接口**（`Predicate` 就是这样设计的）。
