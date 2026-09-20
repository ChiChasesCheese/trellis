---
nodes: [problems.commerce.auction]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction
tags: [no-archive]
---
# Design an Online Auction (eBay) — Hello Interview

值得读：把"竞价的强一致性"列为本题最核心的深入探讨点，强调必须杜绝并发出价产生的
竞态，并提出要支持大规模并发在线拍卖的场景目标。本题采纳了同样"竞价强一致、围观推送
最终一致"的一致性划分，但没有采用它自设的具体容量数字（那是这个网站自己的估算示例），
本题的容量估算完全独立重新计算，并补上了它没有展开的代理出价解析和软关闭时长两个量化
分析。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-auction)
%% trellis:end %%
