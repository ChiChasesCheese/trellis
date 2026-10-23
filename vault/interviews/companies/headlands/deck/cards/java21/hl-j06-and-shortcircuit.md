---
id: hl-j06-and-shortcircuit
node: java21.j06-instanceof-pattern
type: qa
step: 3
---
## Q
`o instanceof String s && s.length() > 3` 为什么 `&&` 右边能使用 `s`？旧写法要怎么写？

## A
`&&` **短路**：左边为 `false` 就不算右边，所以到右边时左边必为 `true`，`s` 一定有值。

旧写法得嵌套 `if`：先 `if (o instanceof String)`，里面再转型取长度判断。新写法一行完成"类型 + 字段条件"。
