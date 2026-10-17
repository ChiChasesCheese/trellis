---
id: amz-parking-fees-objects-and-their-jobs
node: amazon.amz-parking-fees
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，应有哪几个对象？各自只负责什么？

## A
`Tariff`：纯数据的价目表（按车型的小时单价、每日封顶、宽限期），只回答「此刻单价多少、下次变价是何时」。`FeeEngine`：把一次停留切段并算钱，不持有票。`Adjustment`：出场后的会员折扣、丢票罚款等调整。`FeeDesk`：发票、凭票结算，唯一有状态的类。`Money`：整数分。切分依据：价目表、算法、票各自因不同原因而变。车位分配属于另一道题的停车场，这里不重做。
