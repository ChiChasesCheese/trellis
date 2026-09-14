---
title: 'High-Dimensional Factor Timing: Shrinkage Discipline and the Dimension × Sample-Length
  Law'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/high-dim-factor-timing.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 高维因子择时:收缩纪律、维度×样本律,与全天候壳

**能不能提前猜到"这个月哪个因子会火",把权重压过去?** Lehnherr-Mehta-Nagel(2025, FAJ 81(2))说可以——前提是维度够高、且用三层收缩防止被历史噪声骗。本仓库完整复现了这篇论文,又把它推到论文没去过的地方:跨四个市场、做维度受控实验、包成全天候组合层。结论比论文更完整也更冷静:**择时溢价 = 维度 × 样本长度的联合产物,缺一个都是零甚至负。**

> 前置:[从想法到信号](signal-engineering.md)(横截面 vs 时序)、[为什么回测会撒谎](../concepts/why-backtests-lie.md)、[多重检验](../concepts/multiple-testing.md)。全部数字来自真实数据(Ken French / EODHD / Yahoo / OKX / fornax jqdata),冻结在 `research/factor_timing_nagel/` 的 JSON 里(§三前半与§五的 42 回测/RP 全天候书数字冻结于保留分支 `claude/allweather-dimension-study-qccq0p`,PR #253 已关闭归档;main 上的同市场阶梯与 CN 判决见 `dimension_ladder_results.json`),任何人可复算。

## 一、论文的三步(和它们在仓库里的位置)

1. **把"猜时机"变成"分钱"**:给每个因子 F 配预测变量 X(自身动量/波动等),构造 managed portfolio `G_t = X_{t-1} · F_t`。原来的动态择时难题变成对 K×J 个 G 的**一次性静态配权**——经典均值-方差可解。常数预测变量让原始因子留在池内。(`quant.factortiming.managed`)
2. **三层收缩防过拟合**:Ledoit-Wolf 把协方差往缩放单位阵拉;Kozak-Nagel-Santosh 惩罚项把权重往"静态书"拉(旋钮 λ:0=全信历史,∞=退回静态);最后把隐含因子权重重标到 gross=1——只轮动、不加杠杆。(`quant.factortiming.shrinkage`)
3. **扩展窗口诚实考试**:训练→验证(λ 每年在累积验证块上按夏普重选)→样本外,滚动到数据尽头。(`quant.factortiming.timing`)

## 二、复现结果:高维下成立,且收缩是命根子

US 真实数据(FF5+MOM + 15 个 Ken French 十分位价差 = 20 因子),39 年样本外:

| 书 | OOS 年化夏普 | 说明 |
|---|--:|---|
| **timed(三层收缩择时)** | **1.23**(净 10bps 成本 1.16) | KJ=540;推到 KJ=1600 时 0.94 |
| naive(λ=0,不收缩) | 1.03 → KJ=1600 时**崩到 0.40** | 维度越高崩得越狠 |
| static(静态均值-方差) | 0.75 | 论文的对照 |

论文报 0.81 vs 0.47,我们 1.23 vs 0.75——方向、机制、"λ=0 高维崩塌"全部复现(预测变量集不同所以水平不同,论文用了我们离线拿不到的 CRSP 估值价差)。

## 三、跨市场检验:小市场做不出来,而且原因值得知道

同一引擎、同一配方搬到 FX(8 货币对)/CN(6 指数价差)/crypto(8 币,周频):**择时全部无增量**(FX timed 0.04 vs static 0.66)。是不是"维度不够"?我们做了**受控实验**:固定美国市场、固定配方,只变因子数 K∈{4..20}(预注册子集、两窗口共用):

| 窗口 | K=4 (KJ=44) | K=20 (KJ=540) | 读法 |
|---|--:|--:|---|
| **40 年**(1963+) | 溢价 +0.12 | **+0.48** | 维度剂量-响应成立(中位数趋升;前缀路径 K≤16 平坦,跳变在 K=20 单点) |
| **13 年**(2004+,FX/CN 长度) | −0.27 | **−0.33** | 溢价整体转负,**维度越高越糟** |

**这就是本仓库对这篇论文最重要的补充:维度是真原料,但样本长度同样是硬约束**——λ 的选择需要几十年累积验证块才能识别;样本短时维度只放大过拟合。实践规则:**新市场上择时层,先垫 15–20 年可回填历史,否则持静态书。**

"因子库粗不粗"这第三个待验假设,fornax 个股横截面实验(维度阶梯,`research/factor_timing_nagel/dimension_ladder_report_zh.md`)已经给出判决:

- **US 同市场阶梯(独立印证)**:同一 43 年窗口,K=5→20(KJ 60→540),择时溢价 +0.11 → **+0.44**(两臂 λ 均 stable)——在有可择时结构的市场里,维度确是放大器,与上表的剂量-响应互为独立复核;
- **CN 个股臂(否定证据)**:同一 A 股市场、同一窗口,把 6 个指数价差升级成 15 个真正的个股横截面风格因子(PIT 成分、停牌/一字板过滤、jqdata 估值),溢价 −0.29 ± 0.48,相邻协议(min_train 96→84)翻成 +0.10,λ 诊断在 unstable/stable 间跳——**符号对协议都不稳 = 信号不可识别**,低于预注册闸门,判决 **REJECT**。

完整答案:小市场失败 = 维度不够(必要条件)**且**市场本身缺可识别的时序结构(充分条件)——只修维度不修信号没用;REJECT 本身是产出,λ 仪表盘 + 跨协议敏感性让你在部署前就知道,不用等亏钱。

## 四、λ 翻转率:一个免费的单向哨兵

λ 每年重选一次;"重选换值的频率"是个实时可读的风控信号——已落地 main 为 `quant.factortiming.allweather` 的 λ 仪表盘(`diagnose_lambda`,三态红绿灯:`stable` 可考虑部署 / `pinned_max` 引擎自认无信号、持静态书 / `unstable` 验证样本识别不出、不部署):

- US 40 年高维:翻转率 0.03,λ 稳定在重收缩档 → 信号真实;
- FX:λ 在 0 和 1000 之间横跳 → 验证窗根本识别不出 λ,择时输出是噪声;
- crypto:λ 四年全钉在最大收缩 → 引擎自己判断"没有择时信号",自动退回静态附近——**失效时不逞强,这是这套方法最像风控工具的地方**。

诚实的边界(被独立审查用我们自己的数据修正过):它是**单向**哨兵——**翻转率高=可疑,成立;翻转率低≠可信**(短窗口里存在翻转率 0 但溢价 −0.45 的假阴性)。用法:高翻转 → 关择时层;低翻转不构成开仓依据。

## 五、包成全天候壳,以及 Sortino 翻案

择时书是市场中性的(gross=1 轮动),正确用法是当 **sleeve** 装进组合层。全天候能力最终以两种形态存在:**main 上的因子书全天候层 `quant.factortiming.allweather`**(统一因子 store 汇入一本择时书,OOS 证据 + λ 仪表盘 + 可部署目标书,CLI `quant allweather`,随 PR #254 合入);以及**多资产 RP 壳**(因果风险平价 + 波动目标 + λ 哨兵,12 个合成测试)——后者随 PR #253 关闭归档于保留分支,但其真数据实测结论仍然成立。RP 壳把择时书和久期/股票/信用 sleeve 配平(概念背景见[风险平价与全天候](../concepts/risk-parity-and-all-weather.md)),2012–2022 实测(全 committed 数据):

| 书 | 夏普 | **Sortino** | 偏度 | 最大回撤 |
|---|--:|--:|--:|--:|
| 全天候(净融资成本) | 1.15 | **2.12** | **−0.03** | −12.0% |
| 60/40 | 1.14 | 1.87 | −0.45 | −11.3% |
| 纯 SPX | 1.04 | 1.67 | −0.52 | −19.5% |

两个要点:①夏普口径全天候只和 60/40 **打平**(实质是 2–3 倍杠杆风险平价,波动目标不咬合、杠杆帽先到,融资成本已计);②**Sortino 口径它领先 13%**——因为它的波动近乎对称(偏度 −0.03)而基准都是左尾,夏普把上行波动当罪罚掉了。对激进自营(只在乎跌的时候疼不疼),下行度量下这个壳的排名实质性上移。

反过来,择时书自己在 Sortino 下暴露了代价:**偏度 −0.72**(static/naive 都是正偏)——"低波加仓"平时管用,偶发因子崩盘会在高仓位上挨打。进 overlay 池要和正偏的东西(趋势/尾部对冲)搭配,别单吊。

## 六、方法论彩蛋:独立审查循环抓住了真 bug

本轮按"开发 → 独立只读审查(需求/逻辑/边界/质量/测试/实跑六方面)→ 修复 → 复验"循环推进。首轮审查 FAIL(1 blocker + 4 major),其中一条不是文字问题:**组合引擎对期中缺值的 sleeve 做了"半本书"静默记账,而且这个缺陷就活在真数据里**(2022-06 被半本书入账,剔除后"全天候胜 60/40"降级为"打平"——上表已是修正后数字)。教训与[为什么回测会撒谎](../concepts/why-backtests-lie.md)同源:**最贵的 bug 不炸程序,只炸结论**;对抗式复核 + 数字逐格对账是抓它们的唯一办法。

## 七、工程沉淀(可复用件)

| 件 | 路径 | 一句话 |
|---|---|---|
| 因子收益数据源 | `quant.data.factors` | `(factor_id, date) -> ret` 源无关层;Ken French 免费全集 + 派生因子留存(`CN_*`/`CNIDX_*`/`FX_*`/`CRYPTO_*` 统一入 committed store)+ JKP 131 因子 paved(WRDS 门控) |
| 择时引擎 | `quant.factortiming` | managed 构造 + 三层收缩 + 扩展窗口 OOS + 隐含权重(可算换手/成本) |
| 全天候层 | `quant.factortiming.allweather` | 统一 store → 一本择时书:OOS 证据 + λ 三态仪表盘 + 可部署目标书(gross=1);CLI `quant allweather`;多资产 RP 壳存档于 #253 保留分支 |
| 复现/实验/报告 | `research/factor_timing_nagel/` | 中文报告(复现/跨市场/维度阶梯)+ 全部冻结 JSON;fornax 实验已执行完毕,CN 判决 REJECT |

## 带走的心智模型

- **择时溢价是"高维 × 长样本"的联合产物**,不是任何市场的普适现象;缺样本时维度是毒药。
- **收缩不是保守,是生存**:λ=0 在高维必崩;λ→∞ 自动退回你本来就要持有的静态书——下行有界、上行真实,这是凸性。
- **λ 翻转率单向哨兵**:高翻转关择时;低翻转不算通行证。
- **夏普会冤枉对称分布、放过左尾**:凡是给激进资金看的报表,Sortino/偏度必须同列。
- 结论的可信度来自流程:预注册协议、四基准对照、独立审查循环、REJECT 也是产出。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [因子风险](factor-risk-and-idiosyncratic-alpha.md) · [统一因子目录](factor-catalog.md) |
| 下游 | [参数与过拟合](parameters-and-hyperopt.md) · [多重检验](../concepts/multiple-testing.md) |
| 同域 | [qlib 挖矿实验室](qlib-alpha-lab.md) · [宏观 regime](../concepts/macro-regime-and-sizing.md) |
| ADR / concepts | [为什么回测会撒谎](../concepts/why-backtests-lie.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [实验框架](../reference/experiment-framework.md)
- **源码:** [`factortiming/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/factortiming) · Nagel(2025) 复现笔记见页内
