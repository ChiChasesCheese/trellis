%% trellis:begin %%
# AWS 账单服务（AWS Billing Service）（low priority）
*Amazon 专项（Amazon OOD）*

按用量计费：阶梯价、免费额度、按服务汇总、用量记录去重，钱用整数分。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.strategy|策略模式与可替换算法（Strategy）]], [[domains/low-level-design/map/oop.values|值对象与不可变性（Value Objects）]]

## Readings
- [[solution-amz-aws-billing|设计题解：AWS 账单服务（AWS Billing Service）（low priority）]]

## Drills
- [[design-amz-aws-billing|Drill：AWS 账单服务（AWS Billing Service）]]

## Cards (9)
1. [[amz-aws-billing-how-asked-and-three-questions]]
2. [[amz-aws-billing-objects-and-their-jobs]]
3. [[amz-aws-billing-stage1-invoice-in-code]]
4. [[amz-aws-billing-tiered-pricing-is-marginal]]
5. [[amz-aws-billing-aggregate-before-tiering]]
6. [[amz-aws-billing-followup-duplicate-usage-reports]]
7. [[amz-aws-billing-followup-mid-month-price-change]]
8. [[amz-aws-billing-concurrency-check-then-insert-race]]
9. [[amz-aws-billing-common-mistake-float-and-per-record-tiers]]
%% trellis:end %%

## Notes
