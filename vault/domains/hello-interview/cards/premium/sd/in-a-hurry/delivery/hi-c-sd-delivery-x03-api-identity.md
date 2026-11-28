---
id: hi-c-sd-delivery-x03-api-identity
node: sd.in-a-hurry.delivery.exam
type: qa
step: 9
---
## Q
**交付框架 · 找出 API 设计的安全错误**｜考点 · 必会
候选人写出：`POST /v1/followers`，请求体 `{ "follower_id": "u1", "followee_id": "u2" }`；`GET /v1/users/{userId}/feed`。有什么问题？怎么改？

## A
- **问题：** 当前用户的身份来自请求体和路径参数，客户端可以随便填别人的 ID，冒充他人关注、读取别人的 feed。
- **改法：** 身份从认证令牌（请求头里的 JWT）里解出。`POST /v1/follows`，请求体只含 `{ "followee_id": "u2" }`；`GET /v1/feed`，由令牌决定是谁的 feed。
- **补充：** 读取他人公开资料才用路径参数的用户 ID；所有端点都要认证。资源用复数名词。
