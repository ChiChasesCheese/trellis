---
id: hl-j03-instanceof-vs-switch
node: java21.j03-pattern-switch
type: qa
step: 30
---
## Q
Java 8 的 `instanceof` + 强转链，与 Java 21 的模式匹配 `switch` 写同一个 `area(Shape s)`，差别在哪里？写出 Java 21 的版本。

## A
Java 8 版要先 `s instanceof Circle` 判断，再 `(Circle) s` 强转（类型写两遍），末尾用 `throw` 靠人兜底。

Java 21 版：
```java
static double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r -> r.w() * r.h();
    };
}
```
`Shape` 是 `sealed` 时：无需强转、无需 `default`，漏一种编译失败。
