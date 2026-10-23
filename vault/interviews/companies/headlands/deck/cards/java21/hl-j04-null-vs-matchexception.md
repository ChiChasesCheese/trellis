---
id: hl-j04-null-vs-matchexception
node: java21.j04-record-patterns
type: qa
step: 22
---
## Q
record 模式相关的 `NullPointerException` 与 `MatchException` 各在什么情况下出现？

## A
- 外层 record 为 `null`（且无 `case null`）→ **NPE**；
- record 的**访问器抛异常** → `MatchException`（原异常在 `cause`）；
- 模式没覆盖的值 → 仅当 `sealed` 层级在编译之后被改过（新增变体而 `switch` 未重编译）时才抛 `MatchException`。

容易混淆，排查时先看异常类型：NPE 说明选择器或外层为 null；`MatchException` 看 `cause` 和是否有版本不一致。
