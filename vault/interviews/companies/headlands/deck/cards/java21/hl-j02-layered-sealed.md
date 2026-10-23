---
id: hl-j02-layered-sealed
node: java21.j02-sealed
type: qa
step: 9
---
## Q
`sealed interface` 怎么分层（一个 sealed 接口继承另一个）？写出指令集 `Instr` → `Update` / `Query` 的结构，并说明好处和中间层的限制。

## A
```java
sealed interface Instr permits Update, Query {}
sealed interface Update extends Instr permits And, Or, Xor /* ... 共 15 个 */ {}
sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}
```
真实指令集：15 种更新 + 3 种查询。

好处：可对 `Instr` 做大 `switch`，也可只对 `Update` 做（只处理 15 种）。

限制：中间层接口必须是 `sealed` 或 `non-sealed`，**接口不能 `final`**。
