---
nodes: [problems.components.notification-service]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/notification-service
---
# lld-python — Design a Notification Service

值得读：少见的 **Python** 实现，需求清单（多渠道、按渠道的最低优先级、退避重试、按人限流、
去重、每次尝试都要有结果对象、加渠道不碰可靠性逻辑）与本题第 1–3 关几乎一致，README 开头那句
"它看起来是写四个 send 方法，其实不是"值得抄进自己的开场白。它的实现走**装饰器栈**：
`RetryingChannel(RateLimitedChannel(DeduplicatingChannel(EmailChannel())))`。本题解在"关键设计
决策"第一条里明确不采用——每个渠道都要各自包一遍，而且跨渠道的用户级限额与优先级在装饰链里
没有位置（它的实现也确实没有优先级这一关）。同步发送、注入时钟、注入传输这三点两边一致。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/notification-service)

## Archived copy
![[src-abhaypaswan-notification-service-clip]]
%% trellis:end %%
