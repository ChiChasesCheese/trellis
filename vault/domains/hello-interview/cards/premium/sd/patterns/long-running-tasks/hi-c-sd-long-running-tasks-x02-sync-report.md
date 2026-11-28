---
id: hi-c-sd-long-running-tasks-x02-sync-report
node: sd.patterns.long-running-tasks.exam
type: qa
step: 2
---
## Q
**长任务 · 同步生成报告的 API 怎么改**｜考点 · 必会

`POST /report` 现在同步等 45 秒才返回，偶尔超时。重新设计接口。

## A
- **返回方式：** 立刻返回任务 ID 和 `pending` 状态（常用 202 Accepted），任务入队。
- **查询：** 提供状态接口让客户端轮询，或在完成后用邮件、推送、WebSocket 通知。
- **重复提交：** 用幂等键避免用户连点生成多份。
- **结果存放：** 文件放对象存储，状态里带下载链接。
- **面试加分：** 讲清状态机（pending、processing、completed、failed）和失败时的通知。
