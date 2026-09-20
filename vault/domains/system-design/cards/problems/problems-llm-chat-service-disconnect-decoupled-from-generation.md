---
id: problems-llm-chat-service-disconnect-decoupled-from-generation
node: problems.realtime.llm-chat-service
type: qa
step: 5
tags: [grown]
---
## Q
In an LLM chat service streaming tokens over SSE (Server-Sent Events), why should a dropped client connection NOT automatically cancel the in-progress generation on the GPU, and how does the server let the client catch up after reconnecting?

## A
By the time a connection drops mid-generation, the GPU has already spent real compute and memory producing the tokens generated so far; canceling on disconnect throws that already-paid-for work away, and network blips (especially on mobile) are common enough that this waste would recur constantly. Instead, generation keeps running server-side regardless of the client's connection state, with generated tokens written to a server-side buffer keyed by the request id. On reconnect, the client requests that buffer starting from the last event id it received: the server first replays whatever was generated while it was disconnected, then seamlessly continues streaming new tokens as they're produced. Only an explicit cancel call — a separate, deliberate action — actually stops generation and frees the GPU's KV cache for that request.

## Q zh
在一个通过 SSE（Server-Sent Events）流式传输 token 的 LLM 聊天服务中，为什么客户端连接断开不应该自动取消 GPU 上正在进行的生成？服务端如何让客户端在重连后接上进度？

## A zh
在生成过程中连接断开时，GPU 已经为目前为止生成的 token 花费了真实的计算和显存；一断线就取消，等于把已经付出的成本直接扔掉，而网络抖动（尤其在移动端）足够常见，这种浪费会反复发生。正确做法是：无论客户端连接状态如何，生成都在服务端持续进行，已生成的 token 被写入一个按请求 id 索引的服务端缓冲区。重连时，客户端携带上次收到的最后一个事件 id 请求这个缓冲区：服务端先回放断线期间生成的内容，再无缝切换到继续流式发送新生成的 token。只有显式的取消调用——一个独立的、刻意的操作——才会真正停止生成并释放这个请求占用的 GPU KV 缓存。
