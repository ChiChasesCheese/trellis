---
nodes: [problems.components.logger]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md
---
# awesome-low-level-design — Designing a Logging Framework

值得读：这道题在面试里被念出来的**标准版需求六条**（级别、时间戳、多目的地、可配置、线程安全、
可扩展），配一张 UML 和六种语言的实现，用来对齐"面试官脑子里的题面"最省事。它的 `Logger` 是
`__new__` 单例、`LoggerConfig` 里只放**一个** appender，于是"控制台收全部、文件只收 ERROR"
这种最常见的需求它答不出来；也完全没有 logger 层级与传播。本题解用 handler 列表 + 两层阈值
（logger 省开销、handler 做分流）取代它的单 appender，用模块级实例取代 `__new__` 单例，理由都在
"关键设计决策"里。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/logging-framework.md)
%% trellis:end %%
