---
title: 'Data Governance: Contracts, Catalog, and Health'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-governance.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 数据治理:契约、目录与健康状态

> 一句话:**读 `config/data_contracts/` 就知道每个数据集是什么、能假设什么;跑
> `scripts/data_contract_scan.py` 就知道它现在还符不符合声明。** 前者是声明,后者是体检。

一个策略号称的 alpha,很多其实是数据假象——除息缺口被当成暴跌、拆分日的幻影亏损、
幸存者偏差、把发布前的财报泄漏进回测。标准对冲基金 / 金融数据管线用**数据契约
(data contract)** 把这类问题挡在源头:每个数据集有一份声明,写清它的 schema、
覆盖区间、更新频率、复权/时区约定、PIT 正确性、以及"什么算合法"。这一页讲我们怎么
落地这套东西。

## 标准做法:五件套

生产级金融数据栈围绕五件事组织,核心是**契约**(数据生产者与消费者之间的 API):

| 件 | 回答什么 | 我们在哪 |
|---|---|---|
| **Data Contract** | 这个数据集是什么、能假设什么(schema/覆盖/复权/PIT/合法判据) | `config/data_contracts/<id>.yaml` |
| **Catalog / 数据字典** | 一共有哪些数据集,一个地方查全 | `quant data-contracts`(读上面那批 YAML) |
| **Freshness & Quality 监控** | 现实还符不符合声明(新鲜/陈旧、PASS/WARN/FAIL) | `scripts/data_contract_scan.py` → `research/data_status.md` |
| **Lineage 血缘** | 数据从哪来、怎么变形到可研究 | raw→bars→panel([ADR-0002](../adr/0002-data-stages-raw-bars-panel-not-lake-layers.md)、[数据管线](data-pipeline.md)) |
| **PIT 正确性** | 有没有前视(用了当时还看不到的值) | 契约 `pit:` 字段 + `quant.data.health.pit_violations` |

我们早就有**检查原语**——`quant.data.quality.audit_bars`(单序列质量闸:schema/OHLC/
样本量/日历缺口/staleness/异常值/幸存者)和 `quant.data.health`(跨源复权对账、
`^TNX×10` 类缩放 bug、schema 漂移、PIT 前视、全 store 扫描)。缺的是把它们**绑定到每个
真实数据集的声明层**。数据契约就是那一层。

## 一份契约长什么样

`config/data_contracts/cn_price.yaml`(A 股日线,系统里最深整合的源之一):

```yaml
id: cn.price
source: jqdata
stage: raw                 # raw / bars / panel —— 见 data-pipeline.md
path: daily/price/{code}.parquet
grain: code x date         # 主键
schema:                    # 列 -> 粗粒度类型(float/int/object/datetime/bool)
  date: datetime
  close: float
  pre_close: float
  paused: float
  factor: float
coverage: {start: '2005-01-04', end: rolling}   # end=rolling 表示活数据集
cadence: daily
freshness_sla_days: 45     # 最后一条最多能落后 asof 多少天,超了 = FAIL
adjustment: pre_close total-return (factor=1.0 no-op; close/pre_close-1 是真收益)
timezone: Asia/Shanghai
pit: true                  # point-in-time 正确、无前视
legality: {min_rows: 200, min_years: 1}         # 合法判据阈值
provenance: jqdata export, 每个 .XSHE/.XSHG 一个 parquet(5511 只)
owner: cn-data
notes: A 股 bars 源(CNStockSource)。paused 日必须丢;raw close.pct_change() 会把除息
  缺口记成暴跌 —— 用 pre_close。
```

`notes` 和 `adjustment` 是"给未来的自己/agent 的话":**用错这个数据集的典型翻车方式**
写在这里,一读就避开。

## 两个入口

**声明(永远可用、离线):**

```bash
uv run quant data-contracts              # 全目录一览:id/source/stage/PIT/SLA/覆盖
uv run quant data-contracts --id cn.price   # 单个契约完整 JSON
uv run quant data-contracts --json          # 整个目录 JSON(agent 直接读)
```

**健康(需要数据,所以在 fornax 跑):**

```bash
CN_DATASET=~/dataset/cn_stock PYTHONPATH=src \
  ~/miniconda3/envs/zc/bin/python scripts/data_contract_scan.py
```

它对每个契约抽一个真实文件,用 `validate_contract` **拿现实对账它自己的声明**,产出
`research/data_status.md`(+ `.json`)。校验复用 `Check`/`Severity` 词汇,所以一份契约
verdict 读起来和质量报告一模一样。

## 校验做哪些检查

`quant.data.contract.validate_contract(contract, df, *, asof, check_coverage_start)`:

1. **schema** —— 声明的列都在吗?dtype 类型对得上吗?缺列 = **FAIL**;类型漂移 = **WARN**。
2. **min_rows** —— 行数够 `legality.min_rows` 吗?不够 = **FAIL**。
3. **coverage_start** —— 抽样是否回溯到声明的 `start`(留一年余量)?晚太多 = **WARN**。
   多文件/多标的数据集抽单个分区时**跳过**这项(单个 code 的上市日说明不了全集覆盖)。
4. **freshness** —— 仅 `end: rolling` 且给了 `asof`:最后一条落后 `asof` 超过
   `freshness_sla_days` = **FAIL**(陈旧)。冻结数据集(`freshness_sla_days: null`)不查。

## 当前健康(2026-07-13 fornax 实扫)

29 个非模板契约,**全部抽样命中,大部分 OK**。建这套系统时它当场抓到 5 处真实错配并修掉(契约 path 指向了元数据表而非日频表、year-分区采样采到最早年份误报陈旧、commodities 的 date 是索引而非列)——这正是契约的价值:
**声明与现实的偏差会立刻现形**,而不是等某个策略悄悄吃了脏数据。

完整快照见 [`research/data_status.md`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/research/data_status.md)。冻结/特例值得知道:

- `cn.northbound_hold` —— **冻结**:交易所 2024-08-16 停了陆股通每日实时披露,`end` 是定值不是 rolling。
- `fx.rates` / `crypto.prices` —— 价格面板完整,但 **carry(利率差)/ 链上(TVL/funding)缺失**——
  那是该资产类的头号 alpha 输入,开放项见 `bd ready`(勿写退役的 `research/backlog/*.md`),不是面板缺陷。
- `xa.cn_options` —— WARN:日频表 `date` 存成 object 字符串(该是 datetime),小 hygiene 提示。

## 加一个新数据集

1. 复制 `config/data_contracts/_TEMPLATE.yaml` → `<id>.yaml`,填真值(schema/coverage 从真实文件抽,
   别拍脑袋;`adjustment`/`pit`/`notes` 是策展知识)。
2. `uv run quant data-contracts` 确认它进了目录、字段无误。
3. 在 fornax 跑 `scripts/data_contract_scan.py`,看它 PASS;不 PASS 说明**声明和现实对不上**——
   要么改契约(声明错了),要么这数据集真有问题(该修数据)。契约的作用就是逼这个二选一显式化。

契约放 git(声明是 canonical 共享知识);数据本身绝不进 git(见
[数据管线](data-pipeline.md) 的 raw→bars→panel 与 gitignore 约定)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [数据管线](data-pipeline.md) · [ADR-0002](../adr/0002-data-stages-raw-bars-panel-not-lake-layers.md) |
| 下游 | [仓库状态](data-warehouse.md) · [OpenBB 接入](openbb-integration.md) |
| 同域 | [数据层与自动化](data-layer-and-automation.md) · [2 · 数据面](../architecture/data-flow.md) |
| ADR / concepts | [架构与数据流](../concepts/architecture-and-data-flow.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [能力速查](../reference/capabilities.md)
- **源码:** [`data/contract/`](https://github.com/ChiChasesCheese/Quant-Stroller/tree/main/src/quant/data/contract) · [`data/quality.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/data/quality.py) · `config/data_contracts/` · CLI `quant data-contracts`
