---
id: amz-parking-fees-lost-ticket-adjustment-order
node: amazon.amz-parking-fees
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，丢票出场怎么处理？它和会员折扣同时出现时，顺序为什么重要？

## A
丢票没有票号，用车牌从未结算的票里找到入场记录，照常计价，再加固定罚款（`LostTicketPenalty`），票同样关闭。调整按列表顺序应用：小汽车周五 10:00–12:00 应收 800 分，罚款 1500 分，会员 50% 折扣。先折扣后罚款：400 + 1500 = 1900；先罚款后折扣：(800 + 1500) 再减半 = 1150，罚款也被打了折。顺序由调用方显式给出，每一步在收据上留一行明细。
