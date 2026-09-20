---
nodes: [problems.commerce.stock-exchange]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood
tags: [no-archive]
---
# Design Robinhood — Hello Interview

值得读：把这道题定义为"两个正交子系统"——一个有损、软实时的报价广播，一个强一致、可
审计的订单与账本路径，用幂等键、复式记账账本、saga 三个概念串起经纪商侧的正确性。本题
采纳了同样的"两个正交子系统"框架划分交易所与经纪商的边界，但没有采用它给出的具体容量
数字（那是这个网站自设的估算示例），本题的容量估算完全独立重新计算。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/robinhood)
%% trellis:end %%
