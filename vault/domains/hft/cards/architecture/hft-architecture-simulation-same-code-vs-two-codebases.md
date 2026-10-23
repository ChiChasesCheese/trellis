---
id: hft-architecture-simulation-same-code-vs-two-codebases
node: architecture.simulation
type: qa
step: 4
---
## Q
研究员用 Python 写一份回测，工程师用 C++ 另写一份生产代码，与"回测和生产跑同一份代码"相比，有什么风险？

## A
两份代码对同一份行情可能给出不同的订单：舍入、边界条件、事件处理顺序的细微差别累积起来，就是"研究显示赚钱，实盘不赚钱"，而且很难判断差在哪一份。

跑同一份代码时，回测与生产的区别只剩输入来源和模拟器，差异容易定位。

如果现实中必须有两份实现（比如 Python 做研究原型），就用**差分测试（differential testing）**：把同一天的数据喂给两个实现，逐笔比较订单输出，必须一致；有差异就逐条解释并修正。
