# Distributed Metadata Catalog and Schema Registry（分布式元数据目录与 Schema 注册中心）

我们要给公司内部所有数据处理系统（查询引擎、摄取管道、特征平台，未来还要接外部的开源查询引擎）
做一个统一的元数据目录：记录有哪些数据集（表/数据集）、它们当前的 schema、schema 的历史演进
版本（因为不同消费者可能还 pin 在旧版本做迁移）、以及数据物理存放位置（表 → 文件清单/分区）。
多个团队会并发注册新数据集、并发演进各自数据集的 schema——同名数据集不能被两个并发请求都注册
成功；schema 变更要先做兼容性校验（比如加一个可空字段是兼容的，删字段或改类型是破坏性的）才能
被接受。读远多于写：每一次查询规划都要查 schema + 物理位置，延迟要求很低；写（注册新数据集、
schema 演进、提交新的文件清单）相对少但必须强一致——两个摄取任务并发往同一张表提交新文件清单
不能互相覆盖丢更新。目录还要能通过标准协议对外暴露，让外部开源查询引擎也能读它。**这道题官方
描述本身就说需求是模糊的（"Design Under Vague Distributed Requirements"）**——预期你自己去
明确诸如"schema 版本粒度多细""目录是不是也要管访问控制""多区域下目录读写怎么分工"这些边界，
而不是等面试官告诉你。请设计这个系统。

---

**面试环境说明**：Snowflake onsite 或技术电面的 System Design 轮，Hard，45–60 分钟。白板工具未
证实；面试官风格两极，沉默时要自己推进——这道题的官方题面本身就在提示"面试官可能不会给你补齐
需求"。

**题目原始报告与来源**：
- **LOW（聚合站自建题库，无一手印证）**：PracHub "Distributed Metadata Catalog and Schema
  Registry"（Hard，"Design Under Vague Distributed Requirements"，181 人做过，2025-09-06）。见
  `../../../catalog/raw/system_design.md` §1.14 与 §3 第 5 条（该文件明确把这题归为"聚合站自建
  题库，练习价值仅供覆盖面，不代表已证实的 Snowflake 原题"）。**按覆盖面练，不按真题押。**
- 与 Snowflake 的关系：元数据（表版本、micro-partition 清单）集中存在 **FoundationDB**，用
  "不可变快照 + 原子指针切换"实现 Time Travel；**Iceberg / Apache Polaris**（2026-02 成为
  Apache 顶级项目的开源 REST catalog）正是"用标准协议对外暴露目录，让外部引擎互操作"这件事的
  真实产品化——`../../../01-company-brief.md` §1。**[推断]**
