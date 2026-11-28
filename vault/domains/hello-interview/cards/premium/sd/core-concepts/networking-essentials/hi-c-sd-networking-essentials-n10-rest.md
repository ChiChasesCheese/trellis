---
id: hi-c-sd-networking-essentials-n10-rest
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 10
---
## Q
**网络基础 · REST**｜摘要 · 必会

REST 的核心思想是什么？怎么把"操作"改写成"资源"？默认选它合适吗？

## A
- **核心：** 客户端对资源（像数据库表或服务器上的文件）执行简单操作。设计的主要挑战是给资源建模并定义可以对它们做什么，借用 HTTP 方法并遵循关于路径和正文的约定，常用 JSON 表示资源（不是必须）。核心实体常能直接映射成资源。
- **例子：** `GET /users/{id}` 取用户；`PUT /users/{id}` 更新已有资源；`POST /users` 创建新资源，正文里不给 ID，由服务器分配；`GET /users/{id}/posts` 用嵌套表示用户有很多帖子。
- **从操作到资源：** `updateUser`、`startGame` 是操作，不是资源，不 RESTful。改成 `PUT /users/{id}`；`startGame` 可以是对 `/games/{id}` 的 `PATCH`，正文 `{"status": "started"}`。
- **适用：** 灵活，适合各种用例（ElasticSearch 用它管理文档、配置索引）。不是高吞吐服务的最高性能方案，JSON 序列化也低效，但多数应用不会被序列化卡住。
- **建议：** 和 TCP 一样，面试默认选 REST；有 REST 满足不了的特定需求再考虑 GraphQL、gRPC、SSE、WebSocket。
