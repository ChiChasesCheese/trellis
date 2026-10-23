---
id: hl-j06-generic-rule
node: java21.j06-instanceof-pattern
type: qa
step: 9
---
## Q
`instanceof` 模式遇到泛型有什么限制？下面三个哪些合法：`o`（`Object`）`instanceof List<String> l`、`o instanceof List<?> l`、`o` 的静态类型是 `List<String>` 时 `o instanceof ArrayList<String> al`？

## A
- `Object o instanceof List<String> l`：**被拒绝**，擦除后无法在运行时检查 `<String>`。
- `o instanceof List<?> l`：**合法**。
- 静态类型已是 `List<String>` 时 `o instanceof ArrayList<String> al`：**安全合法**，类型参数能由静态类型推出。

规则同 `switch` 模式里的泛型擦除限制。
