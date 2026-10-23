---
id: hl-j05-enum-switchmap
node: java21.j05-switch-expressions
type: qa
step: 16
---
## Q
`enum` 的 `switch` 在编译时有哪两种实现方式？为什么 `enum` 在另一个文件时要生成合成的 `$SwitchMap$`？

## A
- `enum` 与 `switch` 在**同一个顶层类**：直接 `ordinal()` + `tableswitch`。
- `enum` 在**另一文件**：编译器生成合成类（如 `Use$1`），含静态数组 `$SwitchMap$Col`，类初始化时把"`ordinal()` → 本次编译的 case 编号"映射好（每次写入包在 `catch NoSuchFieldError` 里）。

原因：枚举被增删 / 重排后 `ordinal()` 会变，写死旧序号会走错分支；运行时查表就安全。
