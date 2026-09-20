---
id: problems-online-judge-sse-not-websocket-verdict-stream
node: problems.realtime.online-judge
type: qa
step: 5
tags: [grown]
---
## Q
In an online judge design, why is SSE (Server-Sent Events) chosen over WebSocket for streaming a submission's per-test-case verdicts back to the client, when both would work?

## A
The verdict stream only ever needs to push data one direction — from the judge worker to the client as each test case finishes — the client never needs to send messages back over that channel during judging. WebSocket provides a full bidirectional channel, which costs connection state and complexity the judge doesn't need for this path. SSE provides exactly the unidirectional server-push semantics required, at lower connection overhead, while polling GET /submissions/{id} remains as a fallback for clients that can't hold an SSE connection.

## Q zh
在一个在线判题系统设计中，两种方案都能实现的情况下，为什么把一次提交逐条测试用例的判定结果流式返回给客户端，选择 SSE（Server-Sent Events）而不是 WebSocket？

## A zh
判题结果流自始至终只需要单向推送——从判题工作节点在每条测试跑完时推给客户端——客户端在判题过程中完全不需要通过这条通道往回发消息。WebSocket 提供的是完整的双向通道，会带来这条链路根本用不上的连接状态和复杂度开销。SSE 恰好提供所需的单向服务器推送语义，连接开销更低；同时保留轮询 `GET /submissions/{id}` 作为无法维持 SSE 连接的客户端的兜底方案。
