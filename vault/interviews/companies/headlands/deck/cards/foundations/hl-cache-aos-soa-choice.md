---
id: hl-cache-aos-soa-choice
node: foundations.cpu-cache-locality
type: qa
step: 20
---
## Q
什么时候选 SoA，什么时候 AoS 没问题？订单簿热路径怎么用 SoA 思想？

## A
- 查询**只用部分字段**且要扫描大量记录（行情分析、聚合、风控批量检查）→ **SoA**，没用的字段不占缓存。
- 每次操作**同时用全部字段**、按 id 随机访问单条记录 → AoS 没问题；SoA 要读 4 条数组的 4 个不同缓存行，反而更差。
- 订单簿热路径：用平行数组 `head[side][tick]`、`next[]`、`qty[]` 把链表也平铺成数组下标，是 SoA 思想的极致应用。
