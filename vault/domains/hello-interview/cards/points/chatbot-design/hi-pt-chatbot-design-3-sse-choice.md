---
id: hi-pt-chatbot-design-3-sse-choice
node: qb.sd.chatbot-design.points
type: qa
step: 3
---
## Q
**对话式 AI 聊天服务 · 为什么用 SSE 而不是 WebSocket**｜必会 · 出自：对话式 AI 聊天服务 › 整体设计

聊天回复需要逐词元推送给浏览器。应该选 SSE（Server-Sent Events）还是 WebSocket？接口上如何组织发送、停止和重新生成？

## A
**选择。** SSE。回复是单向的服务器推送，基于普通 HTTP，穿透代理与负载均衡容易，浏览器内建重连。
**接口。** `POST /conversations/{id}/messages` 返回 `text/event-stream`，不断推送 `delta`，最后推送 `done`（含消息 ID 和词元用量）；停止和重新生成是独立的 HTTP 请求。
**何时换。** 需要双向实时（语音、协同）时才用 WebSocket。
