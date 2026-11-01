---
id: hi-pt-online-chess-platform-10-anti-cheat-spectate
node: qb.sd.online-chess-platform.points
type: qa
step: 10
---
## Q
**在线国际象棋平台 · 作弊检测与观战**｜出自：在线国际象棋平台 › 深入 4

引擎外挂能在对局中实时判定吗？观战者怎么接入而不拖累对局？

## A
**作弊。** 实时只做轻量信号（每步用时形态、窗口失焦）；赛后把走子日志投分析队列，用引擎（如 Stockfish）算每步偏差（平均厘兵损失）和一致率，结合历史画像打分，超阈值交人工或封号。离线流水线，不占对局路径。
**观战。** 观战者不进所有者节点，订阅只读的 `game:{id}:spectate` 频道，由网关扇出；热门对局可加几秒延迟防通风报信。
