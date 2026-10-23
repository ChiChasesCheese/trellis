---
id: hl-bs-s1-followups-a
node: behavioral.stories
type: qa
step: 13
---
## Q
被追问结算管线 S1：具体哪部分是你的？为什么不用 Airflow 或 Spark？怎么保证没有重复也没有丢手续费？是 exactly-once 吗？
What exactly was yours? Why not Airflow or Spark? Exactly-once?

## A
- **What exactly was yours?** 从**拓扑**往后的一切，约一打加固 PR；**最大的 PR** 就是这条管线。
- **Why not Airflow or Spark?** **数据本地性**，且步骤在仓库里是**事务性**的；代价是**编排较弱**，所以我在上面建了监控。
- **No duplicate, no lost fee?** 每个阶段**幂等**；被拒的记录**保留**。
- **Exactly-once?** 不是；**至少一次 + 幂等写入**，效果上等于一次。
