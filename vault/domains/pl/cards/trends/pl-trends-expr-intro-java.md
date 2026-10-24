---
id: pl-trends-expr-intro-java
node: trends.expression-orientation
type: qa
step: 3
---
## Q
Java 14 起的 `switch` 表达式（`->` 箭头、`yield`）是什么？它与传统 `switch` 语句的穿透（fall-through）有什么本质区别？

## A
**传统 `switch` 语句**：每个 `case` 是一个入口点，执行会**继续往下穿透**，直到遇到 `break`。忘写 `break` 就是经典 bug：

```java
switch (d) {
    case 1: r += "one";           // no break
    case 2: r += "two"; break;
    default: r += "other";
}
```

当 `d == 1`，真实结果是 `onetwo`：执行了 case 1，又穿透到 case 2。

**`switch` 表达式**（Java 14 正式）：用箭头 `->`，每个分支独立，**没有穿透**，整个 `switch` 产生一个值：

```java
String kind = switch (day) {
    case 1, 7 -> "weekend";
    case 2, 3, 4, 5, 6 -> { String t = "week"; yield t + "day"; }
    default -> throw new IllegalArgumentException();
};
```

真实输出：`day = 3` 得到 `weekday`。要点：
- 多个标签可以用逗号合并（`case 1, 7`）。
- 分支需要多条语句时用花括号，用 `yield` 给出该分支的值。
- 分支可以 `throw`，表示这个分支没有值。
- 作为表达式，`switch` 必须**穷尽**：枚举或密封类型漏了某个成员，编译器报错，不需要 `default`。

同样的 `switch(1)`，表达式版本得到 `one`，不会穿透。

**要记住的一点**：Java 没有把整个语言改成表达式导向，而是**把最容易出错的那个语句改造了**：`switch` 表达式一并消除了穿透、变量未初始化和遗漏分支三类问题。
