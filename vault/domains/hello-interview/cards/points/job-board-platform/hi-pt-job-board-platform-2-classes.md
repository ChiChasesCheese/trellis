---
id: hi-pt-job-board-platform-2-classes
node: qb.lld.job-board-platform.points
type: qa
step: 2
---
## Q
**招聘信息平台 · 类与职责划分**｜出自：招聘信息平台 › 核心实体与接口

招聘信息平台需要哪些核心类，各自的职责是什么？

## A
**数据类。** Job（雇主、薪资区间、技能集合、发布与过期时间、状态）；Application（求职者、职位、简历引用、状态）。
**逻辑类。** Specification 接口及 KeywordSpec、LocationSpec、SalarySpec、SkillSpec、OpenSpec；JobBoard 作门面与服务，持倒排索引；EventBus 发布 ApplicationSubmitted、StatusChanged。
**不做。** 雇主与求职者不用继承，只是权限不同，用角色字段更简单。
