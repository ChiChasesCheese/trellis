---
id: hi-c-sd-networking-essentials-n12-grpc
node: sd.core-concepts.networking-essentials.notes
type: qa
step: 12
---
## Q
**网络基础 · gRPC**｜摘要 · 必会

gRPC 是什么？为什么内部服务适合用、对外为什么不用？

## A
- **是什么：** Google 的高性能 RPC（远程过程调用）框架，基于 HTTP/2 和 Protocol Buffers。Protocol Buffers 像 JSON 但模式更严格，序列化更高效。
- **体积差异：** 同样的 id 和 name，JSON 每条消息都要重复写字段名、引号和分隔符，二进制编码只写字段编号和值，标签很瘦、整数变长编码，通常占空间小得多、解析的 CPU 也少。
- **服务定义：** 用 `.proto` 定义消息和 `service`（如 `rpc GetUser`），编译成客户端和服务端桩代码，多种语言和框架都能使用。还带流式传输、截止时间（deadline）、客户端负载均衡等运营微服务的特性。
- **适用：** 微服务之间高效通信；强类型在编译期而非运行时发现错误；二进制协议通常比 JSON over HTTP 更高效，具体提升取决于负载与基准。特别适合性能关键，或延迟主要在网络而非服务器工作的内部调用。
- **不适合对外：** 二进制协议加上工具链不如 JSON over HTTP 成熟，对你不控制的客户端不友好。常见做法是内部 gRPC、外部 REST。
- **建议：** 公开 API 用 REST，gRPC 留给内部服务间通信，尤其在传二进制数据或性能关键时；很多面试里内外都用 REST 也行。别在其他瓶颈解决前过度优化 RPC 协议。
