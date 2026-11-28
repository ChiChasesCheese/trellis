---
id: hi-c-sd-problem-breakdowns-n02-medium-a
node: sd.in-a-hurry.problem-breakdowns.notes
type: qa
step: 2
---
## Q
**常见题目拆解 · 中等题上半（7 道）**｜摘要 · 必会

中等难度里 Ticketmaster、Instagram、FB News Feed、Tinder、LeetCode、WhatsApp、Strava 各自的考点是什么？

## A
- **Ticketmaster：** 竞争——座位被多人同时抢；带过期的占座（分布式锁）、热门演出的排队、搜索和读缓存。
- **Instagram：** 大图 / 视频走对象存储加 CDN；信息流怎么生成；读写比极高。
- **FB News Feed：** 写扩散（发帖时推到每个粉丝的收件箱）与读扩散（读时拉取）的取舍，以及大 V 的粉丝太多怎么办。
- **Tinder：** 按位置推荐、滑动记录写量大、已看过的人不能重复出现、双向喜欢才算匹配的一致性。
- **LeetCode：** 不可信代码的沙箱执行与隔离、判题任务排队、比赛期间的排行榜。
- **WhatsApp：** 长连接实时消息、离线时消息暂存、群聊扇出、投递状态。
- **Strava：** 运动轨迹的采集和离线上传、活动数据的存储与查询、排行榜。
