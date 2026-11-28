---
id: hi-pt-driver-heatmap-backend-7-tile-cache
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 7
---
## Q
**司机热力图 · 瓦片缓存**｜追问 · 出自：司机热力图 › 深入 4

1,000 个运营看板每 5 秒刷新一次司机热力图。读路径怎样让后端压力不随观众增长？

## A
**做法。** 视口按固定瓦片 (zoom, x, y) 请求，每个瓦片的响应缓存 5 秒；大家看同一座城市时命中同一批瓦片。

**数字。** 1,000 个看板每 5 秒刷新是 200 次/秒，缓存后几乎不回源。

**实时。** 用 SSE 按瓦片订阅，只推变化的格。
