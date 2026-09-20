---
id: problems-logger-chain-vs-handler-list
node: problems.components.logger
type: qa
step: 2
tags: [grown]
---
## Q
日志框架要把一条记录同时送到控制台、文件和告警三个目的地。用责任链模式（Chain of Responsibility）把 handler 串起来，和让 logger 直接持有一个 handler 列表，该选哪个？

## A
选列表。责任链的核心规则是**某个处理者接下请求之后就停止**（审批流里正好只该有一个人负责）；日志要的是广播——一条 ERROR 必须同时到达所有目的地。套用责任链就必须把"接住就停"这条规则删掉，剩下的只是"用 `next` 指针串起来的列表"，那不如直接用列表：加目的地不用维护指针，handler 之间零耦合，同一个 handler 还能同时挂在多个 logger 上。面试里主动说出"我考虑过责任链，但它的终止语义和日志的广播语义相反，用它就得把模式的核心删掉"，比背出模式名字值钱得多。
