---
id: patterns-extensibility-followup
node: patterns.selection
type: qa
---
## Q
The classic LLD follow-up: "now add a new payment method / notification channel / pricing rule without touching existing code." What's the standard two-pattern answer, and what remains that you must still edit?

## A
**Strategy + factory (registry)** — the bread-and-butter OCP combo:

1. The varying behavior sits behind an interface (`PaymentMethod.charge()`); core flow depends only on it — closed for modification.
2. A **registry-based factory** maps a key to a `Supplier<PaymentMethod>`; adding UPI = one new class + one `register()` line (or an annotation/config entry).

Honest caveat to state: something must still change — the registration line and the composition root. OCP means changes are **additive and localized**, not zero. If variants also need new *data* fields end-to-end (request parsing, storage), no pattern hides that; say so.

## Q zh
LLD 轮的经典追问："现在加一种新支付方式 / 通知渠道 / 定价规则，但不许改动已有代码。"标准的两模式答案是什么，又有什么是你仍然必须改的？

## A zh
**Strategy + factory（注册表）** —— 最家常的 OCP 组合：

1. 变化的行为藏在一个接口后面（`PaymentMethod.charge()`）；核心流程只依赖这个接口 —— 对修改封闭。
2. 一个**基于注册表的工厂**把 key 映射到 `Supplier<PaymentMethod>`；加 UPI = 一个新类 + 一行 `register()`（或者一条注解/配置项）。

要诚实说出的保留意见：总有东西必须改 —— 那行注册代码，以及 composition root。OCP 的意思是改动**可加且局部**，不是零改动。如果新变体还需要端到端的新*数据*字段（请求解析、存储），没有哪个模式能掩盖这一点；直说。
