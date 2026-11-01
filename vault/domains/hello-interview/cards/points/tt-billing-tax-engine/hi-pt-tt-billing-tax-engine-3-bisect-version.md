---
id: hi-pt-tt-billing-tax-engine-3-bisect-version
node: tt.lld.tt-billing-tax-engine.points
type: qa
step: 3
---
## Q
**计费与计税引擎 · 按生效时间二分**｜出自：计费与计税引擎 › 深入 1

计费引擎为什么不保存"当前配置"，而要按生效时间查版本？边界时间属于哪个版本？

## A
**问题。** 只存当前配置，重算上月交易会用今天的规则，账对不上；退款手续费复用错误价格计划是真实缺陷。
**做法。** 完整保存每个版本，quote 用 bisect_right(starts, ts) 取最后一个 start ≤ ts 的版本，O(log V)；版本少，空间不是问题。
**边界。** 交易时间恰等于生效时间属于新版本，要写测试固定。
