---
id: amz-aws-billing-common-mistake-float-and-per-record-tiers
node: amazon.amz-aws-billing
type: qa
step: 9
tags: [grown]
---
## Q
在 AWS 账单服务里，候选人最常见的错误是什么？给一个会暴露它的输入。

## A
最常见的是用 float 存钱，并且逐条记录分档。前者：`0.1 + 0.2` 得 `0.30000000000000004`，加一百行账单总额和各行之和对不上；费率应用 `Decimal("0.023")`，金额用整数分，每个账单行只舍入一次。后者：两条各 30000 GB 得 1380.00，正确是 1371.20。第三个同类错误：三个服务各 0.004 元，每行显示 0.00，总额却一次性舍入成 0.01，客户核对不上。
