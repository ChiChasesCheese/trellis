---
title: 'The Unified Factor Catalog: Raw Material vs Vetted Research'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/factor-catalog.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 统一因子目录:原料库 vs 研究面

> 前置阅读:[alpha 从哪来又为什么消失](where-alpha-comes-from.md)、
> [qlib 挖矿实验室](qlib-alpha-lab.md)、[数据层分层与自动化](data-layer-and-automation.md)、
> [公开 alpha 因子库](../reference/public-alpha-libraries.md)。
> 本页讲 2026-07-08 落地的**目录层**:多源如何归一、如何过闸、如何避免把
> 「两千个未测模板」误读成「两千个 alpha」。

## 先分清两层(否则目录是噪音)

| 层 | 含什么 | 文档站怎么对待 |
|---|---|---|
| **研究面** | scouted 种子 · vault · ledger 已过闸族 | 进 [因子目录快照](../live/factor-catalog.md)· ideas 讲解 |
| **battery / 公开 zoo 原料** | generator 窗口网格(~1k) · qlib158/360 · tsfresh · ta · Alpha101/191 | **不进 textbook 正文表**;全量只在 web `/reports/factor-zoo` 与 CSV 快照 |

**纪律**:条数不是成绩。generator 的 `reversal_5/10/20` 是同一机制的低熵变体;把它们和
「谁在另一边亏」的研究页并列,是信息熵污染。

## 为什么需要一个目录

到 2026 年中,仓库从多源积累实体:自研生成器模板、两套公共 alpha zoo、qlib 表达式、
网络蒸馏种子、手写 ledger 判决。格式各异。**同一个问题("我们试过什么?哪些活着?")
要翻多个地方。** 目录解决归一;判决仍只认 ledger。

`quant.alpha.catalog` 把它们归一成一个 `CatalogEntry` schema:

| 字段 | 含义 |
|---|---|
| `id` / `family` / `origin` | 唯一键 / 研究方向(与 ledger 的 family 同义)/ 来源(九选一) |
| `formula` / `mechanism` / `inputs` | 公式原文(qlib 表达式原样保留)/ 机制一句话 / 需要的原始面板 |
| `source` / `license` / `published` | 出处(实现库+论文)/ 许可证 / 发表时间 |
| `tags` | 风格分面(momentum/reversal/volatility/…),确定性关键词映射 |
| `status` / `sharpe` / `dsr_prob` / `n_runs` | join ledger 的诚实判决(按族取最优 run,与记分板同口径) |

两条设计纪律:**缺源如实报告**(`alphas` extra 没装时 ta_cn/ta/tsfresh 进
`skipped_sources`,绝不静默少一截),**每个上过闸的族都可浏览**(手写研究轮只存在于
ledger,就生成 `origin="ledger"` 行;`vault_<family>` 前缀被 join 看穿)。

## 九个源,一个注册面

| origin | 数量 | 接入方式 |
|---|---|---|
| generator | 1118 | `quant.alpha.generator` 机制族 x 窗口模板(含 pairwise 复合) |
| qlib_alpha360 / qlib_alpha158 | 360 / 158 | 隔离环境机器导出 JSON(`qlib_lab/scripts/export_expressions.py`),主环境零 pyqlib import |
| alpha191 / alpha101 | 191 / 101 | ta_cn(wukan1986,MIT)——社区实现,不重抄公式 |
| tsfresh | 193 | simple 计算器 x 参数网格,`fn = close.rolling(126).apply(...)` 真可算 |
| ta | 77 | bukosabino ta(MIT),函数 API 程序化枚举(必填参数 ⊆ OHLCV 即入选) |
| scouted | 68 | 网络蒸馏种子(`research/alpha2026_candidates.json` + `alpha_seeds_*.json`) |
| ledger | 55 | 手写研究轮的族(bab / fx_carry / capstone …) |

**不在上表:** Chen-Zimmermann OSAP(~212)——无一等公民 `load_osap` / catalog origin(票 `qs-aec` 确认暂不做;见 [公开 alpha 库](../reference/public-alpha-libraries.md))。

加第十个源的成本:一个 loader(`quant.alpha.library.load_*`,缺依赖 raise
ImportError 即可)或一个 JSON seam,catalog、API、前端全部自动收录。依赖判决也
记录在案:pandas-ta 在 numpy>=2 上依赖不可解析(已否决),ta 0.11 / tsfresh 0.21.2
实测兼容。

## 从目录到判决:两条 battery 管线

目录只是清单;判决来自既有的诚实漏斗(`vault.save_factor` →
`gate_vault_factor` → `run_experiment` 闸门 → ledger):

- **`research/library_battery.py`**(函数型指标池):IC 预筛(|IC|≥0.015@fwd5)后过闸;
  指标无先验方向,按样本内 IC 符号选向,所以 **n_trials = 2 x 池**——方向也是搜索,
  DSR 为整个搜索付费。`--market us.stock`(基线缓存)/ `cn.stock`(jqdata PIT,
  long-only + T+1/涨跌停约束,fornax 上跑)。
- **`research/seeds_battery.py`**(公式型种子池):公式自带方向,n_trials = 本轮
  扫描规模(扫 30 篇论文挑 3 条,为整个扫描-蒸馏付费)。

首轮判决与仓库既有定论逐位一致:US 大盘上 ta 77 指标 76 个连预筛都不过,唯一过筛的
keltner_channel_wband 裸 Sharpe 0.85 被 DSR@154 砍到 0.57 → REJECT;r2 种子三条全
REJECT,其中 10 日横截面趋势(+0.01)正好给 arXiv:2607.01550「短期趋势已死」盖章。
CN 轮(hs300+zz500 PIT,1840 名)更有意思:**39/77 过 IC 预筛**(IC 幅度最高 0.115,
证实 A 股才是价量指标的原生市场)**但过闸依然全 REJECT**——最好的 ATR/ADX 系
(long-only Sharpe 0.4-0.51)被无做空 + T+1/涨跌停 + DSR 联手拦下:**IC 有、书不赚**。
**目录的价值不在挖到金子,在于每一铲都有归档**——同方向的下一轮会被 family 累计
trials 诚实加价。

## 怎么看

- **Textbook / 文档站** `/live/factor-catalog/`:只渲染研究面 + 已过闸判决(构建钩子过滤原料)。
- **工作台** `/reports/factor-zoo`:全量原料表(筛选/排序/CSV),给 battery 用,不是成绩单。
- API:`GET /api/reports/factor-catalog` 与工作台同口径。

所有读取离线走基线缓存与 ledger,任何缺源降级 200。

## 持久化:实体 vs 判决的两种生命周期

`ta_cn`/`ta`/`tsfresh` 三个源需要装 `alphas` extra 才能枚举——但文档站的构建环境
(`uv run --extra docs mkdocs build`)和部分 web 部署主机**不装**这个 extra,现算会
漏掉这 556 个实体(2326 掉到 1770)。修法不是给构建环境也装上 alphas(那样每次加
一个可选依赖都要动 CI/Cloudflare 配置),而是把两种数据的生命周期拆开持久化:

- **实体**(公式/tags/出处)只在装齐 `alphas` extra 的主机上算一次,物化到
  `research/catalog/entries.csv` + `meta.json`(`research/export_catalog.py`,数据区,
  可直推 main)。没装 extra 的主机直接读这份 committed 快照,拿到全量九源。
- **判决**(status/Sharpe/dsr_prob)绝不进快照——ledger 每天有新 battery 结果入账,
  焊进快照会让文档站显示几天前的过期结论。读者(web 端点、mkdocs 构建钩子)统一走
  `quant.alpha.catalog.load_or_build_entries_table`(优先读快照,缺快照才现算实体)
  + `join_ledger_status`(永远现读 committed ledger),**每次读、每次现 join**。

一句话:重(依赖)而稳(结构不常变)的一半持久化,轻(依赖)而快(每天变)的一半
永远现算——两种数据不同的更新频率决定了两种不同的物化策略。

实现:`src/quant/alpha/catalog.py`(纯函数,测试
`tests/alpha/test_alpha_catalog.py` 即 spec);`research/export_catalog.py` 生成快照,
`research/README.md` 记着这条纪律;battery 脚本在 `research/` 下。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [数据层与自动化](data-layer-and-automation.md) · [qlib 挖矿实验室](qlib-alpha-lab.md) |
| 下游 | [高维因子择时](high-dim-factor-timing.md) · [因子风险](factor-risk-and-idiosyncratic-alpha.md) |
| 同域 | [catalog 总览](../catalog/index.md) · [能力速查](../reference/capabilities.md) |
| ADR / concepts | [领域模型](../concepts/domain-model.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [Web 研究台](../engineer/web-console-benchmarks.md)
- **源码:** [`alpha/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/alpha) · [`vault.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/vault.py)
