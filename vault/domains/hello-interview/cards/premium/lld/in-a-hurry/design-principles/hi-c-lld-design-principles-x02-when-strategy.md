---
id: hi-c-lld-design-principles-x02-when-strategy
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 2
---
## Q
**设计原则 · 要不要上策略**｜考点 · 必会

停车场现在只有按小时计费一种规则。你要不要为计费引入 `PricingStrategy` 接口？什么信号出现时再引入？

## A
- **现在不要：** 只有一种规则，一个方法就够（KISS、YAGNI）
- **留余地：** 把计费集中在一个方法里，别散在各处
- **该引入的信号：**
  - 出现第二、第三种规则，且会按场景切换
  - 每加一种规则就要改多处代码
- **面试说法：** 先说"我现在放在 `Ticket` 里，规则增加时抽成策略"，而不是一开始就搭
