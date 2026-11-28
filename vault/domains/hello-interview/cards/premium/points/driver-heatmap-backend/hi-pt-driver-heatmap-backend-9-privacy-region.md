---
id: hi-pt-driver-heatmap-backend-9-privacy-region
node: qb.sd.driver-heatmap-backend.points
type: qa
step: 9
---
## Q
**司机热力图 · 隐私与多区域**｜追问 · 出自：司机热力图 › 深入 6

司机热力图涉及司机位置，且司机分布在全球多个区域。隐私和多区域怎么处理？

## A
**隐私。** 格内司机少于 k（如 3）个就不显示，防止定位到个人。

**多区域。** 司机上报到就近区域，区域内独立计算；全球视图只汇总最粗一层（4 位格，每格约 39 km × 20 km），数据量小，可跨区同步。
