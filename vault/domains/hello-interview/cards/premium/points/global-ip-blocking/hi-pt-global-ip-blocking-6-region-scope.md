---
id: hi-pt-global-ip-blocking-6-region-scope
node: qb.sd.global-ip-blocking.points
type: qa
step: 6
---
## Q
**全球分布式封禁系统 · 地区范围的规则**｜必会 · 出自：全球分布式封禁系统 › 深入 2

有些规则只对特定地区生效。怎样在数据平面里表达，对内存和变更有什么好处？

## A
**要点。** 规则带 `regions` 字段，快照构建时决定哪些节点加载它：每个边缘节点只装自己地区适用的规则。

**好处。** 进一步缩小内存，也减少每个节点收到的变更条数；判定接口仍是 `isBlocked(ip, userId, region)` 的纯内存调用。
