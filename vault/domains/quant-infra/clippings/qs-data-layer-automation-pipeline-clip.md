---
title: Data Layering and the Alpha Automation Pipeline
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-layer-and-automation.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 数据层分段与 alpha 自动化流水线

这一页是数据侧的 canonical 设计文档,面向未来的 AI agent 与人类读者:回答三个问题——
**数据怎么分段(raw/bars/panel)、怎么全自动拉取并清洗、怎么把"测所有 alpha"变成一条可无人值守
重跑的链路**。所有数字均为实测(2026-07 数据线建设轮),重跑可复现。

## 一、为什么要分段:一次真实的数据污染

2026-07-05 的全库体检发现:委托基线里 **MO(Altria)的收盘价没做 spinoff 复权**——2007-04-02
Kraft 分拆、2008-03-31 PMI 分拆两天,Yahoo 的 close 记成了 **−22.3% / −69.9% 的幻影暴跌**
(真实是 +3.5% / −2.5%)。`clean_panel` 和 `data_quality_gate` 两道现有闸都放行了它,因为
单向跳空看起来像真实危机行情。**一个未复权的除权日,足以毒化任何波动率/反转因子。**

根因是**没有分段、没有独立对账源**:YFinance 和 YahooChart 同源,互查抓不到同一个复权 bug。
教训直接催生了下面的 raw/bars/panel 分段——**raw 永久留底,才能事后追查厂商口径;独立第二源(EODHD)
才能对账出这类污染。**

## 二、raw / bars / panel 三段契约

| 层 | 是什么 | 谁在这层 | 铁律 |
|---|---|---|---|
| **raw** | 厂商原样、不可变 | raw store `data_lake/raw/eodhd/`(EODHD)、fornax `~/dataset`(jqdata) | 字段/类型/顺序照抄,只追加不修改;修数据永远在下游层修,**绝不回头改 raw** |
| **bars** | 规范化后的逐票 bars | `quant.data.raw`(EODHD)、`CNStockSource`、Yahoo 源 | 统一 schema(`[ts,open,high,low,close,volume]`、UTC、排序、去重、复权口径) |
| **panel** | universe 掩码 + 清洗 + 对齐的横截面面板 | `quant.data.panel.ohlcv_panels`、`cn_ohlcv_panels`、`artifacts.clean_panel` | 去幸存者、PIT 掩码、内容寻址;**研究/挖矿/部署只读 panel** |

门禁(`quality.audit_bars` / `health.cross_source_reconcile` / `data_quality_gate`)是**检查器不是
变换**,站在层与层的边界上,不改数据。

**分段纪律由 CI 强制**,不靠约定:`tests/data/test_layer_discipline.py` 用 AST 扫描——raw 路径标记
(`~/dataset`/`data_lake`/`CN_DATASET`/`raw/eodhd`)只允许出现在 `src/quant/data/` 内,
`quant.data.sources` 越层 import 禁止;历史遗留脚本进显式 legacy 名单,只许缩不许长。
绕层的代价已经真实付过一次:A 股 row-pick bug 家族(四个脚本基本面结论作废)正是老脚本内联读
raw 的产物。

### panel 统一入口:`ohlcv_panels(market, ...)`

各市场的 bars 底料和 panel 处理都不同(jqdata pre_close vs raw store adjusted;SP500 PIT 掩码 vs 固定
篮子),但**调用方(sweep、qlib staging、dashboard)不应该按市场分叉**。一个分发器把脏活藏在身后:

```python
from quant.data.panel import ohlcv_panels
panels = ohlcv_panels("us.stock", start, end)   # {open,high,low,close,volume,vwap}
```

- `cn.stock` → `cn_ohlcv_panels`(jqdata pre_close、去幸存者、PIT 掩码);
- `us.stock` → `us_ohlcv_panels` = **raw store bars(adjusted)+ SP500 PIT 掩码 + clean**;
- `fx.spot` / `crypto.spot` → raw store固定篮子(bars adjusted + clean;固定篮子无成分/幸存者概念,不做 PIT 掩码)。

**这条 seam 保证挖矿的 universe = 门禁的 universe = 部署的 universe**,三者共享同一个去幸存者面板。
(此前 US 的 PIT 掩码曾被内联在 sweep 脚本里 = 架构味道,已归位到 panel。)

**全路径统一到同一 panel 处理**(2026-07):不止 sweep,dashboard 与 CLI 的离线基线也走同一 clean 处理——
`quant.data.baseline.load_us_stock_panels(clean=True)`(默认)对基线缓存套 `clean_panel`,
把它定性为**panel-一致的固定篮子**(committed 是策展的固定名单、无成分概念,故无 PIT 掩码,同 FX/crypto 分支;
实测真实基线为 no-op,因 MO 已修)。`run_experiment` 本身信号无关(吃 `{"close": ...}` bundle),
所以"研究路径统一"= 面板构建收口到 `ohlcv_panels` / `load_us_stock_panels` 这一个 seam,三处
(dashboard 离线 / sweep-fornax / 门禁)看到的都是同口径 panel 数据。

**FX/crypto 的 panel 也被行为钉死**:`ohlcv_panels("fx.spot"/"crypto.spot")` 的固定篮子分支同样套
`clean_panel`(垃圾源票被丢)、vwap=典型价——`tests/data/test_raw_basket_golden.py` 注入垃圾源验证,
不只 shape 测试。

### EODHD close 的坑(务必用 adjusted)

实测(2026-07-06,别信厂商文档):EODHD `eod` 的 **`close` 是原始 as-traded 打印、未做拆股复权**
(WMT 2024-02-26 3:1 拆股日 close 有 −66% 假崩盘)。收益型研究**必须用 `adjusted_close`**
(拆股+分红+spinoff 全复权)。`quant.data.raw` 默认就是 adjusted 基准,把这个教训钉死在了 bars 入口。

## 三、raw 全自动拉取:raw 归档器

`scripts/eodhd_archive.py` 把 EODHD 全量灌进 fornax `~/workspace/zc/data_lake`(raw)。
四条设计让它可以无人值守:

- **断点续跑**:每笔完成写 `_state/done.txt` + `_state/manifest.jsonl`(机器账本:每笔一行,
  记 key/路径/行数/mode/时间),重跑跳过已完成。
- **原生增量**(重跑即刷新,零人工判断):拉什么是数据自身状态的纯函数——文件缺→全史;符号在退市表
  →首拉后**永久冻结**(3.2 万只退市票零后续开销);在市→从 `max(已存日期)−7天` 增量,并**校验重叠窗口**
  ——EODHD 每逢新除权除息会回溯重述全历史,重叠行不一致就整票重拉,杜绝一个文件混两套复权基准。
- **并发 + 限速**:归档实测**延迟受限**(串行 ~9.5 req/min vs EODHD 1000 req/min 上限,只用 1%)。
  加线程池(`--workers 12`)+ 令牌桶限速(`--rate 600`)+ 线程安全 Budget,把 t1 全史 EOD 从
  **~5 天压到 <1 天**(转为日配额受限,100k/天)。
- **预算感知**:本地估算 + 每 250 请求向 `/api/user` 校准真实扣费(账户级,本地+fornax 多进程共享
  同一视图,合计不超日配额)。`--loop` 跨 UTC 日自动续。

分段(易腐优先):`lists`(符号表)→ `t0` 日内(1m 仅 120 天窗口,最易腐)→ `t1` 全史 EOD(US 含退市
~6.1 万 + FX/CC/GBOND/INDX)→ `t2` div+splits 事件表 → `t3` 新闻情绪。库存快照一条命令:
`python scripts/eodhd_archive.py --root <lake> --inventory`。

### 跨源对账(独立第二源根治污染)

历史上用 EODHD 作 Yahoo 的**真独立第二源**对账过全基线(~90 credits/轮,统一拆股基准后
71 ok / 10 warn / 9 fail):MO 的 spinoff 污染被独立源正式抓到并修复;2026-07-11 迁移对账又抓到
RTX 分拆日 ~6.2% 幻影亏损。这些发现最终促成 bars 基线**退役 git 提交、直接以 EODHD
`adjusted_close`(拆股+分红+分拆全复权)为唯一源**(`quant.data.provision`,对账脚本随迁移退役,
数字冻结在 `docs/changelog.md`)。检测能力已用双源录制 fixture 钉进回归测试
(`tests/data/test_source_swap_equivalence.py`)。

## 四、alpha 自动化流水线:从数据到分阶段报告

整条链路一条命令(`scripts/alpha_pipeline.py`),每个阶段幂等、cron 友好:

```
archive → stage(panel) → mine(qlib) → sweep(公式因子+双闸门) → report
```

- **stage**:`ohlcv_panels` 出 panel 面板 → qlib staging CSV → `.bin` bundle(US 走 `qlab stage-lake` 的 panel 分支)。
- **mine**:qlib 表达式挖矿(rank IC 扫描)→ 幸存者进 `quant.vault`,`n_candidates` 记进元数据。
- **sweep**:`research/alpha2026_sweep.py` 把网络搜集的 2026 新因子(`alpha2026_candidates.json`,
  逐条带来源/机制)经 `quant.alpha.formulaic` 编译闸(AST 允许列表 + **负 shift 前视拒绝** + 安全内建)
  → `panel_signal` 统一月度分位 book → `run_experiment` 标准门禁(成本三档 / 交易日历 / `cn.stock`
  T+1·涨跌停·无做空)→ ledger。**幂等键 = `exp_id`**;数据未落齐记 SKIP 待下轮;
  **DSR 的 `n_trials` = 整场计划尝试数**,为整个搜索付费而非只为幸存者。
- **report**:`quant.experiment.report.staged_alpha_report`(纯函数,可测)把 ledger 渲染成中文
  分阶段报告(覆盖概览 → 各族记分板 → 可部署 lead),`research/alpha_report.py` 是 CLI。

### alpha 自动生成器(factory):把"测尽可能多的因子"变成诚实 routine

`quant.alpha.generator.generate_formulas` 从 14 个文献机制族(反转/动量/低波/振幅/量能/
彩票/偏度/非流动性/加速度/签名流…)× 窗口**模板化排列组合**出因子公式(默认 70 单窗口 +
91 两两复合),全部经 `compile_formula` 保证 AST 安全、因果、higher=long,确定性(routine
重跑同池)。`research/alpha_factory.py` 是两阶段漏斗:**生成池 ∪ 65 网络种子**(去重)→ rank-IC
预筛 → 幸存者入 `quant.vault`(因子库,和 qlib 挖矿同一队列)→ `gate_vault_factor` 过双闸门 →
ledger → 报告。

**核心诚实设计**:生成 N 个因子测试是天然的 p-hacking 机器——所以 `n_trials` 记的是**整池 N**
(生成 + 种子,预筛前),Deflated Sharpe 为整个搜索付费而非只为幸存者。实测(CN,limit=30):
29/30 过 IC 预筛、全部入库过闸、**全 REJECT**——这正是框架该有的样子:海量提出、门禁诚实处决,
vault 仍累积所有因子值供未来集成/元学习。幂等键 = 公式哈希,routine 重跑只补新增。作为编排器的
`factory` phase 跑,或独立 `alpha_factory.py --market`。

### 幂等 = 自适应重跑的前提

数据归档(一个 tmux 循环)与 alpha 扫描(另一个)速度不同、同时进行。扫描每轮只用"此刻已落地"的
数据:判过的 `exp_id` 跳过、数据没到的 SKIP 不写账。所以一个**自适应循环**(数据还在落时短间隔、
追平后退避)就能让扫描跟着归档进度分批自动补齐,无需人工盯数据。US 侧还有一道守卫:湖里 SP500 成员
不足 400 只时整体 SKIP,**绝不在半拉子 universe 上锁死判决**。

## 五、怎么在 fornax 上把它跑成常驻

```bash
# 一次性装环境
bash scripts/fornax_qlib_setup

# 归档器(raw 全自动拉取,并发,--loop 常驻)
tmux new -d -s eodhd_archive \
  "~/miniconda3/envs/zc/bin/python quant/scripts/eodhd_archive.py --root ~/workspace/zc/data_lake \
   --env-file quant/.env --sp500-csv quant/market_data/reference/sp500_constituents.csv \
   --workers 12 --rate 600 --loop"

# alpha 流水线(自适应循环:跟着归档进度补齐,报告持续刷新;factory phase = 自动生成器)
tmux new -d -s alpha_pipeline \
   "cd qlib_lab && QUANT_RAW_ROOT=~/workspace/zc/data_lake QUANT_ARTIFACTS_DIR=~/workspace/zc/af_vault \
   MLFLOW_ALLOW_FILE_STORE=true uv run python ../scripts/alpha_pipeline.py --loop \
   --phases stage,mine,sweep,factory,report --vault-root ~/workspace/zc/af_vault \
   --ledger-root ~/workspace/zc/a26_ledger"
```

铁律照旧(借用机):只写 `~/workspace/zc`、conda `zc` 环境、后 4 卡、`~/dataset` 只读、不在 fornax
上 commit。

## 六、离 hedge-fund / top indie quant 级还差什么

已达到的:去幸存者 PIT universe、公司行为(spinoff)可对账可修复、独立第二源交叉验证、成本三档硬约束、
purged-CV / Deflated Sharpe / PBO 统计闸、raw 永久留底 + 分段 CI 强制。

**组合级执行闸(整书,2026-07-10 落地)**:`quant.backtest.book_engine.BookNautilusEngine` 把整个
权重面板一次过 NautilusTrader 撮合(全部名字注册 instrument、共享一本 $0.5M MARGIN 账户、按整书
实时 NAV 定仓、lot 整手取整、涨跌停日订单封锁),`quant.experiment.book_e2e.book_e2e_check` 输出
整书 vs 向量书的年化 CAGR gap 一个数 + 审计三件套(fills/skipped/constraints)。此前的抽样代理
(`sampled_e2e`,每腿固定 $1M 不复利单独重放)已**退役删除**——它会把持仓记账约定差误报成执行
gap(动量书曾被报 −711bps,整书真实 −32bps),历史对比数字冻结在
`research/book_e2e_framework_compare.json`。

**基线供给 seam(2026-07-11)**:`quant.data.provision` 把"研究基线从哪来"变成自动机制
——按 `config/baseline_universe.yaml` 的冻结篮子,经 `EODHDEODSource(adjusted=True)` 增量
供给 gitignored `.baseline_cache/`。方向是让远端 vendor 成为唯一事实来源、git 不再承载 bars
数据;供给端周一快照 + CI actions/cache 把 vendor 流量压到每周至多每名一个小请求。激活清单见
`docs/superpowers/specs/2026-07-11-remote-baseline-provisioning-design.md`。CI/baseline 的
bars 数据已退役(`quant.data.provision` 之前曾有 `QUANT_DATA_MODE=committed|remote` 开关,现在
默认且唯一的模式就是 remote 供给;`QUANT_LAKE_ROOT` 也被 `QUANT_RAW_ROOT` 替代,fornax raw
store `~/workspace/zc/data_lake` 是唯一事实来源)。

仍在路上的(开放状态只认 `bd ready`;`research/BACKLOG.md` / backlog md 仅叙事档案):逐行权价 IV
历史(真 US VRP)、分析师预期(真 SUE)、intraday 深度累积到可过 DSR、混合市场 book
(per-symbol 约束 + 多币种账户,见 `qs-vfx`)。

---

相关代码:`src/quant/data/panel.py`(panel 分发器)、`src/quant/data/raw.py`(bars loader)、
`scripts/eodhd_archive.py`(raw 归档器)、`scripts/alpha_pipeline.py`(编排器)、
`src/quant/experiment/report.py`(报告)、`src/quant/data/DATA_SOURCES_REPORT.html`(数据源边界实测);
分段纪律见 `tests/data/test_layer_discipline.py`。相关概念页:[qlib 挖矿实验室](qlib-alpha-lab.md)、
[交易成本与价格的真相](costs-and-prices.md)、[因子、风险与特异 alpha](factor-risk-and-idiosyncratic-alpha.md)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [数据管线](data-pipeline.md) · [数据治理](data-governance.md) |
| 下游 | [qlib 挖矿实验室](qlib-alpha-lab.md) · [统一因子目录](factor-catalog.md) |
| 同域 | [仓库状态](data-warehouse.md) · [高维因子择时](high-dim-factor-timing.md) |
| ADR / concepts | [多重检验](../concepts/multiple-testing.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [参数与过拟合](parameters-and-hyperopt.md) · [实验框架](../reference/experiment-framework.md)
- **源码:** [`alpha/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/alpha) · [`experiment/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/experiment) · `qlib_lab/`
