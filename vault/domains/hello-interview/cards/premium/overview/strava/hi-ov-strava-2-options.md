---
id: hi-ov-strava-2-options
node: sd.problem-breakdowns.strava
type: qa
step: 2
tags: [通览]
---
## Q
**Strava 运动记录 · 高层设计**｜通览

Strava 运动记录的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 手机应用、活动服务、数据库；地图交给地图服务画。

**每条路径。**
- **开始、暂停、结束、保存：** 手机 POST 创建活动，再用 PATCH 改状态为 STARTED、PAUSED、COMPLETE；库里存状态加时间戳的日志，用时是各段运行区间之和。
- **运动中看数据：** 手机按固定间隔取 GPS 点，用 Haversine 公式累加距离；最简版把点发给服务写进 Route 表，深挖后改为只在本机计算。
- **查看活动：** GET 按 COMPLETE 状态过滤，自己的按 userId，好友的按好友表子查询，先返回列表，点开再取详情。

**存储。** 活动、路线、好友都放一个关系库，规模靠分片和分层；好友表每对好友存两行，复合主键防重复。
