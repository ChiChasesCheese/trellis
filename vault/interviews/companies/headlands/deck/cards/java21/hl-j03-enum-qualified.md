---
id: hl-j03-enum-qualified
node: java21.j03-pattern-switch
type: qa
step: 11
---
## Q
Java 21 里怎么在选择器是 `sealed interface Signal permits Level, Tick` 的 `switch` 中，把 `enum Level` 的常量当 `case` 标签？写出代码。

## A
Java 21 允许用**限定名**写 `enum` 常量当 `case`，即使选择器是包含它的 `sealed` 接口：

```java
sealed interface Signal permits Level, Tick {}
enum Level implements Signal { LOW, MID, HIGH }
record Tick(long px, long qty) implements Signal {}

switch (s) {
    case Level.LOW -> ...
    case Level.MID -> ...
    case Level.HIGH -> ...
    case Tick t -> ...
}
```
列全 `LOW` / `MID` / `HIGH` 三个常量，`Level` 就算被覆盖，整个 `switch` 穷尽，无需 `default`。
