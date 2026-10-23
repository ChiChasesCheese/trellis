---
id: hl-j06-null-and-chain-quiz
node: java21.j06-instanceof-pattern
type: qa
step: 22
---
## Q
`o` 为 `null` 时 `o instanceof String s` 的结果是什么？`s` 有值吗？如果代码里有十几个 `else if (x instanceof Foo f)`，应该怎么建议？

## A
- 结果是 **`false`**，`s` 未绑定（不进分支）。
- 十几个 `else if` 的 `instanceof` 链：改用 **`sealed` 接口 + `switch` 模式匹配**——编译器检查穷尽，字节码走 `typeSwitch`；或把行为放进**多态方法**。
