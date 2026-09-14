# Petabyte-Scale Database Sync（两个 PB 级数据库之间同步数据）

我们有两个数据库系统，一个是源端，承担线上业务写入，另一个是目标端，给分析和下游团队读；两边的数据量都在 PB 级，表的数量在几万张，其中少数大表单表就有几百 TB，写入最热的表每秒有几十万行变更，而且源端的 schema 会不定期演进——加列、改类型、偶尔拆表。现在需要你设计一个同步系统，让目标端持续地、尽量接近实时地反映源端的数据：第一次接入一张表时要把全量历史搬过去，之后要持续跟上增量变更，包括更新和删除；搬运过程中源端不能停写，也不能因为同步把源端的线上业务拖慢；任何一个环节挂了之后要能从断点继续，而不是从头再搬几百 TB；同步完成后，业务方会问"目标端这张表现在和源端到底一不一样"，你得能回答这个问题，并且能说清楚延迟是多少。请设计这个系统。

---

**面试环境说明**：Snowflake 技术电面或 onsite 的 System Design 轮，45–60 分钟。**一手报告的关键信息是：这道题面试官不允许做需求澄清**（"no requirements gathering allowed"），候选人形容为 "worst 30 minutes"。所以不能指望通过提问拿到约束——要在开场 2 分钟内**自己把假设大声说出来**（规模、延迟目标、一致性语义、源端类型），然后按假设推进；面试官不纠正就视为接受。白板工具未证实。

**题目原始报告与来源**：
- **一手（高置信度）**：Reddit r/leetcode 帖 1s2xtox 评论（约 2026-03），Backend IC2 system design："how will you sync databases with petabytes of data between them"，面试官不允许 requirements gathering。—— `../../../catalog/discovery/TRIAGE.md` #11，URL 见该行。**[高，单一一手来源]**
- 与 Snowflake 业务的关系：这正是 Snowflake 摄取侧（Openflow 的 Oracle/PostgreSQL CDC 连接器、Snowpipe Streaming、Snowflake Postgres ↔ 分析侧的同步）每天在解决的问题。**[推断]**
