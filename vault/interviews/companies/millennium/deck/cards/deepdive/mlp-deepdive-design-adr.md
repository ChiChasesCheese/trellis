---
id: mlp-deepdive-design-adr
node: deepdive.design
type: qa
step: 4
---
## Q
**质检框架的四方案对比**｜项目深挖

“You found a granularity flaw in your own framework. What alternatives did you consider, and why did you choose that one?”

## A
问题：就绪度是数据域级，一个商户的数据坏了，整张表对所有商户都不可读；生产里约 50 个持续失败的商户（约 4%）挡住 35,000 个。

- **方案 A：** VARIANT 列加逐行 UDF。安全视图（secure view）遇到逐行 UDF 或 VARIANT 解析会关闭谓词下推，五千万行的表不能这样跑，否决。
- **方案 B：** VARIANT 加 FLATTEN 中间视图。可接受，但 VARIANT 单元格有 16 MB 上限（约 98K 商户），否决。
- **方案 C：** 新建逐商户失败表。连接最优，但要新表和 Iceberg 同步的 stream 与 task，否决。
- **方案 D（选）：** 复用结果表，摊平成“汇总行加逐商户失败行”。平的列做等值连接，不加基础设施；已有一个数据域这样跑了 16 个月。
- **正确性：** strictest wins。读查询先判表级失败再判商户级失败，所以改造过和未改造的过程混跑永远安全，未改造的退化成今天的表级阻塞。
- **容量：** 96.4% 的检查一次通过，只存失败行，极端每月约 80 万行；若每商户每次都写一行，每天 240 万行。

**英文答法。**
- Readiness was per table: about **fifty bad merchants** blocked **thirty-five thousand**. I wrote an ADR with **four alternatives**.
- I rejected VARIANT with a per-row UDF because it **disables predicate pushdown**, and VARIANT has a **per-cell size ceiling**.
- I chose a **flat summary row plus per-merchant failure rows**: equality joins, **no new infrastructure**, and one subject area had run that way for **sixteen months**.
- Correctness is **strictest wins**, and failures are rare, so I store **only failures**.

**追问。**
- **Status?** The framework and eight rollouts are live; merchant-level is designed, reviewed and proven for one subject area, sequenced behind the net-settlement ramp.
