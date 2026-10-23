---
id: hl-j02-too-many-permits
node: java21.j02-sealed
type: qa
step: 18
---
## Q
`permits` 名单很长（如几十种变体）时怎么办？

## A
`permits` 不是越长越好。指令集的 `Update` 有 15 个子类已经啰嗦。

变体到几十种就：
- **分层**：`Instr` → `Update` / `Query`；
- 或换 `enum` + 策略（strategy）。
