---
id: hi-pt-online-chess-platform-9-undo-race
node: qb.sd.online-chess-platform.points
type: qa
step: 9
---
## Q
**在线国际象棋平台 · 悔棋与走子的竞态**｜出自：在线国际象棋平台 › 深入 3

走子方悔棋时对手正好落子，怎么处理？悔棋要不要对手同意？

## A
**竞态。** 每局事件串行，只有两种顺序：先处理悔棋，则校验最后一步是请求者走的，弹出该步，时钟恢复到走子前快照（每步都存了前后剩余时间），广播 `move_undone`，对手的 `move` 因 moveNo 过期被拒；先处理对手走子，则悔棋前置条件不成立，直接拒绝。
**同意。** 产品决策：无条件悔棋状态机最简单；需同意则多一个 `pending_undo` 状态，对手回应前不能走子，pending 设超时。
