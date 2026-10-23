---
id: hl-j04-generic-record-pattern
node: java21.j04-record-patterns
type: qa
step: 8
---
## Q
对泛型 record `Box<T>(T content)`，怎么用 record 模式拆开 `Box<String>` 和 `Box<?>`？类型参数能省略吗？

## A
```java
record Box<T>(T content) {}

case Box<String>(var s) -> "string box: " + s.toUpperCase();   // s : String

static String unboxAny(Box<?> b) {
    return switch (b) {
        case Box<?>(String s)  -> "string " + s;
        case Box<?>(Integer i) -> "int " + (i + 1);
        case Box<?>(var other) -> "other " + other;
    };
}
```
类型参数能由选择器类型推出时可省略（`Box(var s)` 也行）。
