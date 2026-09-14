---
title: The Truth About Trading Costs and Prices
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/costs-and-prices.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 交易成本与价格的真相

**价格不只是收盘价;交易成本远比想象复杂,常常是一个策略生死的真正分界线。** 配合 [为什么回测会撒谎](../concepts/why-backtests-lie.md) · [验证方法论](../reference/validation-methodology.md)。

## 0. 先记住一句话:成本是 quant 的生死线

一个策略在"不算成本"的回测里 Sharpe 2.0,扣掉真实交易成本后可能变成 -0.5。**毛收益(gross)和净收益(net)之间隔着一堵墙,很多漂亮策略就死在这堵墙上。** 本仓库实测:close-location-in-range 这个信号毛 Sharpe **+1.18**(全场最强),但它每天换手 142%,扣成本后净值是负的、被拒。**所以学会"成本怎么算"和"价格里藏了什么",和学会"怎么找信号"一样重要。**

---

## 1. 价格不只是 close —— OHLCV 里藏了维度

每根日 K 线其实是 5 个数:**开盘 open、最高 high、最低 low、收盘 close、成交量 volume**。绝大多数新手(和很多策略)只用 close,等于把另外四个维度白白扔了。

### 复权价(adjusted price)—— 必须先懂

历史价格要"复权"才能用,否则会有假信号:
- **拆股(split)**:1 拆 4,股价从 400 变 100,但公司没变。不复权的话历史上会看到一根 -75% 的假暴跌。
- **分红(dividend)**:派息当天股价掉一个红利,也是假跌。

**前复权/后复权**把这些机械跳动抹平,让"价格变化"只反映真实涨跌。本仓库的 `YahooChartSource(adjusted=True)` 用 `adjclose/close` 比例把 OHLC 全部按复权调整。**用错复权 = 用错数据,后面所有分析都歪。**

### 隔夜 vs 日内 —— 一个被忽视的金矿

一根日 K 可以拆成两段会话:
- **隔夜(overnight)** = `open[t] / close[t-1] - 1`(昨收 → 今开,盘后那段)
- **日内(intraday)** = `close[t] / open[t] - 1`(今开 → 今收,白天那段)

学术界(Lou-Polk-Skouras 2019)发现一个反直觉的事实:**股票的收益几乎全部在隔夜赚到,白天日内平均接近零甚至为负**,而且隔夜收益有**动量**、日内收益有**反转** —— 两拨不同的钱(机构 vs 散户)在拔河。本仓库在 89 只大盘上实测:隔夜单位风险收益(Sharpe 0.67)确实高于日内(0.43)。

**要点:同样的 OHLCV,换个角度切,就是一个"别人没认真看"的维度。** 量(volume)、日内区间位置 `(close-low)/(high-low)`、high-low 振幅,都是 close 看不见的信息。

---

## 2. 买卖价差(bid-ask spread)—— 第一种成本

市场上同一时刻有两个价:**买一(bid,别人愿意买的最高价)** 和 **卖一(ask,别人愿意卖的最低价)**。你**市价买入**要付 ask、**市价卖出**只拿到 bid,中间这个差就是**价差**,是你白交给做市商的过路费。

- **报价价差(quoted spread)** = ask − bid。
- **中点(mid)** = (ask + bid)/2,理论"公允价"。
- **半价差(half-spread)** = 价差/2 = 你单边交易相对中点的损失。**这是单边成本,通常用它。**
- **有效价差(effective spread)** = 2×|成交价 − 中点|,真实成交离中点多远(可能比报价价差小,因为有时能成交在价差内)。

价差用 **bps(基点,万分之一)** 表示。美股 **mega-liquid 大盘**(AAPL/MSFT)的有效半价差约 **1-5 bps**;小盘股能到 **20-100+ bps**。**越流动越便宜,越冷门越贵。**

---

## 3. 没有逐笔数据,怎么估价差?—— Corwin-Schultz

真实价差要逐笔报价数据才能直接量,但那很贵。**Corwin-Schultz (2012)** 给了个免费的妙招:**只用每天的 high 和 low 就能估价差。**

**直觉**:一天的最高价往往是有人按 ask 买上去的、最低价是有人按 bid 砸下来的,所以观察到的 high-low 范围 = **真实波动 + 价差弹跳**。关键技巧:**把范围拉到两天看 —— 波动随时间放大(2 天≈2 倍方差),但价差弹跳是固定的、不随时间放大。** 对比"两个单日范围"和"一个两日范围",就能用代数把波动和价差分离。

公式(了解即可):用 $\beta$(两个单日 log-range² 之和)和 $\gamma$(两日 log-range²),解出价差比例
$$S = \frac{2(e^{\alpha}-1)}{1+e^{\alpha}}, \quad \alpha = \frac{\sqrt{2\beta}-\sqrt{\beta}}{3-2\sqrt2} - \sqrt{\frac{\gamma}{3-2\sqrt2}}$$
负的估计置零,再按月平滑。代码:`quant.backtest.costs.corwin_schultz_spread_bps`。

### ⚠️ 关键陷阱:CS 对流动大盘严重高估

CS 假设 high-low 范围主要是价差弹跳。但大盘股真实价差才 1-2 bps,而日内 high-low 范围有 **100-200 bps**(全是真实波动)。CS 的波动修正不完美(隔夜跳空、日内趋势、离散噪音留残差),这点残差被错算成"价差"——**本质是想在 150bps 的波动噪音里量一个 1bps 的信号,测量误差直接淹没信号,系统性偏高。**

本仓库实测:CS 给大盘 **~25 bps**,而 TAQ 实测真实才 1-5 bps。**结论:CS 是小盘 / 宽横截面的对工具(那里价差占范围比例大、信噪比好),却是流动大盘的盲区。** 大盘要用下面的 TAQ 校准固定值。

---

## 4. TAQ —— 真实价差的金标准

**TAQ = "Trade and Quote" database**(NYSE 出品)。它记录美股**每一笔成交 + 每一次报价(bid/ask)**,逐笔、带时间戳。是测**真实有效价差**的金标准,也是检验 CS 这类估计器准不准的基准。**付费**(走 WRDS)。

所以"realistic 成本"的正确做法:**小盘 / 宽横截面用 CS(数据驱动、时变);流动大盘用 TAQ 实测校准的固定半价差(~1-2 bps)。** 本仓库的 `realistic_cost_bps(..., spread_bps=1.5)` 就是给大盘用固定档。

---

## 5. 市场冲击(market impact)—— 第二种成本

价差是"小单"的成本。但你下**大单**时,自己会把价格推动:买太多把价格买高,卖太多把价格砸低。这部分叫**市场冲击**,且**单越大、冲击越大**。

**平方根冲击律(square-root law,Almgren / Bouchaud / Kyle)**——业界标准近似:
$$\text{impact (bps)} \approx k \cdot \sigma \cdot \sqrt{\frac{\text{订单金额}}{\text{日均成交额(ADV)}}}$$
- $\sigma$ = 日波动率,$k$ ≈ 0.1(标准标定)。
- **参与率** = 订单金额 / ADV:你的单占当天成交额越大,冲击越大,而且是**平方根**关系(不是线性)。
- **和价差的本质区别:价差与你的规模无关(永远要穿价差);冲击随 AUM 增长** —— 所以**容量(capacity)**问题就藏在这里:小钱没事,大钱被自己的冲击吃掉。

代码:`quant.backtest.costs.sqrt_impact_bps`。对 mega-liquid 大盘、$10M 仓位,参与率极小,冲击只有 ~0.5 bps。

---

## 6. 总成本 = 换手率 × 单位成本 —— 为什么短周期信号会死

一个周期的总成本不是固定的,而是:
$$\text{成本} = \sum_{\text{标的}} |\Delta w_{\text{标的}}| \times \text{单位成本}_{\text{标的}}$$
其中 $\sum|\Delta w|$ 就是**换手率(turnover)**:每期权重变动的绝对值之和。

**这解释了那堵成本墙**:
- **短周期信号**(日内反转、close-in-range 这种 1-5 天效应)**换手极高**(天天大幅调仓)。
- 每次调仓都付价差 + 冲击。换手 142%/天 × 哪怕 2 bps = 每天 ~3 bps 拖累,一年吃掉几百 bps。
- 所以:**毛收益再漂亮,如果信号周期短于它的交易成本周期,净收益就是负的。**

本仓库的拯救尝试也证明:把持有期从 1 天拉到 10 天,换手降 4.3×,但**信号本身也衰减**(日内反转毛 Sharpe 从 0.61 掉到 0.33)——**降到能扛成本时,已经没边际了。**

---

## 7. 本仓库的实证:成本墙是真的

我们建了 realistic 成本模块,把最强的几个 live 信号在三档成本下重跑:

| 信号 | flat 5bps | CS(对大盘高估) | TAQ 校准 ~3.7bps |
|---|---|---|---|
| close-in-range 反转 | -0.78 | -5.42 | **-0.31** |
| 日内反转 | -0.65 | -4.77 | **-0.26** |

读法:
- **成本确实是一半问题**(-0.78 → -0.31,合理成本比 flat 5bps 友好得多)。
- **但即便在可辩护的真实成本下,仍然净负、仍被拒。** 更深的原因:那个 +1.18 是**全样本毛值**,在 purged 5 折样本外下毛收益已接近零 —— **墙是双重的:成本 + 样本外衰减。**

**教训:好看的毛 Sharpe ≠ 能赚钱。** 一个信号要活,得同时过三关:样本外不衰减、扣真实成本还正、容量够大。

---

## 8. 怎么在框架里用

```python
from quant.backtest.costs import realistic_cost_bps
# 大盘:TAQ 校准固定价差;小盘:留 spread_bps=None 用 Corwin-Schultz
cost = realistic_cost_bps(high, low, close, volume, aum=1e7, spread_bps=1.5)
run_experiment(signal, bundle, ..., fee_bps=cost)   # fee_bps 同时吃 float 或成本面板
```
`fee_bps` 传 float = 老的 flat 成本;传 `(日期 × 标的)` 的 bps 面板 = 每个名字按自己的流动性付费。**给未来任何有真样本外毛 alpha 的信号一个公平(而非惩罚性 flat-5bps)的成本检验** —— 这正是判一个边缘信号生死的关键。

---

## 9. 三档成本档案(cost_profile):测出来、记下来、驱动全局

上面的 `realistic_cost_bps` 是**每个名字**的成本面板;但很多时候你只想要一个问题的答案:「**这个市场,一笔交易到底大概花多少?**」而且要一个**确定值、保守值、激进值**,让回测、实盘、dryrun 用**同一套**数字。这就是 `quant.core.cost_model` 这个单一 seam 干的事。

![cost-model-dataflow](../diagrams/cost-model-dataflow.drawio)

**最佳实践三原则**(为什么这样设计):

1. **绝不揉成一个数。** 成本 = `手续费 + 价差 + 冲击`,三部分**真值来源不同**:手续费是**确定的费率表**;价差要**从数据实测**(且随行情变);冲击**取决于你的下单量**。揉成一个「5bps」,你就不知道是哪一部分杀死了策略(日内动量死于价差墙,不是手续费)。
2. **价差只能从日线得到上界。** 日线 H/L 区间对流动品种主要是**波动率**,不是买卖价差 —— 所以 Corwin-Schultz 对 SPY 报 15bps 是荒谬高估(真实 ~1bps)。真值 floor 来自公开 effective-spread 研究或日内数据。审计脚本会把这一点显式标出来,**绝不盲目拿 CS 覆盖记录值**。
3. **三档而非一档。** aggressive(地板:最流动+小单+平静)/ central(现实中位)/ conservative(thin+大单+压力)。**DSR 闸用 conservative** 判生死,别让乐观成本把死策略放行;P&L 预期用 central;aggressive 只做「理论地板上还有没有 edge」的 sanity。

**实测记录的三元组**(单边 bps,已含费率表;数字来自真实数据 —— US 用 `market_data` 25 名、A股用 fornax jqdata HS300+ZZ500 共 2006 名):

| 市场 | aggressive | central | conservative | 说明 |
|---|---|---|---|---|
| `us.stock` | ~1 | ~3 | ~10 | 费≈0;价差 floor 0.5bps → CS 上界 |
| `cn.stock` | ~10 | ~20 | ~45 | 费 5(佣金 2.5 + **摊销卖出印花 2.5**);价差实测主导 |
| `crypto.spot` | ~3 | ~12 | ~20 | maker/VIP → Binance taker 10bps |
| `fx.spot` | ~1 | ~2 | ~5 | 纯做市商价差(日线测不了,CS 对 FX 无意义) |

> **cn 的费率坑**:裸 `instrument_spec("cn.stock").fee_bps` 只读到佣金 2.5bps,**漏掉了 5bps 卖出印花税**。cost_profile 把印花按往返摊销进单边(2.5 + 5/2 = **5.0**),重测脚本已用真实数据验证这个 5.0。这就是「单一 seam」的价值 —— 一处改对,处处用对。

**产物是 committed + 可重测的:** 三元组存在 `market_data/reference/cost_profiles.csv`(每市场 3 行,含 provenance 和测量日期),随 main 被每个 session 继承。`scripts/seed_cost_profiles.py` 重新测量并**和记录值并排对比、标记漂移**(不盲目覆盖,因为价差 level 需要判断)。

**实测 TCA 闭环(qs-lop):** PaperTrack / LiveEngine 每笔 fill 携带决策价 / 到达中间价 / 成交价三价(`Order.decision_price` / `arrival_price` / `avg_fill_price`,汇总为 `FillTCA`)。`aggregate_fills_to_profiles` 按 `market × scenario` 取中位 trading→`spread_bps`、非负 delay→`impact_bps`(fee 保留费率表),`write_cost_profiles` 合并回 CSV。这把成本从「文献先验 + 一次性标定」升级为「自有成交可回填」——小资金唯一免费的执行研究数据源。详见 [`quant.execution.tca`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/execution/tca.py)。

```python
from quant.execution.tca import aggregate_fills_to_profiles, write_cost_profiles

# PaperTrack 回放后:
measured = aggregate_fills_to_profiles(track.fills, fee_from="market_data/reference/cost_profiles.csv")
write_cost_profiles("market_data/reference/cost_profiles.csv", measured, base="market_data/reference/cost_profiles.csv")
```

**默认档在 config 里定(不是硬编码):** `config/base.yaml` 的 `cost.default_scenario`(全局)+ 每个 `config/markets/<m>.yaml` 的 `cost:` 块(可单独覆盖)。当前四个市场都定为 `central`。

**怎么用(全局同一套):**

```python
from quant.core.cost_model import cost_profile, cost_bps

cost_bps("cn.stock", "conservative")        # 46.3 —— 一个标量,给闸门/预期用
p = cost_profile("cn.stock")
p.central.fee_bps, p.central.spread_bps, p.central.impact_bps   # 分解:5.0 / 12.0 / 4.1
p.round_trip_bps("central")                 # 42.2 —— 往返

# 回测里:命名市场 = 自动吃该市场 config 默认档的实测成本(cn.stock -> 21bps,不是旧的 flat 5)
run_experiment(signal, bundle, ..., market="cn.stock")                       # 默认 central
run_experiment(signal, bundle, ..., market="cn.stock", cost_scenario="conservative")  # 压测用尾
```

**优先级(`resolve_fee_bps`,least-surprising):** 显式 `fee_bps` 永远赢 > 显式 `cost_scenario` 用实测 > **命名 `market` 用它 config 默认档的实测成本** > 不命名市场 = 学术默认 5.0。所以:命名市场的回测**自动**按真实成本跑;要旧的 flat-5 就显式传 `fee_bps=5.0`;完全 market-agnostic(不传 market)字节不变。

![resolve-fee-precedence](../diagrams/resolve-fee-precedence.drawio)

> **这是一次有意的语义变更**:以前 `market=` 对成本中性(只管年化/结构/闸门),现在命名市场就等于「按这个市场的真实成本收费」。更诚实 —— A股旧的 flat 5bps 是严重低估(真实 ~21bps),US 旧的 5bps 是高估(真实 ~2.8bps)。

一句话:**把「真实成本」从散落在脚本里的 `fee_bps=5.0` 猜测,升级成一份测出来、记下来、能审计、config 定义默认档、命名市场即自动生效的三档档案。**

---

## 一句话总览

| 概念 | 全称 / 含义 | 量级(美股大盘) |
|---|---|---|
| 半价差 | bid-ask 的一半,单边过路费 | 1-5 bps |
| Corwin-Schultz | 用 high/low 免费估价差;小盘准、大盘偏高 | — |
| TAQ | Trade and Quote,逐笔真实价差金标准(付费) | — |
| 平方根冲击 | 大单推动价格,∝√(订单/ADV) | ~0.5 bps(小仓) |
| 换手率 | Σ\|Δ权重\|,决定成本被乘几倍 | — |

**核心:价格里藏着 close 看不见的维度(隔夜/量/区间);交易要付价差 + 冲击;总成本被换手率放大;短周期信号常死在成本墙上 —— 这堵墙是真的,不是回测里调个数字就能绕过的。**

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [信号工程](signal-engineering.md) · [策略风格光谱](strategy-styles.md) |
| 下游 | [慢定方向+快做日内](slow-fast-layering.md) · [参数与过拟合](parameters-and-hyperopt.md) |
| 同域 | [回测指标](../reference/backtest-metrics.md) · [9 · vs 主流](../architecture/vs-mainstream.md) |
| ADR / concepts | [为什么回测会撒谎](../concepts/why-backtests-lie.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [市场结构](../architecture/seams.md) · [freqtrade 对照](../architecture/freqtrade-full-comparison.md)
- **源码:** [`backtest/costs.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/backtest/costs.py)
