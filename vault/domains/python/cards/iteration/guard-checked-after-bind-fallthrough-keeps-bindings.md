---
id: guard-checked-after-bind-fallthrough-keeps-bindings
node: iteration.pattern-matching
type: qa
source: peps
---
## Q
`case ['go', direction] if direction in current_room.exits:` 里的 `if` 守卫（guard）是模式的一部分吗？如果模式匹配成功但守卫条件为假，会发生什么？

## A
守卫不是模式的一部分，而是这个 `case` 分支的附加条件，只有在模式先匹配成功、把变量都绑定好之后才会被求值（所以守卫表达式能直接用到 `direction` 这样的绑定变量）。如果模式匹配但守卫为假，`match` 会把这个 `case` 当作没匹配，继续尝试下一个 `case`——但这一轮里模式已经产生的变量绑定这个副作用并不会被撤销。
