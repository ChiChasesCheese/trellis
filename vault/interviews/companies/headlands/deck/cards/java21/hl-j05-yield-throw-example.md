---
id: hl-j05-yield-throw-example
node: java21.j05-switch-expressions
type: qa
step: 20
---
## Q
补全代码：用 `switch` 表达式写 `parsePositive(String s)`：空串抛 `IllegalArgumentException("empty")`，否则解析为 `long`，非正数抛异常，否则返回该值。

## A
```java
static long parsePositive(String s) {
    return switch (s.isEmpty() ? 0 : 1) {
        case 0 -> throw new IllegalArgumentException("empty");
        default -> {
            long v = Long.parseLong(s);
            if (v <= 0) throw new IllegalArgumentException("not positive: " + v);
            yield v;
        }
    };
}
```
要点：`throw` 分支不产出值；块里先校验再 `yield`；块内局部变量 `v` 的作用域只在该分支。
