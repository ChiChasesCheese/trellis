---
id: mlp-deepdive-pitch-quality
node: deepdive.pitch
type: qa
step: 4
---
## Q
**怎么讲质检框架**｜项目深挖

“Tell me about something you built that other people build on.”

## A
这是“平台化”的项目：别人往上接，而不是你自己用。适合讲你怎么把重复劳动变成配置，以及你怎么发现并修自己设计的缺陷。

- **背景：** 团队有几十张对账表，每张新表都手写一个校验任务。
- **三块：** 一张契约配置表，一行是（数据域，校验）：存储过程名、日期列、以小时计的 SLA、JSON 参数；一个通用执行器，用 `EXECUTE IMMEDIATE` 拼调用，用 `RESULT_SCAN` 取结果，归一成 PASS、FAIL、WARNING，崩溃也转成一条 FAIL；一个 trigger-status 状态机，某数据域当日所有启用的校验都通过就置为 `Completed`，该行复制到共享层，下游 `JOIN` 它。
- **结果：** “数据能不能读”从 Slack 约定变成 SQL 条件；加一条校验从“写任务、评审、部署”变成插入一行配置。你自己铺开了八个数据域，框架 PR 约 1,500 行。
- **后续：** 发现粒度缺陷后写 ADR，把就绪度降到商户级。

**英文答法。**
- The team had **dozens of reconciliation tables**, each with its own hand-written validation task. I built a **config-driven quality-check framework**.
- A **contract config table**, a generic executor using `EXECUTE IMMEDIATE` and `RESULT_SCAN`, and a **trigger-status state machine** replicated to a share layer that downstream consumers `JOIN` on.
- "Is this data safe to read" became **a join condition, not a Slack convention**; adding a check became **inserting a config row**.
- I rolled it across about **eight subject areas** myself.

**5 分钟展开。**
- **0:00 痛点：** 每张表一个手写校验。
- **1:00 三块机制。**
- **2:30 为什么用状态表：** 消费者在不同库甚至不同账号，复制一行状态是最低公共约定，任务依赖跨不过去。
- **3:30 缺陷与 ADR：** 表级放行，约 50 个坏商户挡 35,000 个。
- **4:30 状态：** 框架与八次铺开已上线，商户级已设计并在一个数据域验证。

**追问。**
- **Why dynamic SQL?** It's the price of config-driven; the config is engineer-controlled, so injection isn't the threat model; the cost is no static checking, mitigated by the exception handler and a health check on the results table.
