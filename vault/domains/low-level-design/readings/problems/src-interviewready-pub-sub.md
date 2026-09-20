---
nodes: [problems.components.pub-sub]
url: https://github.com/InterviewReady/Low-Level-Design/tree/main/distributed-event-bus
tags: [no-archive]
---
# InterviewReady/Low-Level-Design — distributed-event-bus

值得读：它的 README 是一份**加分项清单**，基本就是本题第 3、4 关的来源——可配置重试次数、
死信队列、事件接收的幂等、推拉双模、从某个时间戳或位点开始订阅、订阅前置条件。Java 实现，
用一个 `KeyedExecutor` 把同一 key 的事件串行化，这个思路本题解放在"扩展与追问"里作为
"按 key 保序"的答案。分歧在于它把"按位点订阅"和"推模式"做成两条独立的代码路径，而本题解只有
一条：推只是拉之上的一层投递线程，存储与位点完全共用。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/InterviewReady/Low-Level-Design/tree/main/distributed-event-bus)
%% trellis:end %%
