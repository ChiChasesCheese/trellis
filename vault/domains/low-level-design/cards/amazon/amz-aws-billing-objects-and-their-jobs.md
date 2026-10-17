---
id: amz-aws-billing-objects-and-their-jobs
node: amazon.amz-aws-billing
type: qa
step: 2
tags: [grown]
---
## Q
在 AWS 账单服务设计里，应有哪几个对象？各自只负责什么？

## A
系统是「去重的用量仓库 + 一组费率 + 出账单的流程」。`Money`：整数分的值对象，币种不同不能相加。`RatePlan`：把周期内总用量变成未舍入金额，实现有一口价、阶梯价、免费额度后再计费。`UsageLedger`：按 `usage_id` 去重存用量。`PriceBook`：每个服务按生效时间保存价格版本。`BillingService`：聚合、套费率、每行舍入一次。`Invoice`：账单行与总额。切分依据：变化原因不同。
