---
title: 'Family 9: Macro & Cross-Asset'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/09-macro-crossasset.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 9:宏观与跨资产(Macro & Cross-Asset)

> **核心概念(从零讲)**:**自上而下,不看个股,看整个经济和各大类资产之间的关系。** 利率、通胀、增长、信用、风险偏好 —— 这些宏观变量决定股/债/商品/汇率谁该涨谁该跌。**为什么存在(风险溢价 + regime)**:不同经济环境(regime)下,资产的风险报酬不同;市场对宏观转折反应有先后。**谁在另一边亏**:满仓单一资产、不做跨资产配置、在错误 regime 里押错方向的人。

> 注意:本仓库的关键实测结论:**宏观状态主要是一个"跨市场波动率定律",用来调仓位(sizing),不是用来择时牛熊收益。** 详见 [宏观状态与仓位管理](../concepts/macro-regime-and-sizing.md)。用宏观去"预测涨跌"基本不灵;用它去"什么时候该减险"才有用(VRP 是唯一稳定有效的降险信号)。

## 方向清单

69. **收益率曲线斜率(期限利差)** — 长短端利差(10Y-3M)预测增长/衰退,配置股债。**教**:期限利差、收益率曲线倒挂作为衰退信号。**数据**:本仓库 macro 层有完整 UST 曲线。
70. **信用利差 regime** — 高收益债利差扩大 = 风险偏好恶化,降险。**教**:信用利差、风险情绪代理。**数据**:macro 层 HYG/LQD。
71. **增长-通胀四象限(Growth/Inflation Quadrants)** — 按增长↑↓ × 通胀↑↓ 把环境分四类,每类配不同资产(全天候/桥水思路)。**教**:宏观 regime、资产对宏观的敏感度。
72. **风险开/关(Risk-On/Off)择时** — 用 VIX/信用/动量综合判断风险偏好,risk-off 时降险。**教**:risk-on/off、综合 regime 信号。**状态**:本仓库 [实测](../ideas/multi-asset-book.md)发现叠在趋势 book 上**帮倒忙**(滞后+冗余)—— 重要的诚实负结果。
73. **跨资产动量轮动** — 在股/债/商品/REIT/金 大类间做时序动量轮动(资产配置版趋势)。**教**:大类轮动、为什么趋势在配置层也有效。
74. **美元周期** — 美元强弱系统性影响新兴市场、商品、跨国公司。**教**:美元作为全球流动性变量。**数据**:macro 层 DXY。
75. **通胀对冲篮子** — 通胀上行时做多商品/TIPS/能源股、做空长债。**教**:通胀 beta、实物资产对冲。
76. **全球宏观相对价值** — 跨国家比较利率/汇率/股指的相对吸引力(全球宏观基金思路)。**教**:跨国相对价值、宏观套利。

## 共同的坑

- **宏观数据滞后 + 修正**:GDP、就业等是滞后发布且会被修正的,用"当时真正可得"的值,否则严重前视(本仓库 macro 层强调严格因果)。
- **样本太少**:宏观周期以年计,几十年也就几个完整周期 —— **DSR 极难过**(独立事件太少)。宏观择时的回测自由度高、样本少,是过拟合重灾区。
- **regime ≠ 收益预测**:再强调一次,宏观对**波动率/风险**的预测力远强于对**收益方向**的预测力。用错地方(拿它择时牛熊)基本亏。

延伸:[宏观状态与仓位管理](../concepts/macro-regime-and-sizing.md) · [组合构造与风险管理](11-portfolio-risk.md)。

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
