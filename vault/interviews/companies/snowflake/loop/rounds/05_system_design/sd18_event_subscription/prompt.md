# Event Subscription System（事件订阅与通知系统，1M events/s）

平台上会产生大量事件：查询完成、仓库（warehouse）被挂起、数据加载失败、账单超过阈值、表结构变更。用户和下游系统想"订阅"自己关心的事件：比如"我的任何查询跑超过 30 分钟就通知我"、"`PROD` 数据库里有表被 drop 时调这个 webhook"、"账号 credit 用量超过 80% 发邮件"。事件总量峰值每秒约一百万条，订阅规则总共约一千万条，属于数十万个账号。投递渠道有 webhook、邮件、站内消息、以及推送到客户自己的消息队列。要求：事件发生后大多数通知在几秒内送达；同一事件对同一订阅**不要重复打扰**用户（下游 webhook 能接受偶尔重复，但邮件不行）；某个客户的 webhook 挂了或很慢，不能拖慢别的客户；用户可以随时增删改订阅，改动要在一分钟内生效。请设计这个系统。

---

**面试环境说明**：Snowflake onsite 或技术电面的 System Design 轮，45–60 分钟。

**题目原始报告与来源**：
- **LOW（单一培训站，无日期、无一手印证）**：staffengprep.com "Event Subscription System — 1M/s QPS 用户通知"。见 `../../../catalog/raw/system_design.md` §3。**按覆盖面练，不按真题押。**
- 题面里的具体事件类型、渠道、SLA 为 **(reconstructed)**，选取 Snowflake 产品里真实存在的事件（查询、仓库、加载、账单）使题目落地。
- 与 Snowflake 的关系 **[推断]**：Snowflake 有 Notification Integration（邮件 / webhook / 云消息队列）、Alerts（`CREATE ALERT … IF EXISTS (query) THEN …`）与 resource monitor 阈值通知，正是这个系统的产品面。
