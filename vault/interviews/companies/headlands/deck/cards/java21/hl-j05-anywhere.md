---
id: hl-j05-anywhere
node: java21.j05-switch-expressions
type: qa
step: 13
---
## Q
`switch` 表达式可以出现在哪些位置？写一个把它拼进字符串的例子。

## A
任何表达式能出现的地方：`return`、赋值、方法参数、字符串拼接等。

```java
System.out.println("level is " + switch (level) {
    case 1 -> "low";
    case 2 -> "mid";
    default -> "high";
});
```
`level` 为其他值时输出 `level is high`。
