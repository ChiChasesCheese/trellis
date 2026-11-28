---
id: hi-c-sd-api-design-b04-grpc-deadline
node: sd.core-concepts.api-design.beyond
type: qa
step: 4
---
## Q
**API 设计 · gRPC 与 REST 的运维差异**｜拓展 · 加分
把内部接口从 REST 换成 gRPC 后，负载均衡和排障会出什么新问题？

## A
- **长连接让四层负载均衡失效：** gRPC 基于 HTTP/2，一个连接上复用很多请求。四层（按连接分发）均衡器把一个连接钉在一台后端，导致负载不均；需要七层（理解 HTTP/2 流）的均衡器，或客户端侧均衡。
- **截止时间（deadline）：** gRPC 把"剩余时间"随调用链传下去，超时后下游就不再做无用功，比各层各自设超时更可控。
- **排障：** 二进制载荷不能直接用 curl 看，需要 `grpcurl` 或反射；日志要记录方法名和状态码。
- **兼容性规则：** protobuf 字段号一旦使用就不能复用或改类型，可以新增字段，删除字段要保留旧号，这是它的"版本策略"。
- **浏览器：** 浏览器不能直接发 gRPC，需要 gRPC-Web 之类的代理，所以对外仍多用 REST。
