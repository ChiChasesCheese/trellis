---
id: hi-pt-parking-lot-system-5-exit-idempotent
node: qb.lld.parking-lot-system.points
type: qa
step: 5
---
## Q
**停车场管理系统 · 离场幂等**｜必会 · 出自：停车场管理系统 › 深入 2

重复的离场请求会导致什么最严重的 bug？怎么避免？

## A
**问题。** 重复释放会让同一车位在堆里出现两次，随后被分给两辆车，是最严重的 bug。
**做法。** 用 `self._active.pop(ticket_id, None)` 的返回值判断是否第一次处理，不是第一次就直接返回，不再释放。
