---
id: hi-c-sd-strava-n03-entities-api
node: sd.problem-breakdowns.strava.notes
type: qa
step: 3
---
## Q
**Strava 运动记录 · 实体与接口**｜摘要 · 必会

Strava 的实体有哪些？接口怎么逐条对应需求，为什么用 PATCH？

## A
- **实体：**
  - User：资料与设置；
  - Activity：类型（跑步/骑行）、起止时间、路线、距离、时长；
  - Route：运动中记录的一串 GPS 坐标，也可以直接做成 Activity 的一个字段；
  - Friend：用户之间的连接，好友管理虽不做，但分享要用它。
- **接口：**
  - `POST /activities`（体：类型 RUN/RIDE）创建；
  - `PATCH /activities/:id`（体：状态 STARTED / PAUSED / COMPLETE）改状态，并且"保存"就是改成 COMPLETE，好友自动可见，不需要单独的分享接口；
  - `POST /activities/:id/routes`（体：一个 GPS 点）追加路线；
  - `GET /activities?mode=USER|FRIENDS&page=&pageSize=` 返回部分字段的列表；
  - `GET /activities/:id` 取详情。
- **为什么 PATCH：** 只传要变的字段，PUT 要求传整个资源；面试里两者可互换，但有些面试官在意 REST 规范，要准备好解释。
- **列表返回部分字段：** 只给距离、时长、日期，减少传输，点进去再取详情。
