---
id: pl-types-algebraic-data-types-found-java-sealed-record
node: types.algebraic-data-types
type: qa
step: 3
---
## Q
Java 的 `record`、`sealed` 接口和 `switch` 模式匹配各是什么？它们怎样合起来表达「几种之一」？

## A
三个特性分别补一块：

- `record`（Java 16）：一行声明一个不可变的数据类，编译器自动生成构造器、访问器、`equals`、`hashCode`、`toString`。它是积类型。
- `sealed`（Java 17）：`sealed interface Cmd permits Quit, Move` 限定只有列出的类可以实现它，实现者集合在编译期就是封闭的。
- `switch` 模式匹配（Java 21）：`switch` 可以按类型分支，还能把 record 的字段解构出来；对 `sealed` 类型，编译器检查是否覆盖了所有实现者，不需要 `default`。

```java
record Point(int x, int y) {}
sealed interface Cmd permits Quit, Move {}
record Quit() implements Cmd {}
record Move(int dx, int dy) implements Cmd {}

static String run(Cmd c) {
    return switch (c) {
        case Quit q -> "quit";
        case Move(int dx, int dy) -> "move " + dx + "," + dy;
    };
}
```

实际输出：`new Point(1, 2)` 打印为 `Point[x=1, y=2]`，两个相同坐标的 `Point` 用 `equals` 比较为 `true`；`run(new Move(3, 4))` 得 `move 3,4`，`run(new Quit())` 得 `quit`。

少写 `Move` 分支，编译失败：`the switch expression does not cover all possible input values`。三者合起来，Java 得到了函数式语言里的代数数据类型，而且是在不破坏旧语法的前提下增量加入的。
