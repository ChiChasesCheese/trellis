---
nodes: [problems.social.chat-messaging]
url: https://highscalability.com/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an/
tags: [engineering-blog]
---
# How WhatsApp Grew to Nearly 500 Million Users, 11,000 Cores, and 70 Million Messages a Second
值得读：记录了 WhatsApp 早期用 Erlang + 定制 FreeBSD 内核做到单机百万级并发连接、11,000+ 核心支撑约 5 亿用户、峰值约 70 万消息/秒的真实历史数字，是本题解容量估算里"专用栈上限 vs 商用栈默认假设"这组对比的原始出处。本题解与它的隐含立场不同之处：本题解不建议默认架构照抄这套专用栈,而是把它当作可选的深度优化方向。

%% trellis:begin %%
## Source
[Open the original ↗](https://highscalability.com/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an/)

## Archived copy
![[src-highscalability-chat-messaging-clip]]
%% trellis:end %%
