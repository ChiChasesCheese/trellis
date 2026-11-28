---
id: hi-c-sd-instagram-n10-large-upload
node: sd.problem-breakdowns.instagram.notes
type: qa
step: 10
---
## Q
**Instagram 图片分享 · 大媒体的上传**｜摘要 · 必会

4GB 的视频怎么可靠地传上去？上传完成后元数据怎么更新？

## A
- **为什么要分片：** 单个 HTTP 请求的负载上限通常小于 2GB，4GB 的视频至少要拆成两次以上请求，实际更多；分片还能断点续传、并行传输。
- **流程（S3 multipart upload）：**
  - `POST /posts` 先创建元数据，返回 postId 和一个限时（例如 1 小时）的预签名 URL；
  - 客户端用分片接口直传 S3，不经过我们的服务器，省带宽和 CPU；
  - S3 自己把分片合并成完整文件。
- **更新元数据：** 创建帖子时媒体状态是 pending，上传完成后写入 S3 对象键，状态改为 complete。
  - 客户端驱动：客户端发 PATCH 报告完成。简单，但要信任客户端，客户端崩了状态就卡住；
  - 服务端驱动（推荐）：S3 事件通知触发 Lambda 或后台任务来更新。更复杂但一致性更好，我们自己掌握状态。
