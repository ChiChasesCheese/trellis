---
id: pl-trends-convergence-intro-java
node: trends.convergence
type: qa
step: 2
---
## Q
Java 近年加入的 `record`、`sealed` 接口、`switch` 模式匹配和 `var` 分别是什么？合在一起一个例子里怎样工作？

## A
- **`record`**（Java 16 正式）：声明“只携带数据”的不可变类，一行得到构造器、访问器、`equals`、`hashCode`、`toString`。
- **`sealed`**（Java 17 正式）：密封接口或类，用 `permits` 列出**全部**允许的子类型，别处不能再实现。
- **`switch` 模式匹配**（Java 21 正式）：`switch` 可以按类型分支并解构，`switch` 作为**表达式**返回值；对密封类型，编译器检查是否覆盖所有子类型。
- **`var`**（Java 10）：局部变量类型推断，写 `var x = ...`，类型仍是静态的，由右侧推出。

```java
sealed interface Shape permits Circle, Square {}
record Circle(double r) implements Shape {}
record Square(double s) implements Shape {}
static double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Square q -> q.s() * q.s();
    };
}
```

真实输出：`Circle[r=1.0] -> 3.14` 与 `Square[s=2.0] -> 4.00`。注意：`switch` 里没有 `default`。

**穷尽性检查**：如果给 `Shape` 再添加一个 `Tri` 却忘了在 `switch` 里处理，编译器报错：`the switch expression does not cover all possible input values`。这就是密封类型加表达式 `switch` 的核心价值：新增变体时，所有漏处理的地方会在编译期暴露。

**要记住的一点**：这三个特性（record、sealed、pattern switch）合起来，等于 Java 补上了代数数据类型（和类型加乘积类型）加模式匹配，是对函数式语言长期优势的追赶。
