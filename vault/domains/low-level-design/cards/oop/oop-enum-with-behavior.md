---
id: oop-enum-with-behavior
node: oop.values
type: qa
---
## Q
When does an enum with behavior (per-constant fields/methods) beat a class hierarchy for variants — and what signals you've outgrown the enum?

## A
- **Enum wins** for a small, closed variant set whose behavior is a pure function of the variant: `VehicleType.SUV.spotSize()` — constants and logic co-located, switches exhaustiveness-checked.
- **Outgrown** when variants need their own mutable state, substantially distinct logic, or open extension (new variants without editing the enum) → promote to interface + one class per variant (strategy).

## Q zh
什么时候带行为的 enum（每个常量各自的字段和方法）比类层次更适合表达变体——又有哪些信号说明你已经用不下 enum 了？

## A zh
- **Enum 胜出**：变体集合小而封闭，且行为是变体的纯函数：`VehicleType.SUV.spotSize()` —— 常量和逻辑放在一起，switch 还能拿到编译器的穷尽性检查。
- **用不下了**的信号：变体需要各自的可变状态、逻辑差异很大、或者需要开放扩展（不改 enum 就能加新变体）→ 升级成 interface + 每个变体一个类（strategy）。
