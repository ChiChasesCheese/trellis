---
id: hl-cache-design-orderbook-layout
node: foundations.cpu-cache-locality
type: qa
step: 41
---
## Q
订单簿存 100 万个订单（`id`、`price`、`qty`、`side`），热路径是撮合时按价位顺序扫描订单的 `qty`，用对象数组还是平行数组？

## A
用**平行数组（SoA）**：扫描只用 `qty`（及按价位找订单的链接），不碰 `id` / `price` / `side`；`qty` 是连续的 `int` 数组，一个缓存行装 16–32 个订单数量，扫描几乎全命中。

对象数组每个订单约 40 字节，读 `qty` 要拉进整个对象，对象还可能散落在堆里。需要按 id 随机取全部字段时，另配 `id → 下标` 映射。
