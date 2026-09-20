---
id: problems-online-shopping-saga-vs-try-except
node: problems.marketplaces.online-shopping
type: qa
step: 5
tags: [grown]
---
## Q
电商下单要跨“预留库存—扣款—扣减库存—创建运单”四个会失败、又不在同一个事务里的参与方。为什么用 Saga（每步配一个补偿动作、失败时反向补偿）而不是一串嵌套的 `try/except`？

## A
嵌套 `try/except` 会把同一段补偿逻辑抄好几遍（退款在两层 `except` 里各出现一次），参与方每多一个就多一层缩进、要改三处，而且极容易补偿一个根本没执行成功的步骤。Saga 把“做什么”和“怎么撤销”在同一个步骤对象里**成对声明**，顺序和补偿逻辑收敛到一处，加一个参与方就是数组里多一项。额外的好处是这个执行器与业务无关——它不知道什么是订单、什么是库存，可以脱离商品被单独测试。
