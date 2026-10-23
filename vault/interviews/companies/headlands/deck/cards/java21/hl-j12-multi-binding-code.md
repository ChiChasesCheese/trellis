---
id: hl-j12-multi-binding-code
node: java21.j12-scoped-values
type: qa
step: 14
---
## Q
补全：同时绑定 `USER` 和 `DEPTH`，内层用另一个值遮蔽并看到还原；再写一个有返回值的 `call`。预期输出是什么？

## A
```java
ScopedValue.where(USER, "alice").where(DEPTH, 1).run(() -> {
    print(describe());                     // alice@depth1
    ScopedValue.where(USER, "admin-on-behalf-of-alice").where(DEPTH, 2)
        .run(() -> print(describe()));     // 内层: ...@depth2
    print(describe());                     // 还原: alice@depth1
});
String r = ScopedValue.where(USER, "carol").call(() -> USER.get().toUpperCase());
```
`r` 为 `CAROL`；用 `getWhere(USER, "dave", () -> USER.get() + "!")` 得 `dave!`。重点是「还原」那行：出内层自动回到外层的值，无需手写恢复。
