---
id: runtime-go-lifecycle-timeout-layers
node: runtimes.go-lifecycle
type: qa
---
## Q
Why is one `http.Client.Timeout` insufficient for a production CDN origin client?

## A
It caps the whole exchange but does not tell you which phase failed or protect every server-side phase. Configure phase-aware limits: dial, TLS handshake, response-header, idle connection, and an overall request deadline from `Context`; on servers, bound header reads and idle connections, and use write limits carefully for streaming. A single broad timeout can hide pool starvation or a slow header and may incorrectly kill legitimate long streams.

## Q zh
为什么生产 CDN 的 origin client 只配置一个 `http.Client.Timeout` 不够？

## A zh
它只限制整个 exchange，既不能说明哪个 phase 失败，也不能保护 server 端的每个阶段。应配置 phase-aware limits：dial、TLS handshake、response-header、idle connection，并从 `Context` 得到整体 request deadline；server 端限制 header read 和 idle connection，streaming 场景谨慎使用 write timeout。单一宽泛 timeout 会掩盖 pool starvation 或 slow header，也可能错误杀死合法长 stream。
