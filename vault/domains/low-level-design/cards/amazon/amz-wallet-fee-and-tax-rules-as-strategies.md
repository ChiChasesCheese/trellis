---
id: amz-wallet-fee-and-tax-rules-as-strategies
node: amazon.amz-wallet
type: qa
step: 5
tags: [grown]
---
## Q
在钱包设计里，追加「转账收手续费、利息要交税」，怎么做到以后再加规则不改核心代码？

## A
定义 `FeeRule`：`apply(txn) → 额外分录列表`，手续费、税、跨境费各是一个类，转账时依次执行规则列表。规则返回的是分录而不是直接改金额，所以费用也在账本上可查。舍入全用整数：税 = `(金额 × 税率千分点 + 500) // 1000`，固定为四舍五入。加新规则 = 新增一个类并加入列表，转账代码不动。
