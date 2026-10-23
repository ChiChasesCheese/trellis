---
id: hl-j05-enum-no-default
node: java21.j05-switch-expressions
type: qa
step: 11
---
## Q
`enum` 的 `switch` 表达式为什么不要写 `default`？有什么例外？

## A
写了 `default` 之后，枚举**新增常量时编译器不再提醒**，新常量悄悄落入 `default`。不写则新增常量让所有漏处理的 `switch` 编译失败。

**例外**：枚举来自外部库、你控制不了它何时加常量时，`default -> throw ...` 合理，因为本来就没有"新增即编译失败"的保护。
