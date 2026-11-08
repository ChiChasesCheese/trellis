---
id: hi-pt-tt-installment-plan-7-strategy-step
node: tt.lld.tt-installment-plan.points
type: qa
step: 4
---
## Q
**分期计划生成器 · 到期日策略注入**｜必会 · 出自：分期计划生成器 › 核心实体与接口

分期计划生成器要支持按月、按两周等不同节奏，接口怎么设计才能加新节奏不改主函数？

## A
**要点。** 把"第 k 期的到期日"抽成策略函数 step(start, k)，通过参数注入（monthly、biweekly）。
**实体。** Instalment(seq, due, principal, interest) 不可变，total 是本息合计；schedule 返回元组。
**例。** pay-in-4：biweekly 作 step，利率传 0。
