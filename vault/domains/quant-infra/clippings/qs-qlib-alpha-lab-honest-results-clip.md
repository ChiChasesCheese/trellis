---
title: 'The Factor-Mining Lab: A Full Honest Accounting'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/qlib-alpha-lab.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 因子挖矿实验室与诚实结果全览

> 一句话:我们把微软 qlib 装进一个**隔离实验室**(`qlib_lab/`)、又自建了一台**组合式因子
> 生成器**,两者负责海量提出候选因子;我们自己的门禁(purged-CV / Deflated Sharpe / 成本
> 模型 / A股结构)负责处决。跨 US + A股 + FX + crypto 四市场、从 74 只到 2000+ 只、**近
> 400 次实验**下来,**没有一个横截面单因子过得了诚实门槛**——最强的价量因子净 Sharpe 也就
> 0.5 出头,为整个搜索付费后 P(real) 全在 0.2 以下。**唯一真过闸的是组合层的多资产 book
> (Sharpe 0.97),以及唯一一条"慢信息"单因子 lead:业绩预告 PEAD×动量 0.52。** 这不是挖矿
> 失败,这是门禁在说真话:公开价量前沿是有效的,alpha 不在因子层、在组合层。

这页是**全部因子挖矿战役的汇总**。想先懂"为什么多重检验必须付费"看
[多重检验](../concepts/multiple-testing.md);想懂"alpha 为什么会消失"看
[alpha 从哪来又为什么消失](where-alpha-comes-from.md)。

## 为什么要一个"实验室",而不是把 qlib 装进主环境

qlib 带来三件我们缺的东西:声明式**因子表达式引擎**(`Ref($close,20)/$close-1` 一行就是
一个因子)、Alpha158/360 预置因子库、以及 LightGBM→Transformer 的训练管线。但它同时拖
一整车重依赖(mlflow / gym / cvxpy / pymongo / jupyter)。所以 `qlib_lab/` 是一个**独立
的 uv 项目**(自己的 lockfile、自己的 venv),主环境永远不安装 pyqlib;耦合单向 ——
实验室 import `quant`(读数据、写 vault),`src/quant` 零 qlib import。删除整个能力 =
删一个目录 + 一个 CI job + 一个 yaml 块。

数据契约只有一个:staging CSV `date,open,high,low,close,volume,factor`(价格已复权、
`factor=1.0`),`qlab pipeline --recipe X` 一条命令完成 stage → dump(qlib .bin)→ mine。
挖出来的因子经 `quant.vault` 统一持久化(因子值 + 元数据 + 多重检验记账),再由
`quant.experiment.vault_gate` 回灌进和手写因子**同一条**门禁漏斗。

## 一条主线:门禁怎么工作,为什么它拦得下漂亮回测

每个候选无论来自 qlib、生成器还是网络调研,都过同一套闸:数据质量 → truncation 不变性
(前视探测)→ trade_mode(A股无做空则拦单票做空)→ 成本模型(点差 + 冲击 + A股印花税)
→ **Deflated Sharpe**。最后这道是关键:它按**整个搜索规模** `n_trials` 扣 haircut——你
试了 133 个因子,每一个的置信度都要为"试了 133 次"付费。ledger 是 append-only 的,
`cum_trials` 跨运行累加,所以一个方向试得越多、门槛越高。**一句直觉:`IR = IC × √Breadth`**
——信号强度(IC)撑不起、或宽度(标的数)不够,Sharpe 就过不了 0.95 的置信线。下面每一轮
的"REJECT"几乎全卡在这道闸,这正是它该做的事。

## 第一轮 · US 74 只:波动率家族存活,却死在宽度上

配方 `qlib_lab/configs/us_dev_sweep24.yaml`:基线篮子的 74 只美股单票(2010→2025,
eval 2018+),动量/反转/波动/RSV/量价相关/K线形态 × 多窗口共 24 个表达式,label 是 5 日
前瞻收益。

| 候选 | eval 窗口日频 rank IC | 结论 |
|---|---:|---|
| **vol20 / vol60 / vol120**(收益率滚动波动) | **+0.026 / +0.020 / +0.024** | **全家族存活** —— 不是幸运窗口 |
| mom252_21(12-1 动量) | −0.019 | 弱反转,勉强过线 |
| 其余 20 个(动量/反转/RSV/量价/K线) | −0.013 ~ +0.005 | 全部低于阈值,如实丢弃 |

波动率家族三个窗口同向、同量级 —— 这是结构性信号的样子(高波动票下周平均涨得更多)。
但送进门禁(`n_trials=31`:24 挖矿候选 + 1 家族集成 + 6 book 配置),vol120 L/S 净
Sharpe 0.82、P(real)=0.74;vol20 L/S 0.71、P(real)=0.61 —— **全 REJECT**。数据质量、
truncation、成本全过,唯一拦下它的是 Deflated Sharpe:**31 次尝试后,0.8 的 Sharpe 在
74 只票上不足以证明不是运气**。诊断清楚:信号是真的,**宽度不够**。

## 第二轮 · 扩到宽度 + 穷举机制:381 实验,0 过闸

第一轮的诊断直接给了下一步——把宽度从 74 拉到 2000+,并把机制从 24 个扩到穷举。
`qlab pipeline --recipe configs/cn_hs300zz500_ohlcv.yaml` 在 A股 hs300+zz500(~2000 只)
上挖出 `cnohlcv__vol20/60/120/klen` 等因子;自建的组合式生成器
(`quant.alpha.generator`,**43 个机制族** × 窗口 → 单窗口 + 复合)把能想到的价量机制
(动量/反转/波动/峰度/下行波/RSV/Parkinson/特异波/换手变异/资金流/尾频/RSI/CCI/…)全
覆盖;再叠 65 条 2025-2026 公开发表因子的网络调研(`research/alpha2026_candidates.json`)。
全部走 `research/alpha_factory.py` 两阶段漏斗,**n_trials = 整池规模**(DSR 为整个搜索
付费 = 不做 p-hacking 机器)。

汇总报告 `research/alpha_factory_report.md`:**381 条实验、174 个因子族、四市场,PASS 0
条,净 Sharpe ≥ 0.5 的可部署 lead 0 条。** 各族最强的那次:

| 因子族 | 市场 | 净 Sharpe | cum_trials | dsr_prob | 判定 |
|---|---|---:|---:|---:|---|
| signed_flow_obv20(量价符号流) | crypto | +0.69 | 133 | 0.21 | REJECT |
| vault_overnight(隔夜收益) | A股 | +0.56 | 217 | 0.12 | REJECT |
| frog_in_pan(渐进信息扩散) | A股 | +0.54 | 133 | 0.14 | REJECT |
| vault_upside_vol(上行波动) | US | +0.54 | 2710 | 0.03 | REJECT |
| turnover_cv(换手变异) | A股 | +0.52 | 2260 | 0.03 | REJECT |
| momentum_12_1(经典 12-1 动量) | A股 | +0.51 | 133 | 0.13 | REJECT |

`cum_trials` 那列是重点:US 的 upside_vol 裸 Sharpe 0.54 看着能打,但那个方向历史上累计
试了 **2710** 次,Deflated Sharpe 把它 haircut 到 P(real)=0.03。**裁决:穷举更多价量机制
不产生 lead,只会抬高诚实的 N,反过来证明公开价量前沿是有效的。** 各市场露出了自己最强的
机制(US 偏尾部/上行波、A股偏隔夜/换手/反转、crypto 偏量价流),但无一存活。

## 第三轮 · 跳出价量:另类数据轴 —— 第一条真 lead 出现

价量穷尽后,价值转向**经济上不同的数据轴**。解耦架构(见
[数据层分层与自动化流水线](data-layer-and-automation.md))让每条轴 = 一个 `DataProvider`
+ 一个 `AlphaDef` 库,挖矿队列零改动。在 A股 fornax jqdata 上接通了四条轴:

| 数据轴 | 最强 alpha | 净 Sharpe | dsr_prob | 判定 |
|---|---|---:|---:|---|
| **业绩预告(guidance PEAD)** | 预告惊喜 × 动量 | **0.52** | **0.82** | REJECT(**全场最接近门槛**) |
| 基本面(value/quality/growth) | value × 动量复合 | 0.45 | 0.40 | REJECT |
| 两融(margin,融资/融券) | 融资拥挤反转 | 0.25 | 0.37 | REJECT |
| 龙虎榜(billboard,游资席位) | 游资净买跟随 | −0.15 | 0.11 | REJECT |

**跨轴定论一句话:非价量轴里"慢信息/基本面惊喜"是真 alpha 源,"资金情绪/关注度"是
噪声。** 业绩预告 PEAD×动量的 **P(real)=0.82 是整个 session 最高**——质的接近 0.95,机制
是经典 PEAD 精髓(盈余惊喜 + 价格动量确认),而且 A股业绩预告是**原生盈余惊喜源**(不需
买分析师预期数据)。它是价量全灭后第一个值得单独做成可部署 sleeve 的方向。反面:两融拥挤
在流动大中盘已被套利掉;龙虎榜连微盘(zz1000,游资主战场)都是负的——上榜=高关注本身弱
预示跑输,但方向无 alpha。

## 两个"机制而非信号"的探针:止损 + 组合

**出场管理救不了因子。** 常见质疑:"只横截面选股买入、没设止损止盈,是不是票砸手里拖累
alpha?" 我们把止损/止盈/移动止损做成研究 overlay(`research/xs_exits.py`,qs-6yyk.10 前在 backtest 包),拿最强 lead
(guidance PEAD×动量)同一门禁对照——**baseline 持有到再平衡 0.52 是最好的,每一档出场都
更差**(stop −8% 腰斩到 0.21 且左尾被锁死、skew 恶化;stop −15% 只砍灾难 0.46),而
MaxDD 几乎没救(−0.53 → 最好 −0.49)。**止损是降险不是 alpha**:单票暴跌已被宽度稀释,真
正压 book 的是**因子级/风格级相关回撤**(A股风格轮动时整篮子同跌),per-name 止损治不了。

**低相关组合不是免费午餐。** 组合探针(`research/ensemble_probe.py`)在三市场查"叠一堆
低相关因子能不能过闸":

| 市场 | 宽度 | 个体 Sharpe | 平均成对相关 | 等权组合 Sharpe | dsr_prob |
|---|---:|---:|---:|---:|---:|
| US | 795 | 0.15–0.31(弱) | 0.074(极低) | 0.24 | 0.02 |
| A股 | 1840 | 0.48–0.53(尚可) | 0.911(极高) | 0.35(**反降**) | 0.04 |
| crypto | 7–8 | 高达 1.36 | 0.135(低) | 0.94(<最好单个) | 0.17 |

**组合过闸需"够强 × 低相关 × 真宽度"三者齐全——US 缺强、A股缺正交(以为 10 个不同因子实则
同押一个短期反转)、crypto 缺宽度,无一凑齐。** crypto 单个 1.36 是 170 池里 max 的选择
灌水,组合把运气平均掉后 0.94 才是诚实期望。

## 唯一真过闸的东西:组合层

累计 ledger 里少数几个过 Deflated Sharpe 的,**没有一个是横截面单因子**:

- **多资产 risk_parity book(Sharpe 0.97,P(real) 0.97)** —— 5 个低相关 sleeve(股票低波/
  动量 + 商品动量 + 多资产 TSMOM 趋势)风险平价 + vol-target。这是全仓库最强的"策略",
  印证了主线:**alpha 在组合层,不在因子层**。它被诚实标注的短板是负偏 + 肥尾(尾部管理
  问题,不是收益问题)。
- 52周高点择时过了 DSR,但**打不过纯 MA200 滤波**,预声明守门 FAIL(是个更差的慢趋势
  滤波,不是 distinct edge)。

## 这一切意味着什么

1. **门禁 REJECT 一片 = 机器在正常工作,不是坏了。** 市面上大量"Sharpe 1.5"的回测进这套
   purged-CV + 诚实 DSR + 子样本衰减 + 全额成本会一样 REJECT——我们不是更差,是更不肯骗
   自己。参数/止损/组合调到过线本身就是多重检验作弊(见
   [参数、超参与过拟合的边界](parameters-and-hyperopt.md))。
2. **单因子的天花板就是 0.3–0.5。** `IR = IC × √Breadth`,流动市场单因子 IC 被套利到
   ~0.02–0.05,数学上到不了 Sharpe 1。想要更高只能在组合层叠低相关源,或换未被套利的
   数据/niche。
3. **两条活的方向**:① 组合层——把已验证低相关的真源(PEAD / TSMOM / 低波 / value×动量)
   正确拼 book 再过衰减闸;② 慢信息——业绩预告 PEAD 硬化(真 SUE 标准化 + event-time
   持仓)。价量穷举、情绪轴、更多止损都已证无路。
4. **小资金是优势不是约束**:真正还有 >0.5 净 Sharpe 的角落恰是拥挤大基金进不去的容量
   受限 niche(A股微盘月频、冷门横截面、guidance PEAD)——见资金规模约束。

## 去哪里看

- **研究记分板**(web 控制台主界面,或 legacy Streamlit):记分板页 → "qlib 挖矿 vault" 区
  (因子表 / 策略表 / OOS 净值曲线,离线跑在 committed 数据上)。
- **报告**:`research/alpha_factory_report.md`(43 族穷举全表)、`research/alpha2026_report.md`
  (网络调研因子)、`research/BACKLOG.md`(每轮 lead / 裁决的跨轮记忆)。
- **代码**:`qlib_lab/`(实验室)、`quant.alpha.generator`(生成器)、`quant.alpha.providers`
  + `quant.experiment.alpha_queue`(解耦数据轴队列)、`quant.vault`(统一持久化)、
  `quant.experiment.vault_gate`(回灌门禁)、`research/xs_exits.py`(出场 overlay,qs-6yyk.10 自 `quant.backtest` 迁出)。
- **设计 spec**:`docs/superpowers/specs/2026-07-04-qlib-alpha-lab-design.md`(仓库内路径,
  未发布到文档站)。

## 与已有页面的关系

- 多重检验为什么必须付费:[多重检验](../concepts/multiple-testing.md)、[参数、超参与过拟合的边界](parameters-and-hyperopt.md)
- 数据轴/自动化如何解耦:[数据层分层与 alpha 自动化流水线](data-layer-and-automation.md)
- alpha 的生命周期与为什么消失:[alpha 从哪来又为什么消失](where-alpha-comes-from.md)
- 剥掉因子暴露找特异 alpha 的实证:[因子、风险,与只押特异赌注](factor-risk-and-idiosyncratic-alpha.md)
- 低风险异象的经济学:[低风险与质量](../catalog/04-lowrisk-quality.md)

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [数据层与自动化](data-layer-and-automation.md) · [统一因子目录](factor-catalog.md) |
| 下游 | [高维因子择时](high-dim-factor-timing.md) · [参数与过拟合](parameters-and-hyperopt.md) |
| 同域 | [多重检验](../concepts/multiple-testing.md) · [实验框架](../reference/experiment-framework.md) |
| ADR / concepts | [为什么回测会撒谎](../concepts/why-backtests-lie.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [低风险与质量](../catalog/04-lowrisk-quality.md) · [想法库](../ideas/index.md)
- **源码:** `qlib_lab/` · [`experiment/gates.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/experiment/gates.py)
