---
id: patterns-adapter-vs-facade
node: patterns.structural
type: qa
---
## Q
Adapter vs facade — both "wrap other code". What's the discriminating question?

## A
Ask **"does an interface already exist that the client expects?"**

- **Adapter**: yes — the client is written against a target interface, and you convert an *incompatible existing* class to fit it (`SlackNotifier implements Notifier` wrapping the Slack SDK). Usually wraps **one** class; the shape is dictated by the target interface.
- **Facade**: no — you *invent a new, simpler* interface over a whole **subsystem** of classes to shield clients from its complexity (`OrderFacade.checkout()` hiding inventory + payment + shipping calls). Clients could bypass it; it exists for convenience and decoupling, not compatibility.

One-liner: adapter changes an interface's **shape**; facade reduces a subsystem's **surface**.

## Q zh
Adapter vs facade — 都是「包装其他代码」。区分它们的关键问题是什么？

## A zh
问**"是否已存在客户端期望的接口？"**

- **Adapter**：是的——客户端是针对某个目标接口编写的，你需要将一个*不兼容的既有*类适配成它。（如 `SlackNotifier implements Notifier` 包装 Slack SDK）。通常包装**一个**类；形状由目标接口决定。
- **Facade**：不是——你在一个完整的**子系统**上*发明一个新的、更简单的*接口来给客户端隐藏复杂性。（如 `OrderFacade.checkout()` 隐藏库存、支付、配送的调用）。客户端可以绕过它；它是为了便利和解耦而存在，不是为了兼容性。

一句话：adapter 改变接口的**形状**；facade 缩减子系统的**表面**。
