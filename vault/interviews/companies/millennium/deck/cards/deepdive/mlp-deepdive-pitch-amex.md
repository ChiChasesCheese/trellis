---
id: mlp-deepdive-pitch-amex
node: deepdive.pitch
type: qa
step: 2
---
## Q
**怎么讲 Amex 结算管线**｜项目深挖

“Walk me through the Amex settlement pipeline end to end.”

## A
面试官更想听生产系统时用它。先讲为什么特殊，再讲机制，再讲你的决定。

- **为什么特殊：** American Express 是闭环网络，不像 Visa、Mastercard 有近实时的结算视图，而是每天一个专有定宽对账文件。所以 Amex 交易不能乐观入账，要先在待处理表里等文件确认，这是 good-funds model。
- **机制：** 定时任务（Snowflake Task）把 S3 上的文件 `COPY INTO` 到暂存表，一行一条记录；六条只追加的 Stream 按记录类型分流；六个存储过程用 `SUBSTRING` 按偏移切字段，按复合键 `MERGE` 进类型化表；两个校验函数用 `FULL OUTER JOIN` 对待处理交易，不匹配的写进错误日志；下游任务有两个上游依赖，在一个显式事务里算手续费，再把聚合交给出款服务。
- **你的决定：** 只追加 Stream 让各类型独立前进；`COPY INTO` 文件级去重加每级 `MERGE` 键，保证重试幂等；一个功能开关把 Amex 摘成独立流，不碰其他卡网络。
- **量级：** 一年几千万笔、数十亿美元；18 个月生产。

**英文答法。**
- Amex is a **closed-loop network**: it sends one **fixed-width reconciliation file** a day, so we can't book a transaction until the file confirms it settled — our **good-funds model**.
- I owned the pipeline **end to end**: `COPY INTO` into staging, **six append-only Streams** by record type, `MERGE` on a composite key, validation that logs every mismatch instead of dropping it, then a **fee Task** with two upstream dependencies.
- Decisions: independent offsets per record type, **idempotent at every stage**, and one **feature flag** so Amex never touches other networks' code path.
- It handles **tens of millions** of transactions a year and is the team's reference for file-based sources.

**5 分钟展开。**
- **0:00 背景：** 为什么不能乐观入账。
- **1:00 机制：** 沿数据流走一遍六步。
- **2:30 取舍：** Streams 加 Tasks 对 Airflow；幂等三层。
- **3:45 出过什么事：** 文件落进昨天的目录；同一笔交易先结算后拒付。
- **4:30 重做：** 六份偏移表改成配置加通用解析函数。

**追问。**
- **Your part?** I inherited a one-table stub; everything from the topology onward is mine, including the design doc.
- **How big?** The biggest single PR in my tenure, about 1,800 lines.
