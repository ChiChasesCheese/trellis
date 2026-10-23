---
id: hl-j02-sealed-vs-open
node: java21.j02-sealed
type: qa
step: 19
---
## Q
什么场景应该选开放的 `interface` 而不是 `sealed`？`sealed` 适合什么场景？

## A
**选开放 `interface`**：需要让使用者（别的团队、插件、测试替身）自己**提供实现**，如 `Comparator`、`Runnable`、`Handler`；以及变体很多且经常新增时。

**选 `sealed`**：变体由你控制、几乎不变；只想让用户**消费**你返回的类型，如 `sealed interface Result`。
