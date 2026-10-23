---
id: hl-j14-inference-fix
node: java21.j14-stream-api
type: qa
step: 14
---
## Q
`Collectors.teeing(minBy(Comparator.naturalOrder()), maxBy(Comparator.naturalOrder()), ...)` 编译报 `inference variable T#1 has incompatible upper bounds`，怎么修？

## A
`teeing` 和 `mapMulti` 的泛型很深，类型推断失败时报错很长。修复：给泛型方法加**显式类型参数**，例如 `Comparator.<Long>naturalOrder()`。

经验：`teeing`/`mapMulti` 推导不动时，先加显式类型参数（`.<Fill>mapMulti(...)`）。编译器除此之外几乎什么都不做：它们都是库方法，无新语法。
