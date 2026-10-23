---
id: hl-j05-arrow-rhs
node: java21.j05-switch-expressions
type: qa
step: 6
---
## Q
`switch` 表达式里箭头右边可以是哪三种东西？各自怎么给出值？

## A
```java
return switch (cmd) {
    case "LIMIT"  -> 1;                      // ① 表达式：它的值就是这个分支的值
    case "CANCEL" -> {                       // ② 块：多条语句，用 yield 给值
        int x = compute();
        yield x * 2;
    }
    default       -> throw new IllegalArgumentException(cmd);   // ③ throw：不产出值
};
```
- 右边是表达式时**不要加 `yield`**。
- 块里必须 `yield`，**块不能不给值就结束**，否则报 `switch rule completes without providing a value`。
- `throw` 分支合法。
