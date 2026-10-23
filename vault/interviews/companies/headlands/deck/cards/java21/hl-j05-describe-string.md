---
id: hl-j05-describe-string
node: java21.j05-switch-expressions
type: qa
step: 19
---
## Q
补全代码：用字符串 `switch` 表达式写 `describe(String cmd)`：`"LIMIT"`/`"limit"` → `limit order`，`"MARKET"` → `market order`，`"CANCEL"` → `cancel`，其余 `unknown: ` 加原值。为什么必须有 `default`？

## A
```java
static String describe(String cmd) {
    return switch (cmd) {
        case "LIMIT", "limit" -> "limit order";
        case "MARKET" -> "market order";
        case "CANCEL" -> "cancel";
        default -> "unknown: " + cmd;
    };
}
```
`String` 是**开放集合**（值域无限），编译器无法证明已穷尽，所以必须有 `default`。
