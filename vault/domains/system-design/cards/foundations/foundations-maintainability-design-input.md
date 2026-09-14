---
id: foundations-maintainability-design-input
node: foundations.method
type: qa
---
## Q
DDIA's three maintainability goals — name them, and where does each show up in a design interview answer?

## A
- **Operability** — make life easy for ops: metrics, runbooks, sane defaults, no manual toil. Show it: say how you deploy, monitor, and migrate the thing you just drew.
- **Simplicity** — remove *accidental* complexity with good abstractions. Show it: refuse components a number doesn't justify.
- **Evolvability** — cheap to change later. Show it: schema evolution plan, versioned APIs, reversible decisions.

Most software cost is maintenance, not initial build — treating these as requirements (not virtues) is a senior signal.


## Q zh
DDIA 的三个可维护性目标 — 说出它们的名字，每一个在设计面试的回答里会体现在哪里？

## A zh
- **可运维性（Operability）** — 让运维的生活轻松：指标、运行手册、合理的默认值、没有人工苦活。展示方式：说明你会如何部署、监控、迁移你刚画出来的东西。
- **简洁性（Simplicity）** — 用好的抽象去除*偶然*复杂性。展示方式：拒绝任何数字没有证明其必要性的组件。
- **可演化性（Evolvability）** — 以后改起来便宜。展示方式：schema 演化计划、版本化 API、可逆的决策。

大多数软件成本花在维护上，而不是最初的构建 — 把这三者当作需求（而不是美德）来对待，是资深工程师的信号。
