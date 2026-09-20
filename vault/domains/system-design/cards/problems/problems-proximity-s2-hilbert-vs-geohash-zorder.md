---
id: problems-proximity-s2-hilbert-vs-geohash-zorder
node: problems.geo.proximity
type: qa
step: 3
tags: [grown]
---
## Q
Google's S2 library projects the earth onto a cube and orders cells along a Hilbert curve, while geohash interleaves latitude/longitude bits, which is equivalent to ordering along a Z-order curve. Why does this specific difference make S2 cells better at preserving spatial locality near cell boundaries than geohash?

## A
Both a Hilbert curve and a Z-order curve are space-filling curves that map 2D coordinates to a 1D ordering so nearby points tend to get nearby index values, but a Z-order curve has more discontinuities where the curve jumps a long physical distance between consecutive index values, especially at boundaries between larger grid quadrants. A Hilbert curve is constructed specifically to minimize the number and severity of these jumps, so two S2 cells with numerically close 64-bit cell IDs are more consistently close in physical space than two geohash strings with a shared prefix, reducing the boundary cases where a physically nearby point falls outside the searched cell range.

## Q zh
Google 的 S2 库把地球投影到一个立方体上、沿希尔伯特曲线（Hilbert curve）给单元排序，而 geohash 是交织纬度/经度的二进制位，这等价于沿 Z 字形曲线（Z-order curve）排序。为什么这个具体差异让 S2 单元在格子边界附近保持空间局部性的能力比 geohash 更好？

## A zh
希尔伯特曲线和 Z 字形曲线都是空间填充曲线，把二维坐标映射成一维排序，使得相邻的点倾向于拿到相邻的索引值，但 Z 字形曲线有更多不连续点——曲线会在相邻索引值之间跳跃很长的物理距离，尤其是在更大网格象限的边界处。希尔伯特曲线的构造就是专门为了最小化这类跳跃的数量和严重程度，所以两个数值上接近的 S2 64 位单元 ID，对应的物理位置比两个共享前缀的 geohash 字符串更稳定地接近，减少了'物理上很近的点却落在被搜索的单元范围之外'这种边界情况。
