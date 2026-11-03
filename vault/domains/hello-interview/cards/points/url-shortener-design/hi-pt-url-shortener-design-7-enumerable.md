---
id: hi-pt-url-shortener-design-7-enumerable
node: qb.sd.url-shortener-design.points
type: qa
step: 11
---
## Q
**短链接服务 · 短码可枚举**｜追问 · 出自：短链接服务 › 深入 5

计数器方案的短码是递增的，别人能猜出下一个。如果要求短链接不可枚举，怎么改？多区域部署时计数器怎么办？

## A
**要点。** 对计数器值做一次可逆置换：在 62^7 空间内乘以与模数互质的常数再取模，或用 Feistel 网络，既保持唯一又打散顺序。
**多区域。** 每个区域分配不相交的号段。
