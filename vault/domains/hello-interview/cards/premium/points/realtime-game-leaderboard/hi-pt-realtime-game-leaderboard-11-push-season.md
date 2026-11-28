---
id: hi-pt-realtime-game-leaderboard-11-push-season
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 11
---
## Q
**在线游戏排行榜 · 赛季与推送**｜加分 · 出自：在线游戏排行榜 › 深入 7

排行榜还有哪些进阶需求：赛季重置、分地区的榜、让玩家实时看到名次变化？

## A
**赛季。** 重置靠新键，旧榜归档。
**分榜。** 地区、服务器放进键里。
**推送。** 榜单服务订阅变更，通过 WebSocket 只对打开榜单页面的在线玩家推送“你的名次变了”，不广播给所有人。
