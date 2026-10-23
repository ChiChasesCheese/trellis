---
id: hl-j03-arrow-vs-colon
node: java21.j03-pattern-switch
type: qa
step: 12
---
## Q
模式标签用冒号 `case X x:` 而不是箭头 `->` 有什么限制？

## A
模式标签最自然的是 `case X x ->`。用经典 `case X x:` 也行，但：
- **不允许 fall-through 进入模式标签**，报 `illegal fall-through to a pattern`，因为绑定变量那时没有值。
- 一个 `case` 里**不能放多个会绑定变量的模式**，如 `case String a, Integer b` 报错。
