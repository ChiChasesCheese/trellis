---
nodes: [microstructure.adverse-selection, microstructure.spread, microstructure.queue-position, microstructure.market-making-pnl]
tags: [drill]
---
# 练习：用 markout 判断哪些订单流在让你亏钱

你在一只价差 0.02 美元（半价差 0.01 美元）的股票上做市。把一天的成交按来源分组，算成交后 1 秒的 markout（成交后过固定时间，用那一刻的中间价重新评估这笔成交的每股盈亏）：散户经批发商转来的单 +0.004，指数基金调仓单 +0.001，跨市场套利者的单 −0.006。另有一份估计：知情成交之后，价格平均再朝不利方向走 0.04 美元；不知情成交之后价格不动。

**要你给出的**
- 算出半价差 0.01 时，知情成交占比到多少你开始赔钱；半价差改成 0.02 后这个占比变成多少。
- 读上面三组 markout：哪一组该给更窄的价差、哪一组该拉宽或缩量；并说出批发商为什么愿意花钱买散户的单。
- 财报公布前一分钟，你的报价该怎么变；说清拉宽价差的代价最后落在谁身上。
- 解释排在队尾的挂单为什么比队首更容易亏钱，以及"撤单保命"和"保住队首位置"怎么取舍。

**评分要点**
- 逆向选择的机制：对手愿意成交，恰恰因为这笔交易对他有利；你挂的报价等于给全世界免费提供选择权 ([[hft-adverse-selection-mechanism]])
- 平衡占比 = 半价差 ÷ 知情成交后的价格移动：0.01 ÷ 0.04 = 25%，半价差拉到 0.02 后是 0.02 ÷ 0.04 = 50%；只拉宽价差就能承受更高的知情占比 ([[hft-adverse-selection-breakeven]], [[hft-participants-breakeven-numbers]])
- markout 的算法（买入用之后的 mid 减买入价，卖出相反）、取 1 毫秒到 1 分钟多个时间尺度，平均为负就是有毒订单流 ([[hft-adverse-selection-markout]], [[hft-adverse-selection-toxic-flow]])
- 区别对待：散户单毒性低，窄价差、大量；套利者的单平均 markout 为负，拉宽、缩量、撤得更快。批发商付钱买散户单，正是因为它的 markout 为正 ([[hft-adverse-selection-toxic-flow]], [[hft-spread-components]])
- 财报前的做法：先缩量或撤单，价差从 0.01 拉到 0.10 甚至更宽，公布瞬间撤掉所有旧报价；代价由想在这一刻交易的普通投资者承担，流动性在最需要时消失 ([[hft-spread-event-widening]], [[hft-participants-flow-withdraw]])
- 队尾的单要等前面的订单全被吃光才成交，说明这一价位被一路清空、价格很可能继续走坏；队首的单常在小卖压下成交，之后价格还会回弹 ([[hft-queue-position-adverse-in-queue]], [[hft-queue-position-fifo-queue]])
- 撤单会丢掉队首位置，重挂排到队尾；信号越强越该撤，信号弱就留着，比较"留下被吃的期望亏损"和"放弃位置的价值" ([[hft-queue-position-cancel-cost]])
- 用盈亏分解检查结论：价差收益 − 逆向选择损失 − 库存损失 + 费用返佣净额，逆向选择常占掉价差收益的大头 ([[hft-market-making-pnl-decomposition]])

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
