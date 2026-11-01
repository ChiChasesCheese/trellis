---
id: hi-pt-url-shortener-design-8-cache-layers
node: points.url-shortener-design
type: qa
step: 8
---
## Q
**短链接服务 · 跳转加速的三层**｜出自：短链接服务 › 深入 2

跳转要在 100ms 内、峰值 6 万次/秒，数据库点查压不住。逐层说明加速手段，并估算热集缓存大小。

## A
**分层。** 主键点查几毫秒但峰值压垮单库 I/O；Redis cache-aside 命中亚毫秒；CDN 边缘直接返回热门重定向。
**数字。** 热集假设 20% 链接，每条约 150 字节，10 亿条的 20% 约 30GB，几台缓存节点够，LRU 淘汰。
**代价。** CDN 难失效，靠短 TTL 或 purge。
