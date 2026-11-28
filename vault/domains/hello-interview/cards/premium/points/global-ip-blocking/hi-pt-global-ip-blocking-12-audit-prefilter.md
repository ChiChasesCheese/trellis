---
id: hi-pt-global-ip-blocking-12-audit-prefilter
node: qb.sd.global-ip-blocking.points
type: qa
step: 12
---
## Q
**全球分布式封禁系统 · 审计与预过滤**｜加分 · 出自：全球分布式封禁系统 › 深入 7

封禁系统在合规和性能上还有哪些加分项？

## A
**审计。** 每条规则保留法规来源编号、操作人、时间，可导出；规则可设到期自动撤销。

**预过滤。** 加布隆过滤器，或在内核层（eBPF）直接丢弃，进一步减少用户态开销。
