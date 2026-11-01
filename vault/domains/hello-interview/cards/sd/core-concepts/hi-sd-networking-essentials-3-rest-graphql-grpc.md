---
id: hi-sd-networking-essentials-3-rest-graphql-grpc
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 3
---
## Q
**REST、GraphQL、gRPC**｜系统设计 · 核心概念

面试里三种 API 范式（REST、GraphQL、gRPC）各解决什么问题？默认选哪个，什么情况下改选另外两个？

## A
**要点。**
- REST：把实体当资源，用 HTTP 方法（GET、POST、PUT、PATCH、DELETE）加路径表达操作，如 `GET /users/{id}/posts`。核心实体常能直接映射成资源。默认选它，公网和内部都可以。
- GraphQL：客户端声明要哪些字段，一次请求拿齐，解决前端的欠取（under-fetching，多次往返）和过取（over-fetching）。
- gRPC：基于 HTTP/2 与 Protocol Buffers 的二进制 RPC，强类型。同样的数据 JSON 约 40 字节，二进制约 15 字节，吞吐可到数倍。

**取舍。** GraphQL 适合需求常变的复杂客户端；面试里需求固定，反而碍事，只在题目强调灵活、需求不确定时提。gRPC 用于内部服务之间；外部公开 API 仍用 REST，因为二进制协议对不受控的客户端不友好。

**易错。** 不要在其他瓶颈未解决时过早纠结 RPC 协议。
