---
id: nr-amz-s1-followups
node: amazon.s1
type: qa
step: 3
---
## Q
【Amex 结算管线（端到端 owner）】面试官会追问什么？每个怎么答？

## A
- **What exactly was yours vs. the team's?**
    - 从 **stub** 起全部设计是我的；写了团队评审的**设计文档**；最大 PR ~1,800 行
    - 不说迁了 Funding 的 Ruby 脚本：我做的是接收侧 **Snowflake-native** 替代
- **Why Streams/Tasks, not Airflow or Spark?**
    - **数据局部性** + 事务性 `MERGE` + `STREAM_HAS_DATA` 空输入不开 warehouse
    - 代价是**编排弱**；补 **Streamlit 监控** + **Datadog 告警**
- **How do you know it's correct?**
    - **行级**：`TRY_TO_DECIMAL/DATE`，坏字段不炸整批
    - **批级**：每笔结算交易都有费用
    - **对账级**：费用总额对 Amex 汇总记录，不一致**停 task、page on-call**
- **What broke?**
    - **迟到文件**：Amex 把文件丢进昨天的目录 → 改 `PATTERN` 扫所有日期目录 + load history 去重
    - **拒付标志**：引出复合键（reference number + reject indicator）
- **What would you do differently?**
    - **偏移配置表** + 一个通用定宽解析；新增第七种记录 = 加一行配置
    - 后来在 quality-check 框架里做了同样的模式
- **How does the AFTER A,B dual-upstream task stay consistent?**
    - `AFTER` 只保证各跑过一次，不保证同一批；**FULL OUTER JOIN** 兜底，错位记一次错误，**下一轮自愈**
- **Did you ever lose or double-count money?**
    - 不说 "no accidents"；设计目标是**坏了就记录**；「ACH 费用 NULL 事故」 的 ACH 事故在下游，我拥有那次 RCA
