---
nodes: [problems.geo.proximity]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp
tags: [no-archive]
---
# Yelp

值得读：Hello Interview 对这道题的付费拆解给出了整体的功能/非功能需求框架和规模假设
（100M 日活、1000 万商户、搜索延迟 < 500ms），并把"邻近搜索"列为需要单独深入的模块。
与本题解不同的地方在于：本题解用 Yelp 真实披露的 SEC 文件数字（App 月活 2,859.5 万、
已认领商户 773.6 万）重新推导了容量估算，并给出了完整的字节级存储计算，而不是采用一个
未说明来源的整数规模假设。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp)
%% trellis:end %%
