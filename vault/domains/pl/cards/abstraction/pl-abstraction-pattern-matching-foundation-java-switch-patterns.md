---
id: pl-abstraction-pattern-matching-foundation-java-switch-patterns
node: abstraction.pattern-matching
type: qa
step: 3
---
## Q
Java 21 的 `sealed` 接口、`record` 和模式 `switch` 怎样组合出代数数据类型与穷尽检查？

## A
三个部件各司其职：

- **`record`**：不可变的数据载体，`record Circle(double r)` 自动生成构造器、访问方法、`equals`/`hashCode`，是**积类型**（一组字段）。
- **`sealed` 接口**：用 `permits` 列出所有允许的实现，编译器因此知道这个集合是**封闭**的，是**和类型**（几种之一）。
- **模式 `switch`**（Java 21 起正式）：`case` 后面写类型加解构，还能加 `when` 守卫。

```java
sealed interface Shape permits Circle, Rect, Tri {}
record Circle(double r) implements Shape {}
record Rect(double w, double h) implements Shape {}
record Tri(double b, double h) implements Shape {}
static double area(Shape s) {
    return switch (s) {
        case Circle(double r) -> Math.PI * r * r;
        case Rect(double w, double h) when w == h -> w * w;
        case Rect(double w, double h) -> w * h;
        case Tri(double b, double h) -> 0.5 * b * h;
    };
}
```

`area(new Rect(2, 3))` 得 `6.0`，`area(new Tri(4, 3))` 得 `6.0`。因为 `Shape` 是封闭的，`switch` 不需要 `default`；删掉 `Tri` 那个分支，编译器报：

```text
error: the switch expression does not cover all possible input values
```

这里的穷尽检查依赖 `sealed`：普通接口是开放的（别人随时可以新增实现），编译器无法证明覆盖了所有情形，只能要求 `default`。
