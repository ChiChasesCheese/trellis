---
title: 'Alpha, overlay or book: what a result is claiming'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/domain-model.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 框架领域模型:两条分层轴与核心对象

> 一句话:这个框架里有**两条互相正交的"分层"**——**数据分段 raw/bars/panel**(原料多干净)和
> **策略栈 alpha/overlay/book**(你主张的是什么)。把它们分清,才能正确读记分板:
> 一个 vol-target overlay 的 Sharpe 0.9 和一个横截面 alpha 的 0.5 **不可同榜比较**,
> 因为它们回答的是不同的问题。规范语汇的唯一出处是仓库根的 `CONTEXT.md`。

## 为什么需要这页(一次真实事故)

2026-07-07 读记分板时,`macro_vol_target_*` / `mvt_mom` / `vrp_timing` 一排 PASS(Sharpe
0.78–0.90)看起来像"6 个 alpha 通过了诚实门槛"。核实后:它们是 **2-3 个风险覆盖(overlay)
的重复别名**——Sharpe 来自"吃股票 beta + 波动率目标把曲线抹平",不是选股 edge;而真正的
横截面 alpha 全军 REJECT。混淆的根源是记分板只有一张平表,没有"这行实验主张的是什么"
这个维度。修法见下文「策略栈」;完整判决见
[qlib 挖矿实验室与诚实结果全览](../deep/qlib-alpha-lab.md)。

## 轴一:数据分段(raw / bars / panel)——原料多干净

用**名词**命名三段(旧称 "lake"、L0/L1/L2 "layer" 已弃用,见
[ADR-0002](../adr/0002-data-stages-raw-bars-panel-not-lake-layers.md)):

| 段 | 是什么 | 谁能碰 |
|---|---|---|
| **raw** | vendor 原样归档(jqdata parquet、EODHD raw),唯一落盘实体,只进不改 | 只有 `quant.data`(CI 强制) |
| **bars** | 单标的规范序列:复权、UTC、去重、schema 统一(读时派生) | 数据管道 |
| **panel** | 对齐多标的研究面板:PIT 掩码、生存者无偏、清洗(读时派生) | 研究/回测/挖矿的**唯一**入口 |

约定被 CI 钉死(`tests/data/test_layer_discipline.py` AST 扫描):策略代码 import raw 路径直接
红灯。详见[数据管线:raw → bars → panel](../deep/data-pipeline.md)与
[数据层分段与 alpha 自动化流水线](../deep/data-layer-and-automation.md)。

## 轴二:策略栈(alpha / overlay / book)——你主张的是什么

| stack | 主张 | 该问的问题 | 例子 |
|---|---|---|---|
| **alpha** | "我知道谁会涨/何时会涨"(预测性 edge) | DSR vs 零假设(为整个搜索付费) | 横截面 PEAD、动量、单资产择时 |
| **overlay** | "我让已有 book 的风险更好"(重塑分布) | **vs 裸 benchmark 的净增益** | vol-target、VRP 降险、止损 |
| **book** | "我把多个源拼成可交易组合" | 组合质量 + 尾部(偏度/肥尾) | risk-parity 多资产 book |

三层的 **PASS 语义不同**:overlay 过了 DSR 常常只说明"beta+风控抹平了曲线"——把它读成
alpha 就会误判"找到了 0.9 的策略"。实测教训两则:52 周高点择时过 DSR 但打不过纯 MA200
(overlay 性质的慢趋势滤波);止损套在分散因子篮子上**降低** Sharpe 且几乎不救回撤
(压 book 的是风格级相关回撤,per-name 止损治不了)。

**落地机制**:ledger 每行记 `stack` 字段(`run_experiment(stack=...)`,不传则按 family 名
回填);`quant scoreboard` 按层分段呈现,三层永不同榜。命名为什么是 `stack` 不是
`layer`——见 `docs/adr/0001-strategy-stack-not-layer.md`(一词两义正是事故根源)。

## 核心对象地图(30 秒版)

**数据侧**:`Symbol`(`<market>.<kind>.<code>` 全局键)→ `DataSource`(vendor 适配)→
`BarStore`(存储)→ `UniversePanel` / panel 面板(PIT、生存者无偏)。宏观级数序走
`quant.data.macro`。

**alpha 生产侧**:`AlphaDef`(声明式工件:公式 + 数据需求)← 六路来源(生成器/网络调研/
基本面/业绩预告/两融/龙虎榜)+ **zoo**(Alpha101+GTJA191);`DataProvider` 按需求供面板
(`resolve_bundle` 合并为 **bundle**);**跨模态** jungle(`mine_from_requirements`)在价量
之外搜基本面/做空/宏观,family=`crossmodal_jungle`。**测试队列**
(`quant.experiment.alpha_queue`)数据无关地跑闸,`n_jobs` 并行(`run_queue` 直调,
qs-6yyk.5 起不再有 1:1 Prefect flow 包装)。加一条数据轴 = 加一个 provider,队列零改动。US 空头面板键是
**`short_interest`**(≠ CN `short_ratio`)。US Fundamental/Short/Macro 与 CN peer 一样可自加载
(EDGAR / FINRA / `macro_panel`);`resolve_bundle` 从 ohlcv ``close`` 推导 ``dates``/``codes``
下传。

**门禁侧**:`run_experiment` 五闸(数据质量/截断不变性/trade_mode/成本/DSR)→ `ledger`
(append-only 判决,per-family 累计诚实 N)+ `vault`(因子值/净值对象)。**DecayMonitor**
把衰减/对账/孵化收成 `DecayReport`;**TrackingSink** 只做 MLflow/W&B sidecar。开放工作单元
(**ticket**)在 beads 票据库(`bd ready`/`--claim`),与 ledger、backlog 叙事档案三库
单向指针,见 `CONTEXT.md`「工作流」。**双闸**:研究闸
(VectorEngine)AND 执行闸(NautilusEngine),`confirmed` = 两者皆真。

**市场结构侧**:`MarketStructure`(T+1/涨跌停/无做空,causal 钳制)、`cost_profile`
(三档实测成本,硬约束)、`ExitPolicy`(持仓级出场,属 overlay 层;横截面 overlay 版 `xs_exits` 已迁 `research/`)。

每个对象的 canonical 深页:[实验框架 API](../reference/experiment-framework.md)、
[架构与数据流](architecture-and-data-flow.md)、
[多重检验](multiple-testing.md)。

## 术语纪律

- **规范语汇只有一处**:仓库根 `CONTEXT.md`(每词带 _Avoid_ 列表)。写代码、写文档、
  起 family 名之前先对齐;教学向大白话在[术语表](../reference/glossary.md)。
- **family 命名卫生**:一个研究方向**只准一个 family 名**。别名(`mvt_mom` ≡
  `macro_vol_target_momentum`,历史事故)会让记分板虚增 PASS 数、让累计多重检验 N 漏记。
- **数据分段用名词 raw/bars/panel**("lake"/L0/L1/L2 已弃用,ADR-0002);策略维度说
  **stack**(ADR-0001);软件架构分层说 **tier**。

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
- **注:** 两条分层轴
