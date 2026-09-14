---
title: 'Slow Sets the Direction, Fast Trades Intraday: Layering Strategies Across
  Timescales'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/slow-fast-layering.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 慢定方向 + 快做日内:多时间尺度策略怎么分层

**慢策略(月度~年度)定方向 / 择资产,快策略(分钟~小时)管执行与短周期 alpha**——真实多策略机构(尤其 CTA、multi-strat)在做的事。但"慢+快"有**三种完全不同**的含义,对应不同研究脉络;分清三种,给出机构真实架构,落到小资金/个人尺度怎么挂。
>
> 前置:这页假设你已经知道[慢策略 Sharpe 2-3 = 偷看未来](../concepts/crisis-convexity-vs-short-premium.md)这条怀疑论(那页第 7 节)。日内层把它再翻三倍严。

## 三种"慢+快",别混为一谈

### 选项 1:慢定方向,快只做执行(execution-only)

快策略**没有自己的方向观点**,只负责把慢策略已决定的那笔交易**更便宜、更隐蔽地执行掉**。

- 慢策略说:"做多 100 手 ES。" 快策略的工作:**怎么买**——拆单、择时下单、避免冲击成本、用 VWAP/TWAP/POV 算法在日内找好成交点。
- 它不改变"要不要买、买多少",只优化 *how to fill*。
- 衡量标准:**implementation shortfall(执行落差)**——成交均价 vs 决策时点价格差多少,越小越好。这是**省钱,不是赚钱**。
- → 机构里的 **execution / algo trading 层**,纯成本优化。文献是 **Almgren-Chriss** 那一支 optimal execution。

### 选项 2:快慢两条独立 alpha,无层级

两条**完全独立、互不管辖**的 alpha:慢的长持有、快的日内,各按各的信号下注,最后在组合层 netting / 加权。快策略不受慢策略方向约束——可以慢的在多 ES、快的在空 ES,两者只在风险预算上汇总。→ 经典的 **portfolio of alphas / factor timing**。

### 选项 3:快在慢圈定的方向内做独立日内 alpha(分层 / hierarchical)

快策略**有自己的方向判断,但被约束在慢策略圈定的范围内**。它在赚自己的钱,不只是省执行成本。

- 慢策略说:"现在 risk-on,整体偏多股指,且看好 ES 而非 NQ。"(配置 / 择资产层)
- 快策略:在"做多 ES"这个大方向内,用自己的**日内信号**(order flow、microstructure、日内反转 / 突破)决定何时进出、甚至日内做波段,赚额外日内 alpha。
- **关键约束 = 方向围栏(direction fence)**:快策略只能在慢策略给的**方向 + 风险预算**内活动(不准净空 ES、日内敞口不超配置上限)。
- 衡量标准:**日内 P&L / 日内 Sharpe**。

| | 选项 1 | 选项 3 |
|---|---|---|
| 快有方向观点吗 | ❌ 只执行别人的决定 | ✅ 有,但被慢的方向围栏约束 |
| 快在干嘛 | **省钱**(降执行成本) | **赚钱**(日内独立 alpha) |
| 衡量 | implementation shortfall | 日内 P&L / Sharpe |
| 类比 | 司机(你定目的地,他选最优路线) | 副驾交易员(你定大方向,他在框内抓机会) |

## 顶级机构的真相:不是二选一,是三层全要

"3 比较对"和"1 偏大资金优化"这两句判断**都对,但不冲突**——它们活在不同楼层。顶配机构是**三层都做、严格分开**,各有专门团队:

![three-layer-slow-fast](../diagrams/three-layer-slow-fast.drawio)

**3 坐在 1 上面**,不是选 1 或选 3。

## 文献怎么说(这想法有正经理论支撑)

- **多信号最优交易(arXiv 2502.04284,multi-period optimal trading)**:明确把"管理者同时拥有一个慢信号(预测日级变动)和一个快信号(预测日内变动)"列为研究方向,且最优解形态正是这个分工——**按快信号的速度做决策、同时结合慢信号,从两者都获益**。
- **two-scale alpha(arXiv 2112.02944)**:给大资金一个关键洞见——**快 alpha 的幅度对大组合而言,通常不值得为吃它专门做一次往返交易;但它仍有用,可以给慢 alpha 的执行择时。** 这直接回答了"1 还是 3":**资金体量决定快信号是当 alpha(选 3)还是当 execution timing(选 1)**。
  - **小资金**:快信号预测力足够覆盖来回成本 → 让它独立赚日内 alpha(选 3)。
  - **大资金**:同样信号因冲击成本随规模放大、专门去吃不划算 → 快信号**降级为建仓择时**(选 1)。
  - 这就是为什么"1 偏大资金"是**有数学依据的**:规模越大,快信号越倾向退化成执行层。
- **多时间尺度分层(crypto,arXiv 2508.02356)**:把"方向围栏"讲得最清楚——**较大时间框架的信息约束并影响较短时间框架的走势;微结构数据为方向变化提供早期信号、再向上传导。** 日线趋势确立主方向(bias),影响小时级形态。这就是选项 3 的内核:慢定 bias,快在 bias 内动作,能显著降假信号。
- **执行层也在往分层走(survey,arXiv 2411.12747)**:最佳实践是两级——高层 agent 负责成交量调度、低层 agent 负责精确下单;甚至有把选股与执行合到一个分层框架联合求解的(HRT)。

## 对我们(小资金 / 个人尺度)的实际意义

资金小**反而是好消息**——对我们,**选项 3 是对的、且可行**:

1. **快信号值得当独立 alpha**:小资金时快信号的预测力能覆盖交易成本(大机构被迫把它降级成执行,我们没这约束)。
2. **务必保留方向围栏**:让慢策略([TSMOM](../concepts/crisis-convexity-vs-short-premium.md) / [FX value](../ideas/fx-value.md),月度~季度)输出**方向 + 风险预算**,快策略只在预算内做日内、**不准净反向**。这是选项 3 区别于选项 2 的关键,也是 hierarchical 的核心——降假信号、防快策略在慢策略不利方向上乱赌。
3. **日内的防偷看标准要比慢策略严三倍**:日内快 alpha 对执行成本和延迟**极度敏感**。慢策略的 lookahead 吃掉几个点;日内的 lookahead(fill 假设过于乐观、用了未来 tick、没算真实点差和滑点)能让一个**根本不存在的策略看起来 Sharpe 5**。本仓库已反复印证"微结构 alpha 死在分辨率 + 成本墙"(见 `research/BACKLOG.md` 的 Directional Change 三市场全 REJECT、[交易成本与价格的真相](costs-and-prices.md))。

## 落到本仓库:怎么把日内层挂到现有 sleeve 上

这是一个**未来 feature**(见 `research/BACKLOG.md` 的"分层慢+快 overlay"条),骨架:

1. **慢层输出**:现有 TSMOM / FX value sleeve 每日产出 `{方向 sign, 风险预算 budget}`(per-symbol)。
2. **快层信号**:在 `budget` 内、`sign` 方向上做日内信号(日内反转 / order-flow 代理),**硬约束** `|日内敞口| ≤ budget` 且 `sign(日内净敞口) == sign(慢层)`。
3. **闸门**:日内回测必须扣**真实点差 + 滑点 + 2× 成本**仍为正,且过 [DSR](../reference/metrics.md);fill 假设写死成保守口径(不许用未来 tick)。
4. **数据瓶颈**:intraday 历史深度是真瓶颈(免费源 Yahoo 1min 仅近 7 天、5min 近 60 天)→ 只能前向累积,落 R2(见 BACKLOG 的 intraday 持久化条)。**所以这是 data-gated 的中长期题,不是今天就能跑。**

## 一句话总结

**"慢定方向、快做日内"有三种含义:① 快只执行(省钱,Almgren-Chriss,偏大资金)② 快慢各跑各的(portfolio of alphas)③ 快在慢的方向围栏内赚日内 alpha(hierarchical)。顶级机构三层全做、严格分层(3 坐在 1 上)。资金体量决定快信号当 alpha 还是当执行择时——小资金选 3、保留方向围栏、把日内回测的防偷看标准拉到比慢策略严三倍,是最合理的路线。**

---

**延伸**:[危机凸性 vs 做空溢价](../concepts/crisis-convexity-vs-short-premium.md)(慢层 lead 怎么选)· [交易成本与价格的真相](costs-and-prices.md)(为什么短周期信号死在成本墙)· [参数、超参与过拟合](parameters-and-hyperopt.md) · `research/BACKLOG.md`(分层 overlay 的 feature 条目)。

> _知识来源:与 Chi 关于"慢策略定方向 + 快策略日内交易是否合适、顶级机构最佳实践"的讨论(2026-06,doc-knowledge-maintenance 轮归档)。文献:arXiv 2502.04284 / 2112.02944 / 2508.02356 / 2411.12747;Almgren-Chriss optimal execution。_

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [成本与价格](costs-and-prices.md) · [策略风格光谱](strategy-styles.md) |
| 下游 | [宏观 regime 与 sizing](../concepts/macro-regime-and-sizing.md) · [6 · Pod book](../architecture/citadel-pod-book.md) |
| 同域 | [日内策略报告](../reference/intraday-strategy-report.md) · [因子风险](factor-risk-and-idiosyncratic-alpha.md) |
| ADR / concepts | [危机凸性](../concepts/crisis-convexity-vs-short-premium.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [执行引擎](../architecture/vs-mainstream.md) · [playbook](../playbook.md)
- **源码:** [`execution/engine.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/execution/engine.py) · [`macro/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/macro)
