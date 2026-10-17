---
id: amz-aws-billing-aggregate-before-tiering
node: amazon.amz-aws-billing
type: qa
step: 5
tags: [grown]
---
## Q
在 AWS 账单服务里，阶梯价应对每条用量记录分别计算，还是先按月聚合再计算？为什么？

## A
先聚合再分档。两个选项：(甲) 逐条分档，每条都被当成「第一档」；(乙) 先把同一 (服务, 指标) 的月总量加起来再分档。例：两条各 30000 GB，甲得 2 x 690.00 = 1380.00，乙把 60000 GB 按 51200 x 0.023 + 8800 x 0.022 得 1371.20。单价随用量递减，甲会多收客户的钱。免费额度同理，扣在月总量上。选乙；`RatePlan.charge` 只接收周期内总量，这是策略模式：计费方式可互换，`invoice` 里没有 if 链。
