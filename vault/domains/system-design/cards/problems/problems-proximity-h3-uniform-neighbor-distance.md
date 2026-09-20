---
id: problems-proximity-h3-uniform-neighbor-distance
node: problems.geo.proximity
type: qa
step: 4
tags: [grown]
---
## Q
Uber's H3 spatial index divides the globe into hexagonal cells instead of square cells. Why does a hexagonal grid matter specifically for computations like density interpolation or spatial smoothing, beyond just being a different tiling shape?

## A
A square grid cell has two different distances to its neighbors: 4 edge-adjacent neighbors at one distance and 4 diagonal neighbors at a longer distance, so any computation that treats all neighbors symmetrically (like averaging nearby demand to smooth a density estimate) introduces a systematic bias toward the closer edge-adjacent neighbors. A hexagonal cell has exactly 6 neighbors, all at the same distance from its center, so density interpolation or smoothing across hexagon neighbors doesn't have to correct for an asymmetry baked into the grid geometry — the tradeoff is that hexagons cannot be recursively subdivided into four equal children the way a square can, making the subdivision logic more complex.

## Q zh
Uber 的 H3 空间索引把地球划分成六边形（hexagon）单元而不是正方形单元。除了'只是换了一种拼接形状'之外，为什么六边形网格对密度插值或空间平滑这类计算特别重要？

## A zh
正方形网格单元到邻居有两种不同的距离：4 个边相邻的邻居是一种距离，4 个对角相邻的邻居是更长的另一种距离，所以任何对所有邻居一视同仁的计算（比如平均周边需求来平滑密度估计）都会系统性地偏向更近的边相邻邻居。六边形单元恰好有 6 个邻居，且都与中心距离相等，所以在六边形邻居之间做密度插值或平滑不需要修正网格几何本身带来的不对称——代价是六边形不能像正方形那样递归地四等分成子单元，subdivision 的实现逻辑更复杂。
