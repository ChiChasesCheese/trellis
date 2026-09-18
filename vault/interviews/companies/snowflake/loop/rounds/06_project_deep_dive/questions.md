# Expertise / 项目深挖轮 —— 题库（16 题）

> 来源：`catalog/raw/bq_hm_recruiter.md` §3（Blind xcavd10l 2024-06 IC3 40 min 一手；Blind 3tbrdamq 2024-02 senior；早期职业为 coding 轮前 15–20 min + onsite resume 轮）。练习：`python3 loop/mock.py bq expertise -n 3 -m 5`。
> **一句话**：这一轮考的是"每个决策的 why + 被否方案 + 系统属性"，不是"做了什么"。

## 两个可深挖的项目（各准备 15 min 版）

| 项目 | 架构一句话 | 三个决策（各带 2 个被否方案） | 失败模式与监控 | 重做清单 |
|---|---|---|---|---|
| **[[S1]] AMEX GRRCN 管线** | S3 定宽文件 → staging → 6 条 append-only stream 分流 → proc 解析 MERGE → UDTF 合并 → fee 计算 → Funding 出款 | ① Snowflake-native 而非 Airflow（数据不出仓、事务 MERGE；弃：Airflow 编排 / Ruby 脚本续命）② 按 record type 分流 6 条 stream（弃：单表单 stream 全量扫描 / 外部解析服务）③ feature-flag 急停 + 幂等 MERGE 键（弃：手工回滚） | 半截文件、重复投递、stream 过期；`TASK_HISTORY` + Streamlit 监控 + Datadog 告警；summary 记录对账不一致则停 | 商户粒度质量门从第一天做；Dynamic Tables 做下游聚合 |
| **[[S5]] Net Settlement 迁移** | interchange 取数 Trans View → Settle View；plan-code/fee 映射；schedule 同步；对 Fiserv 上报对账 | ① shadow-run 再切（弃：flip-and-monitor）② 按商户灰度 toggle（弃：全量切换）③ CDC backfill 三级时间兜底模板（弃：一次性脚本） | 字段不一致率、迟到数据；day-level 对账 13.7M 行 0.224% | 更早引入 handshake；自动化差异分类 |

## 题目

| 问题原文 | 来源 | 这题在考什么 | 踩雷点 |
|---|---|---|---|
| "Pick a project and walk me through it end to end." | 一手 IC3 | 结构：一句话 → 架构 → 三个决策 → 结果数字 | 从需求背景讲 5 分钟 |
| "Why that architecture? Alternatives?" | 一手 ×2 | **必须有被否方案** | 只讲最终方案 |
| "Which external libraries/services, and why?" | 一手 | 选型理由与边界 | "团队一直这么用" |
| "Availability / fault tolerance?" | 一手 | 依赖挂了怎样、SLA、重试与幂等 | 没想过 |
| "Partial failure mid-pipeline?" | 推断 | MERGE 幂等、flag 急停、重放 | 说"不会发生" |
| "100× volume?" | 推断 | 瓶颈定位（解析 proc → 并行、仓库规格）| 泛泛"加机器" |
| "Your contribution vs team?" | 通用 | "I designed / I wrote / I owned" + 数字 | 团队功劳含糊 |
| "How did you verify correctness?" | [[S5]] | shadow-run、对账、灰度 | "跑了测试" |
| "Hardest bug?" | [[S3]] | 根因链（NULL 拼接 → UDF overload）| 讲现象不讲根因 |
| "What would you redo?" | 一手 senior | 具体两条 | "没什么要改" |
| "Monitoring?" | [[S1]] | 什么会 page、什么不该 page | 只说 Datadog |
| "Deadline trade-off and payback?" | HM 通用 | 明确技术债与还债时间 | 只讲赶上了 |
| "Who disagreed?" | [[S2]] | ADR、三个被否方案、如何达成一致 | 把对方说成不懂 |
| "On Snowflake's own primitives?" | 桥 | Dynamic Tables / serverless tasks / Streams offset 的取舍 | 不了解产品 |
| "Net-settlement source-of-truth switch?" | [[S5]] | Trans → Settle view，shadow-run 数字 | 数字说错 |
| "Quality-check framework granularity?" | [[S2]] | 4% 阻塞全部 → 商户级；自我修正 | 回避自己的缺陷 |

## 追问三层自检

每个决策：**why**（当时的约束）→ **alternatives**（至少两个 + 弃因）→ **now**（现在看的问题 / 重做）。讲不出第二层就是这轮的挂点。
