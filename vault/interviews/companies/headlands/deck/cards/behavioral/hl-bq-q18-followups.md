---
id: hl-bq-q18-followups
node: behavioral.question-bank
type: qa
step: 38
---
## Q
"最大的系统"之后的追问：为什么不用 Airflow 或 Spark？是 exactly-once 吗？两个上游任务不同步怎么办？
Why not Airflow or Spark? Exactly-once? Two upstream tasks out of step?

## A
- **Why not Airflow or Spark?** **数据本地性**，且步骤在仓库里是**事务性**的；代价是**编排较弱**，所以我在上面自建了监控。
- **Exactly-once?** 不是；**至少一次 + 幂等写入**，效果上等于一次。
- **Two upstream tasks out of step?** `AFTER A, B` 保证两者都跑过，但不保证是**同一批**；不匹配的进**错误日志**，下一轮**自愈**。
