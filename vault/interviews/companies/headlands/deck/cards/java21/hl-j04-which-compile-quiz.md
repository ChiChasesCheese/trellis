---
id: hl-j04-which-compile-quiz
node: java21.j04-record-patterns
type: qa
step: 25
---
## Q
`record Order(long id, Side side, long qty)`，下面三行哪些不能编译？为什么？
(a) `case Order(var id, Side side, var qty) when side == Side.BUY -> ...`
(b) `case Order(var id, Side.BUY, var qty) -> ...`
(c) `case Order(int id, Side side, var qty) -> ...`

## A
- (a) **合法**。
- (b) **不能编译**：子模式不能是常量，报 `<identifier> expected`。
- (c) **不能编译**：组件 `id` 是 `long`，`int id` 不适用（`pattern of type int is not applicable at long`），基本类型不自动拓宽。
