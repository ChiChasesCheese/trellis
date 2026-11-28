---
id: hi-c-sd-large-blobs-x04-no-size-limit
node: sd.patterns.large-blobs.exam
type: qa
step: 4
---
## Q
**大文件 · 预签名 URL 没设大小限制**｜考点 · 必会

头像上传的预签名 URL 只限定了路径。会出什么事？

## A
- **风险：** URL 到手的人可以上传任意大小，几 TB 数据推高存储成本；可以上传非图片内容，如可执行文件。
- **做法：** 把大小和类型限制签进凭证，不符合就被存储拒绝。S3 的预签名 POST 用策略条件 `content-length-range` 和 `Content-Type`；预签名 PUT 没有范围条件，只能签入确切的 `Content-Length` 和 `Content-Type`，要限制范围就用 POST 策略。其他云有各自的等价写法。
- **配套：** 缩短有效期；服务端生成不可猜测的存储键；上传先进隔离桶，扫描通过后才公开。
- **加分：** 还要按用户做配额和频率限制。
