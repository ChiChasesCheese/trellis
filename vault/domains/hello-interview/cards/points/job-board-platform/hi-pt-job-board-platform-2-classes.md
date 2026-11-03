---
id: hi-pt-job-board-platform-2-classes
node: qb.lld.job-board-platform.points
type: qa
step: 2
---
## Q
**招聘信息平台 · 类与职责划分**｜必会 · 出自：招聘信息平台 › 核心实体与接口

招聘信息平台需要哪些核心类，各自的职责是什么？

## A
**数据类。** Job（雇主、标题、薪资、发布与过期时间、状态）；Application（求职者、职位、状态）。
**逻辑类。** Spec 接口及 SalarySpec、OpenSpec（再按需加 KeywordSpec 等）；JobBoard 作门面与服务；EventBus 发布 ApplicationSubmitted、StatusChanged。
**不做。** 雇主与求职者不用继承，只是权限不同，用角色字段更简单。
