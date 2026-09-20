---
id: problems-ride-hailing-hexagon-supply-demand-gradient
node: problems.geo.ride-hailing
type: qa
step: 5
tags: [grown]
---
## Q
In a ride-hailing design that computes a supply/demand gradient between a geographic pricing cell and its neighbors, why does using a hexagonal grid (like Uber's H3) avoid a systematic bias that a rectangular grid would introduce?

## A
A rectangular grid cell has two different neighbor distances — shorter to its 4 edge-adjacent neighbors, longer to its 4 diagonal neighbors — so any gradient computed by comparing a cell to its neighbors would be systematically skewed toward the closer edge-adjacent cells, an artifact of the grid's orientation rather than the real underlying supply/demand pattern. A hexagonal cell has exactly 6 neighbors all at the same distance from its center, so the same gradient computation doesn't need a correction term for grid orientation, which is the specific geometric reason surge-pricing regions are built on hexagonal cells rather than rectangular ones.

## Q zh
在一个网约车设计中计算某个地理定价单元和其相邻单元之间的供需梯度时，为什么使用六边形网格（比如 Uber 的 H3）能避免矩形网格会引入的一种系统性偏差？

## A zh
矩形网格单元到邻居有两种不同的距离——到 4 个边相邻的邻居更近，到 4 个对角相邻的邻居更远——所以任何通过比较一个单元和它的邻居算出来的梯度，都会系统性地偏向更近的边相邻单元，这是网格朝向带来的假象，不是真实的供需模式。六边形单元恰好有 6 个邻居且都与中心距离相等，所以同样的梯度计算不需要为网格朝向额外做修正，这正是动态定价区域用六边形而不是矩形单元搭建的具体几何原因。
