---
id: mlp-hm-fail-tech-debt
node: hm.failure
type: qa
step: 3
---
## Q
**技术债与自己的设计缺陷**｜经理面与行为面

“How do you decide what technical debt to pay down? Tell me about a flaw in your own design.”

## A
两问用同一组素材：说得出自己系统里最该还的债，以及你设计里真实出过的缺陷。

- **债一：六份偏移表。** Amex 管线的六个解析存储过程各自重复了同一张定长字段偏移表。你会改成一张配置表加一个通用解析函数，加第七种记录类型就是一行配置，不是一个新过程。这正是你后来在质检框架里用的做法。
- **缺陷二：表级放行。** 质检框架把“数据可读”放在表级，约 50 个持续失败的商户（约 4%）挡住 35,000 个。你自己发现后写了 ADR，比较四种方案，选“汇总行加逐商户失败行”：用等值连接，没有新表，已有一个数据域这样跑了 16 个月。
- **判断依据：** 先还会出事的债，不还只是难看的债；按风险调整后的价值排，不按沉没成本。
- **状态：** 框架和八个数据域的铺开已上线；商户级就绪度已设计、评审，并在一个数据域验证过，整体铺开排在净额结算之后。

**英文答法。**
- The debt I'd pay first: the **six parsers repeat one offset table six times**. I'd move offsets into a **config table** and write one generic parser; a seventh record type becomes a **config row**.
- A flaw in my own design: readiness was **per table**, so about **fifty bad merchants out of thirty-five thousand** could block everyone.
- I wrote an **ADR with four alternatives** and a **strictest-wins** correctness argument, so mixed deployments stay safe.
- Status: framework and **eight rollouts are live**; merchant-level is designed, reviewed, and proven for **one subject area**.

**追问。**
- **Why not store a VARIANT per merchant?** A secure view over a per-row UDF or VARIANT parse disables predicate pushdown, and VARIANT has a per-cell size ceiling; flat rows keep pruning.
- **What does strictest-wins mean?** The read checks table-level failure first, then merchant-level, so an unrefactored procedure just degrades to today's behaviour.
- **Why is the sparse model cheap?** Most checks pass, so only failures are stored.
