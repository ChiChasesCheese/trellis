---
title: 'The Data Pipeline: Raw, Bars, Panel'
source: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/data-pipeline.md
codebase: quant-stroller
clipped: c0cc39c68d33
---

# 数据管线:raw → bars → panel

本仓的市场数据走三段。用**名词**命名(不再用 "lake" 或 L0/L1/L2 "layer" —— 见
[ADR-0002](../adr/0002-data-stages-raw-bars-panel-not-lake-layers.md)、根目录 `CONTEXT.md`)。

## 三段

| 段 | 是什么 | 物理性 | 代码 |
|---|---|---|---|
| **raw** | vendor 原样归档,`<root>/raw/<vendor>/…`,只进不改 | **唯一物化实体**(真 parquet) | `scripts/eodhd_archive.py` 写;`data/raw.py` 读(EODHD) |
| **bars** | 单标的规范复权序列 `[ts,ohlcv]`,UTC、去重 | 逻辑视图(读时现算) | `raw_bars` / 各 vendor 的 `DataSource.fetch_bars` |
| **panel** | 对齐 date×code 横截面 + PIT 掩码 + 清洗 | 逻辑视图(读时现算) | `ohlcv_panels(market, …)` / `UniversePanel` |

- **raw 是实体,bars/panel 是它的读时视图**(schema-on-read,不落盘)。改复权/掩码逻辑立刻对全历史生效,不存两份漂移数据。
- **bars 是 vendor-agnostic 汇合点**:过了它,下游不再关心数据来自哪家 vendor。
- **panel 按 market 分派**(US 叠 S&P500 PIT 掩码、CN 叠指数成分、FX/crypto 固定篮子无掩码)——不是按 vendor。
- 研究/回测**只准碰 bars/panel**,绝不直接开 raw 文件(`test_layer_discipline` AST 强制)。

## vendor 分派(加一个数据源怎么做)

fornax 是唯一 source of truth;每个 vendor 是一个 **raw 后端**:

```
market → vendor 后端 (raw 分区 + adapter)
  us/fx/crypto → eodhd  (raw/eodhd/…,  data/raw.py + sources/raw_src.py)
  cn.stock     → jqdata (~/dataset/cn_stock, sources/cn_stock_src.py + cn_ashare.py)
  crypto.perp  → ccxt   (无 raw 现货序列)
```

**加一个新 vendor / 数据轴**(期货、期权、北向……)三步:

1. **归档进 raw**:archiver 把 vendor 原样字节写到 `<root>/raw/<vendor>/…`(参照 `scripts/eodhd_archive.py`)。**raw 契约**=不改名/不处理时区/不复权。
2. **写 adapter**(raw→bars 归一化):实现 `DataSource.fetch_bars` 或一个 `*_bars(...)` reader,把该 vendor 的 raw 派生成规范 `[ts,ohlcv]`。这是四大 ABC 里 `DataSource` 的职责——每 vendor 各自的复权/清洗逻辑住这。
3. **接进分派**:
   - 单标的 bars → 在 `config/markets/<m>.yaml` 声明 `data.source: <name>`,并在 `data/ingest.py::_SOURCE_BUILDERS` 加一个 `<name> → 工厂`。换某市场的源 = 改 yaml 一行(开闭原则)。
   - 横截面 panel → 在 `data/panel.py::ohlcv_panels` 的 market 分派里加该 market 的组装(PIT 掩码等)。

**OpenBB 例外通道(2026-07-18)**:新 vendor **第一选项**仍是薄
`OpenBBSource(provider=...)`(采集层重合),物化前缀 `raw/openbb/<provider>/`,且**不得**改默认
`data.source: raw`。详见[OpenBB 接入](openbb-integration.md)。存量 EODHD/jqdata/ccxt/EDGAR
不迁移。

**默认源纪律**:us/fx/crypto 的默认是 `source: raw`(`RawSource`)——只读 fornax raw store,**off-host 抛 `RawUnavailableError`**(fail loud,不静默降级 vendor)。EODHD/CCXT/Yahoo 都是**显式 opt-in**(CI 的 `ensure_remote_baseline`、archiver、`--exchange` 逃生口、执行券商),不是默认。所以 local/CI 够不到 fornax 时明确报错,不偷偷直连 vendor。

## 旧名 → 新名对照(port 旧分支用)

在 refactor 之前建的分支(如跨资产 loaders)rebase 后按此改:

| 旧 | 新 |
|---|---|
| quant.data.lake(模块,已删) | `quant.data.raw` |
| `lake_bars` / `lake_root` / `lake_has_exchange` / `lake_universe` / `lake_ohlcv_panels` | `raw_bars` / `raw_root` / `raw_has_exchange` / `raw_universe` / `raw_ohlcv_panels` |
| `LakeSource` / `LakeUnavailableError` | `RawSource` / `RawUnavailableError` |
| sources/lake_src.py | `sources/raw_src.py` |
| `QUANT_LAKE_ROOT`(env) | `QUANT_RAW_ROOT` |
| `data.source: lake`(yaml) / `_SOURCE_BUILDERS["lake"]` | `data.source: raw` / `_SOURCE_BUILDERS["raw"]` |
| polymarket `lake_markets` / `lake_prices`(polymarket/lake.py) | `raw_markets` / `raw_prices`(`polymarket/raw.py`) |
| 术语 "L0 / L1 / L2 / layer / lake" | "raw / bars / panel" |

**物理目录 `~/workspace/zc/data_lake` 暂不改名**:fornax 上有实时 archiver 在写 + 已落 raw 数据,改目录是一条需在 fornax 协调的 ops 步骤(改目录 + archiver 默认根),不在代码内。env 变量已改为 `QUANT_RAW_ROOT`(旧变量此前未在任何主机设置,默认路径照旧,零破坏)。

## 相关页面

| 方向 | 页面 |
|---|---|
| 上游 | [2 · 数据面](../architecture/data-flow.md) · [ADR-0002](../adr/0002-data-stages-raw-bars-panel-not-lake-layers.md) |
| 下游 | [数据治理](data-governance.md) · [仓库状态](data-warehouse.md) |
| 同域 | [OpenBB 接入](openbb-integration.md) · [数据层与自动化](data-layer-and-automation.md) |
| ADR / concepts | [架构与数据流](../concepts/architecture-and-data-flow.md) |

## 深入阅读 / 学习 / 拓展

- **站内:** [能力速查](../reference/capabilities.md) · [入职](../engineer/index.md)
- **源码:** [`data/raw.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/data/raw.py) · [`data/panel.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/data/panel.py) · [`data/ingest.py`](https://github.com/ChiChasesCheese/Quant-Stroller/blob/main/src/quant/data/ingest.py) · 纪律测 `tests/data/test_layer_discipline.py`
