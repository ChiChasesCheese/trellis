---
title: Core · 面试核心能力（MOC）
aliases:
  - Core
  - Interviews Core
  - 面试核心
tags:
  - moc
  - interview
---

# Core — 与公司无关、每场面试都用、每场面完都回写的东西

公司目录（`companies/<co>/`）只**链接**这里，不复制。写法：故事用 `[[S5]]`，答案用 `[[Answers#Q3]]`，技术栈用 `[[TS03]]`——在 Obsidian 里都能直接跳。

## 故事（一故事一文件，frontmatter 有 `aliases`，`[[S1]]` 即可引用）

| 故事 | 一句话 | 最常回答 | 主要 JD 线 |
|---|---|---|---|
| [[S1]] | Amex 结算管线：`COPY INTO` → 六条 append-only Stream → 复合键 `MERGE` → 校验 UDTF → 双上游 Task；18 个月防御 | 最难项目 · 端到端 ownership | SQL · DB internals · production |
| [[S2]] | 配置驱动的质量门禁 + trigger-status 握手；商户级 ADR（strictest wins） | 架构决策 · 定标准 · 说服团队 · 接受批评 | SQL · distributed systems |
| [[S3]] | ACH 费用 `'BT_' \|\| NULL` 静默事故；overload consolidation；fail loudly | 最难 bug · on-call · go-to | SQL · production |
| [[S4]] | AU Amex 退款费：一条查询结束 50 条回复的跨团队争论 | 冲突 · 影响半径 | SQL |
| [[S5]] | Net Settlement / interchange 数据源切换：静态拆分 vs fallback；同源影子核对；四层 MERGE；deploy ≠ release | 技术决策 · 迁移 · 最大业务影响 | SQL · distributed systems · CI/CD |
| [[S6]] | 实习生 ML 检测器的 go/no-go：QA 6 商户 vs 生产 18k；SQL pushdown 先行 | 判断力 · 说不 · 优先级 | production |
| [[S7]] | schema pool：零拷贝克隆池让多 agent 会话并行；三篇 ADR | 主动性 · 开发者效率 · AI fluency | DB internals |
| [[S8]] | Terraform grant-ownership 7 分钟 RCA + 主动指出下一个雷 | 压力下 debug · unblock | Terraform · production |
| [[S9]] | Amex 出款延迟事故：SLA 定论 + region conditional > revert | 事故指挥 · 领域权威 | production |
| [[S10]] | 退款费 billing-terms 复盘：推翻自己 10× 的 blast radius | 定量推理 · 诚实 | SQL |
| [[S11]] | 实习期：Kafka connector / Spring · JPA / Spark 校验；K8s 部署形态 | 广度 · Java · Kafka | Java · Kafka · K8s |

## 答案（Q1–Q24，一个文件，`[[Answers#Q3]]` 跳到题）

[[Answers]] —— 六个维度：技术深度与业务影响 Q1–8 · 技术领导力 Q9–12 · 带教协作 Q13–16 · 模糊性与 ownership Q17–20 · HR / fit Q21–24。每题：首答（60–90 s）→ 追问展开 → 故事链接。

## 技术栈（按 JD 关键词，`[[TS03]]` 跳）

[[Tech Stacks|Tech Stacks 总表]] —— [[01-system-design|TS01 系统设计]] · [[02-kafka-event-streaming|TS02 Kafka]] · [[03-snowflake-warehouse|TS03 Snowflake]] · [[04-terraform-iac|TS04 Terraform]] · [[05-kubernetes|TS05 Kubernetes]] · [[06-cicd-progressive-delivery|TS06 CI/CD 灰度]] · [[07-data-pipelines-cdc|TS07 数据管道 CDC]] · [[08-observability-oncall|TS08 可观测性]] · [[09-sql-data-modeling|TS09 SQL 建模]] · [[10-correctness-idempotency|TS10 分布式正确性]]。每份自包含：来龙去脉 → 我们怎么用 → 我做了什么 → 追问 → 边界。

## 轮次打法与工具

| 目录 | 是什么 |
|---|---|
| `playbooks/` | 按轮次的通用打法。[[ai-voice-screen\|AI 语音筛（Chakra）]]：Reporter 只读 transcript、3/2/1/0、theoretical = Not Met |
| `debrief/` | 面后复盘工具：本机转写 + 语速/填充词/语法/题库覆盖/rubric（[[interviews/core/debrief/README\|说明]]）；实例 [[interviews/companies/snowflake/debrief/2026-09-17-chakra/REVIEW\|2026-09-17 Chakra 评审]] |
| `resume/` | `resume.tex` 唯一源 + 投递 PDF + CHANGELOG |
| `leetcode/` | 公司标签题单工具 `lc_company.py`；`companies/<co>.md` |
| `stories/raw/` | 原始证据（雇主 repo、工单、聊天记录）——**只在本机，不入库**。精炼成可说的表述后才进故事笔记 |

## 诚实红线（所有答案共用）

- 数字只说量级 + "roughly"；精确值与口径在各故事的"量级与口径"表；`$138.6B` 疑为分/元口径差 100×，口播不依赖它。
- 不说：#1 committer / 615 commits · "迁移了 Funding 的 Ruby 脚本" · "ADR 已上线" · "no bugs" · "全 repo 唯一缺该参数"。替代说法都在故事笔记的 `[!warning] 证据边界` 里。
- 带教只讲 domain-ownership / architectural collaboration，不编 code-review 记录或 1:1 细节。
- 不点同事、商户名（"a large marketplace merchant"、"a newer engineer"）。

## 回写规则

- 某公司新问了一道通用题 → 写进 [[Answers]]，公司 kit 只加链接。
- 面完被追到答不上的细节 → 补进对应故事的"追问版"。
- 复盘（[[interviews/core/debrief/README|debrief]]）里的好句子 → 故事的"讲法"或 kit playbook 的追问弹药表。
- 校验：`python3 vault/interviews/core/check_links.py`（所有 wikilink 唯一解析）。
