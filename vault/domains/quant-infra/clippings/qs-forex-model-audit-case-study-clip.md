---
title: 'Case Study: Auditing an FX Deep-Learning Model''s Synthetic-Pair Mirage'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/forex-model-audit.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 案例:审计一个外汇深度学习模型(合成盘假象)

一位合作者训练了一个外汇方向预测的深度模型(Perceiver,三分类 大跌/平盘/大涨),
自报**年化 Sharpe 2.7、Rank IC 0.43、胜率 64%、累计收益 +18 万%**。这类数字若为真,
是 Renaissance 级别的印钞机。本页记录我们**不重训、不改一行模型**,只把他训好的权重放进
我们的诚实闸门,得出的完整结论——以及它为什么是一个教科书级的**回测假象**。

它是 [为什么回测会撒谎](../concepts/why-backtests-lie.md) 与
[多重检验](../concepts/multiple-testing.md) 的一个具体、可复现的实证。

---

## 一、基础原理(先把词汇建起来)

### 外汇报价的三类,和"合成盘"

| 类别 | 例子 | 有没有真实市场 | 能不能下单 |
|---|---|---|---|
| **主流对 majors** | EURUSD、USDJPY、GBPUSD | 银行/做市商真金白银报价,点差极小 | ✅ |
| **交叉盘 cross** | EURJPY、EURGBP | 有真实市场,流动性次一档 | ✅(成本更高) |
| **合成盘 synthetic** | AEDPKR、AEDINR、AUDFJD | **没有**——数据商用美元当中介**算**出来:`AEDPKR = AEDUSD × USDPKR` | ❌ 无对手方 |

被审数据集有 **938 个"对"**,其中只有 ~14 个是真主流,**其余 ~900 个是合成盘**。它们的价格不是
成交出来的,是拼出来的,所以现实中**下不了单**。

### 合成盘为什么会"有利润"——陈旧报价 + 买卖价弹跳

合成盘由两条冷门腿拼成,而冷门货币有两个毛病:**陈旧报价**(一天更新几次,价格会"补涨/补跌"再弹回)
和**巨大买卖价差**(今天记买价、明天记卖价,来回蹦)。两者叠加,制造出**假的一涨一跌**,其指纹是
日收益的**负一阶自相关**:

<figure markdown>
![真实主流对与合成盘的日收益 lag-1 自相关](assets/forex/stale-price-autocorr.svg)
<figcaption>合成盘的日收益均值回复约为真实主流对的 2–3 倍——这不是可交易的 alpha,是买卖价弹跳。</figcaption>
</figure>

模型很聪明,它学到了"合成盘今天异常跳动 → 明天赌它弹回",于是"预测"命中率很高。**但这个利润拿不到**:
① 合成盘无法成交;② 那个"弹回"本身就是价差——真去交易,每次都要付掉制造它的巨额点差。参见
[交易成本与价格的真相](costs-and-prices.md)。

### 诚实口径:命中率 / 横截面 IC / Sharpe

- **方向命中率**:预测涨跌方向对的比例。50% = 抛硬币。这是最难粉饰的一刀。
- **横截面 IC**:每天在标的截面上,信号与次日收益的 Spearman 相关。要看**逐日 IC 的均值 + t 值**,
  而不是把 N 个对 × T 天**混池**成一个数(混池会把巨大样本量伪装成显著)。
- **Sharpe 的诚实版**:年化要按真实持有频率;要用 **Lo 序列相关校正**(重叠样本会虚高)、**PSR**
  (真 Sharpe > 0 的概率)、**Harvey-Liu 多重检验降权**、**PBO**(回测过拟合概率)。详见
  [指标](../reference/metrics.md) 与 [验证方法论](../reference/validation-methodology.md)。

---

## 二、被审对象

Perceiver(4M 参数):96 天 OHLC+因子窗口 → 三分类。标签由 `create_atr_labels` 生成(次日收益 vs
±0.35·ATR → 大涨/平盘/大跌,**因果合法**)。切分是**干净的时间序**(train 2010–2016 / val 2017–2021 /
test 2021-09→2026-04,train∩test 时间戳交集=0)。**问题不在标签,也不在切分,而在 universe 与记账。**

---

## 三、方法:他的权重 + 我们的闸门(不重训)

用他训好的 `best_model.pt` 在他的测试集上出预测,再过我们 `quant.experiment` 的闸门
(`honesty_report` = Lo-Sharpe/PSR/多重检验降权,`probability_of_backtest_overfitting`,逐日横截面 IC),
并把每一个"惊人数字"在**我们独立来源的干净 EODHD 数据**上复核。整套流程是一个可复现的两环境
harness(推理用带 torch 的环境,审计用带 quant 的环境),见下方"复现"。

---

## 四、发现

### 4.1 表面战绩(全 universe,混池,近零成本)

| Sharpe(混池) | Rank IC(混池) | 累计收益(逐样本求和) | 胜率 |
|---|---|---|---|
| **4.6** | **0.55** | **+182,355%** | **64%** |

这些正是自报口径能算出来的数字。下面逐条拆穿。

### 4.2 拆"可交易 vs 不可交易",命中率立刻塌回抛硬币

<figure markdown>
![逐对方向命中率](assets/forex/hit-by-pair.svg)
<figcaption>7 个真实可交易主流对(蓝)全部贴着 50%(合计 49.9%,z=−0.1,与抛硬币无统计差异)。
两个红色极值 USDEUR* 86% / JPYUSD* 26% 是<strong>合成反向盘</strong>,即陈旧价 artifact。</figcaption>
</figure>

所有横截面 IC 0.43、Sharpe 数字**全部锁在你下不了单的合成盘里**。真实主流对上,该模型**没有方向性 edge**。

### 4.3 "只做高置信"——一个合理论点,值得认真测

对方的辩护:总体准确率低没关系,模型有置信度,**只在它有把握时才交易**。这在业内是标准做法。
我们扫描置信阈值,并在**独立干净数据**上复核:

<figure markdown>
![置信阈值 vs 命中率](assets/forex/confidence-sweep.svg)
<figcaption>高置信(>0.5)的直连主流对信号,在模型训练数据之外的干净数据源上仍命中 <strong>73%</strong>
(琥珀线),显著高于抛硬币。这一点对方是对的——高置信子集确实不是纯噪声。</figcaption>
</figure>

### 4.4 但它坍缩成 ~2 个有效押注——不可部署

<figure markdown>
![高置信信号的逐年分布](assets/forex/signals-by-year.svg)
<figcaption>90 个高置信信号里 79 个挤在 2021+2026 两年,<strong>2023 与 2024 整整两年零信号</strong>,
且只来自 GBPUSD / NZDUSD 两个对。有效独立样本 ≈ 2 段行情。</figcaption>
</figure>

`honesty_report` 会给这条序列判"显著"(PSR=1),但那是**把聚集的 90 天当独立样本**的高估。逐个特征无
单点前视泄漏,方向也非简单追涨/逆势——更像**小样本 regime 运气**(偶尔逮到某个趋势对),而非稳定 edge。

### 4.5 容量:能装很多钱,但赚不了几次

| 维度 | 结论 |
|---|---|
| **流动性/冲击容量** | GBPUSD@1%ADV ≈ **$1.0B/笔**、NZDUSD ≈ **$0.4B/笔** —— 对 <$0.5M 的自营盘富余千倍,**非约束** |
| **信号频率** | ~20 笔/年,仅 2 个对,2 整年空仓 —— **真正的硬约束** |
| **$ 盈亏(若边际为真)** | $0.5M → ~$36k/年,但集中在 2 段行情,期望值不可信 |

**瓶颈永远是"信号够不够",不是"钱放不放得下"。**

---

## 五、判决

1. **自报战绩(Sharpe/IC/胜率)= 不可交易的合成盘陈旧价假象。**
2. **真实可交易主流对 = 抛硬币**(49.9%,z=−0.1)。
3. **高置信直连主流信号确有真东西**(独立数据 ~73%),但坍缩成 GBPUSD/NZDUSD 两对、2021+2026 两段的
   **~2 个有效押注**,统计证据薄,**不可部署**;要证实需在更多对 × 更多时段上重现,要彻底排泄漏需
   特征工程配方或用干净数据重算特征再跑。

### 沉淀:审计任何"惊人回测"的通杀刀

1. **拆可交易 vs 不可交易子集**,读命中率——最难粉饰;
2. **逐日横截面 IC 的均值/t 值**,别信混池单值;
3. **逐标的 lag-1 自相关**,强负=陈旧报价;
4. 重构成**每天一个可复利组合**,净真实成本,过 `honesty_report`(Lo/PSR/haircut/PBO);
5. **在独立干净数据源上复核**存活下来的信号。

统计闸(PSR/haircut/PBO)是**必要不充分**的:它查"这个 Sharpe 是不是运气",查不了"这个组合能不能真交易"。
必须叠加"**可交易 universe 过滤 + 逐标的诊断**",否则会被 breadth 与单点 artifact 骗过。

---

## 复现

审计 harness 归档在代码库 `research/forex_xch_audit/`(不重训、不改模型):
`infer.py`(他的权重→预测)、`audit.py`(过我们闸门→`results/audit_report.json` 可回放判决)、
`make_charts.py`(生成本页 4 张图)、`common.py`/`run_all.sh`,以及数据溯源脚本 `provenance/`。
本页每个数字与图都由 `run_all.sh` 端到端重生成。被审模型的权重与数据留在 fornax 数据面(不进 git),
其参数**逐字未改**。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [参数与过拟合](parameters-and-hyperopt.md) · [为什么回测会撒谎](../concepts/why-backtests-lie.md) |
| 下游 | [G10 FX value](../ideas/fx-value.md) · [信号工程](signal-engineering.md) |
| 同域 | [成本与价格](costs-and-prices.md) · [验证方法论](../reference/validation-methodology.md) |
| ADR / concepts | [多重检验](../concepts/multiple-testing.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [深入理解总览](index.md) · [实验框架](../reference/experiment-framework.md)
- **教训锚点:** 合成盘 / 无点差假设 = 假象;对照本仓 `cost_profile` + DSR 闸
