---
nodes: [amazon.amz-emergency-pubsub]
url: https://www.hellointerview.com/community/questions?company=Amazon
tags: [no-archive]
---
# Hello Interview 社区题库：Amazon（题目 publish-subscribe-system）

值得读：2026-10-01 的中级报告，原话是：需要一个应急响应系统，一些组件订阅（监听）应急事件，另一些组件发布（通知）这些事件，请实现处理发布与订阅逻辑的类。公开可见的只有这一句，事件有哪些类型、严重度、是否异步、失败怎么办，报告都没有写。本题解把这些全部标为重建，并按 Amazon 另一份较早的报告（事件转发框架：批量、慢事件、失败不得阻塞其他订阅者）把「失败隔离」放在第 2 关。
