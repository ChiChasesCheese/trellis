---
id: problems-online-shopping-idempotency-key
node: problems.marketplaces.online-shopping
type: qa
step: 7
tags: [grown]
---
## Q
电商下单失败要退款时，为什么退款接口应该按调用方生成的幂等键（idempotency key，比如订单号）寻址，而不是按扣款接口返回的回执号？

## A
因为补偿必须能在“不知道对方到底做成了没有”的情况下正确执行。钱扣了、响应在网络上丢了，回执号就永远拿不到；如果退款只认回执号，这笔钱就卡在半路上。调用方自己生成的键在发请求之前就存在，所以任何时候都能拿它去退款。契约的另一半由网关承担：同一个键重复扣款只扣一次，对没扣过款的键退款是无操作——这样补偿可以无条件调用。真实的支付 API（如 Stripe）正是这么设计的。
