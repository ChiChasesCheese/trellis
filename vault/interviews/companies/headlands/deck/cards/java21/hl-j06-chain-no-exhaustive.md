---
id: hl-j06-chain-no-exhaustive
node: java21.j06-instanceof-pattern
type: qa
step: 19
---
## Q
`instanceof` 链依然有什么局限？什么时候用 `instanceof` 模式，什么时候改用 `switch` 或多态？

## A
`if / else if` 一路 `instanceof` 下去，**编译器不检查穷尽性**：漏处理一个类型编译器不报。

- `instanceof` 模式适合：**只关心一种类型**，或**一个条件里同时用类型和字段**。
- 分派多个类型：用 `sealed` + `switch` 模式匹配（编译器检查穷尽，字节码走 `typeSwitch`），或把行为放进多态方法。

到处 `if (x instanceof A) ... else if (x instanceof B) ...` 往往是设计信号：该用 `sealed` + `switch` 或多态了。
