---
id: hi-pt-url-shortener-design-3-api
node: points.url-shortener-design
type: qa
step: 3
---
## Q
**短链接服务 · 核心接口与状态码**｜出自：短链接服务 › 核心实体与接口

短链接服务的核心实体和接口怎么定？创建、跳转在别名重复、短码不存在或已过期时分别返回什么状态码？

## A
**实体。** `Url(shortCode PK, longUrl, ownerId, createdAt, expiresAt)`。
**接口。** `POST /urls {longUrl, alias?, expiresAt?}` 返回 shortUrl，别名已存在返回 `409`；`GET /{shortCode}` 返回 `302 Location`，不存在或过期返回 `404`（或 `410`）。
