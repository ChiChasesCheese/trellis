---
id: hi-pt-driver-heatmap-backend-11-client-log-scale
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 11
---
## Q
**司机热力图 · 对数刻度渲染**｜加分 · 出自：司机热力图 › 深入 7

司机热力图的前端渲染中，一个超热格（机场）会让其余格的颜色看起来都一样。怎么处理？还有哪些客户端优化？

## A
**做法。** 颜色用对数刻度分级，避免线性刻度被一个超热格压成同一种颜色。

**其他。** 视口变化做防抖，离屏格不请求。
