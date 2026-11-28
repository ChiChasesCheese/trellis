---
id: hi-c-sd-tinder-n03-entities-api
node: sd.problem-breakdowns.tinder.notes
type: qa
step: 3
---
## Q
**Tinder · 实体与接口**｜摘要 · 必会

Tinder 的核心实体有哪些？三个接口各自传什么，位置、过滤条件和用户身份分别由谁提供？

## A
- **三个实体：**
  - User：同时代表使用者和被展示的资料。通常不把 User 列为实体，但这里用户在滑别的用户，要单列；
  - Swipe：谁（swiping_user）对谁（target_user）表达了 yes 或 no；
  - Match：两人互相 yes 之后产生的连接。
- **接口：**
  - `POST /profile`：年龄区间、距离、interestedIn 等偏好；
  - `GET /feed?lat=&long=&distance=` 返回 User 列表；
  - `POST /swipe/{userId}`，体里是 `decision: yes | no`。
- **谁提供什么：**
  - 位置和半径由客户端传，因为它随时在变，没必要落库；年龄、兴趣等偏好早已存好，服务端自己读；
  - 身份只信会话令牌或 JWT，不信请求体和请求头里的 userId，客户端可以伪造；路径里的 userId 是被滑的对象；
  - 所有接口都要登录，口述时标出即可。
- **为什么 feed 不分页：** 它是在生成推荐而不是翻一张固定列表，用完再请求一次就行，加游标反而多余。
