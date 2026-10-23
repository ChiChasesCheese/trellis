---
id: hl-j15-div-direction
node: java21.j15-math-string-utils
type: qa
step: 5
---
## Q
`-7 / 2`、`Math.floorDiv(-7, 2)`、`Math.ceilDiv(-7, 2)`、`-7 % 5`、`Math.floorMod(-7, 5)` 各是多少？Java 的 `/` 和 `%` 对负数的规则是什么？

## A
- `-7 / 2 = -3`（`/` 向 **0** 截断）
- `Math.floorDiv(-7, 2) = -4`（向下取整）
- `Math.ceilDiv(-7, 2) = -3`（向上取整）
- `-7 % 5 = -2`（`%` 的符号跟被除数）
- `Math.floorMod(-7, 5) = 3`（结果永远在 `[0, n)`）

对正数：`7 / 2 = 3`，`floorDiv = 3`，`ceilDiv = 4`。
