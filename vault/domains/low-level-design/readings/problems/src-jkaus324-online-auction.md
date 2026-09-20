---
nodes: [problems.marketplaces.online-auction]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/019-auction-system
tags: [no-archive]
---
# jkaus324/machine-coding-interview-questions — 019 Auction System

值得读：这份题面把拍卖题切成了"出价策略"和"生命周期状态"两个正交的轴——
`AuctionStrategy`（Ascending / SealedBid / BuyNow）决定一次出价是否被接受、当前能公开的
最高价是多少；状态（OPEN / CLOSED / NO_SALE）只管生命周期。五种语言各给一份实现，Python
版本用一个 `create_strategy(type_)` 工厂函数在三个策略类之间切换。它和本题解只用一种规则
（代理出价加软关闭）不同，值得对照的是它怎么用同一份出价历史算出三种截然不同的"当前应该
公开的价格"——`AscendingStrategy` 公开真实最高价，`SealedBidStrategy` 在拍卖结束前永远
返回 -1（密封出价不该被任何人看到，包括拍卖行自己的查询接口），`BuyNowStrategy` 只要出价
达到底价的 1.5 倍就立即成交。三个策略类只有几行判断逻辑，在 Python 里其实可以塌缩成一个
注入的比较函数，而不需要一整族类——这也是本题解在"关闭策略"扩展点上选择"注入一个函数"而
不是"新增一个策略类"的理由。它的密封出价规则也提醒了一件本题解没有覆盖的事：如果拍卖不是
公开叫价而是密封递交，代理出价这套机制本身就不成立，因为没有"对手当前出到多少"可供压过。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/019-auction-system)
%% trellis:end %%
