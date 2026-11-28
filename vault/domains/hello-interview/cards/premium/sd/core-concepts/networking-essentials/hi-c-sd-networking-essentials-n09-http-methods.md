---
id: hi-c-sd-networking-essentials-n09-http-methods
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 9
---
## Q
**网络基础 · 常见 HTTP 方法与状态码**｜摘要 · 必会

常用的 HTTP 方法和状态码各是什么含义？

## A
- **方法：** GET 取数据（应是幂等的，没有正文）；POST 向服务器发送数据；PUT 更新数据；PATCH 部分更新资源；DELETE 删除数据（应是幂等的）。
- **2xx 成功：** 200 OK 请求成功；201 Created 成功且创建了新资源。
- **3xx 重定向：** 302 Found 资源临时移动；301 Moved Permanently 永久移动。
- **4xx 客户端错误：** 404 Not Found；401 Unauthorized 需要认证；403 Forbidden 服务器理解请求但拒绝授权；429 Too Many Requests 单位时间内请求太多。
- **5xx 服务器错误：** 500 服务器内部错误；502 Bad Gateway 从上游服务器收到无效响应。
- **面试分寸：** 知道常见的就好，除非设计 RESTful 接口，否则很少深入。
