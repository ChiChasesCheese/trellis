---
title: 'Risk Parity and All Weather: Allocating by Risk, Not by Dollars'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/risk-parity-and-all-weather.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 风险平价与全天候(桥水):按风险配钱,不按美元配钱

> 一句话:桥水 All Weather 不是"预测市场的策略",而是**一种配置方法**——让每类资产对组合的*风险*贡献相等,从而在任何经济环境下都有资产在扛。它和 [Citadel 式多策略平台](citadel-multi-pod-platform.md)是两种完全不同的范式:一个是 **beta 工程**,一个是 **alpha 工厂**。

## 从 60/40 的问题说起

教科书组合是 60% 股票 / 40% 债券,看起来"分散"。但股票的波动是债券的 4–5 倍,所以按*风险*算,**这个组合约 90% 的风险都来自股票**——债券那 40% 的美元几乎没在分散任何东西。股市一崩,60/40 跟着崩。

**风险平价(risk parity)**的解法:不按美元配,按**风险贡献**配。让债券贡献和股票一样多的风险,就得给债券**加杠杆**(低波动资产借钱放大),给股票降权。这就是"把钱配平"和"把风险配平"的区别。

## All Weather:四个经济象限

桥水 1996 年推出的 All Weather 把经济环境分成四象限——**增长超/低预期 × 通胀超/低预期**——每个象限配 25% 的风险预算:

| 象限 | 谁受益 |
|---|---|
| 增长↑ | 股票、公司债、商品 |
| 增长↓ | 长期国债 |
| 通胀↑ | 通胀挂钩债(TIPS)、商品、黄金 |
| 通胀↓ | 股票、名义国债 |

关键设计哲学:**它不预测**下一个环境是什么(桥水自己说这是"不需要预测未来的最好组合")。它只保证:无论走进哪个象限,组合里都有 25% 的风险预算在正确的一边。这和本仓库宏观层的实测结论同源——[宏观状态是跨市场波动率定律,用于 sizing 而非牛熊择时](macro-regime-and-sizing.md)。预测宏观方向做不到,但按风险预算配置不需要预测。

## 和 Citadel 式平台的区别:beta 工程 vs alpha 工厂

| | 桥水 All Weather | Citadel 式多策略 |
|---|---|---|
| 赚什么钱 | **beta**(资产类别的长期风险溢价) | **alpha**(特异性边际,[对冲掉因子暴露](../architecture/citadel-pod-book.md)) |
| 方法核心 | 配置方法本身就是策略 | 很多互不相关的 pod + 中央风控 |
| 容量 | 几乎无限(持有的是大类资产) | 每个 alpha 有[容量上界](../reference/experiment-framework.md) |
| 需要预测吗 | 不需要 | 每个 pod 都在下有依据的注 |

桥水真正和 Citadel 类比的是它的 **Pure Alpha** 基金——桥水自己就有"alpha-beta 分离"框架:beta 用 All Weather 便宜地拿,alpha 单独做、单独收费。所以"我们该学桥水还是学 Citadel"是个假问题:**风控方法论学 Citadel(已落地:pod 止损/中性化/容量),资本的底仓配置可以学桥水**。

## 诚实的弱点:2022 股债双杀

All Weather 依赖"债券低波 + 加杠杆"和"股债在危机中此消彼长"。**2022 年通胀驱动的利率暴力上行让股债同跌**,加了杠杆的长久期债反而放大亏损——这是风险平价的已知痛点(通胀象限的资产不足时尤其如此)。所以本仓库对任何风险平价 sleeve 的要求和[危机凸性](crisis-convexity-vs-short-premium.md)的纪律一致:**2008 / 2020 / 2022 三段 regime 必须实测**(教训 #3:抗跌要实测,不是嘴上说),不许只挑对自己有利的危机展示。

## 本仓库怎么借鉴(两条落地路径)

1. **ERC pod 权重**:`portfolio/allocation.py` 现在支持 **ERC(等风险贡献)**权重,`portfolio/erc_weights.py` 提供独立的 ERC 权重计算器,`portfolio/allocation.py` 的 `allocate(scheme="erc")` 把 pod 间按风险贡献配平——把风险平价的思想用在 alpha pod 之间,改动小、book 层直接受益。ERC/Sharpe 权重之上还有一层可选的 F4 容量上界缩放(`apply_capacity_bounds` / `allocate(..., capacity_usd=, firm_nav=)`,`qs-1yp.9`)——**上界缩放,不改变风险平价配权本身,也不是杀闸**,见 [Pod book](../architecture/citadel-pod-book.md)。
2. **跨资产风险平价 sleeve**:股/长债/黄金/商品 ETF 的风险平价底仓,定位是小资金 propshop **闲置资本的 beta 底仓**——容量无限、执行简单、与 alpha pods 低相关。作为 beta 它不按 alpha 的 OOS Sharpe ≥ 0.5 标准验收,但必须给出与现有 book 的相关性 + 危机段实测。

两条中 ERC pod 权重已落地;跨资产风险平价 sleeve 的开放工作见 `bd ready`(搜 risk-parity / allweather),勿写 checkbox backlog。`portfolio/construction.py` 已有单 sleeve 内的风险平价权重原语(该文件里 Edge-style
`expectancy_weight` 的逐笔交易清单依赖已下沉到 `portfolio/core.py::trades_from_weights`,不再借道
`backtest.trades` —— qs-2ql,与本页风险平价原语无关但同文件)。

## 延伸阅读

- [桥水官方:The All Weather Story](https://www.bridgewater.com/research-and-insights/the-all-weather-story)
- [多策略平台(pod 机制)](citadel-multi-pod-platform.md) —— 另一种范式的全景
- [宏观状态与仓位管理](macro-regime-and-sizing.md) —— 为什么"不预测、只配平"和我们的宏观实测结论同源
- [危机凸性 vs 做空溢价](crisis-convexity-vs-short-premium.md) —— 危机表现必须实测的配置纪律

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
- **注:** 桥水式风险平价
