---
title: '100 Quant Strategy Directions: A Study Catalogue'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/index.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 100 个量化方向(学习目录)

两个用途:**(1)** 按家族组织的 100 个量化方向清单,给研究找方向;**(2)** 一条学懂量化方法论的路径——每个家族先讲基础知识再列方向。

## 先懂一件事:任何策略能赚钱,必有人在另一边持续地亏

这是全部量化的第一性原理。市场是零和(扣成本后负和)的:你多赚的,是别人少赚或多亏的。所以**每个策略都必须能回答"谁在另一边、为什么甘愿亏"**。答不出来的,多半是回测假象。盈利来源只有三种:

1. **行为偏差(behavioral)** —— 人性犯错:追涨杀跌、过度反应、处置效应、彩票偏好。这些错误系统性、可重复,所以可被收割。例:动量、短期反转。
2. **风险溢价(risk premium)** —— 你承担了别人不愿承担的风险,市场付你报酬。例:价值(扛得住长期难受)、carry(扛尾部风险)、卖波动率(当保险公司)。**这种"alpha"其实是 beta**:平时赚、危机里该亏的时候真亏 —— 这不是缺陷,是它的定义。
3. **结构性约束(structural)** —— 有人被规则/制度逼着做次优决策:被迫调仓的指数基金、不能用杠杆只能买高波动彩票股的散户、被风控强平的机构、月末窗饰的基金。约束方在另一边亏。例:低波(BAB)、指数再平衡套利。

> 读每一个方向时,先问:**这是 1、2 还是 3?** 想不出来 = 危险信号。详见 [alpha 从哪来又为什么消失](../deep/where-alpha-comes-from.md)。

## 再懂一件事:验证比想法重要十倍

想法很便宜,**能扛住严格检验的想法很贵**。本仓库的研究纪律(也是这门"方法论课"的核心):

1. **严格因果** —— 信号只能用过去的数据。任何"未来函数"都让回测撒谎。
2. **样本外 + Purged/Embargo 交叉验证** —— 在没见过的数据上测,且切断训练/测试之间的信息泄漏。
3. **躲开[四大回测陷阱](../concepts/why-backtests-lie.md)** —— 前视、幸存者偏差、过拟合、成本幻觉。
4. **[Deflated Sharpe / 多重检验](../concepts/multiple-testing.md)** —— 你试得越多,"碰巧好看"的越多;DSR 按试验次数打折,逼你诚实。**这是分辨真 edge 和运气的关键闸门。**
5. **成本墙** —— 很多 gross 信号是真的,但净不抵交易成本就是死的。见 [交易成本与价格的真相](../deep/costs-and-prices.md)。
6. **组合 > 单点** —— 单因子几乎都弱到过不了 DSR;真正的钱在**分散**里(把不相关的弱因子拼起来)。这是本项目最重要的实测结论,见 [多资产组合 book](../ideas/multi-asset-book.md)。

把一个想法跑通这套闸门,用 `run_experiment`(见 [跑一个实验](../guides/run-an-experiment.md))。**一个诚实的"被拒"+ 原因,比一个含糊的"有潜力"值钱。**

## 怎么读这个目录(建议路径)

如果你想**系统学方法论**,按家族顺序读(每个家族开头都从零讲它的核心概念):

1. [趋势与动量](01-momentum-trend.md) —— 行为偏差的代表;也是本项目 book 的王牌腿。
2. [价值与均值回归](02-value-reversion.md) —— 风险溢价 + 反转的代表。
3. [Carry(套息)](03-carry.md) —— "为承担风险收租"的纯粹形态。
4. [低风险与质量](04-lowrisk-quality.md) —— 结构性约束(杠杆受限)的经典。
5. [规模与流动性](05-size-liquidity.md) —— 为不流动性收租。
6. [波动率与期权](06-volatility-options.md) —— 当保险公司:卖波动率收保费。
7. [事件驱动与基本面](07-event-fundamental.md) —— 信息扩散的慢与快。
8. [微观结构与日内](08-microstructure-intraday.md) —— 订单流与做市,机构的地盘。
9. [宏观与跨资产](09-macro-crossasset.md) —— 自上而下,regime 与跨市场。
10. [另类数据与机器学习](10-altdata-ml.md) —— 新数据 = 新 edge,也是新坑。
11. [组合构造与风险管理](11-portfolio-risk.md) —— 不是找因子,是把因子变成 book(钱在这)。
12. [加密与 DeFi](12-crypto-defi.md) —— 最年轻、最不拥挤、结构性套利最多的市场。

如果你完全不懂金融,先读 [交易 101](../concepts/trading-101.md) 再回来。

## "idea creator":让这个目录持续生长

这 100 个不是终点。本仓库有一个**实时方向探针** `quant scout`,从 **arXiv q-fin** 和 **GitHub 活跃仓库**拉最新研究:

```bash
uv run quant scout --json                      # arXiv + GitHub,JSON 输出
uv run quant scout --source arxiv --arxiv-max 20
uv run quant scout --source github --github-query "betting against beta"
```

它返回**真·最新**的论文/仓库活动(例如最近一次拉到了 rough volatility 检测、crypto 时序预测的有效性质疑等前沿)。**纪律:用到一个新方向,就回到对应家族页加一行,并在 [策略思路库](../ideas/index.md) 写一篇讲解页。** 目录越长越厚,成为一本活的量化思路百科。

## 重要的现实主义(别被 100 个冲昏头)

这 100 个里,**绝大多数单独都过不了我们的闸门** —— 这不是悲观,是经验:本项目系统性测过的单因子几乎全 REJECT(见各家族"我们的状态")。**正确的用法不是逐个去挖圣杯**,而是:

- 用它们当**学习地图**(理解量化的全貌与方法论);
- 从中挑**几个不相关、各自有微弱真信号**的,按 [组合方法](11-portfolio-risk.md) 拼成 book —— 这才是实测能赚钱的路(OOS Sharpe ~1.0 的 [多资产 book](../ideas/multi-asset-book.md) 就是这么来的);
- 把 [危机凸性](../concepts/crisis-convexity-vs-short-premium.md)型(趋势/value/卖尾部保险)当 lead,其余当卫星。

延伸:[策略与组合思路总纲](../playbook.md) · [策略家族图谱](../reference/strategy-families.md) · [术语表](../reference/glossary.md)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [playbook](../playbook.md) · [策略家族图谱](../reference/strategy-families.md) |
| 下游 | [想法库](../ideas/index.md) · [深入理解](../deep/index.md) |
| 同域 | [alpha 从哪来](../deep/where-alpha-comes-from.md) · [策略风格光谱](../deep/strategy-styles.md) |
| ADR / concepts | [交易 101](../concepts/trading-101.md) · [危机凸性](../concepts/crisis-convexity-vs-short-premium.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [scout 管线](../concepts/video-scout-pipeline.md) · [给 AI Agent](../for-agents.md)
- **源码:** [`scout/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/scout) · CLI `quant scout`
