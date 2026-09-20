---
nodes: [problems.realtime.llm-chat-service]
url: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
---
# Using server-sent events (MDN)

值得读：SSE 协议本身的权威参考——`text/event-stream` 格式、`EventSource` 的自动重连
行为、`retry:`/`id:` 字段语义，以及 HTTP/1.1 下浏览器对同一域名最多 6 条并发 SSE 连接
的限制（Chrome/Firefox 均标记"不会修复"，需要 HTTP/2 绕开）。本题解「深入探讨」第 1 节
在这个协议事实之上，补充了标准本身不提供的部分——服务端如何用 `requestId` 缓冲区实现
"断线重连接上生成进度"，这是产品设计层面的决策，MDN 文档不涉及。

%% trellis:begin %%
## Source
[Open the original ↗](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)

## Archived copy
![[src-mdn-llm-chat-service-clip]]
%% trellis:end %%
