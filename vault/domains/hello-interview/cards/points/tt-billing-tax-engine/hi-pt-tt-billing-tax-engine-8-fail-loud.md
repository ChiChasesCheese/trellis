---
id: hi-pt-tt-billing-tax-engine-8-fail-loud
node: tt.lld.tt-billing-tax-engine.points
type: qa
step: 8
---
## Q
**计费与计税引擎 · 没有版本就报错**｜追问 · 出自：计费与计税引擎 › 深入 4

计费引擎遇到交易时间早于该商户任何生效版本，应该返回 0 费用还是报错？

## A
**要点。** 抛 LookupError，不返回 0。
**为什么。** 返回 0 是静默漏收：有交易没收费，几个月后对账才发现。
**可复现。** 每行带规则 ID 和版本号，凭它们复现。
