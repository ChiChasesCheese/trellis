---
id: hi-pt-tt-installment-plan-3-conservation
node: tt.lld.tt-installment-plan.points
type: qa
step: 3
---
## Q
**分期计划生成器 · 守恒分摊**｜必会 · 出自：分期计划生成器 › 深入 2

免息分期把 10000 分分 3 期，每期独立四舍五入会少 1 分。怎么做到各期之和恰好等于本金？

## A
**问题。** 3333 × 3 = 9999。
**做法。** 
```python
base, extra = divmod(total, n)
return [base + (1 if i < extra else 0) for i in range(n)]
```
**结果。** 3334、3333、3333，合计 10000。余数给前几期还是最后一期要写进规范并固定。
**例。** 10001 分分 4 期得 2501、2500、2500、2500。
