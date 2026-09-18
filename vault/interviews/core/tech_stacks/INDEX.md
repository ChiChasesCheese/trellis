---
title: Tech Stacks · 十个技术栈总表
aliases:
  - Tech Stacks
  - 技术栈总表
  - TS
tags:
  - interview/stack
  - moc
---

# Tech Stacks — 十个技术栈总表

面试官不按学科、不按轮次提问，他们照着 JD 上的词提问："讲讲你的 Kafka 经验"、"你们怎么做灰度发布"。这里一个栈一份，每份自包含：来龙去脉 → 我们这套系统怎么用它 → 我做了哪部分 → 追问与答法 → 我的边界。

## 怎么用

临考前按 JD 上出现的词挑几份读。每份的 `## 0` 节直接说这个栈在 JD 里通常在问什么,`## 4` 节是追问和答法,`## 5` 节是边界 —— 不会的东西提前想好怎么说。



## 每份文件的结构

| 节 | 内容 |
|---|---|
| `## 0` | 这个栈在 JD 里到底在问什么 |
| `## 1` | **来龙去脉** —— 它出现前人们怎么做、痛在哪、核心抽象、关键权衡、演化到今天。教科书级,零前置知识可读 |
| `## 2` | **在我们这套系统里它怎么用** —— 架构位置、关键 feature 与设计决策及其意图。这是 repo 全貌,不只是我的贡献;我个人做的部分在 `2.x` 单独标 `[me]` |
| `## 3` | stripe kit 考到的对应知识点 |
| `## 4` | 常见追问与答法,含第三层深挖(怎么会坏、边界在哪) |
| `## 5` | 我的边界 —— 不会的就说不会,提前想好措辞 |
| `## 6` | 往深里看:知识层入口 |


> 按 JD 上出现的词挑着读。每份自包含，读一份够说一轮。
> 证据与口播稿在故事笔记：[[S1]] … [[S11]]（每篇 frontmatter 的 `stories:` 列出对应故事）。

---

## 一屏总表

| # | 栈 | 一句话 | 我的底气 | 知识层 |
|---|---|---|---|---|
| 01 | [[01-system-design\|TS01 系统设计]] | 三服务支付清结算流水线，三条接缝各有取舍 | **强** — 主战场，86 PR | `system-design` 9 节点 |
| 02 | [[02-kafka-event-streaming\|Kafka / 事件流]] | 消费侧与 CDC 管道，非 broker 运维 | 中 — 消费者视角 | `kafka` + `system-design` 13 节点 |
| 03 | [[03-snowflake-warehouse\|Snowflake / 数据仓库]] | 生产级 Snowflake 应用：stream + task + 存储过程 | **最强** — 三年主场 | `snowflake` + `system-design` 11 节点 |
| 04 | [[04-terraform-iac\|Terraform / IaC]] | 用 Terraform 管一个数仓，含 grant 事故 | 中 — 5 个 PR，权限方向 | `cdn-content` 3 节点 |
| 05 | [[05-kubernetes\|Kubernetes]] | 部署形态说得清，集群没运维过 | **弱** — 原理为主 | 三域 5 节点 |
| 06 | [[06-cicd-progressive-delivery\|CI/CD 与灰度发布]] | 数据层的渐进式发布：flag + 逐户 gate + 影子对账 | **强** — 真做过迁移 | `cdn-content` + `system-design` 7 节点 |
| 07 | [[07-data-pipelines-cdc\|数据管道与 CDC]] | 同一系统里的文件批 vs 日志捕获，两条管道对照 | **强** — GRRCN 端到端 | `system-design` + `kafka` 7 节点 |
| 08 | [[08-observability-oncall\|可观测性与 On-Call]] | 数据系统的"安静失败"，四个真实事故 | **强** — 四个事故的处理人 | `system-design` + `kafka` 6 节点 |
| 09 | [[09-sql-data-modeling\|SQL 与数据建模]] | 数仓不建索引靠剪枝；一条 MERGE 的四层设计 | **强** — 业务逻辑几乎全是 SQL | `system-design` + `snowflake` 8 节点 |
| 10 | [[10-correctness-idempotency\|分布式正确性]] | 幂等、反向事件、账本、对账 | **强** — 金融正确性是日常 | `system-design` + `code-core` 8 节点 |

---

## 按 JD 关键词查

| JD 上写的 | 读哪份 |
|---|---|
| system design / architecture / distributed systems | 01，补 07、10 |
| Kafka / event streaming / pub-sub / Debezium | 02，补 07 |
| Snowflake / data warehouse / BigQuery / Redshift | 03，补 09 |
| Terraform / IaC / CloudFormation / Pulumi | 04 |
| Kubernetes / EKS / GKE / containers | 05（**先读它的第 5 节再决定**） |
| CI/CD / canary / feature flags / progressive delivery | 06，补 04 |
| ETL / ELT / data pipeline / CDC / Airflow / dbt | 07，补 09 |
| observability / monitoring / SRE / on-call / incident | 08 |
| SQL / data modeling / analytics engineering | 09，补 03 |
| idempotency / reconciliation / ledger / consistency | 10 |

一轮系统设计面通常横跨 01 + 07 + 10；一轮技术深挖多半落在 03 或 09。

---

## 边界一览

这张表是这套材料里最该在面试前扫一遍的东西。**主动说出边界，比被问到才承认强得多。**

| 栈 | 说不会的地方 | 把话接到哪 |
|---|---|---|
| 01 | 超大规模 C 端（十亿日活、全球多活）；在线服务容量规划 | 我的规模挑战在数据量和正确性，不在 QPS；而且每笔都要对得上账 |
| 02 | broker 运维、集群调优、分区再平衡 | 消费侧的语义、位点、重放我熟；CDC 管道是真做过的 |
| 03 | 账号级 Snowflake 管理、Snowpark、Data Sharing | 存储过程、stream/task、剪枝优化是日常 |
| 04 | 大规模 Terraform 治理（workspace 拆分、Terragrunt）；AWS 深度 | grant/ownership 模型摸得透，#1326 加后续反查 |
| 05 | **集群运维全部**；service mesh | 运维经验是真的，只是发生在 Snowflake 侧 |
| 06 | 流量层灰度（k8s canary、mesh 分流） | 我的灰度在数据层：feature flag + 逐商户 gate + 影子对账 |
| 07 | Flink/Spark Streaming 引擎本身；Debezium 建设侧；Airflow | 乱序和迟到问题我真处理过（GRRCN 文件迟到那次） |
| 08 | SRE 专职范畴（容量规划、混沌工程）；误差预算 gate 发布 | 数据系统的"安静失败"这一层我最有话说 |
| 09 | OLTP 调优（锁、隔离级别实现、连接池）；dbt | 数仓性能模型我熟，方法论可迁移 |
| 10 | 2PC / Saga 的生产实现 | 我们靠幂等 + 反向事件 + 对账，这是清醒的取舍不是不懂 |

**三条通用建议**：
1. 说完边界**不要接"但我学得很快"** —— 那句话不加分，接具体的相邻经验。
2. 05 是唯一一份证据明显薄的，JD 重度依赖 K8s 时别用它硬顶。
3. 简历上曾有的 "Kafka in Kubernetes（实习期）"**证据不足，已弃用**。要讲 Kafka 就讲 02 里的生产 CDC 管道。

---

## 三条使用约定

**自包含。** 正文不靠链接撑。链接是"想更深时去哪"，不是"这里省略了"。所有链接失效也能从头读到尾。

**知识层不重写。** 第 2 行的 `<!-- domain-links -->` 指回 `vault/domains/` 已建好的节点（`system-design` ~100 节点、`kafka` 79、`snowflake` 110、`cdn-content` 的 `delivery.*`）。`python3 vault/interviews/core/check_links.py` 校验这些节点名真实存在（所有 wikilink 都要能唯一解析），skeleton 改名不会静默断链。

**证据在故事笔记里。** 每份 frontmatter 的 `stories:` 列出对应的 [[S1]]…[[S11]]；故事笔记的"证据边界"说明什么能讲、什么不能讲。原始证据（雇主 repo、工单、聊天记录）只在本机 `stories/raw/`，不入库。

---

## 已知需要回填的

| 事项 | 在哪 |
|---|---|
| 11 条待查证的生产数字（`$600B` 口径、各事故的影响面复核等） | 本机 `stories/raw/HANDOFF-snowflake-queries.md`；口播先按故事笔记里的"量级"说 |
| 与旧材料对不上的说法（#1 committer、funding 迁移、ADR 未批准、$138.6B 口径等） | 已写进各故事笔记的 `[!warning] 证据边界` |

那两份都该在投简历前处理完 —— **修掉站不住的说法，比补新素材重要。**
