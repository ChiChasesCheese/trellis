---
id: hi-c-lld-design-principles-n11-isp
node: lld.in-a-hurry.design-principles.notes
type: qa
step: 11
---
## Q
**设计原则 · ISP：小而专的接口**｜摘要 · 必会

接口隔离原则（ISP）反对什么？`Robot` 被迫实现 `eat`、`sleep` 的接口该怎么拆？

## A
- **反对大而全的接口：** 如果实现者被迫写自己根本用不到的方法，结果往往是空实现或抛异常，这是明显的坏味道。
- **做法：** 把大接口拆成小而内聚的接口，类按需要组合多个，而不是被迫实现全部。
- **例子：** `Worker` 拆成 `Workable`、`Feedable`、`Restable`；`Human` 三个都实现，`Robot` 只实现 `Workable`。
- **经验判断：** 一个类只需要某个接口十个方法里的两个，说明这个接口太大了。
