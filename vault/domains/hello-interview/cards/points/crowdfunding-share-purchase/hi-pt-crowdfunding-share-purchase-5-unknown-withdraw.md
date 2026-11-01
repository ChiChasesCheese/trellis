---
id: hi-pt-crowdfunding-share-purchase-5-unknown-withdraw
node: qb.sd.crowdfunding-share-purchase.points
type: qa
step: 5
---
## Q
**限时众筹购股系统 · 扣款超时的不确定性**｜出自：限时众筹购股系统 › 深入 2

众筹购股调用余额服务的 withdraw 超时，不知道钱扣了没有。此时股数能不能直接放回库存？应该怎么处理？

## A
**易错。** 绝不能直接放回：钱可能已经扣了，再卖给别人就是超卖或收了钱没给股。
**做法。** 用同一幂等键重试；仍不明确就停在 PAYING，由对账任务按幂等键向余额服务查询：确认没扣才回收股数并置 FAILED，确认已扣置 CONFIRMED。
**取舍。** 终态之前股数一直占用，多占一会儿比超卖安全。
