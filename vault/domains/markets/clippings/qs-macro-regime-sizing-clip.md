---
title: Macro Regime and Position Sizing
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/macro-regime-and-sizing.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 宏观状态与仓位管理

这一层回答一个具体问题:**怎么用宏观信息(收益率曲线、VIX、信用利差)来管理仓位、应对牛熊?** 结论可能和直觉相反,所以先把结论摆前面:

> **宏观状态是一个经跨市场验证的*波动率*预测器,不是股票*收益*择时信号。所以它的正确用法是仓位 sizing(降险/控波动),而不是"熊市清仓"式的牛熊择时。**

下面解释这条结论怎么来的、怎么用。

![macro-regime-sizing](../diagrams/macro-regime-sizing.drawio)

## 三层架构

![macro-three-layer](../diagrams/macro-three-layer.drawio)

数据基线已提交在 `market_data/macro/`(2004→今),像 `market_data/` 一样从 `main` 继承,研究脚本走 cache-first 取数。CLI:`quant macro`(列目录+覆盖)、`quant macro-ingest`。

## 为什么是波动率,不是收益

我们在四个**不同市场**(美股 SPX 为锚,EM 股 EEM、外汇 EUR/USD、加密 BTC 作交叉验证)上,把美国宏观 risk-off 状态对**前向** 21 日结果做了条件检验(非重叠子样本,诚实 t 检验):

| 市场 | risk-off 前向波动 | risk-on 前向波动 | 比值 |
|---|---|---|---|
| SPX(锚) | 20.2% | 11.4% | **1.77** |
| EEM | 27.0% | 17.3% | **1.56** |
| EUR/USD | 8.0% | 7.2% | 1.12 |
| BTC | 60.1% | 57.9% | 1.04 |

- **前向波动规律:4/4 市场同号一致**(传统市场显著)——risk-off 可靠地预示更高波动。这是**强置信度的跨市场定律**。
- **前向收益规律:不一致(1/4)**——股票/外汇 risk-off 后反而略涨(均值回归/"恐慌后反弹"),只有 BTC 例外。

所以拿宏观状态去做"熊市清仓"的收益择时,在快速 V 型危机(如 COVID)会**反向误时**——这也复现了项目早期对朴素 vol-managed 策略的否决。

## 正确用法:前瞻式波动率 sizing

既然宏观能预测*前向*波动,就用它在波动尖峰**之前**降低仓位,而不是像普通 vol targeting 那样等已实现波动升上来才反应。这就是 `MacroVolTarget`:用宏观加权的波动预测(`macro_vol_forecast` = 趋势已实现波动 × `(1 + boost·risk_off)`)做 vol targeting。

实测(同 12% 目标波动,过 gated harness + 危机分解),它**击败反应式 vol targeting**,且在 SPX 与多资产动量书上都成立:

| | reactive vol target | **MacroVolTarget** |
|---|---|---|
| SPX Sharpe / MaxDD | 0.77 / −21.4% | **0.78 / −19.1%** |
| SPX COVID 回撤 | −10.2% | **−4.7%** |
| 动量书 Sharpe / MaxDD | 0.85 / −18.5% | **0.88 / −16%** |
| 动量书 COVID 回撤 | −7.0% | **−2.0%** |

价值集中在**快速崩盘**——前瞻信号提前降险,反应式太慢。结论:**连续 vol sizing 用宏观有效;二元清仓 gate 会误时。**

另外,`VRP>0`(方差风险溢价为正时持有,否则现金)是少数能用的单资产**降险** overlay:≈买入持有 Sharpe,但 MaxDD 大幅降低、2022 实测保护。它读的是"保险费",不是单纯波动水平。

## 怎么用(代码)

```python
from quant.data.macro.ingest import macro_panel
from quant.data.macro.store import MacroStore
from quant.macro.indicators import credit_spread_proxy, macro_risk_state, term_spread
from quant.macro.overlay import MacroVolTarget

m = macro_panel(["UST10Y", "UST3M", "VIX", "HYG", "LQD"], start, end,
                store=MacroStore(root="market_data/macro")).ffill()
risk_off = ~macro_risk_state(term_spread(m["UST10Y"], m["UST3M"]), m["VIX"],
                             credit_spread_proxy(m["HYG"], m["LQD"])).astype("boolean")

# 作为 run_experiment 的 construct 钩子,与任意 signal 复合(因果由截断闸门自动验)
res = run_experiment(my_signal, bundle, construct=MacroVolTarget(risk_off, target_vol=0.12), ...)
```

复现:`research/macro_consistency_e2e.py`(跨市场一致性)、`research/vrp_timing_e2e.py`(VRP)、`research/macro_regime_overlay_e2e.py`(regime gate)、`research/macro_vol_target_e2e.py`(前瞻 sizing)。完整研究笔记 `research/macro_indicators.md`。

## 数据源与未来

EODHD key(配在 `.env` 的 `EODHD_API_KEY`)是**付费层**,现在就能拉:收益率曲线、VIX、DXY、信用债、外汇、加密、情绪。`macro-indicator`(GDP/失业率)和 `economic-events`(经济日历)当前套餐 403——已用 `EODHDIndicatorSource` 桩铺路,开通后即用,可加一条与本轮"风险轴"正交的"增长轴"。不带 key 时整条链自动回落到免费的 Yahoo 源(VIX/收益率照常)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [0 · 研究总览](../quant/index.md) · [playbook](../playbook.md) |
| 下游 | [研究总账](../research-log.md) · [深入理解](../deep/index.md) |
| 同域 | [策略家族图谱](../reference/strategy-families.md) · [想法库](../ideas/index.md) |
| 验证 | [为什么回测会撒谎](why-backtests-lie.md) · [多重检验](multiple-testing.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [能力速查](../reference/capabilities.md) · [给 AI Agent](../for-agents.md)
- **源码:** 页内模块路径均在 `src/quant/`;先 `rg` 再写文档
- **注:** 宏观=sizing 不是择时
