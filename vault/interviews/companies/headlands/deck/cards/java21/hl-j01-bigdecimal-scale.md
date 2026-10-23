---
id: hl-j01-bigdecimal-scale
node: java21.j01-record
type: qa
step: 24
---
## Q
`record` 含 `BigDecimal` 组件时，为什么可能出现"数值相同但不 equal"？金额该怎么表示？

## A
`record` 的 `equals` 对引用组件用 `Objects.equals`，而 `BigDecimal.equals` 要求**数值和 scale（小数位数）都相同**，所以 `1.0` 与 `1.00` 不 equal。

对策：
- 金额用 **`long` 最小单位**（如 ticks、分）；
- 非用 `BigDecimal` 不可，就在紧凑构造器里 `stripTrailingZeros()` 或统一 `setScale`。
