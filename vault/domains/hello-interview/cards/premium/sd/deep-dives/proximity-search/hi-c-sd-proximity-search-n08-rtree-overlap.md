---
id: hi-c-sd-proximity-search-n08-rtree-overlap
node: sd.deep-dives.proximity-search.notes
type: qa
step: 8
---
## Q
**邻近搜索 · R 树的代价：重叠，与实际使用**｜摘要 · 必会

R 树的矩形重叠为什么是代价？生产里怎么缓解、哪些系统在用？

## A
- **重叠：** 与四叉树格子不同，R 树的矩形可以相交。查询点落在两个矩形里，就要下钻两个分支并检查两棵子树。
- **插入策略差则重叠多：** 要走的分支多，性能被拖垮。
- **R*-树：** 通过更聪明的插入与分裂启发式保持低重叠；SQLite 的 R*Tree 模块就是这一思路，PostGIS 的 GiST 实现则用更简单的线性分裂。
- **使用者：** PostGIS 建在 Postgres 的 GiST 框架上，得到 R 树式的边界框行为；SQLite、Oracle Spatial 有各自的变体。
- **适合的问题：** 涉及真实几何，如"这个配送区是否包含这个地址""这条路是否穿过这个县"。点、线、多边形都能处理。
