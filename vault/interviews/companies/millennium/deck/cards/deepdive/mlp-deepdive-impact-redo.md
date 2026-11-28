---
id: mlp-deepdive-impact-redo
node: deepdive.impact
type: qa
step: 3
---
## Q
**重做一次会改什么**｜项目深挖

“What would you do differently?”

## A
每个项目都要有一个具体的“我会改”，而且是从缺陷里学到的，不是客套。

- **Amex 管线：** 六个解析过程重复同一张字段偏移表六次。改成一张偏移配置表加一个通用的定长解析函数，加第七种记录类型就是一行配置。这正是后来质检框架用的做法。
- **质检框架：** 第一版就应该做商户级就绪度，不是表级；表级让约 50 个坏商户挡住 35,000 个。
- **Quant-Stroller：** 更早做成本模型校准；因子目录的元数据放进 DuckDB，而不是 YAML。
- **interchange 切换：** 窗口化 `ON` 的代价是隔一个月以上重处理的记录绕过去重，这是写在注释里的敞口，你知道它在哪。

**英文答法。**
- In the Amex pipeline, the **six parsers repeat one offset table**; I'd move offsets into a **config table** with **one generic fixed-width parser**.
- In the quality framework I'd have built **merchant-level readiness** from day one, not table-level.
- In Quant-Stroller I'd **calibrate the cost model earlier** and keep the factor catalog's metadata in **DuckDB** instead of YAML.
- Each of these is a real flaw I found by running the thing.

**追问。**
- **What about the interchange window?** A record reprocessed after more than a month bypasses dedup; it's documented next to the clause.
