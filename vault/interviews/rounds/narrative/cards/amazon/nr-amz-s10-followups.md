---
id: nr-amz-s10-followups
node: amazon.s10
type: qa
step: 3
---
## Q
【退款费 billing-terms 复盘（推翻自己的数字）】面试官会追问什么？每个怎么答？

## A
- **How did you discover the predicate was wrong?**
    - 见待补
- **Who had seen your first number?**
    - 见待补
- **Why is the blast radius bounded?**
    - 切换后新 credit 自动拿到 **NET 计划 ID**；只有**切换前积压、切换后才跑**的商户受影响
- **How do you fix it?**
    - 费用创建时调 **`EFFECTIVE_PRICING_SCHEDULE(maid, date)`**；**不复制** credit 的历史计划 ID
- **What about the upstream lag?**
    - 函数按查询时**物理存在**的计划解析；批量铺开时滞后可能是**系统性**的；创建时重新解析**两者都缓解**
- **How do you know $5,854.52 is right?**
    - 口径 **`SUM(ABS(amount))/100`**；SQL 附录在复盘文档里
- **What changed in how you work?**
    - **每个结论一条可重跑查询**；爆炸半径谓词检查**时间有效性**
