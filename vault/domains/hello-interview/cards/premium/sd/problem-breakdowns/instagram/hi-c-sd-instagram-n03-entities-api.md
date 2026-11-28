---
id: hi-c-sd-instagram-n03-entities-api
node: sd.problem-breakdowns.instagram.notes
type: qa
step: 3
---
## Q
**Instagram 图片分享 · 实体与接口**｜摘要 · 必会

Instagram 的核心实体有哪些？三个接口怎么设计，大文件为什么不直接放在发帖请求里？

## A
- **实体：**
  - User（用户名、资料等，先保持最简）；
  - Post（媒体引用、说明、作者；一个实体同时服务图片和视频）；
  - Media（媒体文件本身的字节，放对象存储 S3）；
  - Follow（关注者 follower → 被关注者 followed，单向关系）。
- **接口：**
  - `POST /posts` → postId（只提交元数据，真正的字节另走预签名 URL 直传）；
  - `POST /follows`，体里只有 `followedId`；
  - `GET /feed?cursor=&limit=` → Post[] 和下一页游标。
- **关注者 ID 从登录令牌（JWT 或会话）里取，不放请求体：** 这样客户端没法冒充别人去关注，也符合最小权限；若放进体里，服务端必须比对令牌。
- **分页用游标而不是页码：** 帖子不断插入时，页码会让同一条重复出现或被跳过，游标记录"上次看到哪里"。
