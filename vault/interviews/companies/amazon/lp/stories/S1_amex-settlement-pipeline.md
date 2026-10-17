# S1 · Amex 结算管线（端到端 owner）

**I inherited a one-table stub and ran the Amex settlement pipeline end to end for eighteen months.**

## 适用 LP

- 主：**Ownership**、**Deliver Results**
- 副：Dive Deep、Insist on the Highest Standards、Invent and Simplify、Frugality

## 数字

- **~22M** Amex 交易，前六个月：说 "about twenty-two million transactions in the first six months"
- **18 个月**生产运行
- 任期内最大单个 PR **~1,800 行**
- **十几个**加固 PR：说 "about a dozen"
- 不口播具体美元金额
- 【待补：对齐本管线美元量级的最终口径；简历写 "$600B+ annual transaction volume"，与 22M 笔相差两个数量级，Dive Deep 追问「怎么算的」前必须统一：是 Braintree 全量 TPV 还是 Amex 管线？】

## S / T / A / R / L

### S
- **Braintree** 费用平台，跑在 **Snowflake** 上；Visa / Mastercard 走收单方近实时视图
- **Amex** 是闭环：**每天一个定宽文件**，文件确认结算前不能入账

### T
- 我 **owner** 整条管线，从设计文档到生产；接手时只有**一张表的 stub**
- 输出喂给**费用计算和出款**

### A
- 设计 **6 条 append-only stream**，每种记录类型一条，各有独立 **offset**，互不阻塞
- 每个阶段用**复合键 MERGE**，重发文件不会 **double-count**
- 两个**校验函数**，所有不匹配进 **error log**，不丢弃
- 一个 **feature flag** 当 **kill switch**，一条 `UPDATE`，无需发布
- 一直 **on-call**，真实故障后上了**十几个加固 PR**

### R
- 前六个月 **~22M** 笔 Amex 交易；生产 **18 个月**
- 任期内最大 PR，**~1,800 行**

### L
- 坏了的时候，它**记录问题而不是丢数据**

## 追问与回答

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
  - 不说 "no accidents"；设计目标是**坏了就记录**；S3 的 ACH 事故在下游，我拥有那次 RCA

## 换个 LP 讲

- **Ownership**：stub → 设计 → 上线 → 18 个月 on-call；kill switch；EU 扩展不是别人派的；别说成「团队做的」
- **Deliver Results**：22M 笔、最大单 PR、可急停、EU 扩展；不说美元数字
- **Dive Deep**：迟到文件靠读 load history 而不是看板；拒付标志复合键
- **Insist on the Highest Standards**：if it breaks, it must record, never drop；三层正确性；别声称 "no bugs"
- **Invent and Simplify**：一个 flag 把 Amex 从其他卡组织路径分流，一条 UPDATE 急停；会改成配置表 + 通用解析
- **Frugality**：stream-has-data 检查避免空文件起 warehouse；没有成本数字，别编

## 待补

- 【待补：设计文档评审人数/周期（只说角色，不说姓名）】
- 【待补：业务影响的客户侧数字（商户数、出款金额）】
- 【待补：是否有第二个文件型结算源按这套模式接入、谁接的？有 → 说 "someone else onboarded X using my pattern without me"；没有 → 不说 "reference implementation"】
- 【待补：设计评审里资深同事/他团队提出过什么反对意见，你怎么回应、是否改了设计（Have Backbone 素材）】
- 【待补：EU 扩展是独立做的，还是需要说服另一个团队/合规方】
- 【待补：on-call 里其他人靠你写的 runbook / Streamlit 监控处理过事故吗】

<details><summary>逐字稿</summary>

> The project I'm proudest of is the American Express settlement pipeline on our Snowflake-based fee platform at Braintree. Amex is a closed-loop network: instead of the near-real-time views we get from our acquirer for Visa and Mastercard, it sends one fixed-width reconciliation file a day. So we can't book an Amex transaction until that file confirms it settled.
>
> I inherited a stub with a single table and owned the pipeline from the design doc through eighteen months of production. I made three design calls. First, six append-only streams, one per record type, so each has its own offset and none blocks the others. Second, a composite-key `MERGE` at every stage, so a re-delivered file or a re-run task can't double-count. Third, two validation functions that send every mismatch to an error log instead of dropping it, and a single feature flag that doubles as a kill switch, so I could stop it with one `UPDATE`, no deploy.
>
> Because I was on-call for it, I shipped about a dozen hardening PRs after real failures. It processed about twenty-two million Amex transactions in its first six months, and it's the largest change I've merged — around 1,800 lines. The part I'm proudest of: when it breaks, it records the problem instead of losing data.

</details>
