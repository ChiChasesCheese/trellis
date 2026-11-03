---
id: hi-sd-dropbox-2-entities-api
node: sd.problem-breakdowns.dropbox.exam
type: qa
step: 2
---
## Q
**Dropbox：核心实体与接口**｜系统设计 · 问题拆解

Dropbox 的核心实体和上传、下载、分享、同步四个接口怎么定义？接口里怎么识别当前用户？

## A
**实体。** 三个就够：File（原始字节）、FileMetadata（名称、大小、MIME 类型、上传者等）、User。

**接口。**
- 上传：先写成 `POST /files`（带文件和元数据），后面会演化
- 下载：`GET /files/{fileId}`
- 分享：`POST /files/{fileId}/share`，请求体是被分享的用户列表
- 同步：`GET /files/changes?since={timestamp}`，返回 ChangeEvent 列表（fileId、变更类型 created / updated / deleted、新元数据），客户端只拉上次同步之后的变更

**易错。** 不要用请求体或请求头里的 userId 识别调用者，客户端可以伪造。应校验会话令牌或 JWT 得到当前用户，再检查他对目标文件的权限。

**说法。** 先说「我先给出简单接口，深入后可能回头改」，因为上传下载接口后面会因预签名 URL 大幅改变。
