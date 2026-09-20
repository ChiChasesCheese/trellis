---
nodes: [problems.components.logger]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/logging-service
tags: [no-archive]
---
# Hello Interview — Low-Level Design: Logging Service

值得读：商业课程的题目拆解，强项是把这道题在面试里**怎么被打分**讲得很直白——面试官先看你有没有
把"目的地"和"格式"拆开，再看你会不会主动提线程安全和异步，最后看你能不能说清关闭时日志怎么不丢。
拿它来校准分关节奏很合适。它偏向讲话术与评分维度，代码骨架仍是 Java 味的单例加 appender 列表；
本题解的重点完全落在它一笔带过的两处：logger 层级与传播的准确语义、异步 handler 的关闭契约。
付费站点，只链接不摘录。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/logging-service)
%% trellis:end %%
