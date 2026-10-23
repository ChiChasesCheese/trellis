---
id: hl-j13-underscore-history
node: java21.j13-unnamed-variables
type: qa
step: 2
---
## Q
`_` 作为标识符在 Java 各版本经历了什么？这和未命名变量特性有什么关系？

## A
`_` 在 Java 1.0 是合法标识符，**Java 8 起使用它给警告，Java 9 起直接是错误**。

关系：这是在给未命名变量**腾位置**：先让它在旧代码里变成错误，防止有人当普通变量名，才能安全地赋予它「未命名」的新含义。
