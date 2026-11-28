---
id: hi-c-sd-strava-n06-view-activities
node: sd.problem-breakdowns.strava.notes
type: qa
step: 6
---
## Q
**Strava 运动记录 · 查看自己与好友的活动**｜摘要 · 必会

已完成的活动怎么查？好友关系怎么存？

## A
- **查询：** 活动已经在库里，只需要按状态 COMPLETE 过滤，再按模式加条件：我自己的是 `userId = :me`，好友的是 `userId IN (SELECT friendId FROM friends WHERE userId = :me)`，用 LIMIT/OFFSET 分页。
- **好友表：** 两列 userId、friendId，关系双向，每对好友存两行（A→B 和 B→A）。复合主键 (userId, friendId) 防重复，再给 userId 建索引，查"某人的好友"高效。
- **两步取数据：** 先取只含基本信息和 activityId 的列表，用户点开某一项再用 activityId 取完整详情，减少首屏数据量。
- **地图：** 把路线坐标数组交给地图服务（如 Google Maps API）画出连线。
