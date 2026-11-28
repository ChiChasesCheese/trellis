---
id: mlp-deepdive-design-quant
node: deepdive.design
type: qa
step: 1
---
## Q
**Quant-Stroller 的架构与技术栈**｜项目深挖

“Walk me through the tech stack and why each piece. How are the modules related? What was your storage strategy?”

## A
每个选择都要给一句“为什么”，而且说出替代方案。

- **接缝：** DataSource、Factor、Strategy、Broker 四个窄接口。数据面是 raw 到 bars 到 panel；账本（ledger）只追加，不改。
- **DuckDB 加 Parquet：** 列存、本地、零运维；Parquet 按市场和日期分区，DuckDB 做谓词下推。不用 Postgres，因为列存加本地 Parquet 扫描比行存快一个量级，而且不用运维。
- **NautilusTrader：** 要的是撮合和成本模型，不是重写引擎，所以用现成的。
- **PyTorch：** 因子模型训练，在 8 卡服务器上，自托管 CI。
- **FastAPI 加 React：** 研究台；**Prefect：** 调度。
- **并发：** 数据拉取用 asyncio 加信号量限制并发，训练用多进程；不混用，因为一个是 I/O 密集，一个是 CPU 密集。
- **为什么不用全内存 pandas：** 面板太大，DuckDB 可以把谓词下推。

**英文答法。**
- **DataSource, Factor, Strategy, Broker** are four narrow seams; the data plane goes **raw, bars, panel**, and the experiment ledger is **append-only**.
- **DuckDB over Parquet**: columnar, local and zero-ops, partitioned by market and date, with predicate pushdown; Postgres would be row storage and more to run.
- **NautilusTrader** because I wanted its **matching and cost models**, not to rewrite an engine.
- Async for data pulls with a **semaphore** for concurrency limits; **multiprocessing** for training; I don't mix them.

**追问。**
- **Why not plain pandas?** The panel is too big for memory; DuckDB pushes the predicates down.
- **Why a ledger that never changes?** Experiments are evidence; 340-plus runs must stay auditable.
