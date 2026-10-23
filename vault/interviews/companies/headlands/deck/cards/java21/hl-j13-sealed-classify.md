---
id: hl-j13-sealed-classify
node: java21.j13-unnamed-variables
type: qa
step: 11
---
## Q
对 sealed 事件层级（`Fill`、`Cancel`、`Reject`、`Heartbeat`，其中 `Fill(orderId, qty, px)`）写两个 `switch`：一个分类标签（Cancel 和 Reject 共用 "TERMINAL"），一个取订单号。

## A
```java
static String label(Event e) {
    return switch (e) {
        case Fill _ -> "FILL";
        case Cancel _, Reject _ -> "TERMINAL";
        case Heartbeat _ -> "HB";
    };
}
static long idOf(Event e) {
    return switch (e) {
        case Fill(var id, _, _) -> id;
        case Cancel(var id) -> id;
        case Reject(var id, _) -> id;
        case Heartbeat() -> -1;
    };
}
```
`label` 用未命名模式变量和共用分支；`idOf` 用 record 解构跳过不要的字段。`Heartbeat()` 无字段，不需要 `_`。
