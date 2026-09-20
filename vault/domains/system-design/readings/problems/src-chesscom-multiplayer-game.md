---
nodes: [problems.realtime.multiplayer-game]
url: https://www.chess.com/blog/CHESScom/an-update-regarding-our-server
---
# An Update Regarding Our Server

值得读：Chess.com 官方博客对一次真实过载事故的第一手记录——月活跃用户一个月内从约 700
万涨到超过 1,100 万，单日新增注册峰值 403,000，导致数据库过载和负责实时对局的 Live
Server 过载掉线，最终推动把单体 Live Server 重写为跨机器水平扩展的分布式服务、对数据库
做分片。本题解在「瓶颈、故障与演进」一节直接引用这次事故，说明"每局一个 actor 放在单机
内存里"这类简化设计必须尽早规划成可以跨机器分片，而不是等过载后才补救。
