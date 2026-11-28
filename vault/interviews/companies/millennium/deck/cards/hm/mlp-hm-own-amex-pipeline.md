---
id: mlp-hm-own-amex-pipeline
node: hm.ownership
type: qa
step: 2
---
## Q
**从 stub 做成生产管线**｜经理面与行为面

“Tell me about something you owned end to end.”

## A
用 Amex 结算管线。它是你最有分量的一件事，从一张表的占位代码（stub）做到生产，再做了 18 个月加固。

- **背景：** American Express 是闭环网络，每天发一个专有的定宽对账文件，而不是像 Visa、Mastercard 那样近实时。所以 Amex 交易先放在待处理表，等文件确认结算后才算数（good-funds model，资金到账才入账）。
- **你的部分：** 接手时只有前任留下的一张表。拓扑、六个解析存储过程、两个校验函数、费用计算任务、急停开关、EU 扩展，都是你做的；最大的单个 PR 约 1,800 行就是它。
- **规模：** 一年处理几千万笔交易、数十亿美元。口播只说量级。
- **最自豪的设计：** 坏了的时候管线把错误记下来而不是丢掉。

**英文答法。**
- I inherited a **stub with one table** and owned the Amex settlement pipeline end to end, from the design doc to **eighteen months** of production hardening.
- A daily fixed-width file goes through `COPY INTO`, six **append-only Streams**, `MERGE` on a composite key, validation against pending transactions, then a fee **Task**.
- Every mismatch lands in an **error log instead of being dropped**; a feature flag keeps Amex off every other card path.
- It processes **tens of millions** of transactions a year, and it's the team's reference for onboarding a file-based settlement source.

**追问。**
- **What was specifically yours?** Everything from the topology onward, plus about a dozen hardening PRs and the design doc the team reviewed.
- **Why Streams and Tasks, not Airflow?** The file lands in Snowflake, so every step is a `MERGE` in a transaction and nothing leaves the account; the cost is thinner orchestration, so I built a task monitor and Datadog alerts.
- **What would you change?** The six parsers repeat one offset table; I'd make it a config table and one generic parser.
