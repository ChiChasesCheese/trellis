---
title: 'Family 4: Low-Risk & Quality'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/04-lowrisk-quality.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 4:低风险与质量(Low-Risk & Quality)

> **核心概念(从零讲)**:**"无聊的稳公司,长期跑赢刺激的烂公司"**(风险调整后,甚至绝对都可能)。两个异象:**低波/低 beta** —— 波动小的股票每单位风险回报更高;**质量** —— 高盈利、低负债、稳定的公司更值得持有。**为什么存在(经典的结构性约束)**:很多投资者**不能用杠杆**(共同基金、散户),想博高回报只能去买高波动的"彩票股",把它们买贵了 → 高波动股长期反而回报差;同时基金经理被考核相对排名,倾向追高 beta 博出位。**谁在另一边亏**:杠杆受限却追求高回报的人、爱买彩票股的散户。这是**结构性约束**型 edge 的教科书案例。

## 方向清单

27. **低波动率(Low Volatility)** — 持有过去波动最小的一档股票。**教**:低波异象、彩票偏好、为什么"无聊"赚钱。**谁亏**:买彩票股的散户。**状态**:本项目美股/A股都测过,单独 Sharpe 0.78–0.79、**回撤显著低于大盘**,是 [多资产 book](../ideas/multi-asset-book.md) 的防御腿。
28. **Betting Against Beta(BAB)** — 做多低 beta(加杠杆)、做空高 beta(减杠杆),赌低 beta 的更优风险回报。**教**:杠杆约束、beta 与杠杆的权衡(Frazzini-Pedersen)。**状态**:本项目测过 → [被拒](../ideas/betting-against-beta.md)(干净数据上证伪)。
29. **质量 / 盈利能力(Profitability)** — 买高毛利率/高 ROE/低应计的公司。**教**:质量因子、应计异象、为什么"赚真钱"的公司被低估。**数据**:PIT 基本面。**状态**:本项目测 ROE → 大盘加宽即散、小盘负(ROE 是糟糕的杠杆放大代理)。
30. **低 beta 而非低波** — 用对大盘的 beta(而非总波动)排序,剥离特质风险。**教**:beta vs 总波动的区别。
31. **质量减垃圾(Quality minus Junk, QMJ)** — 综合盈利/成长/安全/分红打质量分,买高质量卖低质量。**教**:多维度质量合成、AQR QMJ。
32. **低杠杆 / 财务稳健** — 买低负债、高利息覆盖的公司,危机里抗跌。**教**:财务杠杆风险、防御性。
33. **盈利稳定性(低盈利波动)** — 买盈利波动小、可预测的公司。**教**:盈利质量、可预测性溢价。
34. **防御性 + 动量叠加** — 低波/质量本身慢,叠加动量做择时改善时点。**教**:因子叠加、慢因子配快择时。

## 共同的坑

- **利率敏感**:低波/质量股像"债券替代品",利率快速上行时(2022)会同步受伤 —— 不是无条件防御。
- **拥挤化**:smart-beta ETF 大量涌入低波/质量,把它们买贵了,未来溢价可能压缩。
- **价值反向**:低波/质量常和价值反向(优质公司通常不便宜),组合里要注意因子打架。
- 单独几乎过不了 DSR(本项目实测),但因为**和动量/趋势低相关**,是绝佳的[组合](11-portfolio-risk.md)分散腿。

延伸:[alpha 从哪来又为什么消失](../deep/where-alpha-comes-from.md)(结构性约束型 edge 最耐套利) · [多空·中性·自融资](../concepts/long-short-and-neutral.md)。

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
