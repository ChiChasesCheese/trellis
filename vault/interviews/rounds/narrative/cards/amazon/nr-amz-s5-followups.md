---
id: nr-amz-s5-followups
node: amazon.s5
type: qa
step: 3
---
## Q
【Net Settlement · interchange 数据源切换（技术决策 + 零回归迁移）】面试官会追问什么？每个怎么答？

## A
- **What's the trade-off of the time window?**
    - 同一记录**超过一个月**才重处理时绕开去重
    - 可解释、**写在注释里**的风险；换**扫描量恒定**
- **Why not dual-write?**
    - 两个 task 被**同一 toggle 反向控制** = 互斥；没有显式互斥的 dual-write 就是重复收费
- **What would have made you not switch?**
    - 见待补
- **How did you handle the 0.224% difference?**
    - 是记录数差异，一侧多 **30,760 行**；构成见待补
- **Postgres vs Snowflake?**
    - 定价计划在 **Postgres**：OLTP、费率 system of record、唯一约束、header + N 行费用**原子写**
    - **Snowflake** 做数十亿行聚合；应用层**幂等 upsert** 同步，冲突以 `FAILED_PRECONDITION` 暴露
- **Who else was involved?**
    - **定价服务**、**结算平台**、**出款服务**、**收单行**；对齐靠数据契约与信任
- **Did the toggle ever get flipped back?**
    - 一次 migration 里 **prod 关、preprod 开**；灰度执行细节无记录，不编
