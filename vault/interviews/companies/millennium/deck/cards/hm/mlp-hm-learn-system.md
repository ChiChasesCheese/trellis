---
id: mlp-hm-learn-system
node: hm.learning
type: qa
step: 1
---
## Q
**快速学会陌生系统**｜经理面与行为面

“Describe a time you had to learn a large, unfamiliar system quickly.”

## A
这是 LEaD 轮岗的核心题：每半年换一个陌生系统。回答里要有一套方法，再配两个真例子。

- **方法：** 从入口和数据流开始，在动手之前把画出的图拿给负责人确认，分清什么是真的、什么只是文档里写的。
- **例一：Amex 管线。** 接手时只有一张表的 stub；你从设计文档起，先定拓扑，再逐段实现，没有靠猜。
- **例二：基础设施仓库。** 发布在 QA 失败，`GRANT OWNERSHIP` 被 Snowflake 拒绝，被点名调查的是别人，你只是被抄送。7 分钟后你贴出根因：ownership 资源没设 `outbound_privileges`，Terraform 没先撤销别的角色持有的依赖授权。修法是设为 `REVOKE`，当天 QA、预生产、生产全部部署。
- **之后：** 扫了全仓库，79 个同类资源里 42 个缺该参数，多数是无害的 `future_*`，但另一个模块里有两个同形状、尚未触发的风险，你主动标了出来。
- **能快的原因：** 对整个仓库的授权结构有全局图景。

**英文答法。**
- I start from the **entry point and the data flow**, then confirm a diagram with the owner **before touching anything**.
- When a release failed in QA on `GRANT OWNERSHIP`, someone else was named; I was cc'd. **Seven minutes later** I posted the root cause: the resource didn't set `outbound_privileges`.
- I proposed `REVOKE`, checked the neighboring modules, and QA, pre-prod and prod went out **that afternoon**.
- Afterwards I scanned the repo, found **two real look-alikes** in another module that hadn't fired yet, and flagged them.

**追问。**
- **How did you know so fast?** I have a global picture of the repo's grant structure.
- **Anything you got wrong?** On the day I only checked the neighboring modules; the full scan afterwards found dozens of missing parameters, mostly harmless.
- **How do you know what is true in a system you do not know?** Entry point and data flow first, then a diagram confirmed with the owner before I change anything.
