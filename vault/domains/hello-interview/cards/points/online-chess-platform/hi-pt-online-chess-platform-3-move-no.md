---
id: hi-pt-online-chess-platform-3-move-no
node: qb.sd.online-chess-platform.points
type: qa
step: 3
---
## Q
**在线国际象棋平台 · 走子消息带 moveNo**｜出自：在线国际象棋平台 › 核心实体与接口

走子消息里为什么要带期望的下一步序号 `moveNo`？它解决了什么问题？

## A
**要点。** `moveNo` 是期望的下一步序号，让重复发送和乱序到达都能被幂等地拒绝或忽略。
**配合。** 移动网络断线重连是常态，所以需要凭 `moveNo` 补发缺失步的机制。
**悔棋。** 悔棋后对手那条 `move` 带的 `moveNo` 已过期，被拒绝，客户端回滚到最新局面。
