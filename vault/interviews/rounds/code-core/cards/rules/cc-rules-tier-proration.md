---
id: cc-rules-tier-proration
node: rules.tiers
type: qa
---
## Q
A user switches plans mid-period. The flat fee and the included allowance must both be prorated by `r = fixed_sessions / total_sessions`. State the two different roundings.

## A
**The fee is rounded half-up to the cent; the allowance is floored to a whole unit.**

```python
fee_cents  = (2 * 1500 * fixed + total) // (2 * total)   # half-up
allowance  = 40000 * fixed // total                       # floor
```

They differ because money is rounded to the nearest cent by convention, while an allowance is a quantity you are *granted* and partial units are not granted.

Two further points: `r` is defined by whatever the statement counts — session counts here, not token counts or elapsed days — and a prorated allowance that is not a multiple of the billing block gets floored again when the block rule is applied.

## Q zh
用户在计费周期中途切换套餐。固定费用和包含额度都要按 `r = fixed_sessions / total_sessions` 分摊。说出两种不同的取整。

## A zh
**费用按 half-up 取整到分；额度向下取整到整单位。**

```python
fee_cents  = (2 * 1500 * fixed + total) // (2 * total)   # half-up
allowance  = 40000 * fixed // total                       # floor
```

两者不同，是因为按惯例钱要四舍五入到最近的分，而额度是**授予**你的量，不足一个单位就不授予。

还有两点：`r` 由题面所计的东西定义 —— 这里是会话数，不是 token 数或天数；以及按比例算出的额度若不是计费块的整数倍，在应用块规则时会再被向下取整一次。
