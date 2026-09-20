---
nodes: [problems.marketplaces.stock-brokerage]
url: https://github.com/kumaransg/LLD/tree/main/StockExchange
---
# kumaransg/LLD — StockExchange（Navi 面试的 geektrust 题面，Java）

值得读：这是被真实面试用过的版本，题面把**价格-时间优先**写得比任何一份 OOD 题面都清楚
（"同一价位上最先进簿的单最先成交"），并给了一组标准输入输出——六张单、四笔成交——非常适合
当回归用例，本题解的确定性测试用的就是这组序列。代码是 Java，分层为 dao/model/service/ui，
`OrderFactory` 造 `BuyOrder` / `SellOrder` 两个子类；Python 里这两个子类应该塌缩成一个 `Side`
枚举。与本题解唯一但关键的分歧在成交价规则：它规定"成交一律记在**卖单**的价上"，所以在
"买单先挂、更低价的卖单后到"那一笔上，它让买家按 236.00 成交，而本题解按挂单方（买方）
公布的 237.80 成交。看懂这处差别，就看懂了 maker/taker 的价格改善归谁。
