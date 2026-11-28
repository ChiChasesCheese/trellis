---
id: hi-c-lld-patterns-n03-factory
node: lld.in-a-hurry.patterns.notes
type: qa
step: 3
---
## Q
**设计模式 · Factory：把创建集中到一处**｜摘要 · 必会

Factory 解决什么问题，什么时候用？面试里写的是哪个版本？

## A
- **作用：** 调用方不必决定创建哪个具体类；"支持不同通知类型"这类需求就是触发词
- **做法：** `NotificationFactory.create(type)` 集中创建，加短信渠道只改工厂，其余代码不动
- **版本：** 写的是简单工厂（Simple Factory）；GoF 的工厂方法（Factory Method）靠子类重写创建方法，抽象工厂（Abstract Factory）造一整族对象，都更复杂，几乎不会被要求
- **注意：** 有些工程师认为工厂是过度设计，面试官的反应要观察
