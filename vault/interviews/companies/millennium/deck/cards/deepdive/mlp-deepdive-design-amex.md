---
id: mlp-deepdive-design-amex
node: deepdive.design
type: qa
step: 2
---
## Q
**Amex 管线为什么这样设计**｜项目深挖

“Why Streams and Tasks instead of Airflow or Spark? What are the trade-offs, and how does it scale?”

## A
设计决定要成对说：做了什么、为什么、代价和怎么兜。

- **只追加 Stream 共六条：** 每种记录类型有独立偏移，互不阻塞。代价是偏移推进和业务写入不在同一个事务里，所以正确性靠下游 `MERGE` 的键，不靠 Stream。
- **幂等三层：** `COPY INTO` 文件级去重（`FORCE=FALSE` 加加载历史），每级 `MERGE` 键，校验函数记错不丢。文件会重投、任务会重跑，所以宁可重跑也不乐观假设一次跑对。
- **为什么不用 Airflow 或 Spark：** 文件本来就落在 Snowflake，解析、校验、计算都留在仓库里，每一步是事务里的 `MERGE`，数据不出账号；`SYSTEM$STREAM_HAS_DATA` 让任务在空输入时不启动仓库。代价是编排比 Airflow 弱：没有分支、没有外部回调，所以你自己补了 Streamlit 任务监控和 Datadog 告警。
- **双上游任务：** `AFTER A, B` 只保证两边各跑过一次，不保证同一批，所以用 `FULL OUTER JOIN` 兜底，错位的记录记一次错、下一轮自愈。
- **宽松解析：** `TRY_TO_DECIMAL` 让一个坏字符不炸整批；坏值变 NULL，要靠校验层抓。

**英文答法。**
- I chose **Streams and Tasks** because the file lands in Snowflake anyway: every step is a **`MERGE` inside a transaction** and **nothing leaves the account**.
- `SYSTEM$STREAM_HAS_DATA` gates each task, so we **never spin up a warehouse on empty input**.
- The trade-off is **weaker orchestration** than Airflow, so I built a **Streamlit task monitor** and **Datadog alerts**.
- **Append-only streams** give each record type its own offset; correctness comes from the **composite-key `MERGE`**, not from the stream.

**追问。**
- **Where does the platform hurt?** Stream staleness is silent and task-level observability is thin; that is why I built health-check procedures and alerts on top.
