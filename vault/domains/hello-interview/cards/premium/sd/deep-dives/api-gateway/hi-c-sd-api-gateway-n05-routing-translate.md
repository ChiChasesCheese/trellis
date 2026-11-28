---
id: hi-c-sd-api-gateway-n05-routing-translate
node: sd.deep-dives.api-gateway.notes
type: qa
step: 5
---
## Q
**API 网关 · 路由表、协议转换与响应转换**｜摘要 · 必会

网关怎么知道请求该发给哪个服务？内部服务用 gRPC 而客户端用 HTTP 时怎么办？

## A
- **路由表：** 一张映射表，按 URL 路径、HTTP 方法、查询参数、请求头组合匹配，例如 `/users/*` 到用户服务、`/orders/*` 到订单服务。表是内存里的，查询很快。
- **协议转换：** 客户端发 HTTP GET `/users/123/profile`，网关转成内部的 gRPC 调用，再把 gRPC 结果转回 JSON 返回。好处是内部服务可以选最高效的协议，客户端无感知。
- **现实：** 大多数内部服务仍说 HTTP，协议转换并不常见，只当作可选能力提一句，不要当主角。
- **响应转换的同一思路：** 内部格式可以丑，对外保持干净一致的 API。
