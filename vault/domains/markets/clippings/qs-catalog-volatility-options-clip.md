---
title: 'Family 6: Volatility & Options'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/06-volatility-options.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 6:波动率与期权(Volatility & Options)

> **核心概念(从零讲)**:**你可以当保险公司。** 期权是保险:别人怕暴跌,买期权对冲,付你保费。统计上,**隐含波动率(期权价格里隐含的"预期波动")长期高于实际波动率** —— 这个差叫**方差风险溢价(VRP)**,就是保费里的利润。卖期权/卖波动率 = 系统性收这个保费。**为什么存在(风险溢价)**:人**厌恶不确定性、愿意为安心多付钱**,尤其怕崩盘(左尾)。**谁在另一边亏 / 付保费**:对冲基金、养老金买保护的人。**卖方什么时候反咬**:崩盘真来时,一次赔光几年保费(负偏到极致)。

> 这是**风险溢价型 alpha 最纯粹的形态**:平时月月收保费(高 Sharpe),崩盘时巨亏。和趋势(危机里赚)是绝配。本仓库的 [VRP 研究](../concepts/macro-regime-and-sizing.md)发现 VRP 是**唯一能用的降险信号**。

## 方向清单

42. **卖方差风险溢价(Short VRP)** — 卖跨式/做空 VIX 期货,收隐含-实际之差。**教**:VRP、隐含 vs 实际波动率、保险商心态。**谁亏**:买保护的人。**坑**:崩盘一次清零,**必须**带尾部对冲或仓位上限。
43. **波动率风险溢价择时** — 只在 VRP 为正/够厚时卖,VRP 转负时离场或反手。**教**:VRP 作为 regime 信号(本仓库实测它是有效的降险信号)。
44. **离散度交易(Dispersion)** — 卖指数波动率、买成分股波动率(指数波动 < 成分股波动之和,因相关性)。**教**:相关性溢价、指数 vs 个股波动。**数据**:个股 + 指数期权。
45. **波动率风险偏斜(Skew / 25-delta)** — 下跌保护(put)比上涨(call)贵,交易这个偏斜的均值回归。**教**:波动率微笑/偏斜、崩盘恐惧定价。
46. **波动率期限结构** — VIX 期货 contango(远月贵)时做空滚动,赚 roll-down(波动率版 carry)。**教**:波动率期限结构、roll yield。**坑**:崩盘时期限结构瞬间倒挂、巨亏。
47. **Gamma scalping / 做多波动率** — 买期权 + 动态对冲,赌实际波动 > 隐含(VRP 的反面,危机里赚)。**教**:gamma、delta 对冲、为什么这是凸的。
48. **尾部对冲(Tail Hedge / 长尾凸性)** — 长期小额买深度虚值 put,平时小亏、崩盘暴赚 —— 给整个 book 买保险。**教**:凸性、为什么"持续小亏"换"危机暴赚"值得。**用途**:正是 [多资产 book](../ideas/multi-asset-book.md) 改善负偏的候选工具。
49. **隐含波动率因子(横截面)** — 跨股票按隐含波动率/VRP 排序选股(不交易期权,用期权信息选正股)。**教**:用期权市场的信息给股票打分。**数据**:个股期权链。
50. **波动率目标 / 波动率管理的因子** — 用波动率信号动态缩放任意策略仓位(波动高时减仓),提升 Sharpe、削尾部。**教**:vol targeting、波动率聚集性。**状态**:本项目 book 用了 10% vol-target,是标准做法。

## 共同的坑

- **左尾杀手**:卖波动率类策略的回测 Sharpe 极具欺骗性 —— 它把"偶尔清零"藏在平滑的收租曲线后。**[Deflated Sharpe](../concepts/multiple-testing.md) + 偏度/肥尾诊断是必须的。**
- **数据贵 + 难**:期权数据(隐含波动率曲面、希腊字母)是付费、难处理的;很多想法卡在数据获取。
- **执行复杂**:期权有流动性、价差、保证金、到期等一堆现实摩擦,回测极易过于乐观。

延伸:[宏观状态与仓位管理](../concepts/macro-regime-and-sizing.md)(VRP 作为降险信号的实测) · [危机凸性 vs 做空溢价](../concepts/crisis-convexity-vs-short-premium.md)。

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
