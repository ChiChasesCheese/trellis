---
title: 'Crisis Convexity vs Short Premium: Who Leads, Who Rides Along'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/crisis-convexity-vs-short-premium.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 危机凸性 vs 做空溢价:谁当 lead、谁当卫星

> 组合层配置纪律:核心仓(lead)优先给**危机里赚钱**(正偏/凸性)的策略;「平时收租、崩盘吐回」的做空溢价型只能当卫星、严格限权——且永远别信平静期那个漂亮的低相关。
>
> 前置:各风格机制见 [策略风格的光谱](../deep/strategy-styles.md)。本页只用**危机响应**排座次。

## 1. 两种收益形状:正偏 vs 负偏

| | 做空溢价型(short premium) | 危机凸性型(crisis convexity) |
|---|---|---|
| 收益形状 | **负偏**:大量小赚 + 偶尔巨亏 | **正偏**:平时小亏小赚 + 危机凸性爆发 |
| 大白话 | 在压路机前面捡钢镚 | 平时交保费、灾难日领赔付 |
| 等价期权 | **做空期权 / 卖保险** | **做多期权 / 买保险** |
| 代表 | carry、credit、short vol | TSMOM、经典 value(含 FX value **性质**) |
| 危机表现 | 低相关瞬间→1,一起垮 | 越跌越赚 / 抄到更深便宜 |

**平均 Sharpe 看不出偏度。** 负偏策略平静期可以很漂亮——那是尾部还没兑现。铁律:看到 Sharpe 极高、回撤极小、月月正 → 先假设伪装 carry / 卖波动,问「我在卖什么保险?」

## 2. 「做空溢价」是什么

收益本质是**向市场卖某种保险**:平时收租,崩盘一次性吐回多年利润。结构上 ≡ 做空期权。典型:FX/商品 carry、信用 spread、卖波动。属于 [alpha 从哪来](../deep/where-alpha-comes-from.md) 里的风险溢价支——能持续几十年,代价是最坏时刻爆给你看。

## 3. 为什么「平时不相关是假象」

相关性是 **regime-dependent**。危机一来,做空溢价型的隐含空头(流动性 / 避险情绪)同时引爆 → 相关→1。平静期估出的低相关是 backtest 幻觉。这也是研究总账纪律「低相关分散器不是免费过关券」的深层原因:机械低相关 ≠ alpha;危机相关跳 1 的「低相关」是陷阱。

## 4. 对照本仓库真实数据(已更新)

| 策略 | 类型(性质) | COVID-2020 | 2022 | **现行裁决** |
|---|---|---|---|---|
| [G10 FX value](../ideas/fx-value.md) | 危机凸性(性质) | 曾 +2.34 | 短窗抗住 | **证伪 / REJECT** — Fed H.10 长样本毛夏普 ~0.07–0.12;旧 Yahoo 短窗 0.61 是 artifact。性质故事仍成立,**强度不够当 lead** |
| FX carry | 做空溢价 | -0.01 | **-0.22** | **REJECT**(危机崩,经典压路机) |

- **FX carry**:平静期近零相关像 diversifier,2022 拖后腿——不配当 lead。
- **FX value**:凸性来自结构性多头波动暴露(便宜货币在危机里缺口更大),但干净长样本上 **edge 不够**。勿再写成「项目唯一 lead」。

TSMOM 同属凸性性质、危机窗曾亮眼,全样本 standalone 弱——见 [playbook](../playbook.md)。**现行最强组合叙事**是 [多资产 book](../ideas/multi-asset-book.md)(OOS ~1.0,DSR 未认证),不是单因子 FX value。

## 5. 为什么 TSMOM 与 value「性质互补」

- **TSMOM = 顺势(右侧)**:崩盘是持续趋势 → 等价做多危机期权。
- **value = 逆势(左侧)**:买被错杀的便宜 → 赌多年回归。

历史上常负相关(Asness 2013)。合起来是路径不同阶段各站一侧——**前提是两条腿都够强**。一强一弱等权会被拖向均值(实测 value+carry 稀释)。

## 6. 配置纪律三条

1. **lead 优先危机凸性 / 正偏**,且必须过闸 + 强度够(standalone Sharpe 门槛 + 诚实 n_trials)。
2. **做空溢价型只能卫星**,严格限权;别信平静期低相关。
3. **不相关的 Sharpe 才能叠加**——做空溢价在危机不满足「真不相关」。

## 7. 慢策略 Sharpe 2–3 = 哪里偷看了未来

慢策略(低频、长持有)一年独立赌注少,统计上难凑出 Sharpe 2–3。冒出来 → 先 audit 前瞻/幸存者/复权([为什么回测会撒谎](why-backtests-lie.md)),别先庆祝。日内层再严三倍:[慢定方向 + 快做日内](../deep/slow-fast-layering.md)。

## 一句话

按「危机里赚钱还是崩」排座次:凸性型当 lead **候选**(还要强度过闸),做空溢价型限权卫星。低相关是状态依赖幻觉。FX value 是**性质教材 + 强度证伪**的活例,不是现行 lead。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [0 · 研究总览](../quant/index.md) · [playbook](../playbook.md) |
| 下游 | [宏观状态与 sizing](macro-regime-and-sizing.md) · [多策略 pod](citadel-multi-pod-platform.md) |
| 同域 | [策略风格光谱](../deep/strategy-styles.md) · [G10 FX value](../ideas/fx-value.md) |
| ideas | [多资产 book](../ideas/multi-asset-book.md) · [研究总账](../research-log.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [alpha 从哪来](../deep/where-alpha-comes-from.md) · [风险平价与全天候](risk-parity-and-all-weather.md)
- **源码:** [`portfolio/allocation.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/portfolio/allocation.py) · [`backtest/regime.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/backtest/regime.py)
- **外部:** Asness et al. Value and Momentum Everywhere; CTA 危机 alpha 文献
