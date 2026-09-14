---
id: structure-state-enum-vs-boolean-soup
node: structure.state-machines
type: qa
---
## Q
An `Order` has `isPaid`, `isShipped`, `isCancelled` booleans. Why does this rot as requirements grow, and what does replacing them with a state enum buy you concretely?

## A
Three booleans encode **2³ = 8 combinations** but only ~4 are legal — nothing stops `isShipped && isCancelled`, and every method starts with fragile flag-combination checks scattered everywhere.

A single `enum State { CREATED, PAID, SHIPPED, CANCELLED }` buys:
- **Illegal states are unrepresentable** — one field, one value.
- Transitions become **checkable in one place** instead of implied by flag flips.
- New states (REFUNDED) are an enum addition + transition entries, and `switch` exhaustiveness finds every spot to update.


## Q zh
一个 `Order` 有 `isPaid`、`isShipped`、`isCancelled` 布尔值。为什么这个在需求增长时腐蚀，替换它们用一个状态枚举给你什么具体?

## A zh
三个布尔值编码**2³ = 8 个组合**但只有 ~4 是合法的 — 什么都不阻止 `isShipped && isCancelled`，每个方法以脆弱的标志组合检查零散开始。

一个单独的 `enum State { CREATED, PAID, SHIPPED, CANCELLED }` 买:
- **非法状态是不可表示的** — 一个字段、一个值。
- 转变变成**在一个地方可检查**而不是由标志翻转隐含。
- 新状态（REFUNDED）是一个枚举添加 + 转变条目，`switch` 穷尽找到每个位置更新。
