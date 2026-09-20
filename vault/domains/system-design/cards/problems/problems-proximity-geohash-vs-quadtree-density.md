---
id: problems-proximity-geohash-vs-quadtree-density
node: problems.geo.proximity
type: qa
step: 2
tags: [grown]
---
## Q
In a proximity search index covering both a dense downtown area and a sparse rural area, why does a geohash grid handle the two regions worse than a quadtree, even though both structures flatten 2D coordinates into an indexable key?

## A
Geohash cells of a fixed character length cover a uniform physical area regardless of local density — a downtown cell at a given precision might contain hundreds of businesses while a rural cell of the same precision contains none, so query cost is density-blind and hot cells scan almost as much data as a full table. A quadtree instead recursively splits a region only when the number of businesses inside it exceeds a threshold, so dense downtown areas automatically get subdivided into many small leaf nodes while sparse rural areas stay as large leaf nodes — the index structure adapts to the actual data distribution instead of applying one grid size everywhere.

## Q zh
在一个同时覆盖密集市中心和稀疏郊区的邻近搜索索引中，尽管 geohash 网格和四叉树（quadtree）都是把二维坐标拍平成可索引的键，为什么 geohash 网格处理这两种区域的效果比四叉树差？

## A zh
固定字符长度的 geohash 格子覆盖的物理面积是均匀的，与局部密度无关——某个精度下市中心的一个格子可能挤着几百个商户，同样精度下郊区的格子可能一个都没有，导致查询开销对密度毫无感知，热点格子几乎要扫描和全表一样多的数据。四叉树则是只在某个区域内商户数超过阈值时才递归分裂——密集的市中心自动分裂出很多细小的叶子节点，稀疏的郊区保留成大的叶子节点，索引结构本身适配真实的数据分布，而不是到处套用同一个网格大小。
