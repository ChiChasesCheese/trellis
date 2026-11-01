---
id: hi-pt-url-shortener-design-9-hot-key
node: qb.sd.url-shortener-design.points
type: qa
step: 9
---
## Q
**短链接服务 · 热点 key**｜出自：短链接服务 › 深入 2

个别病毒式传播的短码会压垮单个缓存分片，怎么办？

## A
**要点。** 读服务进程内再放一层小的本地缓存（几秒 TTL），或把热 key 复制到多个缓存节点。
**为什么。** 点击分布高度倾斜，热点集中在少数 key 上，分片再均匀也分不散单个 key。
