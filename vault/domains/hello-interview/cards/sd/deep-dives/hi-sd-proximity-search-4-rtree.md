---
id: hi-sd-proximity-search-4-rtree
node: qb.sd.driver-heatmap-backend.pre-sd-deep-dives-proximity-search
type: qa
step: 4
---
## Q
**R 树：为形状和磁盘而生**｜系统设计 · 深入专题

R 树用什么办法同时解决「数据不只是点」和「必须在磁盘上高效」？重叠是什么代价？

## A
**最小外接矩形（MBR）。** 把每个对象包进与经纬轴平行的最小矩形：点是宽高为 0 的矩形，高速公路是细长条，一个县是一大块。相邻矩形再被更大的矩形包住，层层嵌套到根。

**像 B 树。** 树保持平衡，所有叶子同深度，每个节点一页，插入删除靠分裂与合并页。移动司机的更新开销可控。

**代价。** 矩形可以重叠：查询点落在两个矩形里就要下钻两支。插入策略差会重叠多、变慢，实践用 R*-tree 的启发式降低重叠。

**使用。** PostGIS 基于 Postgres 的 GiST 提供 R 树式的边界框行为；SQLite、Oracle Spatial 也有变体。问「配送区是否包含这个地址」时用它。
