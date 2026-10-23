---
id: hl-j03-generic-erasure
node: java21.j03-pattern-switch
type: qa
step: 25
---
## Q
`case List<String> l` 在选择器是 `Object` 时为什么被拒？选择器是 `sealed` 泛型类型 `Poll<T>` 时 `case Ready<T> r` 为什么可以？

## A
- 选择器是 `Object`：因类型擦除（erasure），运行时无法检查 `<String>`，编译器拒绝。
- 选择器本身是 `sealed` 泛型类型（如 `Poll<T>`）：类型参数能由选择器类型**推出**，所以 `case Ready<T> r` 合法，不需要运行时检查泛型实参。
