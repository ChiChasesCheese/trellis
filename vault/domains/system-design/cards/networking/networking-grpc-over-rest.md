---
id: networking-grpc-over-rest
node: networking.api-styles
type: qa
---
## Q
When choose gRPC over REST for service-to-service calls — and what do you give up?

## A
Choose gRPC when **you own both ends**: internal microservices wanting compact binary payloads (protobuf), generated typed clients, low per-call overhead, and first-class **streaming** (client, server, bidi) over HTTP/2.

Give up: human-readable payloads, effortless browser support (needs gRPC-Web or a proxy), and HTTP-native caching/tooling. Public-facing APIs stay REST/JSON; gRPC is the internal default.

## Q zh
什么时候为服务到服务调用选择 gRPC 而不是 REST — 你放弃什么？

## A zh
当**你拥有两端**时选择 gRPC：内部微服务想要紧凑的二进制有效载荷（protobuf）、生成的类型化客户端、低每次调用开销，以及对 HTTP/2 的一流**流**支持（客户端、服务器、双向）。

放弃：人类可读的有效载荷、无缝的浏览器支持（需要 gRPC-Web 或代理），以及 HTTP-native 缓存/工具。面向公众的 API 保持 REST/JSON；gRPC 是内部默认。
