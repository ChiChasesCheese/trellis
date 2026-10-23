---
id: hl-j05-real-usage
node: java21.j05-switch-expressions
type: qa
step: 27
---
## Q
真实代码里 `switch` 表达式 + `yield` 常见用在哪些地方？

## A
- **命令解析**：字符串 `switch` 把一行文本变成 `sealed` 的 `Command`，每分支一个块 + `yield`，`default` 里 `throw`。订单簿的 `execute` 块里有**多处 `yield`**。
- **渲染**：`case Ok(var chains) -> { ... yield lines; }`（模式匹配 + 块 + `yield`）。
- **事件解析**：`case "push" -> { ...; yield new Push(...); }`、`case "pop" -> { ...; yield new Pop(); }`。
- **枚举方法**：`switch (this)`，如 `case INT -> Math.toIntExact(s); case LONG -> s;`，无 `default`，靠穷尽性保证。
