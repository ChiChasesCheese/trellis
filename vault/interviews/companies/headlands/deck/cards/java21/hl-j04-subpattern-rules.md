---
id: hl-j04-subpattern-rules
node: java21.j04-record-patterns
type: qa
step: 6
---
## Q
record 模式的子模式个数和类型有什么规则？`P(var x)`（`P` 有两个组件）和 `Order(int id, ...)`（`id` 是 `long`）分别报什么错？

## A
- **个数必须等于组件个数**：`P(var x)` 而 `P` 有两个组件 → `incorrect number of nested patterns`。
- **类型必须兼容**：组件是 `long` 却写 `int id` → `pattern of type int is not applicable at long`。**基本类型不会自动拓宽**，组件是 `int` 也不能写 `long id`。
- 不确定类型就用 `var`。
