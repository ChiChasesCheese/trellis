---
id: networking-rest-as-default
node: networking.api-styles
type: qa
---
## Q
Why does REST over JSON remain the default for public APIs in 2026, despite gRPC and GraphQL?

## A
Because a public API's clients are **unknown and uncontrolled**, and REST maximizes what strangers get for free:

- Works from any HTTP client, browser, or `curl` — zero codegen or SDK required.
- **HTTP-native caching** (GET + Cache-Control + ETags) works through CDNs and proxies.
- Uniform semantics (verbs, status codes) that every tool — gateways, monitors, WAFs — already understands.

Pick gRPC/GraphQL when you control the clients; pick REST when you don't.

## Q zh
为什么 REST over JSON 在 2026 年仍然是公共 API 的默认值，尽管有 gRPC 和 GraphQL？

## A zh
因为公共 API 的客户端是**未知和无法控制的**，REST 最大化陌生人免费获得的：

- 从任何 HTTP 客户端、浏览器或 `curl` 工作 — 零 codegen 或 SDK 需要。
- **HTTP-native 缓存**（GET + Cache-Control + ETags）通过 CDN 和代理工作。
- 统一语义（动词、状态码）每个工具 — 网关、监视器、WAF — 已经理解。

当你控制客户端时选择 gRPC/GraphQL；当你不控制时选择 REST。
