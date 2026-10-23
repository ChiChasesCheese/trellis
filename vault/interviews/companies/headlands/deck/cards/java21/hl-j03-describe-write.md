---
id: hl-j03-describe-write
node: java21.j03-pattern-switch
type: qa
step: 3
---
## Q
补全代码：写一个 `describe(Object o)`，用 `switch` 表达式处理 `null`、`Integer`（返回 `"int " + (i+1)`）、`String`（返回长度描述）、`int[]`，其余走 `default`。

## A
```java
static String describe(Object o) {
    return switch (o) {
        case null -> "null!";
        case Integer i -> "int " + (i + 1);
        case String s -> "string of length " + s.length();
        case int[] a -> "int array of " + a.length;
        default -> "something else: " + o.getClass().getSimpleName();
    };
}
```
输入 `3.14` 得到 `something else: Double`。`case null` 要自己写；`default` 兜底其余类型。
