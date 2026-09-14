---
title: 'Family 3: Carry'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/03-carry.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 3:Carry(套息)

> **核心概念(从零讲)**:**carry = 什么都不发生时,你持有这个头寸自动赚(或亏)的钱。** 例:借日元(利率 0%)买澳元(利率 4%),只要汇率不动,你白赚 4% 利差。**为什么存在**:carry 是最纯粹的**风险溢价** —— 你收的那点"租金",是市场付你**承担尾部风险**的报酬。**谁在另一边亏 / carry 什么时候反咬**:平时月月收租很爽,但**危机一来,carry 货币/资产暴跌**(澳元崩、利差瞬间被汇率亏抹平),"捡钢镚在压路机前"。这是**负偏**的典型。

> 记住这句:**"Carry works until it doesn't."** 它的高 Sharpe 是用"偶尔的暴亏"换来的。所以 carry 几乎一定要配尾部管理或趋势对冲。

## 方向清单

19. **FX carry** — 做多高息货币、做空低息货币,收利差。**教**:利率平价的失效(UIP puzzle)、carry 的负偏。**谁亏**:实际上是 carry 多头自己在尾部还回去 —— 你收的是承担崩盘风险的保费。**数据**:即期汇率 + 短期利率。
20. **债券 carry / 期限溢价** — 收益率曲线向上倾斜时,买长债"沿曲线下滑"赚 roll-down + 期限溢价。**教**:收益率曲线、roll-down、期限溢价。**数据**:国债收益率曲线(本仓库 macro 层有 UST3M–30Y)。
21. **商品 carry(展期收益)** — 期货曲线 backwardation(近高远低)时做多,收正展期收益;contango 时反之。**教**:期货展期、便利收益。**数据**:商品期货多合约。
22. **波动率 carry(卖 VRP)** — 隐含波动率系统性高于实际波动率,卖期权/做空 VIX 期货收这个差。**教**:[方差风险溢价 VRP](06-volatility-options.md)、当保险公司。**谁亏**:买保险对冲的人(心甘情愿付保费)。**坑**:崩盘时一次亏光几年保费。
23. **股息 carry / 股息期货** — 锁定预期股息流,赚股息风险溢价。**教**:股息折现、carry 的股票版。
24. **跨式 carry(cross-asset carry)** — 把上面几种 carry 拼成一个多资产 carry 组合(AQR "Carry" 论文)。**教**:carry 是跨资产统一的因子、分散负偏。
25. **信用 carry** — 持有高收益债收信用利差,赌不违约。**教**:信用利差、违约溢价。**数据**:本仓库 macro 层有 HYG/LQD。**坑**:违约/流动性危机时利差爆炸。
26. **加密资金费率 carry** — 永续合约资金费率持续为正时,做空永续 + 做多现货,收资金费(市场中性)。**教**:永续合约机制、资金费率。**状态**:见 [加密与 DeFi](12-crypto-defi.md),crypto 里最干净的结构性 carry 之一。

## 共同的坑

- **负偏是结构性的**:几乎所有 carry 都是"平时小赚、偶尔暴亏"。单看 Sharpe 会高估安全性(本项目 [book 的负偏问题](../ideas/multi-asset-book.md)同源)。**必配尾部管理或趋势对冲。**
- **拥挤 + 杠杆**:carry 因 Sharpe 好看而被加杠杆,崩盘时挤兑式平仓放大亏损。
- 和趋势是天生一对:carry 收租、趋势在崩盘里赚 —— 两者负相关,合起来平滑(见 [组合方法](11-portfolio-risk.md))。

延伸:[宏观状态与仓位管理](../concepts/macro-regime-and-sizing.md) · [危机凸性 vs 做空溢价](../concepts/crisis-convexity-vs-short-premium.md)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [catalog 总览](index.md) · [策略风格光谱](../deep/strategy-styles.md) |
| 下游 | [想法库](../ideas/index.md) · [playbook](../playbook.md) |
| 同域 | [策略家族图谱](../reference/strategy-families.md) · [alpha 从哪来](../deep/where-alpha-comes-from.md) |
| ADR / concepts | [交易 101](../concepts/trading-101.md) · [为什么回测会撒谎](../concepts/why-backtests-lie.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [深入理解](../deep/index.md) · [跑一个实验](../guides/run-an-experiment.md)
- **增长纪律:** 新方向 → 本页加一行 + [`ideas/_template.md`](../ideas/_template.md);探针 `quant scout`
