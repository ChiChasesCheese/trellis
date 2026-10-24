---
id: pl-types-null-safety-found-java-null-optional
node: types.null-safety
type: qa
step: 2
---
## Q
Java 的 `null` 和 `NullPointerException` 是什么？`Optional` 又是怎么用的？

## A
Java 里所有对象类型的变量都是引用，可以取特殊值 `null`，表示「不指向任何对象」。对 `null` 调用方法或访问字段，运行时抛出 `NullPointerException`（NPE）。类型系统不区分「一定有值」的 `String` 和「可能没有」的 `String`，所以编译器不会提醒你。

```java
String s = null;
System.out.println(s == null);    // true
System.out.println(s.length());   // NPE
```

第二行输出 `true`，第三行抛出 `NullPointerException: Cannot invoke "String.length()" because ... is null`。

`Optional<T>`（Java 8 引入）是一个容器类：要么装着一个值，要么是空。它让「可能没有」在返回类型上可见，并提供安全的链式处理：`map` 在有值时变换，`orElse` 在空时给默认值。

```java
Optional<String> find(Map<String, String> m, String k) {
    return Optional.ofNullable(m.get(k));
}
var m = Map.of("a", "x");
find(m, "a").map(String::toUpperCase).orElse("none");   // m 里 a 对应 x：X
find(m, "b").map(String::toUpperCase).orElse("none");   // none
```

实际输出：`X`、`none`，打印空的 `Optional` 是 `Optional.empty`。

注意 `Optional` 只是库里的一个类，语言并不强制使用：变量仍然可以是 `null`，`Optional` 本身也可以是 `null`。它最适合做方法的返回类型，表达「可能没有结果」。
