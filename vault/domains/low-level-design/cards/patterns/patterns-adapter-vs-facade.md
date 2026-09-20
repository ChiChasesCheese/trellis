---
id: patterns-adapter-vs-facade
node: patterns.structural
type: qa
step: 4
---
## Q
Adapter 和 Facade 都是"在其他代码外面包一层"，区分它们的关键问题是什么？

## A
问**"客户端期望的接口是否已经存在？"**

- **Adapter**：是的——客户端本来就是照着某个目标接口写的，你要把一个不兼容的既有类适配上去（比如让第三方 `SlackClient` 符合项目里定义的 `Notifier` 协议）。通常只包一个类，形状由目标接口决定。
- **Facade**：不是——你在一整个子系统之上发明一个新的、更简单的接口，把复杂性藏起来给调用方（比如 `OrderFacade.checkout()` 背后串联库存、支付、配送）。调用方可以绕过它；它是为了方便和解耦，不是为了兼容。

一句话：Adapter 改变接口的**形状**；Facade 缩减子系统暴露的**表面**。
