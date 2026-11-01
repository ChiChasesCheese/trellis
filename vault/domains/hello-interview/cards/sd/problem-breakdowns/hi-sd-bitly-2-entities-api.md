---
id: hi-sd-bitly-2-entities-api
node: sd.problem-breakdowns.bitly
type: qa
step: 2
---
## Q
**核心实体与 API**｜系统设计 · 问题拆解

短链服务的核心实体有哪些？创建和重定向两个接口怎么设计，用什么 HTTP 方法？

## A
**实体。** 原始 URL、短 URL、用户。先用一个简短列表和面试官对齐，字段细节留到高层设计时再补。

**接口。**
- 创建：`POST /urls`，请求体含 `long_url`，可选 `custom_alias` 与 `expiration_date`，返回 `short_url`。用 POST 是因为新建了一条长短链映射
- 重定向：`GET /{short_code}`，返回 HTTP 302 重定向到原始长链接。用 GET 是因为读取已有映射

**说法。** 十有八九用 REST，重点是选对动词：POST 新建、GET 读取、PUT 更新、DELETE 删除。接口通常与功能需求一一对应。
