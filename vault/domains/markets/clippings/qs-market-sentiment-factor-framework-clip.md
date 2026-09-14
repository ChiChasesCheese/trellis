---
title: A Factor Framework for Market Sentiment
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/market-sentiment-factors.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 市场情绪的因子化框架(2026 调研)

这一层回答:**怎么把"市场情绪"这种听起来很虚的东西,系统地采集、标准化、变成一个严格因果、能进闸门的因子?** 结论先摆前面,因为它和直觉相反,也和本仓库[宏观状态](macro-regime-and-sizing.md)的结论同源:

> **情绪不是一个"预测涨跌"的择时信号,而是一个"极端时反向 + 平时读风险/波动"的信号。** 它在**极端值**处有反转含义(众人极度贪婪→未来低回报),在中间区几乎是噪声;它对**波动率/回撤**的预测力远强于对**收益方向**的。所以正确用法是**极端反向 + 仓位 sizing**,不是"情绪好就满仓、情绪差就清仓"。样本上每个情绪周期以月/季计,独立事件很少 —— [DSR](../reference/glossary.md) 极难过,是过拟合重灾区。

下面分三块:**情绪怎么采(collection)**、**怎么因子化(factorization)**、**怎么落到本仓库**。

## 一、情绪是什么?为什么它能是一个因子?

"情绪(sentiment)"= 投资者**偏离基本面的、被情绪驱动的集体信念**。学术定义(Baker-Wurgler)直接说它是"对基本面无法解释的、对某类证券的乐观/悲观倾向"。

它能成为因子,靠两个前提(缺一不可,这是所有行为因子的通用骨架):

1. **有人在犯系统性错误** —— 散户/追涨杀跌资金在情绪高点买贵、低点割肉。这是"谁在另一边亏"的答案。
2. **套利有限(limits to arbitrage)** —— 聪明钱不能无限做空高估的垃圾股(借券贵、噪声交易者风险、期限约束),所以错误定价能持续一段时间,给你窗口去收敛。

Baker-Wurgler 的核心实证:**情绪高涨后,"难估值/难套利"的股票(小盘、高波动、不盈利、极端成长、不分红)未来回报显著更低** —— 情绪的作用是**横截面**的,专打投机性最强的那一端。2026 年的复制研究(Leong, *Economic Inquiry* 2026)在 2002–2023 的新样本上再次确认了这个横截面效应仍然存在。

## 二、采集层:主流各市场怎么量情绪

情绪没有单一真值,靠**多个代理(proxy)三角定位**。按"信号从哪来"分五族,每族在不同市场有不同抓手:

| 代理族 | 读的是什么 | 美股 | 加密 | 中国 A 股 |
|---|---|---|---|---|
| **调查/持仓(survey/positioning)** | 人**说**自己怎么看 / 实际仓位 | AAII 牛熊、Investors Intelligence、NAAIM 敞口、CFTC COT 持仓 | 交易所多空账户比、大户持仓 | 基金仓位调查、新增开户数 |
| **期权隐含(options-implied)** | 人**花钱**买的保护 | VIX、put/call、SKEW、VVIX、MOVE(债) | 期权 IV、Deribit put/call、DVOL | 50ETF 期权 IV、认沽认购比 |
| **广度(breadth)** | 上涨的**面**有多宽 | %>200日线、新高/新低、涨跌家数、McClellan | 上涨币种占比、BTC 主导率 | 涨停/跌停家数、上涨家数占比 |
| **资金/杠杆(flows/leverage)** | 钱**真的**往哪流 | 基金流(EPFR/ICI)、ETF 流、融资余额(margin debt) | 永续**资金费率**、未平仓量(OI)、稳定币供给比、清算数据 | **北向资金**(陆股通)、**融资融券余额**、换手率、成交额 |
| **新闻/社媒 NLP** | 语言里的**语气** | RavenPack、GDELT+FinBERT/LLM、StockTwits、Reddit/WSB | LunarCrush、Santiment、社媒 buzz、搜索趋势 | 财经媒体语气、百度指数、雪球/东财热度 |

**再往上一层是"复合指数(composite)"**,把上面几族揉成一个 0–100 或 z 分数:

- **CNN Fear & Greed(美股,最流行)**:7 个等权分量 —— 动量(标普距 125 日均线)、价格强度(52 周新高 vs 新低)、价格广度(McClellan 量能)、put/call、市场波动(VIX)、避险需求(20 日股债回报差)、垃圾债需求(高收益 vs 投资级利差)。方法就是"每个分量偏离自己均值多少个正常波幅,等权平均"。**注意本仓库的 macro 层已经天然携带其中至少 4 个分量的原料**(VIX、股债回报差、HYG/LQD 信用利差、动量),见下文第三节。2026-07-01 读数 32(fear)。
- **Crypto Fear & Greed(加密,Alternative.me)**:波动率、动量/成交量、社媒、主导率、搜索趋势等 6 因子加权;各家(CoinMarketCap/Milk Road/CoinGlass)分量略不同,但都重仓**波动率 + 资金费率/OI + 社媒**。
- **Baker-Wurgler 学术指数**:6 个代理(封闭式基金折价、IPO 数量、IPO 首日回报、股权发行占比、分红溢价、换手率——换手率在最新版被剔除)做 **PCA 取第一主成分**,并对宏观(工业产出、消费、就业、NBER 衰退)**正交化**去掉风险成分。这是"情绪指数"的学术金标准。
- **Huang-Jiang-Tu-Zhou "对齐"指数(2015, RFS)**:用 **PLS(偏最小二乘)** 而非 PCA —— 关键区别是 PLS **对着"预测未来回报"这个目标**去提取,剔除各代理里与目标无关的公共噪声。实证上它的**时序**预测力(样本内外)显著强于 Baker-Wurgler,还能预测行业/规模/价值/动量排序的横截面回报。**这条是"怎么聚合"的最佳实践,见下节。**

## 三、因子化层:把原始代理变成一个能进闸门的因子

采集回来的是一堆量纲各异、频率各异、发布滞后各异的原始序列。因子化 = 一条**严格因果**的流水线,和本仓库 [`macro/indicators.py`](macro-regime-and-sizing.md) 的做法同构:

**Step 1 · 标准化(normalize)。** 每条原始序列 → 滚动 **z 分数或百分位**(只用历史窗口,`shift(1)` 防前视)。把"融资余额 5000 亿"和"VIX 32"变成可比的"离自己 2 年常态几个标准差"。

**Step 2 · 定方向(sign)。** 这是最容易搞错、也最值钱的一步:

- **极端反向 + 中间无信号**:情绪的可用信息几乎全在**尾部**。AAII 官方自己都说该调查"不预测方向",但**极端**牛/熊常先于反转 —— 这是**非线性**的,别做成线性回归。做法:只在 z 超过 ±1.5~2 时触发反向,中间置零。
- **时序(TS) vs 横截面(XS)**:同一份情绪数据有两种用法。**TS**(整个市场一个数)→ 择时/降险,少数几个独立周期,DSR 难过。**XS**(每只股票一个新闻情绪分)→ 排序选股,`√Breadth` 上千个独立下注,统计上友好得多(见[主动管理基本定律](../reference/glossary.md))。**优先做 XS。**

**Step 3 · 聚合(aggregate)。** 三种档次,复杂度递增:

1. **等权 z 复合**(CNN F&G 式):简单、稳健、可解释,先做这个当 baseline。
2. **PCA 第一主成分**(Baker-Wurgler 式):提取代理间的公共情绪成分,**必须先对宏观正交化**,否则你提出来的是"经济周期"不是"情绪"。
3. **PLS 对齐**(Huang 式):对着"预测回报"提取,剔共同噪声。样本外最强,但也最容易过拟合目标 —— **必须**走本仓库的 [purged-CV / DSR / PBO 闸门](why-backtests-lie.md)。

**Step 4 · 对齐横向 vs 纵向的坑(causality)。** 情绪数据是前视重灾区:

- **发布滞后**:AAII/II 周频、COT 周五发布含滞后、融资余额 T+1、北向实时但历史口径变过。用"**当时真正可得**"的值,别用后修订版。
- **复合指数的隐形前视**:很多第三方情绪指数会**回填/重算**历史(改分量、改权重),直接下载其历史序列做回测 = 用了未来信息。要么自己从原始分量在 PIT 下重建,要么只在实时 forward 采集。
- **情绪 → 波动的因果强于 → 收益**:见下面本仓库的实测。

**Step 5 · 用法 + 上闸门。** 情绪因子和宏观状态一样,**首选连续 sizing / 极端反向,不是二元清仓**。而且时序情绪的独立事件太少,**单独**做时序择时几乎必然过拟合 —— 要么当**横截面**因子(广度救它),要么当**降险 overlay**(和 VRP 同类),都要过双闸门。

## 四、落到本仓库:情绪层其实已经建了一半

关键洞察:**本仓库的 [macro 层](macro-regime-and-sizing.md)就是情绪采集层的"风险偏好"半边。** VIX、VRP、信用利差(HYG/LQD)、股债回报差、DXY —— 这些正是 CNN F&G 七分量里的五个、也是"期权隐含 + 资金/避险"两族的核心。所以:

- **CNN Fear & Greed 在本仓库几乎可直接重建**:`macro_panel(["VIX","HYG","LQD",...])` + 价格动量/新高新低/put-call,等权 z 即成。缺的分量(put/call、52 周新高广度)是下一步数据活。
- **一个 `SentimentSource` 家族** 已有初步实现:`data.sentiment` 中的 `SentimentStore`(cache-first CSV+PIT,与 `MacroStore` 同构)是 `MacroSource` 的孪生兄弟;同样的 `(series_id, date) -> value` 契约。五族中"调查/持仓"和"资金/杠杆"族已部分可接入(AAII/COT/融资余额有免费源);EODHD `sentiments` 在付费套餐可用(权限以仓库里程碑/contracts 为准),Crypto F&G 已实测。横截面新闻情绪(FinBERT/LLM)仍是 data-gated(需新闻源镜像)。
- **横截面新闻情绪 → `alpha/cross_section` 因子**:用 FinBERT/LLM 给个股新闻打分,写成一列,和现有的低波、残差动量因子一样跑在 `UniversePanel` 上,过闸门。2025–2026 的实证(GDELT+FinBERT、FinBERT×Fama-French 五因子)显示这条有信号,但**半衰期短、且被大量基金消化**(见[家族 10 · 另类数据](../catalog/10-altdata-ml.md))。

**本仓库自己的证据,预言了情绪因子会长什么样。** 我们在四个市场对"宏观 risk-off 状态 → 前向结果"做过诚实条件检验(`research/macro_indicators.md`):

| | 前向**波动率**规律 | 前向**收益**规律 |
|---|---|---|
| 跨市场一致性 | **4/4 同号**(SPX 1.77×、EEM 1.56×…) | **1/4**(股/汇 risk-off 后反而略涨) |

risk-off / 恐慌是**可靠的波动预测器、不可靠的收益择时器**。情绪指数与 risk-off 高度同源,所以这条曾是**预测**:情绪因子应该也是"波动/风险信号 + 极端反向",不是牛熊择时。

**这条预测现在已被实测证实(`research/sentiment_signal_e2e.py`)。** 我们把反向情绪择时(极端贪婪降险)在四个市场过了双闸门:

| 市场 | 信号源 | de-risk Sharpe | buy-hold Sharpe | 判决 | 关键危机 |
|---|---|---|---|---|---|
| BTC | 真 crypto F&G(2018–) | +0.36 | +0.44 | REJECT | MaxDD −62% **两者一样** |
| SPX | 派生股票 F&G(2004–) | +0.66 | +0.69 | PASS\* | 2022 **−10% vs −18%** ✅ |
| EEM | 派生 US F&G(跨市场) | +0.41 | +0.36 | REJECT | MaxDD −34% vs −40% |
| EURUSD | 派生 US F&G(跨市场) | +0.03 | +0.05 | REJECT | ~0 |

\* PASS 只是"没被 DSR 判为假",Sharpe 反而低于 buy-hold —— **不代表跑赢**。

结论坐实:**作为独立 alpha,REJECT。** overlay 几乎就是 buy-hold(corr 0.92–0.98),在母市场 BTC 上反跑输且没削回撤(F&G 由价格/波动算出,**没法给它自己测的那次崩盘择时**);唯一价值是极端贪婪降险在 SPX 2022 / EEM 削了点危机回撤,但比 [VRP](../catalog/06-volatility-options.md) 更弱、更冗余。而 VRP 是本仓库测下来**唯一稳定有效的降险 overlay**(读"保费/恐慌定价")。反过来,朴素的 risk-on/off 择时叠在趋势 book 上是[帮倒忙的负结果](../ideas/multi-asset-book.md)。**一句话:情绪进横截面(新闻情绪打分)或当降险 overlay,别做单资产牛熊择时。**

## 五、坑(情绪因子特有)

- **样本少 = 时序择时必过拟合**:情绪以月/季为周期,几十年也就几十个独立摆动,时序 DSR 极难过。**用横截面或降险,别用市场择时。**
- **复合指数回填前视**:第三方历史序列常被重算,直接回测 = 作弊。PIT 重建或 forward 采集。
- **半衰期短 + 拥挤**:新闻情绪一旦好用就被基金抢跑,alpha 衰减快;要持续挖新数据/新语言模型。
- **极端才有信号**:别把情绪塞进线性模型稀释掉尾部信息。
- **"情绪好"≠"该买"**:情绪高涨在 Baker-Wurgler 里是**未来低回报**的信号(反向),不是顺势加仓的理由。

## 延伸

[宏观状态与仓位管理](macro-regime-and-sizing.md)(情绪的"风险偏好"半边,已实测) · [家族 6 · 波动率与期权](../catalog/06-volatility-options.md)(VIX/VRP 作为恐慌定价) · [家族 9 · 宏观与跨资产](../catalog/09-macro-crossasset.md) · [家族 10 · 另类数据与 ML](../catalog/10-altdata-ml.md)(新闻情绪 NLP) · [为什么回测会撒谎](why-backtests-lie.md) · [多重检验](multiple-testing.md)。

### 参考与数据源

- Baker & Wurgler (2006/2007), *Investor Sentiment and the Cross-Section of Stock Returns* / *Investor Sentiment in the Stock Market* — 情绪指数的 PCA 金标准。[NBER w13189](https://www.nber.org/system/files/working_papers/w13189/w13189.pdf)
- Huang, Jiang, Tu & Zhou (2015, *RFS*), *Investor Sentiment Aligned: A Powerful Predictor of Stock Returns* — PLS 对齐指数。[SSRN 2311618](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2311618)
- Leong (2026, *Economic Inquiry*),Baker-Wurgler 的复制与延伸(2002–2023 样本仍显著)。
- 复合指数实时源:[CNN Fear & Greed](https://www.cnn.com/markets/fear-and-greed)(7 等权分量)、[Crypto Fear & Greed(Alternative.me)](https://alternative.me/crypto/fear-and-greed-index/)、[AAII Sentiment Survey](https://www.aaii.com/sentimentsurvey)。
- 新闻 NLP:GDELT + FinBERT/LLM 近作(arXiv 2505.16136、2505.01432)、RavenPack 宏观情绪白皮书。

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
- **注:** 情绪五族框架
