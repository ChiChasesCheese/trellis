---
id: hi-pt-tt-double-entry-ledger-4-reverse
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 4
---
## Q
**复式账本（类设计） · 冲正代替修改**｜出自：复式账本（类设计） › 整体设计

录错的分录怎么改？`reverse` 怎么实现，为什么不直接改？

## A
**做法。** 永远不改：`reverse` 取出原分录，每条腿取反，用新 ID 写成新分录，`reverses` 指回原分录；再写一条正确的分录，两条都带原因和操作人。
**为什么。** 原分录原样保留，下游从日志能看到「错了、改了、改成什么」。例：冲正后余额回到原值，日志多一条，无一被改动。
