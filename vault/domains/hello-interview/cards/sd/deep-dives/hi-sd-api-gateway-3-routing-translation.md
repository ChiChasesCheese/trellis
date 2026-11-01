---
id: hi-sd-api-gateway-3-routing-translation
node: qb.sd.distributed-rate-limiter.pre-sd-deep-dives-api-gateway
type: qa
step: 3
---
## Q
**路由表与协议、响应转换**｜系统设计 · 深入技术

网关怎么决定把请求发给哪个服务？当内部服务用 gRPC 而客户端用 HTTP 时怎么办？

## A
**路由表。** 网关维护一张映射表，依据 URL 路径、HTTP 方法、查询参数、请求头组合匹配，例如 `/users/*` 到用户服务、`/orders/*` 到订单服务、`/payments/*` 到支付服务，查表很快。

**协议转换。** 客户端发 HTTP GET `/users/123/profile`，网关可转成内部 gRPC 调用 `getProfile`，再把 gRPC 响应转回 JSON 返回。内部可以选最高效的协议，客户端无感。

**取舍。** 实际中多数服务都说 HTTP，协议转换相对少见，不要在面试里当作主角。
