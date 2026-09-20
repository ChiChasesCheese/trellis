---
id: patterns-extensibility-followup
node: patterns.selection
type: qa
step: 2
---
## Q
LLD 面试里经典的追问是"现在要加一种新支付方式 / 通知渠道 / 定价规则，但不许改动已有代码"，标准的两模式答案是什么？又有什么是你仍然必须改的？

## A
**Strategy + 工厂（注册表）**——最常见的开闭原则（OCP）组合：

1. 会变化的行为被抽象成一个接口——哪怕只是一个函数签名，比如 `charge(amount: float) -> None`；核心流程只依赖这个签名，对修改封闭。
2. 一个基于注册表的工厂把 key 映射到构造函数，比如 `REGISTRY: dict[str, Callable[[], PaymentMethod]]`；新增一种支付方式就是新写一个类或函数，再加一行 `REGISTRY["upi"] = UpiPayment`。

要诚实说出的保留意见：总有地方必须改——那一行注册代码，以及组合根（composition root）。OCP 的意思是改动**可加且局部**，不是零改动；如果新变体还需要端到端的新数据字段（请求解析、存储结构），没有哪个模式能替你掩盖这一点。
