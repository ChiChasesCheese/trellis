---
id: hi-sd-tinder-2-entities-api
node: sd.problem-breakdowns.tinder
type: qa
step: 2
---
## Q
**Tinder：实体与接口**｜系统设计 · 问题拆解

Tinder 的核心实体和三个主要接口怎么定义？位置和过滤条件分别在哪里传，为什么 feed 不需要分页？

## A
**实体。** User（既是使用者也是被展示的资料）、Swipe（滑动者 swiping_user 对目标 target_user 的 yes / no）、Match（双方互相 yes 的连接）。

**接口。**
- `POST /profile`：提交年龄区间、距离、interestedIn 等偏好
- `GET /feed?lat=&long=&distance=` 返回 User 列表
- `POST /swipe/{userId}`：请求体是 decision（yes / no）

**设计点。**
- 位置由客户端传，因为它随时会变，没必要在服务端持久化；年龄、兴趣等偏好已存好，服务端自己读
- feed 本质是推荐而不是翻页，列表用完再请求一次即可，不必加分页
- `/swipe/{userId}` 里的 userId 是被滑的对象，不是发起者；发起者必须从 JWT / 会话令牌里取，不能信请求体或请求头
