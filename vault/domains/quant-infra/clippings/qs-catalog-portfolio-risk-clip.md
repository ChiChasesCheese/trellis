---
title: 'Family 11: Portfolio Construction & Risk Management'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/catalog/11-portfolio-risk.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 家族 11:组合构造与风险管理(Portfolio Construction & Risk)

> **核心概念(从零讲)**:**真正的钱不在"找到圣杯因子",在"把一堆弱因子拼成一个好 book"。** 这是本项目最重要的实测结论。单因子几乎都弱到过不了 DSR,但把**不相关**的弱因子按风险拼起来,组合的风险调整收益远高于任何单个 —— 这就是"分散是唯一的免费午餐"。**这一家族不是"赚钱的信号",是"把信号变成钱"的方法论** —— 但它对最终收益的贡献,往往**大于**任何单个因子的选择。

> 读这一家族 = 学会从"因子猎人"升级成"投资组合经理"。详细实战见 [多资产组合 book](../ideas/multi-asset-book.md)(本项目从"单因子全死"翻盘成 OOS Sharpe ~1.0 的全过程)。

## 方向清单

86. **风险平价(Risk Parity)** — 让每条腿贡献相等的风险(波动大的少配),而非等钱配。**教**:风险贡献、为什么等钱 ≠ 等风险、桥水全天候。**状态**:本项目 book 的核心权重法(参数少、不易过拟合)。
87. **波动率目标(Vol Targeting)** — 把整个组合缩放到固定年化波动(如 10%),波动高时自动减仓。**教**:vol targeting、波动率聚集、为什么它提 Sharpe 削尾部。**状态**:book 用 10% vol-target。
88. **因子组合 / IC 加权** — 按各因子的信息系数(IC,预测力)动态加权组合,而非等权。**教**:IC、最优组合权重、`quant.model.combine`。**坑**:权重估计的样本外稳定性(易过拟合权重)。
89. **均值-方差 / Black-Litterman** — 经典 Markowitz 优化及其稳健化(BL 把观点和市场均衡混合)。**教**:有效前沿、为什么裸 MVO 不稳健(对输入极敏感)、稳健化。
90. **Kelly / 最优杠杆** — 用 Kelly 公式定最优下注比例,最大化长期增长。**教**:Kelly 准则、为什么实战用 1/2 Kelly(估计误差)。
91. **滚动样本外权重(no-lookahead)** — 权重只用截至上期的数据估计,避免"用未来定权重"的隐性前视。**教**:为什么全样本权重会高估、诚实的组合回测。**状态**:本项目 book **正是因为换成滚动 OOS 权重**,Sharpe 从 1.17 诚实地落到 0.97。
92. **回撤控制 / 风险预算** — 设回撤上限,触发后降险;给不同腿分配风险预算。**教**:回撤管理、风险预算、crisis management。
93. **尾部塑形 / 偏度管理** — 主动改善组合的负偏(超配正偏的趋势腿、加尾部对冲),而非只看 Sharpe。**教**:偏度/肥尾、为什么 Sharpe 不够、**由经济动机而非凑 DSR 驱动**。**状态**:本项目 book 的当前前沿(负偏 -0.8 是待解问题,见 [book 文档](../ideas/multi-asset-book.md))。

## 共同的坑(也是纪律)

- **拼噪音还是噪音**:分散只在各腿"真·弱但有正期望 + 真低相关"时有效。先让每条腿过基本检验,**相关矩阵是 make-or-break 的检验**。
- **过拟合权重**:别把组合权重 sweep 到样本内最优 —— 那是把多重检验从因子层搬到组合层。**风险平价/等权这种参数少的方法,正因为"笨"而稳健。**
- **别为凑 DSR 调参**:持续微调权重/overlay 直到"恰好过 0.95" = [多重检验](../concepts/multiple-testing.md)自欺。改进必须来自真实的分散/尾部经济学,不是参数搜索。
- **样本外才算数**:组合的回测必须用滚动 OOS 权重,否则"分散收益"里混着用未来定权重的前视。

延伸:[多资产组合 book(实战全过程)](../ideas/multi-asset-book.md) · [策略与组合思路总纲](../playbook.md) · [为什么测试集不够](../concepts/multiple-testing.md)。

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
