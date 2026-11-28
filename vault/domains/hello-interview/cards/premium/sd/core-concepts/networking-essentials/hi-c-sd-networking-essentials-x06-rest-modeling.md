---
id: hi-c-sd-networking-essentials-x06-rest-modeling
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 6
---
## Q
**网络基础 · 把操作改成资源**｜考点 · 必会

把 `updateUser`、`startGame`、查某用户的帖子，设计成 RESTful 接口。

## A
- **updateUser：** `PUT /users/{id}`，正文是要更新的资源内容。
- **startGame：** 是操作不是资源。可设计成对 `/games/{id}` 的 `PATCH`，正文 `{"status": "started"}`，把"开始"表示成资源状态的变化。
- **某用户的帖子：** 嵌套资源，`GET /users/{id}/posts`。
- **创建：** `POST /users`，正文不带 ID，由服务器分配，响应 201 Created。
- **要点：** 核心实体常直接映射成资源；方法的语义（GET 和 DELETE 应幂等）要守住。
