---
nodes: [problems.realtime.multiplayer-game]
url: https://www.gabrielgambetta.com/client-server-game-architecture.html
---
# Fast-Paced Multiplayer (Client-Server Game Architecture)

值得读：客户端预测、服务器状态回放（reconciliation）、实体插值、滞后补偿这一整套快节奏
多人游戏网络技术的经典免费系列教程，免费且不需要账号。本题解把它讨论的"服务器作为权威
时间源、但为可预期的网络延迟预留缓冲"这一设计哲学，迁移到了回合制用时制式的滞后补偿上
（见「深入探讨」第 4 节），并明确说明两者的作用对象不同——原文作用在连续的世界状态时间线
上，本题解的版本作用在离散的走子级时钟扣减上。
