---
nodes: [problems.geo.google-maps]
url: https://github.com/Project-OSRM/osrm-backend/wiki/Traffic
---
# OSRM Wiki: Traffic

值得读：开源路径规划引擎 OSRM 的官方工程文档，明确记录了 Contraction Hierarchies（CH）
和 Multi-Level Dijkstra（MLD）两条流水线在"查询性能"与"能否支持实时路况更新"之间的
权衡——CH 预处理是耗时的离线批处理，路况变化后代价太高无法频繁重跑；MLD 把图划分为
分区，路况变化时只需要局部重算受影响分区的边界捷径。本题解「深入探讨」第 2 节从纯 CH
过渡到分区方案的论证直接建立在这份文档上，比多数刷题站只停留在"用 CH 加速路径规划"这
一层更进一步，指出了 CH 本身在实时路况场景下的局限。
