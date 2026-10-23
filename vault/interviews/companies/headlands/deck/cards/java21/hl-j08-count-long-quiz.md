---
id: hl-j08-count-long-quiz
node: java21.j08-var
type: qa
step: 24
---
## Q
`var count = 0; long big = 5L; count = big;` 会发生什么？为什么？怎么改？

## A
编译错误：`incompatible types: possible lossy conversion from long to int`。

原因：`0` 是 `int` 字面量，`count` 就是 `int`，不能装 `long`。

想要 `long` 就写 `var count = 0L;` 或 `long count = 0;`。
