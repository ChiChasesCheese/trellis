---
title: 'What an Institutional-Grade Trading Engine Needs: A Requirements Scorecard'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/live-and-event-driven.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 13 · 实盘 & event-driven 引擎(0.6)

> 0.6 版本重点。把 [8b · HF×AI 差距计划](hf-ai-gap-plan.md) 里一直被 defer 的「执行」线做深:
> **dry-run→live 接通** + **频率从日频拉到分钟/秒/tick** + **event-driven**。方向决策见
> [ADR-0008](../adr/0008-live-event-driven-nautilus-not-lean.md)。本页是「先钉死再开票」的全量
> 对比:现状 vs Nautilus vs LEAN 三方对照、机构级交易引擎需求逐项打分、频率阶梯、event-driven
> 架构、测试计划、rollout 相位与票图(epic `qs-lve`)。

## 0. 一句话

要「全资产 + event-driven 实盘 + 套我们的反自欺闸」,最省的载体是**深化已在栈内的 Nautilus
`TradingNode`**(backtest-live parity、event-driven、多 venue),**不是**引一个 C# 单体 LEAN。
闸门层留在便宜的 `VectorEngine` 不动;Nautilus 当确认层 + 实盘层。LEAN 唯一真赢的是上市期权/
期货 + 组合保证金成熟度——若 0.6 重心不在重衍生品,引入它是负 ROI。

## 1. 现状(核实,勿当叙事)

- `LiveEngine`(`execution/engine.py`)= **一次 reconcile tick**:拿 marks + 目标权重,对账
  broker 持仓,按实时 equity 定量,过 `RiskManager`,经 `BrokerRouter` 下单。
- **dry-run vs live = router 后面挂哪个 broker**(`venue_mode` → `broker_factory`;P0
  `qs-lve.2`/`.6` 已关)。外环 while/cron + 成交幂等落 `TradeDB`;开机对账 /
  单调订单状态机 / RiskEngine 已硬化(`qs-lve.3`/`.5`/`.4`),hermetic 组合于 `.16`。
- **`LiveEngine.dry_run` 字段已删除**(`qs-v7m0`):它从不被 `tick()` 读,却让 4 个生产点看起来
  像在空跑。唯一开关就是 broker 身份;"这一 tick 什么都别提交" 写作 `risk.halt(...)`。
- **频率**:横截面日频再平衡仍走 tick;**无**生产 TradingNode、无 Strategy 事件回调
  (欠 `.9`/`.11`/`.17`)。实时 feed 的**纪律层**曾在 quant.data.feed(`qs-lve.10`,§5.1)落地,
  但零 vendor transport、零 src 消费者,已退役 → Nautilus `DataClient`(ADR-0008; retired
  qs-6yyk.2),marks 仍由调用方注入。
- Nautilus 在本仓已用 `BacktestEngine` 路径(`NautilusEngine` / book e2e)做确认闸;
  **`TradingNode`(实盘节点)仍为零**——定案见 ADR-0008;`tick` 终态 deprecate 见
  ADR 2026-07-24 addendum 与 [14 · 引擎搭配](vectorbt-nautilus-and-our-engines.md)。

## 2. 机构级交易引擎需求 · 逐项打分

分级:**[NN]** 非可协商(错=亏钱/坏状态,与速度无关)· **[SCALE]** 生产成熟度(多策略/多账户需要)
· **[LAT]** 延迟奢侈(仅逼近 HFT 才重要,propshop 可 defer)。打分:✅有 · 🟡部分/需接线 · ❌缺 · ⛔不适用。
Nautilus 列据其官方文档(`nautilustrader.io/docs`);LEAN 列为定性参照。

### 2.1 市场数据面

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| feed handler:venue 原生→归一 schema | [NN] | ❌ quant.data.feed 纪律层退役(qs-6yyk.2)→ Nautilus `DataClient`(ADR-0008) | ✅ DataEngine + venue adapter | ✅ |
| tick/quote/trade 归一 | [NN] | ❌ TradeTick/QuoteTick 随 quant.data.feed 退役 → Nautilus `DataClient`(ADR-0008); retired qs-6yyk.2 | ✅ QuoteTick/TradeTick/OrderBookDelta | ✅ |
| 序列 gap 检测 + 重连恢复 | [NN] | ❌ FeedGap + 重订阅纪律随 quant.data.feed 退役 → Nautilus `DataClient`(ADR-0008); retired qs-6yyk.2 | ✅ | ✅ |
| L1/L2/L3 订单簿 | L1[NN] | ❌ | ✅ L1/L2/L3 + OrderBookDepth10 | ✅ L1/L2 |
| 历史+实时统一(同一代码路径) | [NN] | 🟡 回测统一,实盘缺 | ✅ 三环共架构 | ✅ |
| 纳秒时间戳 / PTP 时钟同步 | [LAT] | ⛔ defer | 🟡 纳秒分辨率 | 🟡 |

### 2.2 订单管理(OMS)

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| 显式订单状态机(含 in-flight 态) | [NN] | 🟡 PaperBroker 有基本态;live 未验 | ✅ INITIALIZED→…→FILLED + PENDING_UPDATE/CANCEL | ✅ |
| client_order_id ≠ venue id(对账 join 键) | [NN] | ❌ | ✅ | ✅ |
| 幂等:每个 fill/trade_id 恰一次(重连去重) | [NN] | 🟡 TradeDB 幂等 submit;fill 去重未验 | ✅ LiveExecEngine 预过滤 | ✅ |
| 部分成交 + overfill 处理 | [NN] | 🟡 | ✅ | ✅ |
| amend/cancel + in-flight 守护 | [NN] | ❌ | ✅ | ✅ |
| 父子/OCO/OTO/bracket | [SCALE] | ❌ | ✅ order list + contingency | ✅ |
| 全订单类型(9 种)+ TIF + post/reduce-only | [SCALE] | 🟡 market/limit | ✅ 9 型 + 仿真缺失型 | ✅ |

### 2.3 执行(EMS)

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| TWAP/VWAP 调度算法 | [SCALE] | 🟡 AC 轨迹(`optimal_execution`) | ✅ TWAP 内置 + ExecAlgorithm 扩展 | ✅ |
| POV / IS | [SCALE] | ❌ | 🟡 可扩展 | ✅ |
| 智能路由 SOR(多 venue) | [SCALE]/[LAT] | ❌ | 🟡 多 venue 但非竞速 SOR | ✅ |
| TCA(实测成本 vs 到达价) | [NN]-诚实 | 🟡 FillTCA 三价缝(`qs-lop`) | 🟡 事件可算 | ✅ |

### 2.4 盘前 & 实时风险(SEC 15c3-5 市场准入)

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| 盘前校验闸:不过则不达 venue | [NN] | 🟡 RiskManager 前单检(qs-243k 起按敞口方向双边生效,非仅 BUY) | ✅ RiskEngine → OrderDenied | ✅ |
| 仓位/gross-net/名义上限 | [NN] | 🟡 部分 | ✅ max_notional_per_order + instrument max | ✅ |
| fat-finger(价格 collar/最大单量) | [NN] | ❌ | ✅ 精度/量界/价校验 | ✅ |
| 下单限速 | [NN] | ❌ | ✅ submit/modify 限速 | ✅ |
| kill-switch / halt(全局+按策略) | [NN] | ❌ | ✅ TradingState ACTIVE/REDUCING/HALTED + ShutdownSystem | ✅ |
| 保证金/购买力检查 | [NN] | ❌ | ✅ 非保证金账户余额影响检查 | ✅ |
| 回撤熔断 / 按 pod 风险预算 | [SCALE] | 🟡 book gate 离线 | 🟡 TradingState 可编排 | 🟡 |

### 2.5 持仓 & PnL

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| 实时持仓 + NETTING/HEDGING 语义 | [NN] | 🟡 `PositionKeeper` 自持净额账已退休(qs-6yyk.16;0 生产构造点,原 qs-lve.14);SoT = broker 账本 + Nautilus `Position`(ADR-0010),hedging 未做 | ✅ 显式 netting/hedging + 虚拟持仓转换 | ✅ |
| 每 tick mark-to-market + 已/未实现拆分 | [NN] | ⛔ `positions.mark_to_market` 随 `PositionKeeper` 一并退休(qs-6yyk.16);单标的 LiveEngine/paper 路径没有常驻已/未实现拆分了,只有 `BookNautilusEngine` 整书路径经 Nautilus 原生持仓拿到 | ✅ | ✅ |
| 费用/资金费折进 realized | [NN] | ⛔ 随 `PositionKeeper` 一并退休(qs-6yyk.16);手续费仍在 broker `charge_fee`/`cost_profile` 里照扣,但没有常驻 realized PnL 累计器了 | ✅ | ✅ |
| 多币种记账 | [SCALE] | 🟡 按 quote 币种分账 + 注入 FX 才聚合,缺汇率拒给总额;历史汇率未做 | 🟡 | ✅ |
| 公司行动(拆股/分红)调整 | [SCALE]/股[NN] | 🟡 PIT 复权在数据面 | 🟡 | ✅ |

### 2.6 对账 & 状态恢复(小系统最爱跳过、最常被坑)

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| 开机对账 vs venue(拉单/仓/成交合并) | [NN] | ❌ | ✅ OrderStatus/Fill/PositionStatusReport + 合成缺失事件 | ✅ |
| 孤儿单处理(成交了但会话掉线没收到) | [NN] | ❌ | ✅ 重连检出 + external_order_claims | ✅ |
| 事件溯源(durable 事件存储=真相,cache 是投影) | [NN] | 🟡 TradeDB 落盘;非事件溯源真相 | ✅ event store 为权威 | 🟡 |
| crash-only:启动=崩溃恢复同一路径 | [NN] | ❌ | ✅ | 🟡 |
| 幂等重放(每逻辑消息恰一条) | [NN] | 🟡 订单 `client_id` + 成交 `fill_id` 双层去重(qs-lve.5/.14);feed 序列去重欠 `.10` | ✅ 序列去重 | 🟡 |
| 坏数据 fail-fast(NaN/溢出→崩非静默) | [NN] | 🟡 audit 闸在数据面 | ✅ 数据完整性优先于可用性 | 🟡 |

### 2.7 运维 / SRE

| 能力 | 级 | 现状 | Nautilus | LEAN |
|---|---|---|---|---|
| 每模块心跳 + 无响应重启 | [NN] | 🟡 LiveHeartbeat 有环无监控 | ✅ 组件 FSM + 心跳 | ✅ |
| 监控/告警(对齐交易时段) | [SCALE] | 🟡 DecayMonitor/notify | 🟡 | 🟡 |
| 延迟预算测量归因 | [LAT] | ⛔ defer | 🟡 | 🟡 |
| HA/failover / 灾备 | [SCALE] | ❌(可接受手动重启) | 🟡 | ✅ |
| 密钥管理(key 不进码) | [NN] | ✅ Settings/.env | ✅ | ✅ |
| 状态外置(Redis/PG 后备) | [SCALE] | ❌ | ✅ MessageBus→Redis;Cache→Redis/PostgreSQL | 🟡 |

### 2.7b 常驻持仓/PnL 对账(qs-lve.14,**retired qs-6yyk.16**)

The retired module *quant.execution.positions* (`PositionKeeper` / `LivePositionMonitor` /
`PositionState` / `ReconcileReport` / `PositionBreak`, 1,229 LOC) shipped under qs-lve.14 as an
**observer**, not a second OMS: it folded fills into its own average-cost book and
reconciled it against the venue on a resident cadence. Audit T3/T4 (codebase shrink
2026-08) found **0 production construction sites** — `rg -n "PositionKeeper\(|
LivePositionMonitor\(" src` matched only its own docstrings; nothing outside its own
tests and two bug-claim probes (which only used `PositionState.apply` as a *reference
implementation* for average-price/flip math, not the resident keeper itself) ever
constructed it. It was deleted in qs-6yyk.16; the average-price/flip math it duplicated
now lives in `quant.broker._position_math.apply_fill`, shared with the two paper
brokers.

**Position SoT going forward = the broker's own ledger (`BaseBroker.positions()` /
`.account()`) + Nautilus `Position` on the execution-realism path (ADR-0010).** The
resident mark-to-market / realized-PnL-net-of-fees / reconcile→ledger capabilities this
module used to provide (§2.5/§2.6 rows above) have no resident replacement — they are
retired, not relocated. If a future ticket needs them back, `BookNautilusEngine`'s
native netting/mark-to-market (§2.8) is the closer starting point than resurrecting a
parallel keeper.

### 2.8 打分小结

- **现状**:强在数据面 PIT/audit 与研究闸;实盘侧**几乎所有 [NN] correctness 件缺失或未接线**
  ——这正是 0.6 P0 要补的(§7 的 `qs-lve.2–.6`、`.14`、`.16`)。
- **Nautilus**:恰好在 propshop 的 [NN] 非可协商件上全绿(确定性单线程核 + parity、显式订单
  状态机、RiskEngine deny 闸、netting/hedging、四报告对账 + trade_id 去重、crash-only 事件溯源、
  fail-fast)。缺口都在 **[SCALE]** 档:VWAP/POV/IS、SOR、TCA、多币种/公司行动、HA/监控——是成熟度工作,
  **不是延迟奢侈**。
- **LEAN**:全绿但在 C# 单体,和 Nautilus 能力高度重叠;**唯一独占优势 = 上市期权/期货 + 组合
  保证金(SPAN)成熟度**。
- **关键结论**:propshop 的非可协商件全是 **correctness,不是速度**([LAT] 列可整列 defer)。

## 3. 三方对比(现状 LiveEngine · Nautilus TradingNode · LEAN)

| 维度 | 现状 reconcile-tick | Nautilus TradingNode | LEAN |
|---|---|---|---|
| 语言/进程 | Python in-process | **Rust 核 + Python,已在栈内** | C# runtime,进程外 |
| 与我们 ABC | `BaseBroker`/`BrokerRouter` 原生 | `adapter.py` 桥已接回测,延伸到 live | 缝外异构 |
| backtest-live parity | 🟡 同 tick 逻辑但非同引擎 | ✅ **一等特性**,同 Strategy 零改 | 🟡 |
| event-driven | ❌ cron 轮询 | ✅ MessageBus 单线程确定性事件核 | ✅ |
| 资产覆盖 | 股/币现货/永续/FX/CN/预测市场 | + 上市期货/期权(dated,BS greeks,≤4 腿) | + 期权/期货最成熟 |
| venue adapter | CCXT/Alpaca(未接线) | IB(股/期/期权/FX)、Binance/Bybit/OKX/Deribit/dYdX/Hyperliquid/Polymarket/Databento… | 券商广 |
| 反自欺闸 | 上游 VectorEngine | 上游 VectorEngine(不变) | 需自接,且重到扫不动 |
| 接线成本 | — | 中(复用桥 + 补 correctness) | 高(引 C# runtime + IPC) |
| 独占优势 | — | 已在栈内 + parity | 期权/期货 + SPAN 保证金 |

**待验证缺口(`qs-lve.7` spike 证伪/证实)**:Nautilus 期权/期货仅 per-instrument
`margin_init/maint`,无 SPAN/组合保证金证据;期权撮合 quote-driven 无 L2 队列;每 venue adapter
订单类型需逐页核;`TradingNode` **单进程单例**(并行=多进程,一 node 内挂多策略)。

## 4. 频率阶梯(日 → 分 → 秒 → tick)—— **已落地**(`qs-lve.12`)

「再平衡频率」是一等 **cadence 轴**,不是一刀切。**一个配置字段同时定死三件事**
(引擎路径 / 年化因子 / session 边界),它们因此**不可能各自漂移**:

| 档 | 触发 | 引擎路径(已解析) | `bar_freq` | 年化 `periods_per_year` | session |
|---|---|---|---|---|---|
| **`daily`** | EOD cron | `reconcile_tick`(**保持不动**) | `1D` | 市场真实 session 数 | n/a(一根 bar 即一天) |
| **`minute`** | 分钟 bar 事件 | `event_driven` | `1min` | **真实可交易分钟数** | RTH 掩码 |
| **`second`** | 秒 bar / quote 事件 | `event_driven` | `1s` | 分钟数 x 60 | RTH 掩码 |
| **`tick`** | trade/quote 事件 | `event_driven` | **无**(裸事件流) | **无 —— 直接 raise** | RTH 掩码 |

代码入口:`quant.core.cadence`(`Cadence` / `EnginePath` / `CadencePlan.resolve(market, cadence=)`)。
词表(合法档位 + 别名)住在 `quant.config_markets`(schema 模块),**行为**住在 `quant.core.cadence`
——反过来会闭合 `core → config → config_markets` 的导入环(import-linter `acyclic` 闸)。

### 4.1 config 与优先级

`config/markets/<market>.yaml` 增顶层 `cadence:`(缺省 = `daily`,已在六个 market yaml 与
`config/markets/resolved/` 快照里显式写死);`BookSpec.cadence` 可覆盖。
**优先级(越具体越优先)**:`BookSpec.cadence` > market yaml `cadence:` > `daily`。
市场声明的是「该 venue 的默认节奏」,book 允许比它更细(日频股票市场上挂一条日内 overlay),
所以 book 有最终发言权。非法档位在**构造/校验期**就炸,不会带着错年化跑到指标里。

### 4.2 年化:从真实日历导出,导不出就 raise

「一个你导不出来的年化因子就是谎」。三条形状取舍:

- **日频不动**:`daily` 直接委托既有 `clock.daily_periods_per_year`(XNYS 252 / XSHG ~242 /
  24x7 365 / 24x5 252 / 未知回落 252)。**所有既有日频回测数字逐位不变**,有回归测试钉住。
- **日内是 session-bounded,不是 wall-clock**:`clock.trading_minutes_per_year` 直接数日历的
  真实可交易分钟——**含午休、含半日市**。XNYS 2024 = **97 740** 分钟(不是 `365*24*60=525 600`,
  也不是名义 `390*252=98 280`——2024 有三个 13:00 半日:7/3、11/29、12/24);
  XSHG = 242 x 240 = **58 080**(午休 11:30-13:00 被扣掉;按 open→close 的 330 分钟算会高估 37.5%,
  即把年化 Sharpe 吹高 ~17%);FX `24x5` = 252 x 1440 = **362 880**。
- **crypto 24/7 就是 24/7**:`crypto.spot`/`crypto.perp` 没有休市,`minute` = 1440 x 365 =
  **525 600** 是**真的**。同一 cadence,US 与 crypto 差 **5.38x**——这正是硬编码 252(或硬编码
  `365*24*60`)会烙进净值的错。
- **`tick` 不给年化**:tick 到达不规则,「每年多少 tick」是**行情带**的属性不是日历的属性,
  所以 `periods_per_year` 对 `tick` **抛 `CadenceAnnualizationError`**;`CadencePlan.periods_per_year`
  记 `None`(「不存在诚实因子」),不是 0、不是猜。日内 cadence 落在**无法解析的日历**上同样 raise
  ——日频那条 252 回落在日内没有对应物。

`compute_metrics(equity, cadence=..., market=...)` 是消费端:不传则沿用 `DEFAULT_PERIODS_PER_YEAR
= 252`(遗留默认,逐位不变);同时传显式 `periods_per_year` 与 `cadence` 视为**歧义,直接拒**。

### 4.3 session 边界

`cadence_session_mask(index, cadence, market=, extended=)` 复用既有 `clock.session_mask`
(**不另起日历实现**),extended 窗口读 market yaml 的 `session:` 块。`daily` 全 True——日 bar
本身就是 session,再按 minute-of-day 掩一遍无意义;`minute`/`second`/`tick` 走 RTH 掩码
(`session_aware=True`,即 `VectorEngine(session_aware=True)` 那条日内路径)。

### 4.4 引擎路径:解析成决策,不重写 LiveEngine

- **日频不动**:横截面权重天然「EOD 算权重 → 对账下单」,cron reconcile-tick 是对的,
  **不强上事件环**。`run_track`(papertrack 的日频重放)对非 daily 的 book **直接
  `NotImplementedError`**——用日历年化一条分钟 book 会把 Sharpe 悄悄吹 ~20x;日内重放是 `qs-lve.13`。
- **分钟/秒/tick 走 event-driven**:tick → `quant.data.tick.aggregate.time_bars(ticks, plan.bar_freq)`
  → `Strategy.on_bar`(`qs-lve.9` 的事件回调,`supports_events()` 为真才走)。Nautilus
  `BarAggregation`(time/tick/volume/value + imbalance/runs + Renko;INTERNAL 自建或 EXTERNAL
  venue 提供;纳秒分辨率)是 `qs-lve.17` 接 `TradingNode` 时的聚合后端。
- 本票**只解析决策**(`CadencePlan`),**不重写** `LiveEngine`/`LiveHeartbeat`;`qs-lve.17` 消费
  `plan.engine_path` 去配 `TradingNode`。
- related:`qs-1yp.11`(Tick/LOB 缝已落地录制侧)、`qs-2f6`(日内 R2 持久化)、`qs-w3l`(慢+快
  overlay)、`qs-3dx`(盘前盘后 session)、`qs-1yp.10`(首个日内 alpha)。


## 5. Event-driven 架构(目标形态)

Nautilus 事件流(据官方文档),映射我们的 Strategy:

```
数据: venue adapter → QuoteTick/TradeTick/Bar → DataEngine(cache-then-publish)
      → MessageBus topic(data.quotes.<venue>.<sym>)→ Strategy 事件回调
下单: Strategy.submit_order() → RiskEngine 盘前闸(deny 则不达 venue)
      → ExecutionEngine → ExecutionClient/adapter → venue
      → venue 事件(Accepted/Filled/Canceled/Rejected)→ ExecutionEngine
      → 更新 Cache + Portfolio(持仓/PnL)+ 回传 Strategy
```

对我们意味着:
- **Strategy ABC 增事件回调**(`qs-lve.9`)`on_bar`/`on_tick`/`on_quote`,**保留** `signals(bars)
  →Signal` 批路径——truncation-invariance 闸依赖它,研究/回测语义不变。
- **RiskEngine deny 闸**替我们把 §2.4 的 [NN] 件落到「不达 venue」的强位置。
- **确定性单线程核**给回测-实盘 parity;网络 I/O/持久化在别的线程经 MessageBus 回灌。
- 引擎路线(A 自扩 `LiveHeartbeat` 为 feed 事件驱动 / B 采用 `TradingNode`)由 `qs-lve.8` 在
  `qs-lve.7` spike 证据上定夺,回写 ADR-0008 addendum——**不预设**、**不双开两套 live 引擎**。

### 5.1 实时行情 feed handler(`qs-lve.10`,已退役 → Nautilus `DataClient`)

`src/quant/data/feed/`(`FeedTransport`/`LiveFeed`/`ReconnectingFeed`/`ReplayFeed`/
`FeedSequencer`/`FeedGap`/`FeedMarks` 等,1,301 LOC + 978 LOC tests)在 qs-6yyk.2 收缩审计
中被退役:唯一 `FeedTransport` 实现是测试替身 `ReplayTransport`,零 vendor transport、零
src/research/scripts 消费者(仅自己的 5 个测试文件引用),`execution/engine.py`(`LiveEngine`)
从不 import 它。§2.1 打分表里 `feed handler / tick-quote 归一 / 序列 gap + 重连` 三行的
**我方实现路径**改为 → **Nautilus `DataClient`(ADR-0008); retired qs-6yyk.2** ——`.17`
组装真正的 `TradingNode` 时直接对接 Nautilus 原生 `DataClient`,不再经由这个自建包。
`FeedMarks`(「shaped for `LiveHeartbeat.run`」)随包一起删除;`LiveHeartbeat` 自身去留是
另一票(`qs-6yyk.26`),未变动。

## 6. 测试计划(tests-as-spec,`qs-lve.16`)

三层,CI 无网络硬依赖(sandbox e2e 用 `importorskip`/mock 守卫):

1. **零网络单测(correctness 闸,P0)**:订单状态机幂等重放(client_order_id 去重、崩溃重启不重复
   下单)、开机对账漂移分支(孤儿单/持仓不符→halt)、kill-switch/限额/fat-finger/限速熔断、
   netting/hedging 持仓语义、MtM 已/未实现拆分。用录制流,确定性。
2. **backtest-live parity 断言**:同一 `Strategy` 经回测 vs live-node(sandbox)行为一致性容差断言。
3. **sandbox e2e(守卫)**:CCXT testnet / Alpaca paper 跑通至少一条 dry-run 闭环
   (data→signal→order→fill→对账),收据入 PR。

对齐 `tests/README.md` 布局;沿用「改 adapter 先读其测试、加 adapter 镜像 peer」纪律。

## 7. Rollout 相位与票图(epic `qs-lve`)

Epic **`qs-lve`** `[epic] 0.6 实盘 & event-driven 交易引擎`,16 子票,parent-child 挂 epic,
blocks 依赖成图。血脉回指 `qs-1yp`;related `qs-jl1`/`qs-1kr`/`qs-av1`/`qs-1yp.10`/`qs-w3l`/`qs-3dx`。

| ID | P | 组 | 标题 | blocks-on |
|---|---|---|---|---|
| `qs-lve.1` | 0 | docs | ADR-0008 + 本对比 doc + HF scorecard(**本 PR**) | — |
| `qs-lve.2` | 0 | live-enablement | 券商工厂 + paper↔live config 开关注入 BrokerRouter | — |
| `qs-lve.3` | 0 | risk-safety | 开机对账:拉 venue 持仓/挂单,对齐不上 halt | .2 |
| `qs-lve.4` | 0 | risk-safety | 实时 RiskEngine:kill-switch/敞口/fat-finger/限速/回撤熔断 | .2 |
| `qs-lve.5` | 0 | live-enablement | 订单全生命周期持久化 + 幂等崩溃恢复 | .3 |
| `qs-lve.6` | 0 | risk-safety | Live 密钥/配置 + dry-run 护栏(默认 dry-run,显式 arming) | .2 |
| `qs-lve.7` | 1 | event-driven | Nautilus TradingNode spike:一 Strategy 经桥跑通 sandbox | .2 |
| `qs-lve.8` | 1 | event-driven | 决策闸:event-driven 引擎路线 A/B → ADR addendum | .7 |
| `qs-lve.9` | 1 | event-driven | Strategy ABC 事件回调(保留批 signals 路径) | .8 |
| `qs-lve.10` | 1 | market-data | 实时行情 feed handler:L1 订阅 + 归一 + gap 检测 | .2 |
| `qs-lve.11` | 1 | frequency-ladder | Bar 聚合:tick→时间/tick/volume bar(分/秒) | .10 |
| `qs-lve.12` | 2 | frequency-ladder | 频率阶梯 config:cadence 轴驱动再平衡 + 年化(**已落地**,§4) | .9,.11 |
| `qs-lve.13` | 1 | frequency-ladder | 首个日内 event-driven 策略跑到 paper(双闸) | .9,.11 |
| `qs-lve.14` | 1 | live-enablement | 实时持仓/PnL + reconcile→ledger 告警(解阻 qs-av1) | .5,.10 |
| `qs-lve.15` | 2 | ops | Live ops 加固:心跳监控/延迟埋点/重启 runbook/密钥轮换 | .5,.14 |
| `qs-lve.16` | 0 | testing | Live/dry-run 测试计划:sandbox e2e + 幂等/对账/kill 单测 + parity | .3,.4,.5 |

**实施顺序**:

```
.1(docs 本 PR) → .2(券商工厂) → .3/.6(对账+护栏) → .4/.5(风控+订单持久化)
  → .16(correctness 测试绿) → .7(Nautilus spike) → .8(引擎路线定案)
  → .9(事件回调) → .10(feed) → .11(bar 聚合) → .13(首个日内到 paper)
  → .14(实时 PnL 对账) → .12/.15(频率 config + ops 加固)
```

并行域:`.10/.11`(数据面)与 `.7/.8/.9`(引擎路线)文件域基本不相交,可并行。
`.2` 是全局阻塞——所有 live 票等它。

> **ticket 落地**:云端无 beads 库,子票先写文档化回落镜像 `research/backlog/tickets.jsonl`;
> bd 主机上按镜像 `import` 进 beads(SoT)后 `bd dolt push`。

## 相关页面

| 方向 | 页面 |
|---|---|
| 决策 | [ADR-0008](../adr/0008-live-event-driven-nautilus-not-lean.md) |
| 上游 | [9 · 与主流框架差异](vs-mainstream.md) · [8b · HF×AI 差距计划](hf-ai-gap-plan.md) |
| 同域 | [10 · 借鉴 freqtrade](borrowing-from-freqtrade.md) · [3 · 扩展缝](seams.md) · [12 · 高级](advanced.md) · [14 · vectorbt/Nautilus 搭配](vectorbt-nautilus-and-our-engines.md) |

## 外部来源

- NautilusTrader 文档:[architecture](https://nautilustrader.io/docs/latest/concepts/architecture/) ·
  [live](https://nautilustrader.io/docs/latest/concepts/live/) ·
  [execution](https://nautilustrader.io/docs/latest/concepts/execution/) ·
  [orders](https://nautilustrader.io/docs/latest/concepts/orders/) ·
  [data](https://nautilustrader.io/docs/latest/concepts/data/) ·
  [instruments](https://nautilustrader.io/docs/latest/concepts/instruments/) ·
  [integrations](https://nautilustrader.io/docs/latest/integrations/)
- SEC Rule 15c3-5(市场准入,盘前风控底线);OMS/EMS 架构文献;实现细节勿照抄,只借结构与 [NN] 清单。
