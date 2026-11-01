---
id: hi-sd-fb-news-feed-2-entities-api
node: sd.problem-breakdowns.fb-news-feed
type: qa
step: 2
---
## Q
**新闻动态的实体与 API**｜系统设计 · 问题拆解

新闻动态的核心实体和三个主要接口怎么设计？为什么关注用 PUT，翻页用什么游标？

## A
**要点。** 实体：User、Follow（用户之间的单向链接）、Post。接口：
- `POST /posts`，请求体是内容（留空结构，兼容富文本），返回 postId。
- `PUT /users/{id}/follow`：关注谁由路径指定，关注者来自 JWT。取消关注用 DELETE（范围外）。
- `GET /feed?pageSize=&cursor=` 返回帖子列表和 nextCursor。

**为什么。** 关注是二元的，用 PUT 保证幂等，用户点两次不会出错。动态按时间倒序，翻页时看的是更旧的帖子，所以游标就是「已看到的最旧帖子的时间戳」，每页返回比它更旧的 N 条。

**易错。** 不要在显而易见的部分（帖子结构、认证）上花太多时间，说「有时间再回来」；资深候选人要把精力放在有意思的部分。
