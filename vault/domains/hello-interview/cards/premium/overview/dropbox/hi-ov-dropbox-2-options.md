---
id: hi-ov-dropbox-2-options
node: sd.problem-breakdowns.dropbox
type: qa
step: 2
tags: [通览]
---
## Q
**文件存储（Dropbox） · 高层设计**｜通览

文件存储的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 客户端、负载均衡与 API 网关、文件服务（控制平面）、元数据库、S3、CDN。

**每条路径。**
- **上传：** 客户端向文件服务要预签名 URL，服务写一条 uploading 元数据；客户端凭 URL 直传 S3，完成后元数据改为 uploaded。
- **下载：** 文件服务发 CDN 签名 URL；首次从 S3 回源，之后由最近的边缘节点提供。
- **分享：** 单独的分享表，用户 ID 作分区键、文件 ID 作排序键；查「分享给我的」直接命中，也不必改文件元数据。
- **同步：** 本地用文件系统事件发现变化再上传；远端变化经每设备一条 WebSocket 推送，客户端再定期 `changes?since=` 轮询兜底。

**存储。** 字节放 S3，字节量大且不经应用服务器；文件元数据与分享表放 DynamoDB 或 Postgres，按用户查询。
