---
id: hi-sd-api-design-5-rpc-grpc
node: qb.sd.book-seller-platform.pre-sd-core-concepts-api-design
type: qa
step: 5
---
## Q
**RPC 与 gRPC 何时用**｜系统设计 · 核心概念

RPC 和 REST 的思路有什么不同？gRPC 为什么比 JSON 加 HTTP 的 REST 更快，什么时候在面试里选它？

## A
**要点。** REST 是资源导向，RPC 是动作导向：像调用本地函数一样远程调用，如 `getEvent(eventId)`、`createBooking(...)`，`checkPermission(userId, resource)` 这类检查权限的动作用 RPC 比硬套成资源更自然。

**机制。** gRPC 用 Protocol Buffers 做二进制序列化，用 HTTP/2 传输；`.proto` 文件定义服务方法和消息，一份定义可以生成多种语言的客户端和服务端代码，Go 的订单服务和 Java 的支付服务之间有编译期类型安全。支持双向流。Apache Thrift 是类似的框架。

**何时用。** 性能关键、类型安全重要、服务间通信、需要流式传输；面试官提到微服务、内部 API、多语言环境。

**取舍。** 典型组合：面向手机和网页的公共接口用 REST，订票、支付、库存等内部服务之间用 gRPC。除非被问到，API 环节只画面向用户的接口，最多在高层设计里说一句内部走 RPC。
