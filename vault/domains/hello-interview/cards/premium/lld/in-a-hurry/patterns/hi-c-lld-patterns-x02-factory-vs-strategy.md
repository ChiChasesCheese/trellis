---
id: hi-c-lld-patterns-x02-factory-vs-strategy
node: lld.in-a-hurry.patterns.exam
type: qa
step: 2
---
## Q
**设计模式 · 工厂和策略别混**｜考点 · 必会

需求："用户可以选信用卡或 PayPal 付款，之后可能加加密货币"。工厂和策略分别在哪个环节出现？

## A
- **Strategy：** `PaymentStrategy` 接口，各支付方式实现 `pay`；购物车持有并委托，决定"用哪种做法"
- **Factory：** 根据用户选择（字符串或枚举）创建对应的策略对象，决定"造哪个对象"
- **只用一个也成立：** 策略对象由调用方直接构造时，不需要工厂
- **常见错误：** 把两个说成同一回事，或只写工厂却仍然在使用处写 if/else
