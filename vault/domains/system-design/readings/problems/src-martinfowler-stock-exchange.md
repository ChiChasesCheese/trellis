---
nodes: [problems.commerce.stock-exchange]
url: https://www.martinfowler.com/articles/lmax.html
---
# The LMAX Architecture

值得读：Martin Fowler 对真实交易平台 LMAX 架构的第一手技术记录——单线程业务逻辑处理器
（Business Logic Processor）在专用硬件上实测每秒 600 万笔订单、生产环境两个撮合实例加
一个灾备站点、完整重启不到一分钟。它比多数免费题解多的地方是给出了真实的基准数字和硬件
配置，而不是停留在"单线程更快"的定性结论。本题的容量估算一节直接用这个 600 万笔/秒的
基准和本设计假设的单支股票峰值负载做对比，算出 4,000 倍冗余这个数字，这一步换算是原文
没有做的。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.martinfowler.com/articles/lmax.html)

## Archived copy
![[src-martinfowler-stock-exchange-clip]]
%% trellis:end %%
