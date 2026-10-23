---
id: hl-j08-reserved-type-name
node: java21.j08-var
type: qa
step: 8
---
## Q
`var` 是关键字吗？老代码里变量叫 `var`（`int var = 3;`）还合法吗？

## A
`var` 不是关键字，是**保留类型名**（reserved type name）。

- 变量叫 `var`（`int var = 3;`）依然合法，升级不会弄坏旧代码；
- 只是不能把**类**叫 `var`。
